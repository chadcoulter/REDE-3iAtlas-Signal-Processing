"""Continue saved extended chains for a fresh batch; preserve every value.

Starts from the previous final chains, not from the original recording. Only
new files are created. A repeated deterministic endpoint state is recorded
explicitly instead of being mislabelled as a start/finish marker.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from endpoint_phase import DEFAULT_MAPPING, load_archive, numeral_table, phase, views
from native_execution_test import build_source


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--resume', type=Path, required=True)
    parser.add_argument('--passes', type=int, default=100)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Output must be a new directory')
    if args.passes < 1:
        raise ValueError('Pass count must be positive')
    repo = Path(__file__).resolve().parents[2]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    previous_report_path = args.resume / 'continuation_report.json'
    if not previous_report_path.exists():
        previous_report_path = args.resume / 'extension_report.json'
    previous = json.loads(previous_report_path.read_text())
    completed = previous.get('total_passes_each_direction', previous.get('passes_each_direction'))
    if completed is None:
        raise ValueError('Resume pass count unavailable')
    previous_chain_file = args.resume / 'final_chains.json'
    chains = json.loads(previous_chain_file.read_text())
    original_chains = [chain.copy() for chain in chains]
    initial_lengths = list(map(len, chains))
    initial_front = [chain[0] for chain in chains]
    initial_back = [chain[-1] for chain in chains]
    args.output.mkdir(parents=True)
    build = args.output / 'build'
    build.mkdir()
    with (args.output / '.gitignore').open('x', encoding='utf-8') as handle:
        handle.write('build/\n')
    history, traces, zeros = [], [], []
    first_seen = {tuple(initial_front + initial_back): completed}
    repetitions = []
    added_front = [[] for _ in bands]
    added_back = [[] for _ in bands]
    for batch_pass in range(1, args.passes + 1):
        cumulative = completed + batch_pass
        front = [chain[0] for chain in chains]
        back = [chain[-1] for chain in chains]
        right, right_trace = phase(front, back, 'x_to_y', bands, table)
        for channel in range(4):
            chains[channel].append(right[channel])
            added_back[channel].append(right[channel])
            if right[channel] == 0:
                zeros.append({'pass': cumulative, 'channel': channel + 1, 'register': 'target', 'end': 'back'})
        left, left_trace = phase([chain[-1] for chain in chains], [chain[0] for chain in chains], 'y_to_x', bands, table)
        for channel, pair in enumerate(left):
            chains[channel][0:0] = pair
            added_front[channel][0:0] = pair
            for register, value in zip(('state', 'relations'), pair):
                if value == 0:
                    zeros.append({'pass': cumulative, 'channel': channel + 1, 'register': register, 'end': 'front' if register == 'state' else 'second_front'})
        for direction, records in [('x_to_y', right_trace), ('y_to_x', left_trace)]:
            traces.extend({'batch_pass': batch_pass, 'cumulative_pass': cumulative, 'direction': direction, **record} for record in records)
        record = {'batch_pass': batch_pass, 'cumulative_pass': cumulative,
                  'x_before': front, 'y_before': back, 'right_target': right,
                  'left_state_relations': left, 'x_after': [chain[0] for chain in chains],
                  'y_after': [chain[-1] for chain in chains], 'chain_lengths': list(map(len, chains)),
                  'right_other_channel_views': views(right), 'left_other_channel_views': views(left)}
        signature = tuple(record['x_after'] + record['y_after'])
        if signature in first_seen:
            repetitions.append({'pass': cumulative, 'previous_pass': first_seen[signature],
                                'gap': cumulative - first_seen[signature]})
        else:
            first_seen[signature] = cumulative
        history.append(record)
        if batch_pass % 10 == 0:
            print(json.dumps({'batch_pass': batch_pass, 'cumulative_pass': cumulative,
                              'front': record['x_after'], 'back': record['y_after']}), flush=True)
    # Preserve every previously generated value in order and verify chain growth.
    offset = args.passes * 2
    for before, after in zip(original_chains, chains):
        assert after[offset:offset + len(before)] == before
        assert len(after) == len(before) + 3 * args.passes
    current_front = [chain[0] for chain in chains]
    current_back = [chain[-1] for chain in chains]
    check_right, _ = phase(current_front, current_back, 'x_to_y', bands, table)
    check_left, _ = phase(check_right, current_front, 'y_to_x', bands, table)
    fixed = check_right == current_back and [pair[0] for pair in check_left] == current_front
    # Full two-value output invariance also matters; preserve the exact test.
    fixed_pairs = check_left == history[-1]['left_state_relations']
    manifest = []
    for channel, band in enumerate(bands, 1):
        for kind, values in [('extended_chain', chains[channel - 1]),
                             ('new_front_segment', added_front[channel - 1]),
                             ('new_back_segment', added_back[channel - 1])]:
            name = f'pass{completed + args.passes}_{kind}_channel{channel}'
            source, expected, commands = build_source(values, band['ops'], table,
                f'100-pass continuation; cumulative={completed + args.passes}; {kind}; channel={channel}')
            path = build / (name + '.S')
            with path.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(source)
            manifest.append({'program': name, 'cycle': completed + args.passes,
                             'direction': kind, 'channel': channel, 'input_values': len(values),
                             'operator_commands': commands, 'source': path.name,
                             'expected_registers': expected,
                             'source_sha256': hashlib.sha256(source.encode()).hexdigest()})
    save(args.output / 'final_chains.json', chains)
    save(args.output / 'phase_history.json', history)
    save(args.output / 'native_manifest.json', manifest)
    save(args.output / 'new_front_segments.json', added_front)
    save(args.output / 'new_back_segments.json', added_back)
    with (args.output / 'phase_history.csv').open('x', newline='', encoding='utf-8') as handle:
        fields = ['batch_pass', 'cumulative_pass', 'x_before', 'y_before', 'right_target', 'left_state_relations', 'x_after', 'y_after', 'chain_lengths']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: json.dumps(row[key]) if isinstance(row[key], list) else row[key] for key in fields} for row in history)
    with (args.output / 'register_trace.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(traces[0]))
        writer.writeheader()
        writer.writerows(traces)
    report = {'batch_passes_each_direction': args.passes, 'resumed_after_pass': completed,
              'total_passes_each_direction': completed + args.passes,
              'resume_path': str(args.resume), 'resume_chains_sha256': hashlib.sha256(previous_chain_file.read_bytes()).hexdigest(),
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
              'register_mapping_opposite1_to_4': DEFAULT_MAPPING, 'other_register_seed': 1,
              'initial_lengths': initial_lengths, 'final_lengths': list(map(len, chains)),
              'initial_front': initial_front, 'initial_back': initial_back,
              'final_front': current_front, 'final_back': current_back,
              'new_front_values_per_channel': args.passes * 2, 'new_back_values_per_channel': args.passes,
              'previous_chains_preserved_in_order': True,
              'literal_zero_observations': zeros,
              'endpoint_repetition_count': len(repetitions), 'endpoint_repetitions': repetitions,
              'exact_endpoint_fixed_point_verified': fixed and fixed_pairs,
              'additional_identical_batches_can_escape_fixed_point': not (fixed and fixed_pairs),
              'fixed_point_reason': 'The phase function uses only endpoint vectors. All-one seeds and input 1 produce Alpha, which sets state to 1, while target and relations stay 1. Neither pass number nor chain interior enters this phase function.',
              'start_marker_found': bool([z for z in zeros if z['end'] == 'front']),
              'finish_marker_found': False,
              'finish_rule': 'No Y EOF marker has been defined; repeated constants are recorded, not automatically classified as EOF.',
              'continuation_status': 'Exact deterministic loop: identical endpoint-only batches cannot find a different boundary under the unchanged wiring.' if fixed and fixed_pairs else 'No exact endpoint fixed point verified.',
              'native_programs_prepared': len(manifest),
              'native_scope': 'Check all four final extended chains plus each batch-generated front and back segment (12 programs), rather than recompiling every unchanged repeated endpoint step.'}
    save(args.output / 'continuation_report.json', report)
    print(json.dumps({key: report[key] for key in ('total_passes_each_direction', 'final_lengths', 'final_front', 'final_back', 'exact_endpoint_fixed_point_verified', 'start_marker_found', 'finish_marker_found', 'native_programs_prepared')}), flush=True)


if __name__ == '__main__':
    main()
