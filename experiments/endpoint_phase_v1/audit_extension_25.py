"""Verify original-chain preservation and add an inspection CSV; new files only."""
import csv
import json
from pathlib import Path

from endpoint_phase import encode, load_archive, numeral_table, phase

root = Path(__file__).resolve().parent
output = root / 'extension_25_results'
table = numeral_table(root.parents[1] / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
report = json.loads((output / 'extension_report.json').read_text())
bands = load_archive(Path('C:/Users/ccoulter/Downloads/3I_ATLAS_six_recordings_four_stripes_asm.zip'), table)
chains = json.loads((output / 'final_chains.json').read_text())
passes = report['passes_each_direction']
offset = 2 * passes
audit = []
with (output / 'extended_chain_values.csv').open('x', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=['channel', 'index', 'region', 'extension_pass', 'register', 'value', 'numerals'])
    writer.writeheader()
    for channel, (chain, band) in enumerate(zip(chains, bands), 1):
        original = [frame['rounded'] for frame in band['frames']]
        assert chain[offset:offset + len(original)] == original
        assert len(chain) == len(original) + 3 * passes
        for index, value in enumerate(chain):
            if index < offset:
                region, cycle = 'front_extension', passes - index // 2
                register = 'state' if index % 2 == 0 else 'relations'
            elif index < offset + len(original):
                region, cycle, register = 'original', '', ''
            else:
                region = 'back_extension'
                cycle = index - offset - len(original) + 1
                register = 'target'
            writer.writerow({'channel': channel, 'index': index, 'region': region,
                             'extension_pass': cycle, 'register': register,
                             'value': value, 'numerals': encode(value, table)})
        audit.append({'channel': channel, 'original_values_preserved_in_order': True,
                      'front_added': offset, 'back_added': passes, 'final_length': len(chain),
                      'first_six': chain[:6], 'last_six': chain[-6:]})
# Explain, rather than silently classify, the repeated endpoint value.
right, _ = phase([1] * 4, [1] * 4, 'x_to_y', bands, table)
left, _ = phase(right, [1] * 4, 'y_to_x', bands, table)
assert right == [1] * 4 and left == [[1, 1]] * 4
result = {'chains': audit, 'all_one_endpoint_state_repeats_under_current_wiring': True,
          'reason': '1 encodes as Alpha. Its archived instruction writes state=1. With all-one endpoints, target and relations also stay at their all-one seeds.',
          'zero_observations': report['literal_zero_observations'],
          'y_termination': 'No EOF marker defined or identified in this run; repeated 1 is recorded as an endpoint fixed point.'}
with (output / 'chain_integrity_audit.json').open('x', encoding='utf-8') as handle:
    json.dump(result, handle, indent=2)
print(json.dumps(result))
