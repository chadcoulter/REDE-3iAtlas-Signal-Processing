"""Add a compact phase-array view without editing the recorded native run."""
import argparse
import collections
import json
from pathlib import Path


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
    simple = [{'cycle': row['cycle'], 'phase_in': row['phase_in'], 'phase_out': row['phase_out'],
               'projection_state': row['projection_state_vector'],
               'projection_relations': row['projection_relations_vector']} for row in history]
    positions = []
    for index in range(4):
        values = [row['phase_out'][index] for row in history]
        unique = sorted(set(values), key=int)
        positions.append({'position_zero_based': index, 'unique_output_values': len(unique),
                          'constant': len(unique) == 1,
                          'minimum_decimal': unique[0], 'maximum_decimal': unique[-1],
                          'values_with_counts': [{'value_decimal': value, 'count': count}
                                                 for value, count in collections.Counter(values).most_common()]})
    summary = {'initial_phase': report['initial_phase'], 'final_phase': report['final_phase'],
               'cycles': len(history), 'native_programs_passed': report['native_programs_passed'],
               'distinct_output_phase_arrays': len({tuple(row['phase_out']) for row in history}),
               'repeated_phase_arrays_including_initial': len(report['phase_repetitions']),
               'complete_register_state_repeats': len(report['complete_register_state_repetitions']),
               'per_position': positions,
               'projection_state_always_1111': all(row['projection_state_vector'] == ['1'] * 4 for row in history),
               'observed_pattern_cycles': report['observed_pattern_cycles'],
               'final_projection_relations': history[-1]['projection_relations_vector'],
               'signal_chains_unchanged': report['signal_chains_unchanged']}
    save(root / 'phase_arrays.json', simple)
    save(root / 'phase_result_summary.json', summary)
    print(json.dumps({key: summary[key] for key in ('cycles', 'native_programs_passed', 'initial_phase', 'final_phase', 'distinct_output_phase_arrays', 'repeated_phase_arrays_including_initial', 'complete_register_state_repeats', 'observed_pattern_cycles')}))


if __name__ == '__main__':
    main()
