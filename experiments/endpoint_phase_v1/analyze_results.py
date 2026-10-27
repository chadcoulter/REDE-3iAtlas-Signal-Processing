"""Add a seed-retention audit without altering the recorded experiment."""
import csv
import json
from pathlib import Path

root = Path(__file__).resolve().parent / 'results_initial'
counts = {key: 0 for key in (
    'reverse_rows', 'state_equals_its_seed', 'relations_equals_its_seed',
    'state_matches_current_channel_original_x',
    'relations_matches_current_channel_original_x',
    'state_match_also_unchanged_seed', 'relations_match_also_unchanged_seed')}
with (root / 'register_trace.csv').open(encoding='utf-8') as handle:
    for row in csv.DictReader(handle):
        if row['direction'] != 'y_to_x':
            continue
        seeds = json.loads(row['opposite_raw_integers'])
        original = seeds[int(row['channel']) - 1]
        counts['reverse_rows'] += 1
        for register in ('state', 'relations'):
            unchanged = row['before_' + register] == row['after_' + register]
            matches = int(row['after_' + register]) == original
            counts[register + '_equals_its_seed'] += unchanged
            counts[register + '_matches_current_channel_original_x'] += matches
            counts[register + '_match_also_unchanged_seed'] += matches and unchanged
first = json.loads((root / 'first_row.json').read_text(encoding='utf-8'))
# Independent arithmetic check of first-row target projections under the chosen mapping.
y = first['y_rounded']
expected_targets = [1, (y[0] + y[1] + 2) % (1 << 64), 1, y[0] + 1]
assert first['forward_target'] == expected_targets
assert not any(first['state_matches']) and not any(first['relations_matches'])
report = {'counts': counts, 'manual_first_row_target_check': 'passed',
          'first_row_any_original_x_matches': False,
          'interpretation': 'Original x values are supplied as reverse seeds. Matches that retain those seeds must not be treated as reconstruction from projected targets alone.',
          'next_wiring_question': 'The current candidate uses separate banks. A shared cross-channel machine could have different propagation; the missing four-lane assembly would specify this.'}
with (root / 'seed_retention_audit.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, indent=2)
print(json.dumps(report))
