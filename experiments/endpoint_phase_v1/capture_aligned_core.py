"""Capture aligned code between shared repeating boundaries; new files only.

Run in WSL. Preserve the exact retained assembly body, capture its entry state,
assemble native code, and verify core output plus removed suffix equals the
original full-program output. Raw machine bodies exclude the output wrapper.
"""
import argparse
import hashlib
import json
import re
import struct
import subprocess
import tempfile
from pathlib import Path

from endpoint_phase import load_archive, numeral_table
from operator_machine import REGS, execute


def run(command):
    result = subprocess.run(command, capture_output=True, timeout=60)
    if result.returncode:
        raise RuntimeError(result.stderr.decode(errors='replace'))
    return result.stdout


def save(path, value):
    with path.open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError('Choose a new output directory')
    root = Path(__file__).resolve().parent
    repo = root.parents[1]
    latest = root / 'latest_assembled_transforms_pass100'
    originals = json.loads((latest / 'manifest.json').read_text())['programs']
    analysis = json.loads((root / 'assembly_analysis_pass100/assembly_analysis.json').read_text())['channels']
    prefix_pairs = min(channel['prefix_pair_repetitions'] for channel in analysis)
    suffix_values = min(channel['suffix_repetitions'] for channel in analysis)
    start = prefix_pairs * 2
    stop = 2100 - suffix_values
    assert (start, stop) == (74, 2008)
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    args.output.mkdir(parents=True)
    scratch = Path(tempfile.mkdtemp(prefix='atlas-core-capture-'))
    captures = []
    for channel, (band, original) in enumerate(zip(bands, originals), 1):
        source_path = latest / f'channel{channel}_pass100.S'
        source = source_path.read_text(encoding='utf-8')
        assert hashlib.sha256(source.encode()).hexdigest() == original['files']['.S']['sha256']
        markers = list(re.finditer(r'(?m)^ # traversal_index=(\d+) raw_integer=(\d+) numerals=([^\n]*)$', source))
        wrapper = re.search(r'(?m)^ movq \$1,%rax$', source)
        assert wrapper and len(markers) == 2100
        seeds = {register: int(value) for register, value in re.findall(r'(?m)^(\w+): \.quad (\d+)$', source)}
        state = seeds.copy()
        values, glyph_groups = [], []
        entry, expected_exit = None, None
        for index, marker in enumerate(markers):
            end = markers[index + 1].start() if index + 1 < len(markers) else wrapper.start()
            glyphs = re.findall(r'(?m)^ # operator=(.)$', source[marker.start():end])
            if index == start:
                entry = state.copy()
            for glyph in glyphs:
                execute(band['ops'][glyph], state)
            if index == stop - 1:
                expected_exit = state.copy()
            values.append(int(marker[2]))
            glyph_groups.append(glyphs)
        assert state == original['native_registers'] and entry is not None and expected_exit is not None
        body = source[markers[start].start():markers[stop].start()]
        header = ['# Aligned retained core. Exact retained body; captured entry state.',
                  '.section .data', '.balign 8']
        header += [f'{register}: .quad {entry[register]}' for register in REGS]
        header += ['.section .text', '.globl _start', '.globl transform_core_begin',
                   '.globl transform_core_end', '_start:', 'transform_core_begin:']
        captured_source = '\n'.join(header) + '\n' + body + 'transform_core_end:\n' + source[wrapper.start():]
        name = f'channel{channel}_core'
        assembly_path = args.output / (name + '.S')
        object_path = args.output / (name + '.o')
        executable_path = args.output / (name + '.elf')
        code_path = args.output / (name + '.code.bin')
        data_path = args.output / (name + '.data.bin')
        with assembly_path.open('x', encoding='utf-8', newline='\n') as handle:
            handle.write(captured_source)
        run(['/usr/bin/as', '--64', str(assembly_path), '-o', str(object_path)])
        run(['/usr/bin/ld', '--build-id=none', '-o', str(executable_path), str(object_path)])
        output = run([str(executable_path)])
        assert len(output) == 64
        actual_exit = dict(zip(REGS, struct.unpack('<8Q', output)))
        assert actual_exit == expected_exit
        # Account explicitly for the removed suffix to recover the exact full
        # eight-cell result, not only the selected target.
        restored = actual_exit.copy()
        for glyphs in glyph_groups[stop:]:
            for glyph in glyphs:
                execute(band['ops'][glyph], restored)
        assert restored == original['native_registers']
        symbols = {}
        for line in run(['/usr/bin/nm', '-n', '--defined-only', str(executable_path)]).decode().splitlines():
            parts = line.split()
            if len(parts) == 3:
                symbols[parts[2]] = int(parts[0], 16)
        begin = symbols['transform_core_begin']
        end = symbols['transform_core_end']
        assert symbols['_start'] == begin
        text_path = scratch / (name + '.text.bin')
        run(['/usr/bin/objcopy', '-O', 'binary', '--only-section=.text', str(executable_path), str(text_path)])
        run(['/usr/bin/objcopy', '-O', 'binary', '--only-section=.data', str(executable_path), str(data_path)])
        text = text_path.read_bytes()
        code = text[:end - begin]
        assert len(code) == end - begin
        with code_path.open('xb') as handle:
            handle.write(code)
        assert data_path.read_bytes() == struct.pack('<8Q', *(entry[register] for register in REGS))
        for offset, register in enumerate(REGS):
            assert symbols[register] == symbols['state'] + offset * 8
        files = {}
        for path in (assembly_path, object_path, executable_path, code_path, data_path):
            files[path.suffix if path.suffix not in ('.bin',) else ('.code.bin' if path == code_path else '.data.bin')] = {
                'name': path.name, 'bytes': path.stat().st_size,
                'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
        context = {'channel': channel, 'original_source': str(source_path),
                   'original_source_sha256': original['files']['.S']['sha256'],
                   'removed_prefix_values': start, 'removed_suffix_values': 2100 - stop,
                   'retained_original_value_indices': {'first': start, 'last_inclusive': stop - 1},
                   'retained_values': stop - start,
                   'retained_operator_invocations': sum(map(len, glyph_groups[start:stop])),
                   'full_initial_state': seeds, 'captured_core_entry_state': entry,
                   'native_core_exit_state': actual_exit,
                   'suffix_restored_full_exit_state': restored,
                   'matches_original_after_suffix_accounting': True,
                   'native_core_target': actual_exit['target'],
                   'original_full_target': original['native_registers']['target'],
                   'elf_code_address': begin, 'elf_core_end_address': end,
                   'elf_data_address': symbols['state'],
                   'raw_code_load_contract': 'RIP-relative body. Preserve code/data relative placement recorded here. Body falls through at core_end; it has no standalone exit/return. ELF includes the output/exit wrapper.',
                   'files': files}
        save(args.output / (name + '.context.json'), context)
        captures.append(context)
        print(json.dumps({'channel': channel, 'retained_values': stop - start,
                          'raw_machine_code_bytes': len(code), 'target': actual_exit['target'],
                          'native_core_passed': True, 'full_state_restored_after_suffix': True}), flush=True)
    save(args.output / 'core_manifest.json', {
        'selection': 'Aligned interior between the shared repeated full left pairs and right values.',
        'shared_front_pair_repetitions_removed': prefix_pairs,
        'shared_back_values_removed': suffix_values,
        'raw_values_per_channel': stop - start,
        'original_recording_values_per_channel_preserved': 1800,
        'generated_transient_or_alignment_values_retained_per_channel': stop - start - 1800,
        'native_core_programs_tested': 4, 'native_core_programs_passed': 4,
        'all_four_targets': [capture['native_core_target'] for capture in captures],
        'raw_bin_is_standalone_executable': False,
        'sources_unchanged': True, 'channels': captures})


if __name__ == '__main__':
    main()
