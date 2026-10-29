"""Native one-register-at-a-time test of reflection i -> projection (5-i).

Run inside WSL. Execute each captured core forward, copy its actual native
ending registers, substitute one slot with its function output, then compile
and execute the mirrored core backward. No endpoint reseeding at the turn.
Only a fresh output directory and new files are written.
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

from endpoint_phase import load_archive, numeral_table
from native_reassemble_every_pass import render
from operator_machine import REGS, validate


def word_state(state):
    return {register: str(state[register]) for register in REGS}


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output-register', choices=REGS, default='target')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise RuntimeError('Run inside WSL Ubuntu x86-64')
    if args.output.exists():
        raise FileExistsError('Output directory must be new')
    root = Path(__file__).resolve().parent
    repo = root.parents[1]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    cores = json.loads((root / 'captured_aligned_core_pass100/core_manifest.json').read_text())['channels']
    full_chains = json.loads((root / 'native_reassembly_100_results/final_chains.json').read_text())
    chains = []
    for channel, core in enumerate(cores, 1):
        start = core['retained_original_value_indices']['first']
        stop = core['retained_original_value_indices']['last_inclusive'] + 1
        chain = full_chains[channel - 1][start:stop]
        assert len(chain) == core['retained_values'] == 1934
        chains.append(chain)
    validation_cases = sum(validate(band['ops']) for band in bands)
    args.output.mkdir(parents=True)
    scratch = Path(tempfile.mkdtemp(prefix='atlas-mirrored-handoff-'))
    executions, forward, case_results = [], [], []
    with zipfile.ZipFile(args.output / 'assembled_sources.zip', mode='x', compression=zipfile.ZIP_DEFLATED) as sources, zipfile.ZipFile(args.output / 'native_executables.zip', mode='x', compression=zipfile.ZIP_DEFLATED) as binaries:

        def execute_native(name, channel, direction, seeds, role, source_execution_id=None):
            source, expected, count = render(chains[channel - 1], bands[channel - 1]['ops'], table, seeds, direction)
            source_path = scratch / (name + '.S')
            object_path = scratch / (name + '.o')
            executable_path = scratch / (name + '.elf')
            with source_path.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(source)
            for command in (['/usr/bin/as', '--64', str(source_path), '-o', str(object_path)],
                            ['/usr/bin/ld', '--build-id=none', '-o', str(executable_path), str(object_path)]):
                result = subprocess.run(command, capture_output=True, timeout=60)
                if result.returncode:
                    raise RuntimeError(result.stderr.decode(errors='replace'))
            result = subprocess.run([str(executable_path)], capture_output=True, timeout=30)
            if result.returncode or len(result.stdout) != 64:
                raise RuntimeError(f'{name}: exit={result.returncode}; bytes={len(result.stdout)}')
            actual = dict(zip(REGS, struct.unpack('<8Q', result.stdout)))
            assert actual == expected
            record = {'id': name, 'role': role, 'channel': channel,
                      'operation': 'reflection' if direction == 'x_to_y' else 'projection',
                      'direction': direction, 'source_execution_id': source_execution_id,
                      'core_reference': f'core/channel{channel}',
                      'chain_values': len(chains[channel - 1]), 'operator_invocations': count,
                      'seed_registers': word_state(seeds), 'native_ending_registers': word_state(actual),
                      'output': {'format': 'eight_uint64_little_endian', 'stdout_hex': result.stdout.hex(), 'bytes': 64},
                      'checks': {'assembled': True, 'linked': True, 'native_exit': result.returncode,
                                 'all_registers_match_reference': True},
                      'artifacts': {'assembly_member': name + '.S', 'executable_member': name + '.elf',
                                    'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                                    'executable_sha256': hashlib.sha256(executable_path.read_bytes()).hexdigest()}}
            executions.append(record)
            sources.writestr(name + '.S', source)
            binaries.write(executable_path, arcname=name + '.elf')
            return actual, record

        for channel, core in enumerate(cores, 1):
            ending, record = execute_native(f'reflection_channel{channel}', channel, 'x_to_y',
                                            core['captured_core_entry_state'], 'reflection_baseline')
            assert ending == core['native_core_exit_state']
            forward.append({'channel': channel, 'ending': ending, 'execution': record})
        # Each case is independent and starts from the same native reflection
        # outputs. The control changes no slot; target substitution is also an
        # identity case when target is the configured function output.
        for selected_register in [None, *REGS]:
            case_id = 'control_no_substitution' if selected_register is None else f'replace_{REGS.index(selected_register) + 1}_{selected_register}'
            handoffs = []
            for source in forward:
                source_channel = source['channel']
                destination = 5 - source_channel
                before = source['ending'].copy()
                seeds = before.copy()
                function_output = before[args.output_register]
                if selected_register is not None:
                    seeds[selected_register] = function_output
                preserved = [register for register in REGS if register != selected_register]
                assert all(seeds[register] == before[register] for register in preserved)
                changed_seed = [register for register in REGS if seeds[register] != before[register]]
                assert not changed_seed if selected_register is None else set(changed_seed) <= {selected_register}
                ending, record = execute_native(f'{case_id}_reflection{source_channel}_projection{destination}',
                                                destination, 'y_to_x', seeds, case_id, source['execution']['id'])
                handoffs.append({'source_channel': source_channel, 'destination_channel': destination,
                                 'reflection_execution_id': source['execution']['id'],
                                 'projection_execution_id': record['id'],
                                 'function_output': {'source_register': args.output_register, 'value_decimal': str(function_output)},
                                 'substitution': {'register': selected_register,
                                                  'register_index_one_based': REGS.index(selected_register) + 1 if selected_register else None,
                                                  'before_decimal': str(before[selected_register]) if selected_register else None,
                                                  'after_decimal': str(seeds[selected_register]) if selected_register else None,
                                                  'actually_changed_seed_registers': changed_seed,
                                                  'preserved_registers': preserved},
                                 'handoff_registers': word_state(seeds),
                                 'projection_ending_registers': word_state(ending)})
            ordered = sorted(handoffs, key=lambda row: row['destination_channel'])
            readouts = {register: [row['projection_ending_registers'][register] for row in ordered] for register in REGS}
            if selected_register is None:
                control = {row['destination_channel']: row['projection_ending_registers'] for row in handoffs}
            for row in handoffs:
                baseline = control[row['destination_channel']]
                row['changed_projection_outputs_vs_control'] = [register for register in REGS if row['projection_ending_registers'][register] != baseline[register]]
            cases = {'id': case_id, 'substituted_register': selected_register,
                     'register_index_one_based': REGS.index(selected_register) + 1 if selected_register else None,
                     'handoffs': handoffs, 'readout_order': 'projection destination channels 1,2,3,4',
                     'readouts': readouts,
                     'projection_channels_changed_vs_control': [row['destination_channel'] for row in ordered if row['changed_projection_outputs_vs_control']],
                     'observed_target_patterns': {'equals_2222': readouts['target'] == ['2'] * 4,
                                                  'equals_1117': readouts['target'] == ['1', '1', '1', '7'],
                                                  'equals_2151': readouts['target'] == ['2', '1', '5', '1']}}
            if selected_register == args.output_register:
                assert all(not row['substitution']['actually_changed_seed_registers'] for row in handoffs)
                assert all(not row['changed_projection_outputs_vs_control'] for row in handoffs)
            case_results.append(cases)
            print(json.dumps({'case': case_id, 'projection_state_by_destination': readouts['state'],
                              'projection_target_by_destination': readouts['target'],
                              'changed_channels_vs_control': cases['projection_channels_changed_vs_control'],
                              'native_executions_passed': len(executions)}), flush=True)
    assert len(executions) == 40 and len(case_results) == 9
    report = {'test': 'Mirrored native register handoff with one register substitution at a time.',
              'branch': 'codex/atlas-endpoint-phase-test',
              'dataset': 'captured_aligned_core_pass100', 'values_per_channel': 1934,
              'mapping_reflection_to_projection': {'1': 4, '2': 3, '3': 2, '4': 1},
              'handoff': 'Copy all eight actual native ending registers, replace only the tested slot with the configured function output, then execute the mirrored chain backward.',
              'register_order': REGS, 'function_output_register': args.output_register,
              'projection_traversal': 'Reverse destination chain value order and glyph order; preserve register names/positions.',
              'reflection_initialization': 'Captured entry state of each current core.',
              'endpoint_reseeding_at_handoff': False, 'cases_independent': True,
              'chain_extension_performed': False,
              'control': 'Mirrored projection with unchanged reflection-ending state.',
              'native_programs_built_and_run': len(executions), 'native_programs_passed': len(executions),
              'operator_reference_validation_cases': validation_cases,
              'word_encoding': 'Exact unsigned 64-bit decimal strings; raw native output is hex.',
              'pattern_flags': 'Record observed vectors; no numeric pattern is assigned an unprovided success/failure meaning.',
              'forward_target_vector_by_source_channel': [str(source['ending'][args.output_register]) for source in forward],
              'reflection_execution_ids': [source['execution']['id'] for source in forward],
              'executions': executions, 'cases': case_results,
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest()}
    save(args.output / 'mirrored_register_test.json', report)
    save(args.output / 'case_readouts.json', [{key: case[key] for key in ('id', 'substituted_register', 'register_index_one_based', 'readout_order', 'readouts', 'projection_channels_changed_vs_control', 'observed_target_patterns')} for case in case_results])
    lines = ['# Mirrored one-register handoff results', '',
             'Actual native reflection output is handed to projection channel 5-i. Only the named register is substituted; seven other slots are preserved. No endpoint reseeding occurs. Each scenario starts independently from the same four native reflection results.', '',
             f'Function output for this run: `{args.output_register}`. Native programs passed: {len(executions)}/{len(executions)}.', '',
             'Vectors below are ordered by projection destination channel 1, 2, 3, 4.', '',
             '| Substitution | Projection state | Projection target | Changed channels vs control |',
             '|---|---|---|---|']
    for case in case_results:
        label = case['substituted_register'] or 'none (control)'
        lines.append(f'| {label} | {json.dumps(case["readouts"]["state"])} | {json.dumps(case["readouts"]["target"])} | {case["projection_channels_changed_vs_control"]} |')
    lines += ['', '`mirrored_register_test.json` contains all eight input/output registers, source/destination links, the actual changed seed slots, native source and executable hashes, and comparison results. `case_readouts.json` provides a smaller per-case view. `assembled_sources.zip` and `native_executables.zip` preserve every newly compiled program.', '',
              'The target-substitution case is an identity control when target is the selected function output. It must exactly match the no-substitution control. No original source, chain or previous result is edited.']
    with (args.output / 'RESULTS.md').open('x', encoding='utf-8') as handle:
        handle.write('\n'.join(lines) + '\n')
    print(json.dumps({'cases': 9, 'native_programs_passed': len(executions), 'output': str(args.output)}), flush=True)


if __name__ == '__main__':
    main()
