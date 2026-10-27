"""Compare retained-register feedback with the endpoint reset harness.

New experiment only: original recording is replayed because changing feedback
after entering the prior all-one state cannot recover discarded register state.
Opposite-end raw inputs overwrite the same four fixed slots; the other four
slots retain their prior operator outputs across both directions and rounds.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from endpoint_phase import DEFAULT_MAPPING, encode, load_archive, numeral_table, views
from operator_machine import REGS
from operator_machine import execute
from native_execution_test import build_source


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--passes', type=int, default=100)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Output must be new')
    repo = Path(__file__).resolve().parents[2]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    chains = [[f['rounded'] for f in band['frames']] for band in bands]
    original = [chain.copy() for chain in chains]
    states = [{reg: 1 for reg in REGS} for _ in bands]
    args.output.mkdir(parents=True)
    build = args.output / 'build'
    build.mkdir()
    with (args.output / '.gitignore').open('x', encoding='utf-8') as handle:
        handle.write('build/\n')
    history, traces, zeros, repeats = [], [], [], []
    seen = {}
    for cycle in range(1, args.passes + 1):
        result = {'cycle': cycle}
        for direction in ('x_to_y', 'y_to_x'):
            front = [chain[0] for chain in chains]
            back = [chain[-1] for chain in chains]
            current, opposite = (front, back) if direction == 'x_to_y' else (back, front)
            for channel, (value, band) in enumerate(zip(current, bands), 1):
                prior = states[channel - 1].copy()
                state = states[channel - 1]
                for register, raw in zip(DEFAULT_MAPPING, opposite):
                    state[register] = raw
                before = state.copy()
                numerals = encode(value, table)
                glyphs = ''.join(g for g in numerals if g not in ' |0')
                if direction == 'y_to_x':
                    glyphs = glyphs[::-1]
                for glyph in glyphs:
                    execute(band['ops'][glyph], state)
                traces.append({'cycle': cycle, 'direction': direction, 'channel': channel,
                               'current_raw': value, 'opposite_raw': json.dumps(opposite),
                               'executed_commands': glyphs,
                               **{'prior_' + reg: prior[reg] for reg in REGS},
                               **{'seeded_' + reg: before[reg] for reg in REGS},
                               **{'after_' + reg: state[reg] for reg in REGS}})
            if direction == 'x_to_y':
                output = [s['target'] for s in states]
                for channel, value in enumerate(output, 1):
                    chains[channel - 1].append(value)
                    if value == 0:
                        zeros.append({'cycle': cycle, 'channel': channel, 'position': 'back', 'register': 'target'})
                result['right_target'] = output
                result['right_other_channel_views'] = views(output)
            else:
                output = [[s['state'], s['relations']] for s in states]
                for channel, pair in enumerate(output, 1):
                    chains[channel - 1][0:0] = pair
                    for register, value in zip(('state', 'relations'), pair):
                        if value == 0:
                            zeros.append({'cycle': cycle, 'channel': channel,
                                          'position': 'front' if register == 'state' else 'second_front', 'register': register})
                result['left_state_relations'] = output
                result['left_other_channel_views'] = views(output)
        result.update({'front': [chain[0] for chain in chains], 'back': [chain[-1] for chain in chains],
                       'all_registers': [state.copy() for state in states]})
        signature = tuple(result['front'] + result['back'] + [s[r] for s in states for r in REGS])
        if signature in seen:
            repeats.append({'cycle': cycle, 'previous_cycle': seen[signature], 'gap': cycle - seen[signature]})
        else:
            seen[signature] = cycle
        history.append(result)
    for before, after in zip(original, chains):
        assert after[2 * args.passes:2 * args.passes + len(before)] == before
        assert len(after) == len(before) + 3 * args.passes
    manifest = []
    for channel, (chain, band) in enumerate(zip(chains, bands), 1):
        for kind, numbers in [('extended_chain', chain), ('new_front_segment', chain[:2 * args.passes]), ('new_back_segment', chain[-args.passes:])]:
            name = f'stateful_pass{args.passes}_{kind}_channel{channel}'
            source, expected, count = build_source(numbers, band['ops'], table, name)
            source_path = build / (name + '.S')
            with source_path.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(source)
            manifest.append({'program': name, 'cycle': args.passes, 'direction': kind,
                             'channel': channel, 'input_values': len(numbers), 'operator_commands': count,
                             'source': source_path.name, 'expected_registers': expected,
                             'source_sha256': hashlib.sha256(source.encode()).hexdigest()})
    save(args.output / 'phase_history.json', history)
    save(args.output / 'final_chains.json', chains)
    save(args.output / 'native_manifest.json', manifest)
    with (args.output / 'phase_history.csv').open('x', newline='', encoding='utf-8') as handle:
        fields = ['cycle', 'right_target', 'left_state_relations', 'front', 'back']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: json.dumps(row[key]) if isinstance(row[key], list) else row[key] for key in fields} for row in history)
    with (args.output / 'register_trace.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(traces[0]))
        writer.writeheader()
        writer.writerows(traces)
    report = {'passes_each_direction': args.passes,
              'feedback': 'Retain channel register states between directions and cycles; overwrite only the four opposite-end input slots.',
              'seed_mapping': DEFAULT_MAPPING, 'other_register_initial_seed': 1,
              'start_from': 'Original recorded chains, to compare feedback modes without inheriting the reset-mode fixed point.',
              'final_front': history[-1]['front'], 'final_back': history[-1]['back'],
              'final_left_pairs': history[-1]['left_state_relations'],
              'final_chain_lengths': list(map(len, chains)),
              'literal_zeros': zeros, 'first_full_state_repeat': repeats[0] if repeats else None,
              'full_state_repeat_count': len(repeats),
              'front_zero_observed': any(z['position'] == 'front' for z in zeros),
              'y_finish_marker_identified': False,
              'termination_note': 'Full state includes all eight registers in all four banks and both endpoint vectors. An exact repeat cannot escape under the unchanged deterministic wiring. A zero in the second left register is recorded separately from a zero at the chain start.',
              'native_programs_prepared': len(manifest),
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest()}
    save(args.output / 'stateful_comparison_report.json', report)
    print(json.dumps({key: report[key] for key in ('passes_each_direction', 'final_front', 'final_back', 'final_left_pairs', 'first_full_state_repeat', 'front_zero_observed', 'native_programs_prepared')}))


if __name__ == '__main__':
    main()
