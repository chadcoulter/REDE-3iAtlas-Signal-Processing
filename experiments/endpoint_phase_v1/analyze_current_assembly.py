"""Analyze final pass-100 assembly; native seed and repetition sensitivity.

Run in WSL. Original assembly/ELF files are read only. New native variants
change one compiled seed bit or collapse one repeated region for comparison.
"""
import argparse
import collections
import csv
import hashlib
import json
import re
import struct
import subprocess
import tempfile
import zipfile
from pathlib import Path

from endpoint_phase import encode, load_archive, numeral_table
from operator_machine import REGS, execute

EFFECTS = {
    'Α': 'state = 1', 'Β': 'context += 1', 'Γ': 'constraints = state & 255',
    'Δ': 'state += 1', 'Ε': 'observations += (constraints == 0)',
    'Ζ': 'relations ^= state', 'Η': 'target = state', 'Θ': 'constraints += 1',
    'Ι': 'events += 1', 'Κ': 'context += 1', 'Λ': 'state ^= relations',
    'Μ': 'observations += state', 'Ν': 'target = state + 1',
    'Ξ': 'unresolved += state XOR target', 'Ο': 'observations += state XOR relations',
    'Π': 'target = state + context', 'Ρ': 'relations ^= target',
    'Σ': 'state += relations + 1', 'Τ': 'target = state + relations + constraints',
    'Υ': 'if constraints & 1: context += 1; else: relations += 1',
    'Φ': 'target = state XOR context', 'Χ': 'swap(state, target)',
    'Ψ': 'context = observations XOR relations', 'Ω': 'state = target',
    'Ϛ': 'unresolved += 1', 'Ϟ': 'relations ^= events', 'Ϡ': 'context += 1',
}
TARGET_WRITERS = set('ΗΝΠΤΦΧ')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Output must be new')
    root = Path(__file__).resolve().parent
    repo = root.parents[1]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    latest = root / 'latest_assembled_transforms_pass100'
    known = json.loads((latest / 'manifest.json').read_text())['programs']
    args.output.mkdir(parents=True)
    scratch = Path(tempfile.mkdtemp(prefix='atlas-assembly-analysis-'))
    analyses, tests, frames = [], [], []
    semantics = [{'glyph': glyph, 'effect': effect} for glyph, effect in EFFECTS.items()]
    with (args.output / 'operator_semantics.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=['glyph', 'effect'])
        writer.writeheader()
        writer.writerows(semantics)
    with zipfile.ZipFile(args.output / 'native_analysis_sources.zip', mode='x', compression=zipfile.ZIP_DEFLATED) as source_zip:

        def run_source(name, source):
            source_path = scratch / (name + '.S')
            obj = scratch / (name + '.o')
            executable = scratch / (name + '.elf')
            with source_path.open('x', encoding='utf-8', newline='\n') as handle:
                handle.write(source)
            for command in (['/usr/bin/as', '--64', str(source_path), '-o', str(obj)], ['/usr/bin/ld', '--build-id=none', '-o', str(executable), str(obj)]):
                result = subprocess.run(command, capture_output=True, timeout=60)
                if result.returncode:
                    raise RuntimeError(result.stderr.decode(errors='replace'))
            result = subprocess.run([str(executable)], capture_output=True, timeout=30)
            if result.returncode or len(result.stdout) != 64:
                raise RuntimeError(f'{name}: exit={result.returncode}; bytes={len(result.stdout)}')
            source_zip.writestr(name + '.S', source)
            return dict(zip(REGS, struct.unpack('<8Q', result.stdout)))

        for channel, (band, manifest) in enumerate(zip(bands, known), 1):
            source_path = latest / f'channel{channel}_pass100.S'
            source = source_path.read_text(encoding='utf-8')
            assert hashlib.sha256(source.encode()).hexdigest() == manifest['files']['.S']['sha256']
            seeds = {name: int(value) for name, value in re.findall(r'(?m)^(\w+): \.quad (\d+)$', source)}
            assert set(seeds) == set(REGS)
            markers = list(re.finditer(r'(?m)^ # traversal_index=(\d+) raw_integer=(\d+) numerals=([^\n]*)$', source))
            wrapper = re.search(r'(?m)^ movq \$1,%rax$', source)
            assert wrapper and len(markers) == 2100
            chunks = []
            values = []
            counts = collections.Counter()
            state = seeds.copy()
            last_target_write = None
            last_target_change = None
            for index, marker in enumerate(markers):
                end = markers[index + 1].start() if index + 1 < len(markers) else wrapper.start()
                chunk = source[marker.start():end]
                glyphs = re.findall(r'(?m)^ # operator=(.)$', chunk)
                raw = int(marker[2])
                assert ''.join(glyphs) == ''.join(g for g in encode(raw, table) if g not in ' |0')
                region = 'front_extension' if index < 200 else ('original_recording' if index < 2000 else 'back_extension')
                for ordinal, glyph in enumerate(glyphs, 1):
                    before = state.copy()
                    execute(band['ops'][glyph], state)
                    counts[glyph] += 1
                    if glyph in TARGET_WRITERS:
                        location = {'value_index': index, 'raw_integer': raw, 'region': region,
                                    'glyph': glyph, 'operator_effect': EFFECTS[glyph],
                                    'operator_in_value': ordinal,
                                    'source_line': source.count('\n', 0, marker.start()) + 1,
                                    'before': before, 'after': state.copy()}
                        last_target_write = location
                        if before['target'] != state['target']:
                            last_target_change = location
                frames.append({'channel': channel, 'value_index': index, 'region': region,
                               'raw_integer': raw, 'operators': ''.join(glyphs), **state})
                values.append(raw)
                chunks.append(chunk)
            assert state == manifest['native_registers']
            # Find repeated full left pairs, not just their first member.
            pair = values[:2]
            prefix_pairs = 0
            while prefix_pairs * 2 + 2 <= 200 and values[prefix_pairs * 2:prefix_pairs * 2 + 2] == pair:
                prefix_pairs += 1
            tail_value = values[-1]
            suffix_values = 0
            while suffix_values < 100 and values[-1 - suffix_values] == tail_value:
                suffix_values += 1
            baseline = run_source(f'channel{channel}_baseline', source)
            assert baseline == manifest['native_registers']
            seed_tests = []
            for register in REGS:
                new_value = seeds[register] ^ 1
                modified, count = re.subn(rf'(?m)^{register}: \.quad \d+$', f'{register}: .quad {new_value}', source)
                assert count == 1
                result = run_source(f'channel{channel}_seed_{register}_flipbit0', modified)
                changed = [key for key in REGS if result[key] != baseline[key]]
                test = {'channel': channel, 'test': 'seed_bit0_flip', 'seed_register': register,
                        'old_seed': seeds[register], 'new_seed': new_value,
                        'changed_outputs': changed, 'target_changed': 'target' in changed,
                        'native_output': result, 'native_exit': 0}
                tests.append(test)
                seed_tests.append(test)
            head, footer = source[:markers[0].start()], source[wrapper.start():]
            # Collapse each repeated boundary to one occurrence; compare actual
            # native behavior while preserving all original source files.
            collapsed_prefix = head + ''.join(chunks[:2] + chunks[prefix_pairs * 2:]) + footer
            collapsed_suffix = head + ''.join(chunks[:len(chunks) - suffix_values + 1]) + footer
            boundary_tests = []
            for label, modified in [('collapse_front_pair_run_to_one_pair', collapsed_prefix), ('collapse_back_run_to_one_value', collapsed_suffix)]:
                result = run_source(f'channel{channel}_{label}', modified)
                changed = [key for key in REGS if result[key] != baseline[key]]
                test = {'channel': channel, 'test': label, 'changed_outputs': changed,
                        'target_changed': 'target' in changed, 'native_output': result, 'native_exit': 0}
                tests.append(test)
                boundary_tests.append(test)
            instructions = collections.Counter()
            for line in source.splitlines():
                line = line.strip()
                if line and not line.startswith(('#', '.')) and not line.endswith(':') and ': .quad' not in line:
                    instructions[line.split()[0]] += 1
            analyses.append({'channel': channel, 'initial_registers': seeds,
                             'final_registers': baseline, 'raw_values': len(values),
                             'operator_count': sum(counts.values()), 'operator_counts': dict(counts),
                             'static_instruction_counts': dict(instructions),
                             'prefix_pair': pair, 'prefix_pair_repetitions': prefix_pairs,
                             'suffix_value': tail_value, 'suffix_repetitions': suffix_values,
                             'last_target_write': last_target_write, 'last_target_change': last_target_change,
                             'seed_bit0_tests_changing_target': [t['seed_register'] for t in seed_tests if t['target_changed']],
                             'boundary_collapse_tests': boundary_tests,
                             'source_sha256': manifest['files']['.S']['sha256']})
            print(json.dumps({'channel_completed': channel, 'operators': sum(counts.values()),
                              'target': baseline['target'], 'last_target_operator': last_target_write['glyph'],
                              'seed_tests_changing_target': analyses[-1]['seed_bit0_tests_changing_target']}), flush=True)
    with (args.output / 'integer_state_trace.csv').open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(frames[0]))
        writer.writeheader()
        writer.writerows(frames)
    result = {'program_type': 'Fixed unrolled eight-cell uint64 arithmetic/XOR state machine.',
              'logical_registers_are': 'Eight .data memory cells; native RAX/flags perform the arithmetic.',
              'runtime_inputs': 'None read from stdin, files, network, arguments, clock or random source. Initial values and operator sequence are compiled into the ELF.',
              'runtime_output': 'One write(1, address_of_state, 64), then exit(0) if exactly 64 bytes were written; otherwise exit(1).',
              'output_layout': 'Eight little-endian unsigned 64-bit words in REGS order.', 'register_order': REGS,
              'arithmetic': 'Unsigned 64-bit wraparound for additions/increments; XOR, swaps, assignments, low-byte mask and parity/zero tests.',
              'internal_control_flow': 'Forward-only local conditionals for Upsilon plus the output-write failure branch. No backward branches, loops, function calls or recursion.',
              'numeric_grouping': 'Numeral separators and zero groups produce no instructions. 1, 1000 and 1000000 each dispatch the same Alpha reset when their group metadata is removed.',
              'termination': 'Explicit Linux exit syscall in generated wrapper after the unrolled body. Numeric zero has no halt instruction; the repeated numeric boundary vectors are executable data-to-operator patterns.',
              'reversibility': 'Assignments/reset and low-byte masking lose information; reverse traversal is not an algebraic inverse of these operators.',
              'native_tests': {'baselines': 4, 'single_seed_bit_flips': 32, 'boundary_collapses': 8, 'total': 44, 'all_exited_zero': True},
              'sensitivity_scope': 'Only the observed one-bit changes and boundary collapses are tested; unchanged outputs are not proof of independence for arbitrary seeds.',
              'channels': analyses, 'native_tests_detailed': tests}
    with (args.output / 'assembly_analysis.json').open('x', encoding='utf-8') as handle:
        json.dump(result, handle, indent=2, ensure_ascii=False)
    with (args.output / 'native_sensitivity.csv').open('x', newline='', encoding='utf-8') as handle:
        fields = ['channel', 'test', 'seed_register', 'changed_outputs', 'target_changed', 'native_exit']
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows({key: json.dumps(test.get(key, '')) if isinstance(test.get(key), list) else test.get(key, '') for key in fields} for test in tests)
    print(json.dumps({'channels': 4, 'native_tests': 44, 'output': str(args.output)}), flush=True)


if __name__ == '__main__':
    main()
