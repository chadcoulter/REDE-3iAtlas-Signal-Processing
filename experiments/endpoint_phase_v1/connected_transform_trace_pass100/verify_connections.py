"""Independently check connected JSON references and exact native word output."""
import hashlib
import json
import struct
from pathlib import Path

root = Path(__file__).resolve().parent
trace = json.loads((root / 'transform_trace.json').read_text(encoding='utf-8'))
registers = trace['conventions']['register_order']
data = {value['id']: value for value in trace['data']}
executions = {value['id']: value for value in trace['executions']}
transforms = {value['id']: value for value in trace['transforms']}
assert len(data) == 8400 and len(executions) == 804 and len(transforms) == 200

def check_words(state):
    assert list(state) == registers
    for value in state.values():
        assert isinstance(value, str) and value.isdigit() and 0 <= int(value) < 1 << 64

for value in data.values():
    assert isinstance(value['value_decimal'], str)
    assert int(value['value_decimal']) == int(value['value_hex'], 16)
    if value['origin']['kind'] in ('reflection', 'projection'):
        origin = value['origin']
        assert origin['transform_id'] in transforms
        producer = executions[origin['source_execution_id']]
        assert producer['registers']['native_after_execution'][origin['source_register']] == value['value_decimal']
for execution in executions.values():
    for state in execution['registers'].values():
        check_words(state)
    output_words = execution['registers']['native_after_execution']
    raw = bytes.fromhex(execution['output']['stdout_hex'])
    assert len(raw) == 64
    assert list(struct.unpack('<8Q', raw)) == [int(output_words[register]) for register in registers]
    for register, source in execution['seed_sources'].items():
        assert data[source['data_id']]['value_decimal'] == execution['registers']['after_endpoint_seeding'][register]
    previous = execution['feedback_from_execution_id']
    if previous:
        assert execution['registers']['retained_before_seed'] == executions[previous]['registers']['native_after_execution']
chains = [record['initial_data_ids_in_order'].copy() for record in trace['chains']]
for transform in trace['transforms']:
    step = transform['step']
    for update in transform['chain_updates']:
        chain = chains[update['channel'] - 1]
        assert len(chain) == update['before_value_count']
        if update['insert_at'] == 'front':
            chain[0:0] = update['inserted_data_ids_in_chain_order']
        else:
            chain.extend(update['inserted_data_ids_in_chain_order'])
        assert len(chain) == update['after_value_count']
        raw = b''.join(struct.pack('<Q', int(data[value]['value_decimal'])) for value in chain)
        assert hashlib.sha256(raw).hexdigest() == update['after_chain_sha256']
    validation = transform['validation']
    assert validation['validates_transform_id'] == transform['id']
    for execution_id in validation['execution_ids']:
        assert executions[execution_id]['validates_transform_id'] == transform['id']
    if step < 200:
        assert transforms[f'transform/{step + 1:04d}']['source_execution_ids'] == validation['execution_ids']
    for view in transform['other_channel_views']:
        assert len(view['donors']) == 3
        assert view['active_channel'] not in [donor['channel'] for donor in view['donors']]
        for donor in view['donors']:
            assert all(data[value]['channel'] == donor['channel'] for value in donor['data_ids'])
for current, expected in zip(chains, trace['chains']):
    assert current == expected['final_data_ids_in_order']
for core in trace['captured_cores']:
    assert core['derived_from_execution_id'] in executions
    assert len(core['retained_data_ids_in_order']) == 1934
    assert all(value in data for value in core['retained_data_ids_in_order'])
    for state in core['registers'].values():
        check_words(state)
    raw = bytes.fromhex(core['output']['stdout_hex'])
    assert list(struct.unpack('<8Q', raw)) == [int(core['registers']['native_core_exit'][register]) for register in registers]
for row in trace['core_value_trace']:
    assert row['data_id'] in data
    check_words(row['registers_after_value'])
report = {'native_runs_checked': len(executions), 'transforms_checked': len(transforms),
          'values_checked': len(data), 'core_value_snapshots_checked': len(trace['core_value_trace']),
          'all_producer_register_links_exact': True, 'all_native_output_bytes_exact': True,
          'all_seed_and_feedback_links_exact': True, 'all_chain_revisions_reconstructed': True,
          'all_previous_pass_validation_links_exact': True, 'all_other_channel_readouts_linked': True}
with (root / 'connection_audit.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, indent=2)
print(json.dumps(report))
