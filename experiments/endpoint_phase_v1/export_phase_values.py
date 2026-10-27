"""Add a phase-oriented view, preserving every earlier experiment artifact."""
import csv
import json
from pathlib import Path

from endpoint_phase import encode, numeral_table

root = Path(__file__).resolve().parent
table = numeral_table(root.parents[1] / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
fields = ['row', 'second', 'channel', 'right_target', 'right_commands',
          'left_state', 'left_state_commands', 'left_relations', 'left_relations_commands']
count = 0
with (root / 'results_initial/phases.csv').open(encoding='utf-8') as source, (root / 'results_initial/phase_values.csv').open('x', newline='', encoding='utf-8') as output:
    writer = csv.DictWriter(output, fieldnames=fields)
    writer.writeheader()
    for record in csv.DictReader(source):
        right = json.loads(record['forward_target'])
        left = json.loads(record['reverse_state_relations'])
        for channel, (target, (state, relations)) in enumerate(zip(right, left), 1):
            writer.writerow({'row': record['row'], 'second': record['second'], 'channel': channel,
                             'right_target': target, 'right_commands': encode(target, table),
                             'left_state': state, 'left_state_commands': encode(state, table),
                             'left_relations': relations, 'left_relations_commands': encode(relations, table)})
            count += 1
print(json.dumps({'channel_phase_rows': count, 'output': 'results_initial/phase_values.csv'}))
