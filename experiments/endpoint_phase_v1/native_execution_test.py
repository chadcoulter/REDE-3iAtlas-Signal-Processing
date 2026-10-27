"""Assemble generated phases as actual Linux x86-64 executables and run them.

Uses GNU as + ld through WSL. Native programs contain only the reviewed archived
register operators, a 64-byte result write to stdout, and process exit. No libc.
Only new output files/directories are created; a previous output is refused.
"""
import argparse
import csv
import hashlib
import json
import struct
import subprocess
import zipfile
from pathlib import Path

from endpoint_phase import encode, load_archive, numeral_table
from operator_machine import REGS, execute, validate


def linux_path(path):
    absolute = str(path.resolve()).replace('\\', '/')
    if len(absolute) < 3 or absolute[1:3] != ':/':
        raise ValueError('Expected Windows drive path')
    return '/mnt/' + absolute[0].lower() + absolute[2:]


def native(args, timeout=60):
    result = subprocess.run(['wsl', '-d', 'Ubuntu', '--exec', *args],
                            capture_output=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError(f'{args[0]} exited {result.returncode}: {result.stderr.decode(errors="replace")[:3000]}')
    return result


def build_source(numbers, ops, table, provenance):
    text = ['# ' + provenance, '.section .data', '.balign 8']
    text.extend(f'{reg}: .quad 1' for reg in REGS)
    text.extend(['.section .text', '.globl _start', '.type _start,@function', '_start:'])
    expected = {reg: 1 for reg in REGS}
    opcode_count = 0
    for index, value in enumerate(numbers):
        numerals = encode(value, table)
        text.append(f' # value_index={index} integer={value} numerals={numerals}')
        for glyph in numerals:
            if glyph in ' |0':
                continue
            if glyph not in ops:
                raise ValueError('Missing archived operator: ' + glyph)
            text.append(' # operator=' + glyph)
            text.extend(ops[glyph])
            execute(ops[glyph], expected)
            opcode_count += 1
    # Registers are eight contiguous uint64 words in declared order.
    text.extend([' # write(1, &state, 64)', ' movq $1, %rax', ' movq $1, %rdi',
                 ' leaq state(%rip), %rsi', ' movq $64, %rdx', ' syscall',
                 ' cmpq $64, %rax', ' jne 9f', ' movq $60, %rax', ' xorq %rdi,%rdi',
                 ' syscall', '9:', ' movq $60,%rax', ' movq $1,%rdi', ' syscall',
                 '.section .note.GNU-stack,"",@progbits'])
    return '\n'.join(text) + '\n', expected, opcode_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--phases', type=Path, default=Path(__file__).resolve().parent / 'results_initial/phase_values.csv')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Output must be new: ' + str(args.output))
    repo = Path(__file__).resolve().parents[2]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    validation_cases = sum(validate(b['ops']) for b in bands)
    right, left, first = {}, {}, {}
    with args.phases.open(encoding='utf-8') as handle:
        for record in csv.DictReader(handle):
            channel = int(record['channel'])
            right.setdefault(channel, []).append(int(record['right_target']))
            pair = [int(record['left_state']), int(record['left_relations'])]
            left.setdefault(channel, []).extend(pair)
            if channel not in first:
                first[channel] = (pair, int(record['right_target']))
    args.output.mkdir(parents=True)
    build_dir = args.output / 'build'
    build_dir.mkdir()
    # Added ignore file applies only to freshly generated binaries/loose assembly.
    with (args.output / '.gitignore').open('x', encoding='utf-8') as handle:
        handle.write('build/\n')
    reports = []
    source_archive = args.output / 'assembled_sources.zip'
    with zipfile.ZipFile(source_archive, mode='x', compression=zipfile.ZIP_DEFLATED) as sources:
        for channel, band in enumerate(bands, 1):
            original = [row['rounded'] for row in band['frames']]
            prefix, suffix = first[channel]
            programs = [('right_phase', right[channel]),
                        ('left_phase', left[channel]),
                        ('extended_original', prefix + original + [suffix])]
            for kind, numbers in programs:
                name = f'channel{channel}_{kind}'
                source = build_dir / (name + '.S')
                obj = build_dir / (name + '.o')
                executable = build_dir / (name + '.elf')
                result_path = build_dir / (name + '.registers.bin')
                assembly, expected, op_count = build_source(numbers, band['ops'], table,
                    f'{kind}; channel={channel}; {len(numbers)} integer values; native Linux x86-64')
                with source.open('x', encoding='utf-8', newline='\n') as handle:
                    handle.write(assembly)
                sources.writestr(name + '.S', assembly)
                assembled = native(['/usr/bin/as', '--64', linux_path(source), '-o', linux_path(obj)])
                linked = native(['/usr/bin/ld', '--build-id=none', '-o', linux_path(executable), linux_path(obj)])
                run = native([linux_path(executable)])
                if len(run.stdout) != 64:
                    raise AssertionError(f'{name}: result is not 8 uint64 registers')
                actual = dict(zip(REGS, struct.unpack('<8Q', run.stdout)))
                if actual != expected:
                    raise AssertionError(f'{name}: native/interpreter discrepancy: {actual} vs {expected}')
                with result_path.open('xb') as handle:
                    handle.write(run.stdout)
                item = {'program': name, 'kind': kind, 'channel': channel,
                        'input_values': len(numbers), 'executed_operator_commands': op_count,
                        'assembler_exit': assembled.returncode, 'linker_exit': linked.returncode,
                        'native_exit': run.returncode, 'output_bytes': len(run.stdout),
                        'native_registers': actual, 'interpreter_registers': expected,
                        'native_matches_interpreter': True,
                        'executable_sha256': hashlib.sha256(executable.read_bytes()).hexdigest(),
                        'source_sha256': hashlib.sha256(assembly.encode('utf-8')).hexdigest()}
                reports.append(item)
                print(json.dumps({k: item[k] for k in ('program', 'input_values', 'executed_operator_commands', 'native_exit', 'native_matches_interpreter')}), flush=True)
    report = {'criterion': 'Generated transforms assemble, link, and execute as native x86-64 code with correct operator-state execution.',
              'original_value_recovery_is_a_criterion': False,
              'branch': 'codex/atlas-endpoint-phase-test',
              'assembler': native(['/usr/bin/as', '--version']).stdout.decode().splitlines()[0],
              'linker': native(['/usr/bin/ld', '--version']).stdout.decode().splitlines()[0],
              'machine': native(['/usr/bin/uname', '-m']).stdout.decode().strip(),
              'operator_validation_cases': validation_cases,
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
              'phase_values_sha256': hashlib.sha256(args.phases.read_bytes()).hexdigest(),
              'programs_built_and_run': len(reports), 'programs_passed': sum(r['native_matches_interpreter'] and r['native_exit'] == 0 for r in reports),
              'extension': 'Per channel: first-row left state then left relations prepended to original 1800-value chain; first-row right target appended.',
              'phase_chains': 'Right: all per-row targets in recorded row order. Left: all per-row state,relations pairs in recorded row order.',
              'native_program_behavior': 'Execute archived operators over eight uint64 registers, write 64-byte final state to stdout, exit 0. No libc or external I/O.',
              'programs': reports}
    with (args.output / 'native_execution_report.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
    with (args.output / 'native_execution_summary.csv').open('x', newline='', encoding='utf-8') as handle:
        keys = ['program', 'kind', 'channel', 'input_values', 'executed_operator_commands', 'assembler_exit', 'linker_exit', 'native_exit', 'native_matches_interpreter']
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows({k: row[k] for k in keys} for row in reports)
    print(json.dumps({'programs_built_and_run': len(reports), 'programs_passed': report['programs_passed'], 'output': str(args.output)}))


if __name__ == '__main__':
    main()
