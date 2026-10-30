"""Feed rotated projection targets into the next phase array, n+1 mod 4.

Signal/core chains stay fixed. At reflection entry the four phase words fill
the existing input slots (state, relations, constraints, observations); the
remaining cells retain the preceding projection's native state. At the turn,
copy all eight reflection outputs to the next channel and substitute only
state <- target. Every reflection and projection is freshly assembled/run.
Only new output files are created.
"""
import argparse
import hashlib
import json
import platform
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path

from endpoint_phase import DEFAULT_MAPPING, load_archive, numeral_table
from native_reassemble_every_pass import render
from operator_machine import REGS, validate


def words(state):
    return {register: str(state[register]) for register in REGS}


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def digest_chain(chain):
    return hashlib.sha256(b''.join(struct.pack('<Q', value) for value in chain)).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--cycles', type=int, default=100)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise RuntimeError('Run inside WSL Ubuntu x86-64')
    if args.output.exists():
        raise FileExistsError('Output directory must be new')
    if args.cycles < 1:
        raise ValueError('Cycle count must be positive')
    assert tuple(DEFAULT_MAPPING) == ('state', 'relations', 'constraints', 'observations')
    root = Path(__file__).resolve().parent
    table = numeral_table(root.parents[1] / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    core_manifest = json.loads((root / 'captured_aligned_core_pass100/core_manifest.json').read_text())
    full_chains = json.loads((root / 'native_reassembly_100_results/final_chains.json').read_text())
    chains = []
    for channel, core in enumerate(core_manifest['channels'], 1):
        start = core['retained_original_value_indices']['first']
        stop = core['retained_original_value_indices']['last_inclusive'] + 1
        chain = full_chains[channel - 1][start:stop]
        assert len(chain) == 1934
        chains.append(chain)
    chain_hashes = [digest_chain(chain) for chain in chains]
    source_path = root / 'rotated_register_test_results/rotated_register_test.json'
    source_report = json.loads(source_path.read_text())
    source_case = next(case for case in source_report['cases'] if case['id'] == 'replace_1_state')
    initial_phase = [int(value) for value in source_case['readouts']['target']]
    assert initial_phase == [1, 14682301134823862838, 2, 1]
    ordered_handoffs = sorted(source_case['handoffs'], key=lambda row: row['destination_channel'])
    feedback = [{register: int(row['projection_ending_registers'][register]) for register in REGS}
                for row in ordered_handoffs]
    assert [state['target'] for state in feedback] == initial_phase
    phase = initial_phase.copy()
    prior_feedback_ids = [row['projection_execution_id'] for row in ordered_handoffs]
    initial_feedback = [state.copy() for state in feedback]
    validation_cases = sum(validate(band['ops']) for band in bands)
    args.output.mkdir(parents=True)
    scratch = Path(tempfile.mkdtemp(prefix='atlas-rotated-phase-feedback-'))
    executions, history, repeats = [], [], []
    source_body_hashes = {}
    seen_phase = {tuple(phase): 0}
    seen_complete = {tuple(phase + [state[register] for state in feedback for register in REGS]): 0}
    complete_repeats = []
    zeros = []
    pattern_hits = {'2222': [], '1117': [], '2151': []}
    with zipfile.ZipFile(args.output / 'assembled_sources.zip', mode='x', compression=zipfile.ZIP_DEFLATED) as sources, zipfile.ZipFile(args.output / 'native_executables.zip', mode='x', compression=zipfile.ZIP_DEFLATED) as binaries:

        def execute_native(cycle, channel, direction, seeds, source_ids):
            name = f'cycle{cycle:03d}_{direction}_channel{channel}'
            source, expected, count = render(chains[channel - 1], bands[channel - 1]['ops'], table, seeds, direction)
            body_hash = hashlib.sha256(source.split('.section .text\n', 1)[1].encode()).hexdigest()
            key = (channel, direction)
            if key not in source_body_hashes:
                source_body_hashes[key] = body_hash
            assert body_hash == source_body_hashes[key]
            assembly_path = scratch / (name + '.S')
            object_path = scratch / (name + '.o')
            executable_path = scratch / (name + '.elf')
            with assembly_path.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(source)
            for command in (['/usr/bin/as', '--64', str(assembly_path), '-o', str(object_path)],
                            ['/usr/bin/ld', '--build-id=none', '-o', str(executable_path), str(object_path)]):
                result = subprocess.run(command, capture_output=True, timeout=60)
                if result.returncode:
                    raise RuntimeError(result.stderr.decode(errors='replace'))
            result = subprocess.run([str(executable_path)], capture_output=True, timeout=30)
            if result.returncode or len(result.stdout) != 64:
                raise RuntimeError(f'{name}: exit={result.returncode}; bytes={len(result.stdout)}')
            actual = dict(zip(REGS, struct.unpack('<8Q', result.stdout)))
            assert actual == expected
            record = {'id': name, 'cycle': cycle, 'channel_one_based': channel,
                      'channel_zero_based': channel - 1,
                      'operation': 'reflection' if direction == 'x_to_y' else 'projection',
                      'direction': direction, 'source_execution_ids': source_ids,
                      'seed_registers': words(seeds), 'native_ending_registers': words(actual),
                      'output_hex': result.stdout.hex(), 'operator_invocations': count,
                      'chain_values': len(chains[channel - 1]), 'chain_sha256': chain_hashes[channel - 1],
                      'signal_instruction_body_sha256': body_hash,
                      'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                      'executable_sha256': hashlib.sha256(executable_path.read_bytes()).hexdigest(),
                      'checks': {'assembled': True, 'linked': True, 'native_exit': 0,
                                 'native_matches_reference': True}}
            executions.append(record)
            sources.writestr(name + '.S', source)
            binaries.write(executable_path, arcname=name + '.elf')
            return actual, name

        for cycle in range(1, args.cycles + 1):
            phase_in = phase.copy()
            feedback_before = [state.copy() for state in feedback]
            reflected, reflection_ids = [], []
            for channel in range(1, 5):
                seeds = feedback[channel - 1].copy()
                for register, value in zip(DEFAULT_MAPPING, phase_in):
                    seeds[register] = value
                for register in REGS:
                    if register not in DEFAULT_MAPPING:
                        assert seeds[register] == feedback[channel - 1][register]
                ending, execution_id = execute_native(cycle, channel, 'x_to_y', seeds, [prior_feedback_ids[channel - 1]])
                reflected.append(ending)
                reflection_ids.append(execution_id)
            projected, projection_ids = [None] * 4, [None] * 4
            handoffs = []
            for source_channel in range(1, 5):
                destination = source_channel % 4 + 1
                before = reflected[source_channel - 1]
                seeds = before.copy()
                seeds['state'] = before['target']
                assert all(seeds[register] == before[register] for register in REGS if register != 'state')
                ending, execution_id = execute_native(cycle, destination, 'y_to_x', seeds, [reflection_ids[source_channel - 1]])
                projected[destination - 1] = ending
                projection_ids[destination - 1] = execution_id
                handoffs.append({'source_zero_based': source_channel - 1,
                                 'destination_zero_based': destination - 1,
                                 'reflection_execution_id': reflection_ids[source_channel - 1],
                                 'projection_execution_id': execution_id,
                                 'substituted_register': 'state', 'function_output_register': 'target',
                                 'substitution_before_decimal': str(before['state']),
                                 'substitution_after_decimal': str(before['target']),
                                 'handoff_registers': words(seeds)})
            assert all(state is not None for state in projected)
            next_phase = [state['target'] for state in projected]
            phase_key = tuple(next_phase)
            if phase_key in seen_phase:
                repeats.append({'cycle': cycle, 'previous_cycle': seen_phase[phase_key],
                                'phase': [str(value) for value in next_phase]})
            else:
                seen_phase[phase_key] = cycle
            complete_key = tuple(next_phase + [state[register] for state in projected for register in REGS])
            if complete_key in seen_complete:
                complete_repeats.append({'cycle': cycle, 'previous_cycle': seen_complete[complete_key]})
            else:
                seen_complete[complete_key] = cycle
            for channel, state in enumerate(projected):
                for register in ('state', 'relations', 'target'):
                    if state[register] == 0:
                        zeros.append({'cycle': cycle, 'channel_zero_based': channel, 'register': register})
            for pattern, values in [('2222', [2, 2, 2, 2]), ('1117', [1, 1, 1, 7]), ('2151', [2, 1, 5, 1])]:
                if next_phase == values:
                    pattern_hits[pattern].append(cycle)
            history.append({'cycle': cycle, 'phase_in': [str(value) for value in phase_in],
                            'feedback_registers_before_reflection': [words(state) for state in feedback_before],
                            'reflection_execution_ids': reflection_ids,
                            'reflection_target_vector': [str(state['target']) for state in reflected],
                            'handoffs': handoffs, 'projection_execution_ids_by_destination': projection_ids,
                            'projection_state_vector': [str(state['state']) for state in projected],
                            'projection_relations_vector': [str(state['relations']) for state in projected],
                            'phase_out': [str(value) for value in next_phase],
                            'phase_out_supplies_next_cycle': True})
            phase = next_phase
            feedback = projected
            prior_feedback_ids = projection_ids
            save(args.output / f'checkpoint_cycle{cycle:03d}.json',
                 {'cycle': cycle, 'phase_in': history[-1]['phase_in'], 'phase_out': history[-1]['phase_out'],
                  'projection_state': history[-1]['projection_state_vector'],
                  'projection_relations': history[-1]['projection_relations_vector'],
                  'native_executions_passed': len(executions)})
            print(json.dumps({'cycle_completed': cycle, 'phase_out': history[-1]['phase_out'],
                              'projection_state': history[-1]['projection_state_vector'],
                              'native_executions_passed': len(executions)}), flush=True)
    assert len(executions) == args.cycles * 8
    assert [digest_chain(chain) for chain in chains] == chain_hashes
    report = {'test': 'Cyclic n+1 register handoff with native target-vector phase feedback.',
              'cycles': args.cycles, 'native_programs_built_and_run': len(executions),
              'native_programs_passed': len(executions),
              'initial_phase': [str(value) for value in initial_phase],
              'final_phase': [str(value) for value in phase],
              'initial_feedback_registers': [words(state) for state in initial_feedback],
              'final_feedback_registers': [words(state) for state in feedback],
              'source_case': 'replace_1_state', 'source_result': 'rotated_register_test_results/rotated_register_test.json',
              'source_result_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
              'mapping_zero_based': {'0': 1, '1': 2, '2': 3, '3': 0},
              'phase_seed_mapping': {str(index): register for index, register in enumerate(DEFAULT_MAPPING)},
              'phase_entry_rule': 'At each reflection entry, phase fills the four existing input slots; remaining registers retain preceding same-destination projection output.',
              'turn_rule': 'Copy all eight actual native reflection registers to next channel, substitute state <- target only; no endpoint reseeding at the turn.',
              'phase_feedback_rule': 'Projection targets ordered by destination positions 0,1,2,3 are the next cycle phase array.',
              'signal_chain_values_per_channel': [len(chain) for chain in chains],
              'signal_chain_sha256': chain_hashes, 'signal_chains_unchanged': True,
              'signal_instruction_bodies_unchanged': True,
              'native_output_drives_all_feedback': True,
              'phase_repetitions': repeats, 'complete_register_state_repetitions': complete_repeats,
              'zero_observations': zeros, 'observed_pattern_cycles': pattern_hits,
              'patterns_are_observations_not_new_failure_or_eof_labels': True,
              'word_encoding': 'Exact uint64 decimal strings; native output also retained as hexadecimal.',
              'operator_reference_validation_cases': validation_cases,
              'source_archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest()}
    save(args.output / 'phase_feedback_report.json', report)
    save(args.output / 'phase_history.json', history)
    save(args.output / 'execution_trace.json', executions)
    save(args.output / 'final_feedback_state.json', {'phase': report['final_phase'],
                                                  'registers_by_destination': report['final_feedback_registers'],
                                                  'source_execution_ids_by_destination': prior_feedback_ids})
    lines = ['# Cyclic phase feedback results', '',
             f'Cycles: {args.cycles}. Native programs passed: {len(executions)}/{len(executions)}.', '',
             'Phase and readout vectors are ordered by zero-based destination positions 0, 1, 2, 3.', '',
             f'Initial phase: `{report["initial_phase"]}`.', f'Final phase: `{report["final_phase"]}`.', '',
             'The phase array enters the existing state, relations, constraints and observations slots at reflection entry. The other cells retain native feedback. The turn copies all eight reflection outputs to (n+1)%4 and substitutes state with target only. The actual projection targets become the next phase. Signal/core instruction sequences are unchanged; every execution is freshly assembled and linked.', '',
             '| Cycle | Input phase | Output phase | Projection state |', '|---|---|---|---|']
    for row in history:
        lines.append(f'| {row["cycle"]} | {row["phase_in"]} | {row["phase_out"]} | {row["projection_state_vector"]} |')
    with (args.output / 'RESULTS.md').open('x', encoding='utf-8') as handle:
        handle.write('\n'.join(lines) + '\n')
    print(json.dumps({'cycles': args.cycles, 'native_programs_passed': len(executions),
                      'final_phase': report['final_phase'], 'phase_repeats': len(repeats),
                      'complete_state_repeats': len(complete_repeats)}), flush=True)


if __name__ == '__main__':
    main()
