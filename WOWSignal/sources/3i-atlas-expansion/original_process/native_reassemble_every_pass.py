"""Native-driven extension: append/prepend, reassemble, execute, then continue.

Run inside WSL Ubuntu. Every new chain is assembled and executed before any
following projection. Actual native registers drive the next extension. The
portable interpreter only cross-checks execution; it does not supply feedback.
All paths must be new; original code/results are left unchanged.
"""
import argparse
import csv
import hashlib
import json
import platform
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path

from endpoint_phase import DEFAULT_MAPPING, encode, load_archive, numeral_table, views
from operator_machine import REGS, execute, validate


def digest_chain(chain):
    digest = hashlib.sha256()
    for value in chain:
        digest.update(struct.pack('<Q', value))
    return digest.hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def render(chain, operators, table, seeds, direction):
    lines = ['# Native-driven complete chain; ' + direction, '.section .data', '.balign 8']
    lines += [f'{register}: .quad {seeds[register]}' for register in REGS]
    lines += ['.section .text', '.globl _start', '.type _start,@function', '_start:']
    state = seeds.copy()
    count = 0
    values = chain if direction == 'x_to_y' else reversed(chain)
    for index, value in enumerate(values):
        encoded = encode(value, table)
        glyphs = ''.join(g for g in encoded if g not in ' |0')
        if direction == 'y_to_x':
            glyphs = glyphs[::-1]
        lines.append(f' # traversal_index={index} raw_integer={value} numerals={encoded}')
        for glyph in glyphs:
            lines.append(' # operator=' + glyph)
            lines.extend(operators[glyph])
            execute(operators[glyph], state)
            count += 1
    lines += [' movq $1,%rax', ' movq $1,%rdi', ' leaq state(%rip),%rsi',
              ' movq $64,%rdx', ' syscall', ' cmpq $64,%rax', ' jne 9f',
              ' movq $60,%rax', ' xorq %rdi,%rdi', ' syscall',
              '9:', ' movq $60,%rax', ' movq $1,%rdi', ' syscall',
              '.section .note.GNU-stack,"",@progbits']
    return '\n'.join(lines) + '\n', state, count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--passes', type=int, default=100)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if platform.system() != 'Linux' or platform.machine() != 'x86_64':
        raise RuntimeError('Run this native assembler loop in WSL Ubuntu x86-64')
    if args.output.exists():
        raise FileExistsError('Output directory must be new')
    if args.passes < 1:
        raise ValueError('Pass count must be positive')
    repo = Path(__file__).resolve().parents[2]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    validation_cases = sum(validate(band['ops']) for band in bands)
    chains = [[frame['rounded'] for frame in band['frames']] for band in bands]
    originals = [chain.copy() for chain in chains]
    args.output.mkdir(parents=True)
    # Unique scratch build names; retain all generated sources and ELF files in
    # archives. No previously existing file is edited or removed.
    scratch = Path(tempfile.mkdtemp(prefix='atlas-native-per-pass-'))
    programs, history, zeros, validation_patterns = [], [], [], []
    initial_feedback = [{register: 1 for register in REGS} for _ in bands]
    source_archive_path = args.output / 'assembled_sources.zip'
    executable_archive_path = args.output / 'native_executables.zip'
    stage_rows = []
    with zipfile.ZipFile(source_archive_path, mode='x', compression=zipfile.ZIP_DEFLATED) as sources, zipfile.ZipFile(executable_archive_path, mode='x', compression=zipfile.ZIP_DEFLATED) as executables:

        def compile_execute(direction, feedback, validates_step):
            front = [chain[0] for chain in chains]
            back = [chain[-1] for chain in chains]
            opposite = back if direction == 'x_to_y' else front
            states, ids = [], []
            expected_chain_hashes = [digest_chain(chain) for chain in chains]
            if validates_step:
                assert expected_chain_hashes == history[-1]['post_extension_chain_hashes']
            for channel, (band, chain, prior) in enumerate(zip(bands, chains, feedback), 1):
                seeds = prior.copy()
                for register, value in zip(DEFAULT_MAPPING, opposite):
                    seeds[register] = value
                number = len(programs) + 1
                name = f'program{number:04d}_validates{validates_step:03d}_{direction}_channel{channel}'
                source, expected, count = render(chain, band['ops'], table, seeds, direction)
                source_path = scratch / (name + '.S')
                object_path = scratch / (name + '.o')
                executable_path = scratch / (name + '.elf')
                with source_path.open('x', encoding='utf-8', newline='\n') as handle:
                    handle.write(source)
                built = subprocess.run(['/usr/bin/as', '--64', str(source_path), '-o', str(object_path)], capture_output=True, timeout=60)
                if built.returncode:
                    raise RuntimeError(built.stderr.decode(errors='replace'))
                linked = subprocess.run(['/usr/bin/ld', '--build-id=none', '-o', str(executable_path), str(object_path)], capture_output=True, timeout=60)
                if linked.returncode:
                    raise RuntimeError(linked.stderr.decode(errors='replace'))
                run = subprocess.run([str(executable_path)], capture_output=True, timeout=30)
                if run.returncode != 0 or len(run.stdout) != 64:
                    raise RuntimeError(f'{name}: exit={run.returncode}; output_bytes={len(run.stdout)}')
                native_state = dict(zip(REGS, struct.unpack('<8Q', run.stdout)))
                if native_state != expected:
                    raise AssertionError(f'{name}: native/interpreter mismatch')
                sources.writestr(name + '.S', source)
                executables.write(executable_path, arcname=executable_path.name)
                programs.append({'program': name, 'number': number,
                                 'validates_extension_step': validates_step,
                                 'direction_executed': direction, 'channel': channel,
                                 'chain_values': len(chain), 'chain_sha256': expected_chain_hashes[channel - 1],
                                 'operator_commands': count, 'opposite_raw_vector': opposite,
                                 'retained_registers_before_seed': prior.copy(), 'seed_registers': seeds,
                                 'native_registers': native_state, 'reference_registers': expected,
                                 'assembler_exit': built.returncode, 'linker_exit': linked.returncode,
                                 'native_exit': run.returncode, 'native_matches_reference': True,
                                 'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                                 'executable_sha256': hashlib.sha256(executable_path.read_bytes()).hexdigest()})
                states.append(native_state)
                ids.append(name)
            vector = [state['target'] for state in states]
            if vector == [1, 1, 1, 7]:
                validation_patterns.append({'validates_extension_step': validates_step,
                                            'direction_executed': direction, 'target_vector': vector,
                                            'programs': ids})
            return states, ids

        # Bootstrap executes the unextended original chains. All later values
        # come from a program compiled AFTER the preceding chain extension.
        direction = 'x_to_y'
        pending_states, pending_ids = compile_execute(direction, initial_feedback, 0)
        for step in range(1, 2 * args.passes + 1):
            cycle = (step + 1) // 2
            before_front = [chain[0] for chain in chains]
            before_back = [chain[-1] for chain in chains]
            if direction == 'x_to_y':
                projected = [state['target'] for state in pending_states]
                for channel, value in enumerate(projected, 1):
                    chains[channel - 1].append(value)
                    if value == 0:
                        zeros.append({'step': step, 'cycle': cycle, 'channel': channel, 'position': 'back', 'register': 'target'})
            else:
                projected = [[state['state'], state['relations']] for state in pending_states]
                for channel, pair in enumerate(projected, 1):
                    chains[channel - 1][0:0] = pair
                    for register, value in zip(('state', 'relations'), pair):
                        if value == 0:
                            zeros.append({'step': step, 'cycle': cycle, 'channel': channel,
                                          'position': 'front' if register == 'state' else 'second_front',
                                          'register': register})
            record = {'step': step, 'cycle': cycle, 'extension_direction': direction,
                      'projection_source_programs': pending_ids,
                      'front_before': before_front, 'back_before': before_back,
                      'projected_values': projected, 'other_channel_views': views(projected),
                      'front_after': [chain[0] for chain in chains],
                      'back_after': [chain[-1] for chain in chains],
                      'lengths_after': list(map(len, chains)),
                      'post_extension_chain_hashes': [digest_chain(chain) for chain in chains]}
            history.append(record)
            # Rebuild the just-extended complete chains immediately. Native
            # output validates THIS extension and supplies the NEXT projection.
            next_direction = 'y_to_x' if direction == 'x_to_y' else 'x_to_y'
            new_states, new_ids = compile_execute(next_direction, pending_states, step)
            record.update({'validation_programs': new_ids,
                           'validation_direction': next_direction,
                           'validation_target_vector': [state['target'] for state in new_states],
                           'validation_registers': new_states,
                           'validation_passed': True})
            stage_rows.append({key: record[key] for key in ('step', 'cycle', 'extension_direction', 'projected_values', 'front_after', 'back_after', 'lengths_after', 'validation_direction', 'validation_target_vector', 'validation_passed')})
            # Persist a separate new checkpoint each round, so interruption
            # never requires editing existing output files to recover progress.
            if direction == 'y_to_x':
                save(args.output / f'checkpoint_cycle{cycle:03d}.json',
                     {'cycle': cycle, 'last_step': step, 'front': record['front_after'],
                      'back': record['back_after'], 'validation_target_vector': record['validation_target_vector'],
                      'validation_programs': new_ids, 'native_programs_passed': len(programs)})
                print(json.dumps({'cycle_completed': cycle, 'front': record['front_after'],
                                  'back': record['back_after'], 'validation_previous_step': step,
                                  'validation_target_vector': record['validation_target_vector'],
                                  'native_programs_passed': len(programs)}), flush=True)
            pending_states, pending_ids = new_states, new_ids
            direction = next_direction
    assert len(programs) == 4 + args.passes * 8
    assert len(history) == args.passes * 2
    for original, chain in zip(originals, chains):
        assert chain[args.passes * 2:args.passes * 2 + len(original)] == original
        assert len(chain) == len(original) + args.passes * 3
    save(args.output / 'program_manifest.json', programs)
    save(args.output / 'phase_history.json', history)
    save(args.output / 'final_chains.json', chains)
    with (args.output / 'phase_history.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(stage_rows[0]))
        writer.writeheader()
        writer.writerows({key: json.dumps(value) if isinstance(value, list) else value for key, value in row.items()} for row in stage_rows)
    with (args.output / 'native_execution_summary.csv').open('x', newline='', encoding='utf-8') as handle:
        fields = ['number', 'program', 'validates_extension_step', 'direction_executed', 'channel', 'chain_values', 'operator_commands', 'assembler_exit', 'linker_exit', 'native_exit', 'native_matches_reference']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: row[key] for key in fields} for row in programs)
    report = {'passes_each_direction': args.passes, 'extension_steps': len(history),
              'native_programs_built_and_executed': len(programs), 'native_programs_passed': len(programs),
              'native_compilation_per_extension': 'Four fresh full-chain executables immediately after every extension, plus four bootstrap executables.',
              'native_output_drives_next_pass': True,
              'interpreter_role': 'Cross-check only; projections use registers read from executed native ELF programs.',
              'validation_timing': 'The execution after extension step N validates N and supplies the projection used for extension step N+1.',
              'validation_1117_patterns': validation_patterns,
              'validation_1117_is_eof': False,
              'restart': 'Replayed original recorded chains because earlier endpoint-only/batch-compiled runs cannot seed this changed execution loop.',
              'full_chain_traversal': 'X->Y: complete chain in source order; Y->X: complete chain in reverse value and glyph order.',
              'seed_mapping': DEFAULT_MAPPING, 'retained_register_feedback': True,
              'left_prepend_order': ['state', 'relations'],
              'final_front': [chain[0] for chain in chains], 'final_back': [chain[-1] for chain in chains],
              'final_chain_lengths': list(map(len, chains)), 'literal_zero_observations': zeros,
              'front_zero_channels': sorted({row['channel'] for row in zeros if row['position'] == 'front'}),
              'start_finish_interpretation': 'Record projected zeros and validation patterns separately. No unknown Y EOF code is assigned.',
              'operator_validation_cases': validation_cases,
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
              'native_build_scratch_directory': str(scratch),
              'assembler': subprocess.check_output(['/usr/bin/as', '--version'], text=True).splitlines()[0],
              'linker': subprocess.check_output(['/usr/bin/ld', '--version'], text=True).splitlines()[0]}
    save(args.output / 'native_reassembly_report.json', report)
    print(json.dumps({key: report[key] for key in ('passes_each_direction', 'native_programs_built_and_executed', 'native_programs_passed', 'final_front', 'final_back', 'front_zero_channels')}), flush=True)


if __name__ == '__main__':
    main()
