"""Verify n+1 routing and isolate changes from the previous mirrored run."""
import hashlib
import json
import struct
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
current = json.loads((root / 'rotated_register_test.json').read_text(encoding='utf-8'))
old_root = root.parent / 'mirrored_register_test_results'
previous = json.loads((old_root / 'mirrored_register_test.json').read_text(encoding='utf-8'))
registers = current['register_order']
executions = {execution['id']: execution for execution in current['executions']}
previous_exec = {execution['id']: execution for execution in previous['executions']}
previous_cases = {case['id']: case for case in previous['cases']}
assert len(executions) == 40 and len(current['cases']) == 9
assert current['mapping_zero_based'] == {'0': 1, '1': 2, '2': 3, '3': 0}
assert current['mapping_reflection_to_projection'] == {'1': 2, '2': 3, '3': 4, '4': 1}
assert not current['signal_chains_reordered'] and not current['endpoint_reseeding_at_handoff']
assert current['function_output_register'] == previous['function_output_register'] == 'target'
comparisons = []
body_checks = 0
with zipfile.ZipFile(root / 'assembled_sources.zip') as sources, zipfile.ZipFile(root / 'native_executables.zip') as binaries, zipfile.ZipFile(old_root / 'assembled_sources.zip') as old_sources:
    for execution in executions.values():
        assert execution['checks']['native_exit'] == 0 and execution['checks']['all_registers_match_reference']
        for state in (execution['seed_registers'], execution['native_ending_registers']):
            assert list(state) == registers
            assert all(isinstance(value, str) and 0 <= int(value) < 1 << 64 for value in state.values())
        raw = bytes.fromhex(execution['output']['stdout_hex'])
        assert list(struct.unpack('<8Q', raw)) == [int(execution['native_ending_registers'][reg]) for reg in registers]
        artifact = execution['artifacts']
        assert hashlib.sha256(sources.read(artifact['assembly_member'])).hexdigest() == artifact['source_sha256']
        assert hashlib.sha256(binaries.read(artifact['executable_member'])).hexdigest() == artifact['executable_sha256']
    # Reflection source chains, entry seeds and compiled results are identical.
    for execution_id in current['reflection_execution_ids']:
        now, old = executions[execution_id], previous_exec[execution_id]
        assert now['seed_registers'] == old['seed_registers']
        assert now['native_ending_registers'] == old['native_ending_registers']
        assert now['artifacts']['source_sha256'] == old['artifacts']['source_sha256']
        assert now['artifacts']['executable_sha256'] == old['artifacts']['executable_sha256']
    control = current['cases'][0]
    control_states = {row['destination_channel']: row['projection_ending_registers'] for row in control['handoffs']}
    for case in current['cases']:
        old_case = previous_cases[case['id']]
        old_by_destination = {row['destination_channel']: row for row in old_case['handoffs']}
        differences = []
        for row in case['handoffs']:
            assert row['destination_channel'] == row['source_channel'] % 4 + 1
            assert row['destination_channel'] - 1 == (row['source_channel'] - 1 + 1) % 4
            forward = executions[row['reflection_execution_id']]
            reverse = executions[row['projection_execution_id']]
            assert forward['channel'] == row['source_channel']
            assert reverse['channel'] == row['destination_channel']
            expected = forward['native_ending_registers'].copy()
            slot = case['substituted_register']
            if slot:
                expected[slot] = forward['native_ending_registers']['target']
            assert reverse['seed_registers'] == row['handoff_registers'] == expected
            assert all(reverse['seed_registers'][reg] == forward['native_ending_registers'][reg] for reg in registers if reg != slot)
            assert row['projection_ending_registers'] == reverse['native_ending_registers']
            baseline = control_states[row['destination_channel']]
            assert row['changed_projection_outputs_vs_control'] == [reg for reg in registers if reverse['native_ending_registers'][reg] != baseline[reg]]
            old_handoff = old_by_destination[row['destination_channel']]
            old_reverse = previous_exec[old_handoff['projection_execution_id']]
            # Prove that the instruction sequence in each physical destination
            # stayed in place. Only the seeded register data is allowed to differ.
            current_source = sources.read(reverse['artifacts']['assembly_member']).decode('utf-8')
            old_source = old_sources.read(old_reverse['artifacts']['assembly_member']).decode('utf-8')
            assert current_source.split('.section .text\n', 1)[1] == old_source.split('.section .text\n', 1)[1]
            body_checks += 1
            changed = [reg for reg in registers if row['projection_ending_registers'][reg] != old_handoff['projection_ending_registers'][reg]]
            if row['destination_channel'] in (1, 3):
                assert not changed
                assert reverse['seed_registers'] == old_reverse['seed_registers']
                assert reverse['artifacts']['executable_sha256'] == old_reverse['artifacts']['executable_sha256']
            differences.append({'destination_zero_based': row['destination_channel'] - 1,
                                'old_source_zero_based': old_handoff['source_channel'] - 1,
                                'new_source_zero_based': row['source_channel'] - 1,
                                'changed_registers': changed})
        identity_case = case['substituted_register'] == 'target'
        if identity_case:
            assert case['readouts'] == control['readouts']
        target_changes = [index for index, (old, new) in enumerate(zip(old_case['readouts']['target'], case['readouts']['target'])) if old != new]
        comparisons.append({'case_id': case['id'], 'substituted_register': case['substituted_register'],
                            'vector_order_zero_based': [0, 1, 2, 3],
                            'mirrored_projection_target': old_case['readouts']['target'],
                            'rotated_projection_target': case['readouts']['target'],
                            'rotated_projection_state': case['readouts']['state'],
                            'rotated_projection_relations': case['readouts']['relations'],
                            'target_positions_changed_vs_mirror': target_changes,
                            'register_changes_vs_mirror': sorted(differences, key=lambda row: row['destination_zero_based'])})
audit = {'result': 'passed', 'routing_zero_based': {'0': 1, '1': 2, '2': 3, '3': 0},
         'native_programs_checked': 40, 'cases_checked': 9,
         'all_physical_signal_instruction_bodies_unchanged': True,
         'projection_instruction_body_comparisons': body_checks,
         'all_forward_baselines_byte_identical_to_mirror_test': True,
         'all_register_handoffs_exact': True, 'only_selected_register_substituted': True,
         'all_native_outputs_and_artifact_hashes_verified': True,
         'target_identity_control_matches': True,
         'unchanged_routing_destinations_zero_based': [0, 2],
         'unchanged_routing_outputs_and_executables_identical': True}
with (root / 'handoff_audit.json').open('x', encoding='utf-8') as handle:
    json.dump(audit, handle, indent=2)
with (root / 'comparison_to_mirrored.json').open('x', encoding='utf-8') as handle:
    json.dump({'vector_order_zero_based': [0, 1, 2, 3], 'cases': comparisons}, handle, indent=2)
print(json.dumps(audit))
print(json.dumps(comparisons[1]))
