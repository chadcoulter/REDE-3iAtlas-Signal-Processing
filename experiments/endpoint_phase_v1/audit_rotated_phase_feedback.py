"""Verify phase continuity, exact register sources and unchanged signal bodies."""
import argparse
import hashlib
import json
import struct
import zipfile
from pathlib import Path

from operator_machine import REGS


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root = args.output
    report = json.loads((root / 'phase_feedback_report.json').read_text())
    history = json.loads((root / 'phase_history.json').read_text())
    execution_list = json.loads((root / 'execution_trace.json').read_text())
    executions = {row['id']: row for row in execution_list}
    source_report = json.loads((root.parent / report['source_result']).read_text())
    assert hashlib.sha256((root.parent / report['source_result']).read_bytes()).hexdigest() == report['source_result_sha256']
    source_case = next(row for row in source_report['cases'] if row['id'] == report['source_case'])
    source_handoffs = sorted(source_case['handoffs'], key=lambda row: row['destination_channel'])
    previous_states = [row['projection_ending_registers'] for row in source_handoffs]
    previous_ids = [row['projection_execution_id'] for row in source_handoffs]
    phase = source_case['readouts']['target']
    assert phase == report['initial_phase']
    assert len(executions) == report['cycles'] * 8 == len(execution_list)
    assert len(history) == report['cycles']
    fixed_hashes = {}
    connections = []
    with zipfile.ZipFile(root / 'assembled_sources.zip') as sources, zipfile.ZipFile(root / 'native_executables.zip') as binaries:
        assert len(sources.namelist()) == len(binaries.namelist()) == len(executions)
        for execution in executions.values():
            assert execution['checks']['native_exit'] == 0 and execution['checks']['native_matches_reference']
            assert execution['chain_values'] == 1934
            assert execution['chain_sha256'] == report['signal_chain_sha256'][execution['channel_zero_based']]
            for state in (execution['seed_registers'], execution['native_ending_registers']):
                assert list(state) == REGS
                assert all(isinstance(word, str) and 0 <= int(word) < 1 << 64 for word in state.values())
            raw = bytes.fromhex(execution['output_hex'])
            assert list(struct.unpack('<8Q', raw)) == [int(execution['native_ending_registers'][register]) for register in REGS]
            source = sources.read(execution['id'] + '.S')
            binary = binaries.read(execution['id'] + '.elf')
            assert hashlib.sha256(source).hexdigest() == execution['source_sha256']
            assert hashlib.sha256(binary).hexdigest() == execution['executable_sha256']
            body_hash = hashlib.sha256(source.decode().split('.section .text\n', 1)[1].encode()).hexdigest()
            assert body_hash == execution['signal_instruction_body_sha256']
            key = (execution['channel_zero_based'], execution['direction'])
            fixed_hashes.setdefault(key, body_hash)
            assert body_hash == fixed_hashes[key]
    for row in history:
        assert row['phase_in'] == phase
        assert row['feedback_registers_before_reflection'] == previous_states
        reflection_ids = row['reflection_execution_ids']
        reflection = [executions[execution_id] for execution_id in reflection_ids]
        for channel, execution in enumerate(reflection):
            assert execution['channel_zero_based'] == channel and execution['operation'] == 'reflection'
            expected = previous_states[channel].copy()
            phase_links = {}
            for index, register in enumerate(('state', 'relations', 'constraints', 'observations')):
                expected[register] = phase[index]
                phase_links[register] = {'phase_index_zero_based': index,
                                         'source_execution_id': previous_ids[index],
                                         'source_register': 'target', 'value_decimal': phase[index]}
            assert execution['seed_registers'] == expected
            connections.append({'execution_id': execution['id'], 'operation': 'reflection',
                                'phase_array_seed_sources': phase_links,
                                'retained_sources': {register: {'source_execution_id': previous_ids[channel],
                                                               'source_register': register,
                                                               'value_decimal': previous_states[channel][register]}
                                                     for register in REGS if register not in phase_links}})
        projection_ids = row['projection_execution_ids_by_destination']
        projection = [executions[execution_id] for execution_id in projection_ids]
        assert len(row['handoffs']) == 4
        for handoff in row['handoffs']:
            source = handoff['source_zero_based']
            destination = handoff['destination_zero_based']
            assert destination == (source + 1) % 4
            forward = reflection[source]
            backward = projection[destination]
            assert backward['channel_zero_based'] == destination and backward['operation'] == 'projection'
            expected = forward['native_ending_registers'].copy()
            expected['state'] = forward['native_ending_registers']['target']
            assert backward['seed_registers'] == handoff['handoff_registers'] == expected
            assert backward['source_execution_ids'] == [forward['id']]
            connections.append({'execution_id': backward['id'], 'operation': 'projection',
                                'source_channel_zero_based': source, 'destination_channel_zero_based': destination,
                                'register_sources': {register: {'source_execution_id': forward['id'],
                                                                'source_register': 'target' if register == 'state' else register,
                                                                'value_decimal': expected[register]}
                                                     for register in REGS}})
        phase = [execution['native_ending_registers']['target'] for execution in projection]
        assert row['phase_out'] == phase
        assert row['projection_state_vector'] == [execution['native_ending_registers']['state'] for execution in projection]
        assert row['projection_relations_vector'] == [execution['native_ending_registers']['relations'] for execution in projection]
        previous_states = [execution['native_ending_registers'] for execution in projection]
        previous_ids = projection_ids
    assert phase == report['final_phase'] and previous_states == report['final_feedback_registers']
    smoke_dir = root.parent / 'rotated_phase_feedback_smoke_results'
    smoke_equal = None
    if report['cycles'] > 1 and (smoke_dir / 'execution_trace.json').exists():
        smoke = json.loads((smoke_dir / 'execution_trace.json').read_text())
        assert len(smoke) == 8
        for first, repeated in zip(execution_list[:8], smoke):
            assert first['seed_registers'] == repeated['seed_registers']
            assert first['native_ending_registers'] == repeated['native_ending_registers']
            assert first['source_sha256'] == repeated['source_sha256']
            assert first['executable_sha256'] == repeated['executable_sha256']
        smoke_equal = True
    save(root / 'feedback_connections.json', {'source_external_result': report['source_result'],
                                             'register_connections': connections})
    audit = {'result': 'passed', 'cycles_checked': len(history), 'native_programs_checked': len(executions),
             'phase_array_continuity_exact': True, 'all_phase_and_retained_register_sources_exact': True,
             'all_cyclic_n_plus_one_handoffs_exact': True, 'only_state_substituted_at_turn': True,
             'native_output_and_artifact_hashes_exact': True, 'signal_chain_values_unchanged': True,
             'all_eight_directional_signal_bodies_unchanged': len(fixed_hashes) == 8,
             'first_cycle_matches_independent_smoke': smoke_equal,
             'final_phase': phase}
    save(root / 'feedback_audit.json', audit)
    print(json.dumps(audit))


if __name__ == '__main__':
    main()
