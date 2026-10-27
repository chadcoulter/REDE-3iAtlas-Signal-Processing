"""Join recorded register states, outputs, transforms and chain provenance.

No rerun or new interpretation of the transforms: this normalizes the recorded
native-driven run and captured core into a connected, precision-safe JSON.
Only a fresh output directory and new files are written.
"""
import argparse
import csv
import hashlib
import json
import struct
from pathlib import Path

from endpoint_phase import DEFAULT_MAPPING, encode, load_archive, numeral_table
from operator_machine import MASK, REGS

OPERATIONS = {'x_to_y': 'reflection', 'y_to_x': 'projection'}


def words(state):
    assert set(state) == set(REGS)
    return {register: str(state[register]) for register in REGS}


def vector(values):
    return [str(value) for value in values]


def stdout_hex(state):
    return struct.pack('<8Q', *(int(state[register]) for register in REGS)).hex()


def chain_hash(ids, data):
    digest = hashlib.sha256()
    for data_id in ids:
        digest.update(struct.pack('<Q', int(data[data_id]['value_decimal'])))
    return digest.hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Output directory must be new')
    root = Path(__file__).resolve().parent
    repo = root.parents[1]
    run_dir = root / 'native_reassembly_100_results'
    core_dir = root / 'captured_aligned_core_pass100'
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    programs = json.loads((run_dir / 'program_manifest.json').read_text(encoding='utf-8'))
    history = json.loads((run_dir / 'phase_history.json').read_text(encoding='utf-8'))
    run_report = json.loads((run_dir / 'native_reassembly_report.json').read_text(encoding='utf-8'))
    core_manifest = json.loads((core_dir / 'core_manifest.json').read_text(encoding='utf-8'))
    final_values = json.loads((run_dir / 'final_chains.json').read_text(encoding='utf-8'))
    program_by_id = {program['program']: program for program in programs}
    data, executions, transforms = {}, {}, []
    current_chain_ids, initial_chain_ids = [], []
    feedback_ids = [None] * 4
    last_validation_ids = None

    def add_data(data_id, value, channel, origin):
        assert data_id not in data and 0 <= value <= MASK
        numerals = encode(value, table)
        data[data_id] = {'id': data_id, 'channel': channel, 'value_decimal': str(value),
                         'value_hex': f'0x{value:016x}', 'numeric_encoding': numerals,
                         'operator_string': ''.join(glyph for glyph in numerals if glyph not in ' |0'),
                         'origin': origin}
        return data_id

    for channel, band in enumerate(bands, 1):
        ids = []
        for index, frame in enumerate(band['frames']):
            data_id = f'data/c{channel}/recorded/{index:04d}'
            ids.append(add_data(data_id, frame['rounded'], channel,
                {'kind': 'archived_extracted_measurement', 'archive_member': band['source'],
                 'recorded_row': index, 'elapsed_second': frame['second'],
                 'frequency_MHz': frame['frequency_MHz'],
                 'amplitude_as_recorded': frame['amplitude'],
                 'source_numeric_representation': frame['original_numerals']}))
        current_chain_ids.append(ids)
        initial_chain_ids.append(ids.copy())

    def add_execution_group(ids, revision_step):
        assert len(ids) == 4
        direction = program_by_id[ids[0]]['direction_executed']
        endpoint_ids = [chain[-1] if direction == 'x_to_y' else chain[0] for chain in current_chain_ids]
        endpoint_values = [int(data[data_id]['value_decimal']) for data_id in endpoint_ids]
        for expected_channel, execution_id in enumerate(ids, 1):
            assert execution_id not in executions
            program = program_by_id[execution_id]
            channel = program['channel']
            assert channel == expected_channel
            assert program['validates_extension_step'] == revision_step
            assert program['direction_executed'] == direction
            assert program['opposite_raw_vector'] == endpoint_values
            assert program['chain_values'] == len(current_chain_ids[channel - 1])
            assert program['chain_sha256'] == chain_hash(current_chain_ids[channel - 1], data)
            previous_id = feedback_ids[channel - 1]
            prior = program['retained_registers_before_seed']
            assert prior == (program_by_id[previous_id]['native_registers'] if previous_id else {reg: 1 for reg in REGS})
            for register, value in zip(DEFAULT_MAPPING, endpoint_values):
                assert program['seed_registers'][register] == value
            for register in REGS:
                if register not in DEFAULT_MAPPING:
                    assert program['seed_registers'][register] == prior[register]
            assert program['native_matches_reference'] and program['native_registers'] == program['reference_registers']
            assert program['assembler_exit'] == program['linker_exit'] == program['native_exit'] == 0
            executions[execution_id] = {
                'id': execution_id, 'channel': channel, 'operation': OPERATIONS[direction],
                'direction': direction, 'role': 'bootstrap' if revision_step == 0 else 'validates_previous_extension',
                'validates_transform_id': None if revision_step == 0 else f'transform/{revision_step:04d}',
                'input_chain_revision': f'chain/c{channel}/step{revision_step:04d}',
                'input_chain_value_count': program['chain_values'], 'input_chain_sha256': program['chain_sha256'],
                'opposite_endpoint_data_ids': endpoint_ids.copy(),
                'seed_sources': {reg: {'data_id': data_id, 'relation': 'loaded_into_seed_cell'}
                                 for reg, data_id in zip(DEFAULT_MAPPING, endpoint_ids)},
                'retained_sources': {reg: ({'execution_id': previous_id, 'register': reg} if previous_id
                                          else {'literal_decimal': '1'}) for reg in REGS if reg not in DEFAULT_MAPPING},
                'feedback_from_execution_id': previous_id,
                'registers': {'retained_before_seed': words(prior),
                              'after_endpoint_seeding': words(program['seed_registers']),
                              'native_after_execution': words(program['native_registers'])},
                'output': {'format': 'eight_uint64_little_endian', 'register_order': REGS,
                           'byte_count': 64, 'stdout_hex': stdout_hex(program['native_registers'])},
                'artifacts': {
                    'assembly': {'archive': 'native_reassembly_100_results/assembled_sources.zip',
                                 'member': execution_id + '.S', 'sha256': program['source_sha256']},
                    'executable': {'archive': 'native_reassembly_100_results/native_executables.zip',
                                   'member': execution_id + '.elf', 'sha256': program['executable_sha256']}},
                'checks': {'assembler_exit': 0, 'linker_exit': 0, 'native_exit': 0,
                           'all_native_registers_match_reference': True},
                'operator_invocations': program['operator_commands']}
            feedback_ids[channel - 1] = execution_id

    add_execution_group(history[0]['projection_source_programs'], 0)
    for item in history:
        step = item['step']
        transform_id = f'transform/{step:04d}'
        operation = OPERATIONS[item['extension_direction']]
        source_ids = item['projection_source_programs']
        assert all(execution_id in executions for execution_id in source_ids)
        if last_validation_ids:
            assert source_ids == last_validation_ids
        assert vector([int(data[chain[0]]['value_decimal']) for chain in current_chain_ids]) == vector(item['front_before'])
        assert vector([int(data[chain[-1]]['value_decimal']) for chain in current_chain_ids]) == vector(item['back_before'])
        generated, updates = [], []
        for channel, execution_id in enumerate(source_ids, 1):
            state = program_by_id[execution_id]['native_registers']
            selected = ['target'] if operation == 'reflection' else ['state', 'relations']
            values = [state[register] for register in selected]
            expected_values = [item['projected_values'][channel - 1]] if operation == 'reflection' else item['projected_values'][channel - 1]
            assert values == expected_values
            emitted_ids = []
            for order, (register, value) in enumerate(zip(selected, values)):
                data_id = f'data/c{channel}/step{step:04d}/{register}'
                emitted_ids.append(add_data(data_id, value, channel,
                    {'kind': operation, 'transform_id': transform_id,
                     'source_execution_id': execution_id, 'source_register': register,
                     'emitted_order': order, 'insertion_end': 'back' if operation == 'reflection' else 'front'}))
            before_length = len(current_chain_ids[channel - 1])
            if operation == 'reflection':
                current_chain_ids[channel - 1].extend(emitted_ids)
            else:
                current_chain_ids[channel - 1][0:0] = emitted_ids
            assert len(current_chain_ids[channel - 1]) == item['lengths_after'][channel - 1]
            assert chain_hash(current_chain_ids[channel - 1], data) == item['post_extension_chain_hashes'][channel - 1]
            generated.append({'channel': channel, 'source_execution_id': execution_id,
                              'source_registers': selected, 'data_ids': emitted_ids})
            updates.append({'channel': channel, 'before_revision': f'chain/c{channel}/step{step - 1:04d}',
                            'after_revision': f'chain/c{channel}/step{step:04d}',
                            'insert_at': 'back' if operation == 'reflection' else 'front',
                            'inserted_data_ids_in_chain_order': emitted_ids,
                            'before_value_count': before_length, 'after_value_count': len(current_chain_ids[channel - 1]),
                            'after_chain_sha256': item['post_extension_chain_hashes'][channel - 1]})
        add_execution_group(item['validation_programs'], step)
        views = []
        for active in range(1, 5):
            donors = [output for output in generated if output['channel'] != active]
            views.append({'active_channel': active,
                          'kind': 'other_channel_output_readout',
                          'donors': [{'channel': output['channel'], 'data_ids': output['data_ids']} for output in donors]})
        target_vector = vector([program_by_id[execution_id]['native_registers']['target'] for execution_id in item['validation_programs']])
        assert target_vector == vector(item['validation_target_vector'])
        transforms.append({'id': transform_id, 'step': step, 'cycle': item['cycle'],
                           'operation': operation, 'direction': item['extension_direction'],
                           'source_execution_ids': source_ids, 'outputs': generated,
                           'chain_updates': updates, 'other_channel_views': views,
                           'validation': {'validates_transform_id': transform_id,
                                          'execution_ids': item['validation_programs'],
                                          'execution_operation': OPERATIONS[item['validation_direction']],
                                          'target_vector_decimal': target_vector,
                                          'target_register_refs': [{'execution_id': execution_id, 'register': 'target'} for execution_id in item['validation_programs']],
                                          'supplies_next_transform_id': f'transform/{step + 1:04d}' if step < len(history) else None,
                                          'all_native_execution_checks_passed': True,
                                          'matches_1117_pattern': target_vector == ['1', '1', '1', '7']}})
        last_validation_ids = item['validation_programs']
    for channel, ids in enumerate(current_chain_ids, 1):
        assert [int(data[data_id]['value_decimal']) for data_id in ids] == final_values[channel - 1]

    core_records = []
    for context in core_manifest['channels']:
        channel = context['channel']
        start = context['retained_original_value_indices']['first']
        stop = context['retained_original_value_indices']['last_inclusive'] + 1
        source_execution = next(program['program'] for program in programs
                                if program['channel'] == channel and program['validates_extension_step'] == len(history))
        assert program_by_id[source_execution]['source_sha256'] == context['original_source_sha256']
        core_records.append({'id': f'core/channel{channel}', 'channel': channel,
                             'derived_from_execution_id': source_execution,
                             'derived_from_chain_revision': f'chain/c{channel}/step{len(history):04d}',
                             'retained_data_ids_in_order': current_chain_ids[channel - 1][start:stop],
                             'removed_prefix_data_ids': current_chain_ids[channel - 1][:start],
                             'removed_suffix_data_ids': current_chain_ids[channel - 1][stop:],
                             'registers': {'full_program_initial': words(context['full_initial_state']),
                                           'core_entry_after_prefix': words(context['captured_core_entry_state']),
                                           'native_core_exit': words(context['native_core_exit_state']),
                                           'full_exit_after_suffix': words(context['suffix_restored_full_exit_state'])},
                             'output': {'byte_count': 64, 'register_order': REGS,
                                        'stdout_hex': stdout_hex(context['native_core_exit_state'])},
                             'files': {kind: {'path': 'captured_aligned_core_pass100/' + info['name'],
                                              'sha256': info['sha256'], 'bytes': info['bytes']}
                                       for kind, info in context['files'].items()}})
    core_trace = []
    with (root / 'assembly_analysis_pass100/integer_state_trace.csv').open(encoding='utf-8-sig', newline='') as handle:
        for row in csv.DictReader(handle):
            channel, index = int(row['channel']), int(row['value_index'])
            if not 74 <= index < 2008:
                continue
            data_id = current_chain_ids[channel - 1][index]
            assert data[data_id]['value_decimal'] == row['raw_integer']
            core_trace.append({'core_id': f'core/channel{channel}', 'channel': channel,
                               'core_value_index': index - 74, 'full_chain_value_index': index,
                               'data_id': data_id, 'executed_operator_string': row['operators'],
                               'registers_after_value': {register: row[register] for register in REGS},
                               'capture_kind': 'operator_reference_trace_reconciled_with_native_core_exit'})
    for core in core_records:
        trace = [row for row in core_trace if row['channel'] == core['channel']]
        assert len(trace) == 1934
        assert trace[-1]['registers_after_value'] == core['registers']['native_core_exit']
    assert (len(data), len(executions), len(transforms), len(core_trace)) == (8400, 804, 200, 7736)

    document = {
        'schema_version': '1.0', 'run_id': 'native-reassembly-pass100',
        'summary': {'channels': 4, 'passes_each_direction': 100,
                    'reflection_steps': 100, 'projection_steps': 100,
                    'native_executions': len(executions), 'data_values': len(data),
                    'original_values': 7200, 'generated_values': 1200,
                    'captured_core_value_snapshots': len(core_trace),
                    'final_reflection_target_vector': vector(run_report['final_back']),
                    'current_native_core_target_vector': [core['registers']['native_core_exit']['target'] for core in core_records]},
        'conventions': {'uint64_encoding': 'Exact decimal strings; optional 0x-prefixed hexadecimal. Counts/indices are JSON integers.',
                        'register_order': REGS,
                        'operations': {'x_to_y': 'reflection', 'y_to_x': 'projection'},
                        'output_selection': {'reflection': ['target'], 'projection': ['state', 'relations']},
                        'left_insert_order': ['state', 'relations'],
                        'validation': 'Execution after extension N validates N and provides data used in extension N+1.',
                        'other_channel_views': 'Readout selections only; actual insertions and seeding are recorded separately.',
                        'artifact_paths_relative_to': 'experiments/endpoint_phase_v1',
                        'snapshot_granularity': {'native_execution': 'All eight cells before seeding, after seeding and after execution.',
                                                 'captured_core': 'All eight cells after each encoded input value; intermediate trace is reference execution reconciled with native final output.'}},
        'sources': {'archive_name': args.archive.name, 'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
                    'program_manifest_sha256': hashlib.sha256((run_dir / 'program_manifest.json').read_bytes()).hexdigest(),
                    'phase_history_sha256': hashlib.sha256((run_dir / 'phase_history.json').read_bytes()).hexdigest(),
                    'channel_identity': 'Recorded ranked spectral stripes; frequency metadata is retained per source value.'},
        'captured_cores': core_records,
        'executions': list(executions.values()), 'transforms': transforms,
        'data': list(data.values()),
        'chains': [{'channel': channel, 'initial_revision': f'chain/c{channel}/step0000',
                    'final_revision': f'chain/c{channel}/step0200',
                    'initial_data_ids_in_order': initial_chain_ids[channel - 1],
                    'final_data_ids_in_order': current_chain_ids[channel - 1]}
                   for channel in range(1, 5)],
        'core_value_trace': core_trace,
        'checks': {'all_native_output_registers_linked': True,
                   'all_seed_data_refs_resolved': True,
                   'all_transformed_values_match_source_registers': True,
                   'all_chain_revision_hashes_match_native_runs': True,
                   'all_final_chains_reconstructed_exactly': True,
                   'all_core_trace_exits_match_native_output': True}}
    # Do not accidentally reintroduce JavaScript-unsafe machine integers in a
    # nested source object. Every uint64 word must remain a string.
    def check_safe_json_numbers(value):
        if isinstance(value, dict):
            for child in value.values():
                check_safe_json_numbers(child)
        elif isinstance(value, list):
            for child in value:
                check_safe_json_numbers(child)
        elif isinstance(value, int) and not isinstance(value, bool):
            assert abs(value) <= (1 << 53) - 1
    check_safe_json_numbers(document)
    args.output.mkdir(parents=True)
    main_path = args.output / 'transform_trace.json'
    save(main_path, document)
    chosen = transforms[1]
    example_ids = set(chosen['source_execution_ids'] + chosen['validation']['execution_ids'])
    example_data_ids = {data_id for output in chosen['outputs'] for data_id in output['data_ids']}
    for execution_id in example_ids:
        example_data_ids.update(executions[execution_id]['opposite_endpoint_data_ids'])
    save(args.output / 'projection_example.json', {
        'subset_of': 'transform_trace.json', 'note': 'Unexpanded chain and feedback references resolve in the complete trace.',
        'transform': chosen,
        'executions': [executions[execution_id] for execution_id in sorted(example_ids)],
        'data': [data[data_id] for data_id in sorted(example_data_ids)]})
    save(args.output / 'trace_verification.json', {
        'summary': document['summary'], 'checks': document['checks'],
        'javascript_unsafe_json_numbers': 0,
        'transform_trace_sha256': hashlib.sha256(main_path.read_bytes()).hexdigest(),
        'bytes': main_path.stat().st_size})
    print(json.dumps({'path': str(main_path), 'bytes': main_path.stat().st_size, **document['summary']}))


if __name__ == '__main__':
    main()
