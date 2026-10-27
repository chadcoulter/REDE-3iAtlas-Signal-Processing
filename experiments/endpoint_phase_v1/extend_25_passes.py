"""Add 25 alternating directional extensions, only creating new files.

Every cycle reads current chain endpoints. X->Y appends target. Y->X then
prepends [state, relations]. The fixed endpoint_phase.py candidate wiring is
reused unchanged. Emits native source for every channel after every step.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from endpoint_phase import DEFAULT_MAPPING, checks, load_archive, numeral_table, phase, views
from native_execution_test import build_source


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--passes', type=int, default=25)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Choose a fresh output directory')
    if args.passes < 1:
        raise ValueError('Pass count must be positive')
    repo = Path(__file__).resolve().parents[2]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    validation = checks(bands, table)
    chains = [[f['rounded'] for f in band['frames']] for band in bands]
    original_lengths = [len(chain) for chain in chains]
    original_front = [chain[0] for chain in chains]
    original_back = [chain[-1] for chain in chains]
    args.output.mkdir(parents=True)
    build = args.output / 'build'
    build.mkdir()
    with (args.output / '.gitignore').open('x', encoding='utf-8') as handle:
        handle.write('build/\n')
    history, programs, trace_rows = [], [], []
    first_seen = {tuple(original_front + original_back): 0}
    repeats = []
    zeros = []
    for cycle in range(1, args.passes + 1):
        front = [chain[0] for chain in chains]
        back = [chain[-1] for chain in chains]
        right, right_trace = phase(front, back, 'x_to_y', bands, table)
        for channel in range(4):
            chains[channel].append(right[channel])
            if right[channel] == 0:
                zeros.append({'cycle': cycle, 'channel': channel + 1, 'location': 'new_back_target'})
        step = {'cycle': cycle, 'x_before': front, 'y_before': back, 'right_target': right,
                'right_other_channel_views': views(right)}
        for direction in ('x_to_y', 'y_to_x'):
            if direction == 'y_to_x':
                # The newly appended targets are now the right endpoints.
                reverse_current = [chain[-1] for chain in chains]
                reverse_opposite = [chain[0] for chain in chains]
                left, left_trace = phase(reverse_current, reverse_opposite, 'y_to_x', bands, table)
                for channel in range(4):
                    chains[channel][0:0] = left[channel]
                    for label, value in zip(('new_front_state', 'second_front_relations'), left[channel]):
                        if value == 0:
                            zeros.append({'cycle': cycle, 'channel': channel + 1, 'location': label})
                step.update({'reverse_current': reverse_current, 'reverse_opposite': reverse_opposite,
                             'left_state_relations': left, 'left_other_channel_views': views(left)})
                traces = left_trace
            else:
                traces = right_trace
            for trace in traces:
                trace_rows.append({'cycle': cycle, 'direction': direction, **trace})
            for channel, (chain, band) in enumerate(zip(chains, bands), 1):
                name = f'pass{cycle:02d}_{direction}_channel{channel}'
                assembly, expected, count = build_source(chain, band['ops'], table,
                    f'{cycle}/{args.passes} {direction}; channel={channel}; whole extended chain')
                source = build / (name + '.S')
                with source.open('x', encoding='utf-8', newline='\n') as handle:
                    handle.write(assembly)
                programs.append({'program': name, 'cycle': cycle, 'direction': direction,
                                 'channel': channel, 'input_values': len(chain),
                                 'operator_commands': count, 'source': source.name,
                                 'expected_registers': expected,
                                 'source_sha256': hashlib.sha256(assembly.encode('utf-8')).hexdigest()})
        step.update({'x_after': [chain[0] for chain in chains],
                     'y_after': [chain[-1] for chain in chains],
                     'lengths_after': [len(chain) for chain in chains]})
        signature = tuple(step['x_after'] + step['y_after'])
        if signature in first_seen:
            repeats.append({'cycle': cycle, 'previous_cycle': first_seen[signature],
                            'gap': cycle - first_seen[signature],
                            'front': step['x_after'], 'back': step['y_after']})
        else:
            first_seen[signature] = cycle
        history.append(step)
        print(json.dumps({'cycle': cycle, 'front': step['x_after'], 'back': step['y_after'],
                          'lengths': step['lengths_after']}), flush=True)
    expected_lengths = [n + 3 * args.passes for n in original_lengths]
    assert [len(chain) for chain in chains] == expected_lengths
    assert all(len(h['right_target']) == 4 and all(len(pair) == 2 for pair in h['left_state_relations']) for h in history)
    assert len(programs) == args.passes * 2 * 4
    save(args.output / 'phase_history.json', history)
    save(args.output / 'native_manifest.json', programs)
    save(args.output / 'final_chains.json', chains)
    with (args.output / 'phase_history.csv').open('x', newline='', encoding='utf-8') as handle:
        fields = ['cycle', 'x_before', 'y_before', 'right_target', 'left_state_relations', 'x_after', 'y_after', 'lengths_after']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({k: json.dumps(v) if isinstance(v, list) else v for k, v in row.items() if k in fields} for row in history)
    with (args.output / 'register_trace.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(trace_rows[0]))
        writer.writeheader()
        writer.writerows(trace_rows)
    report = {'passes_each_direction': args.passes, 'directional_steps': args.passes * 2,
              'branch': 'codex/atlas-endpoint-phase-test',
              'mode': 'Alternating X->Y append one, then Y->X prepend state and relations; updated endpoints feed the next step.',
              'mapping_opposite1_to_4': DEFAULT_MAPPING, 'other_register_seed': 1,
              'initial_front': original_front, 'initial_back': original_back,
              'final_front': history[-1]['x_after'], 'final_back': history[-1]['y_after'],
              'original_lengths': original_lengths, 'final_lengths': expected_lengths,
              'new_front_values_per_channel': args.passes * 2,
              'new_back_values_per_channel': args.passes,
              'literal_zero_observations': zeros, 'repeated_endpoint_states': repeats,
              'termination_policy': 'Observe literal zero and endpoint repeats; do not stop early. No Y EOF marker is predefined.',
              'native_programs_prepared': len(programs), 'operator_validation_cases': validation,
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
              'criterion': 'Native assembly/link/run and agreement with interpreter, not original measurement recovery.',
              'wiring': 'Reuse endpoint_phase.py separate channel banks and fixed seed mapping unchanged.'}
    save(args.output / 'extension_report.json', report)
    print(json.dumps({'prepared': len(programs), 'zero_observations': len(zeros),
                      'endpoint_repeats': len(repeats), 'output': str(args.output)}), flush=True)


if __name__ == '__main__':
    main()
