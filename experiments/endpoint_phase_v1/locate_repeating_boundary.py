"""Locate the transition into the user's candidate start-boundary pattern.

Creates a new boundary window and exact per-operator provenance, without
altering the existing experiments. The user interprets the repeating Y vector
[1,1,1,7] as indicating that the start has been passed.
"""
import csv
import json
from pathlib import Path

from endpoint_phase import load_archive, numeral_table
from operator_machine import REGS, execute

root = Path(__file__).resolve().parent
source = root / 'stateful_100_results'
output = root / 'repeating_boundary_window'
if output.exists():
    raise FileExistsError('Boundary inspection output already exists')
table = numeral_table(root.parents[1] / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
bands = load_archive(Path('C:/Users/ccoulter/Downloads/3I_ATLAS_six_recordings_four_stripes_asm.zip'), table)
history = json.loads((source / 'phase_history.json').read_text())
target = [1, 1, 1, 7]
entry = next(i for i, row in enumerate(history) if row['back'] == target)
assert all(row['back'] == target for row in history[entry:])
window = history[max(0, entry - 2):entry + 3]
records = []
with (source / 'register_trace.csv').open(encoding='utf-8') as handle:
    for row in csv.DictReader(handle):
        if row['channel'] != '4' or int(row['cycle']) not in (2, 3):
            continue
        state = {reg: int(row['seeded_' + reg]) for reg in REGS}
        for index, glyph in enumerate(row['executed_commands'], 1):
            before = state.copy()
            execute(bands[3]['ops'][glyph], state)
            records.append({'cycle': int(row['cycle']), 'direction': row['direction'],
                            'channel': 4, 'op_index': index, 'glyph': glyph,
                            **{'before_' + reg: before[reg] for reg in REGS},
                            **{'after_' + reg: state[reg] for reg in REGS}})
        assert state == {reg: int(row['after_' + reg]) for reg in REGS}
output.mkdir()
with (output / 'endpoint_window.csv').open('x', newline='', encoding='utf-8') as handle:
    keys = ['cycle', 'right_target', 'left_state_relations', 'front', 'back']
    writer = csv.DictWriter(handle, fieldnames=keys)
    writer.writeheader()
    writer.writerows({key: json.dumps(row[key]) if isinstance(row[key], list) else row[key] for key in keys} for row in window)
with (output / 'channel4_operator_window.csv').open('x', newline='', encoding='utf-8') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)
report = {'working_boundary_criterion': 'User interprets entry into repeating [1,1,1,7] as having passed the start.',
          'layout_producing_this_cycle': 'Retained-register feedback; prepend [state, relations], with state outermost.',
          'first_y_pattern_pass': history[entry]['cycle'],
          'last_y_vector_before_pattern': history[entry - 1]['back'],
          'first_y_vector_in_pattern': target,
          'first_complete_state_repetition': {'pass': 4, 'repeats_pass': 3},
          'channel4_target7_creation': 'Pass 2 reverse, final Phi: target = state XOR context = 1 XOR 6 = 7.',
          'channel4_target7_first_appended': 'Pass 3 forward: Alpha sets state=1 while retained target stays 7.',
          'channel4_zero_creation': 'Pass 3 reverse, Zeta: relations = 1 XOR 1 = 0; state stays 1.',
          'channel4_left_pair_at_entry': history[entry]['left_state_relations'][3],
          'candidate_boundary_window': 'Between passes 2 and 3; inspect the pass-2 reverse creation of target7 before the first repeated endpoint.',
          'y_eof_assignment': None}
with (output / 'boundary_report.json').open('x', encoding='utf-8') as handle:
    json.dump(report, handle, indent=2)
print(json.dumps(report))
