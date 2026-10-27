"""Check CSV precision and reconstruct every captured machine-code byte."""
import csv
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parent
core = root.parent / 'captured_aligned_core_pass100'
with (root / 'core_output.csv').open(encoding='utf-8-sig', newline='') as handle:
    outputs = list(csv.DictReader(handle))
assert len(outputs) == 32
for row in outputs:
    context = json.loads((core / f'channel{row["channel"]}_core.context.json').read_text(encoding='utf-8'))
    expected = context['native_core_exit_state'][row['register']]
    assert int(row['decimal_string']) == expected == int(row['hex_string'], 16)
with (root / 'core_transform_sequence.csv').open(encoding='utf-8-sig', newline='') as handle:
    sequence = list(csv.DictReader(handle))
assert len(sequence) == 7736
for channel in range(1, 5):
    rows = [row for row in sequence if int(row['channel']) == channel]
    text = (core / f'channel{channel}_core.S').read_text(encoding='utf-8')
    markers = list(re.finditer(r'(?m)^ # traversal_index=(\d+) raw_integer=(\d+) numerals=([^\n]*)$', text))
    assert len(rows) == len(markers) == 1934
    for index, (row, marker) in enumerate(zip(rows, markers)):
        assert int(row['core_index']) == index
        assert row['original_value_index'] == marker[1]
        assert row['raw_integer_string'] == marker[2]
        assert row['grouped_greek_numerals'] == marker[3].strip()
        end = markers[index + 1].start() if index + 1 < len(markers) else text.index('transform_core_end:')
        operators = ''.join(re.findall(r'(?m)^ # operator=(.)$', text[marker.start():end]))
        assert row['operator_string'] == operators
with (root / 'core_machine_code.csv').open(encoding='utf-8-sig', newline='') as handle:
    machine_rows = list(csv.DictReader(handle))
restored = {str(channel): bytearray() for channel in range(1, 5)}
for row in machine_rows:
    buffer = restored[row['channel']]
    assert int(row['byte_offset_hex'], 16) == len(buffer)
    chunk = bytes.fromhex(row['machine_code_hex'][2:])
    assert len(chunk) == int(row['byte_count'])
    buffer.extend(chunk)
for channel in range(1, 5):
    assert bytes(restored[str(channel)]) == (core / f'channel{channel}_core.code.bin').read_bytes()
report = {'native_register_rows': len(outputs), 'transform_sequence_rows': len(sequence),
          'machine_code_rows': len(machine_rows), 'uint64_values_preserved_exactly': True,
          'operator_strings_match_assembly': True, 'all_machine_code_bytes_reconstruct_exactly': True,
          'csv_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                         for name in ('core_output.csv', 'core_transform_sequence.csv', 'core_machine_code.csv')}}
with (root / 'verification.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, indent=2)
print(json.dumps(report))
