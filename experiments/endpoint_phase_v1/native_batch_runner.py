"""Run inside WSL to assemble/link/execute an existing extension manifest.

Only newly named native objects/results are created. Reports all checks even
when a program fails. No network, C runtime or external program I/O is needed.
"""
import argparse
import csv
import hashlib
import json
import struct
import subprocess
import zipfile
from pathlib import Path

REGS = ['state', 'relations', 'constraints', 'observations', 'unresolved', 'context', 'target', 'events']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    root = args.output
    manifest = json.loads((root / 'native_manifest.json').read_text())
    build = root / 'build'
    report_path = root / 'native_batch_report.json'
    summary_path = root / 'native_batch_summary.csv'
    archive_path = root / 'assembled_sources.zip'
    if any(path.exists() for path in (report_path, summary_path, archive_path)):
        raise FileExistsError('Native batch results already exist')
    results = []
    with zipfile.ZipFile(archive_path, mode='x', compression=zipfile.ZIP_DEFLATED) as archive:
        for index, item in enumerate(manifest, 1):
            source = build / item['source']
            obj = build / (item['program'] + '.o')
            executable = build / (item['program'] + '.elf')
            binary_output = build / (item['program'] + '.registers.bin')
            if any(p.exists() for p in (obj, executable, binary_output)):
                raise FileExistsError('Refusing to overwrite a native build')
            archive.write(source, arcname=source.name)
            row = {k: item[k] for k in ('program', 'cycle', 'direction', 'channel', 'input_values', 'operator_commands')}
            row.update({'assembler_exit': None, 'linker_exit': None, 'native_exit': None,
                        'native_matches_interpreter': False, 'error': ''})
            try:
                assembled = subprocess.run(['/usr/bin/as', '--64', str(source), '-o', str(obj)], capture_output=True, timeout=60)
                row['assembler_exit'] = assembled.returncode
                if assembled.returncode:
                    raise RuntimeError(assembled.stderr.decode(errors='replace'))
                linked = subprocess.run(['/usr/bin/ld', '--build-id=none', '-o', str(executable), str(obj)], capture_output=True, timeout=60)
                row['linker_exit'] = linked.returncode
                if linked.returncode:
                    raise RuntimeError(linked.stderr.decode(errors='replace'))
                run = subprocess.run([str(executable)], capture_output=True, timeout=30)
                row['native_exit'] = run.returncode
                with binary_output.open('xb') as handle:
                    handle.write(run.stdout)
                if len(run.stdout) != 64:
                    raise RuntimeError(f'Expected 64 output bytes; got {len(run.stdout)}')
                native_state = dict(zip(REGS, struct.unpack('<8Q', run.stdout)))
                row['native_registers'] = native_state
                row['native_matches_interpreter'] = native_state == item['expected_registers']
                row['executable_sha256'] = hashlib.sha256(executable.read_bytes()).hexdigest()
                if run.returncode or not row['native_matches_interpreter']:
                    raise RuntimeError('Native run failed or differs from interpreter')
            except (RuntimeError, subprocess.TimeoutExpired) as error:
                row['error'] = str(error)[:3000]
            results.append(row)
            if index % 8 == 0:
                print(json.dumps({'cycle_completed': item['cycle'], 'programs_completed': index,
                                  'passed_so_far': sum(not r['error'] for r in results)}), flush=True)
    report = {'programs_built_and_run': len(results),
              'programs_passed': sum(not r['error'] for r in results),
              'assembler': subprocess.check_output(['/usr/bin/as', '--version'], text=True).splitlines()[0],
              'linker': subprocess.check_output(['/usr/bin/ld', '--version'], text=True).splitlines()[0],
              'criterion': 'Assemble, link, execute with exit 0; all eight native registers match interpreter.',
              'programs': results}
    with report_path.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2)
    keys = ['program', 'cycle', 'direction', 'channel', 'input_values', 'operator_commands',
            'assembler_exit', 'linker_exit', 'native_exit', 'native_matches_interpreter', 'error']
    with summary_path.open('x', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows({k: row[k] for k in keys} for row in results)
    print(json.dumps({'programs': len(results), 'passed': report['programs_passed']}), flush=True)
    if report['programs_passed'] != len(results):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
