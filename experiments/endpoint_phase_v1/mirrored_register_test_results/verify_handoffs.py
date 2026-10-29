"""Audit mirrored routing, one-slot substitutions and archived native outputs."""
import hashlib
import json
import struct
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
report = json.loads((root / 'mirrored_register_test.json').read_text(encoding='utf-8'))
registers = report['register_order']
executions = {execution['id']: execution for execution in report['executions']}
assert len(executions) == 40 and len(report['cases']) == 9
assert report['function_output_register'] == 'target'
assert not report['endpoint_reseeding_at_handoff']
assert report['cases_independent']
with zipfile.ZipFile(root / 'assembled_sources.zip') as sources, zipfile.ZipFile(root / 'native_executables.zip') as binaries:
    assert len(sources.namelist()) == len(binaries.namelist()) == 40
    for execution in executions.values():
        for state in (execution['seed_registers'], execution['native_ending_registers']):
            assert list(state) == registers
            assert all(isinstance(word, str) and 0 <= int(word) < 1 << 64 for word in state.values())
        native_words = struct.unpack('<8Q', bytes.fromhex(execution['output']['stdout_hex']))
        assert list(native_words) == [int(execution['native_ending_registers'][register]) for register in registers]
        assert execution['checks']['native_exit'] == 0 and execution['checks']['all_registers_match_reference']
        artifact = execution['artifacts']
        assert hashlib.sha256(sources.read(artifact['assembly_member'])).hexdigest() == artifact['source_sha256']
        binary = binaries.read(artifact['executable_member'])
        assert hashlib.sha256(binary).hexdigest() == artifact['executable_sha256']
        assert binary[:5] == b'\x7fELF\x02' and binary[18:20] == b'\x3e\x00'
control = report['cases'][0]
assert control['substituted_register'] is None
control_states = {row['destination_channel']: row['projection_ending_registers'] for row in control['handoffs']}
for case in report['cases']:
    slot = case['substituted_register']
    assert len(case['handoffs']) == 4
    for row in case['handoffs']:
        assert row['destination_channel'] == 5 - row['source_channel']
        forward = executions[row['reflection_execution_id']]
        reverse = executions[row['projection_execution_id']]
        assert forward['channel'] == row['source_channel'] and forward['operation'] == 'reflection'
        assert reverse['channel'] == row['destination_channel'] and reverse['operation'] == 'projection'
        expected = forward['native_ending_registers'].copy()
        if slot:
            expected[slot] = forward['native_ending_registers'][report['function_output_register']]
        assert row['handoff_registers'] == reverse['seed_registers'] == expected
        preserved = [register for register in registers if register != slot]
        assert all(reverse['seed_registers'][register] == forward['native_ending_registers'][register] for register in preserved)
        baseline = control_states[row['destination_channel']]
        assert row['changed_projection_outputs_vs_control'] == [register for register in registers if reverse['native_ending_registers'][register] != baseline[register]]
    ordered = sorted(case['handoffs'], key=lambda row: row['destination_channel'])
    assert case['readouts'] == {register: [row['projection_ending_registers'][register] for row in ordered] for register in registers}
identity = next(case for case in report['cases'] if case['substituted_register'] == report['function_output_register'])
assert identity['readouts'] == control['readouts']
audit = {'result': 'passed', 'native_programs_checked': 40, 'cases_checked': 9,
         'mirrored_handoffs_checked': 36,
         'routing_1_to_4_2_to_3_3_to_2_4_to_1': True,
         'all_ending_registers_passed_without_reseeding': True,
         'only_selected_register_substituted': True,
         'all_other_registers_preserved': True,
         'target_identity_case_matches_control': True,
         'native_output_bytes_and_artifact_hashes_verified': True}
with (root / 'handoff_audit.json').open('x', encoding='utf-8') as handle:
    json.dump(audit, handle, indent=2)
print(json.dumps(audit))
