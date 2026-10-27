"""Check that every extension was rebuilt and native output drove the next one."""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from endpoint_phase import load_archive, numeral_table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--archive', type=Path, required=True)
    args = parser.parse_args()
    root = args.output
    programs = json.loads((root / 'program_manifest.json').read_text())
    history = json.loads((root / 'phase_history.json').read_text())
    report = json.loads((root / 'native_reassembly_report.json').read_text())
    by_name = {program['program']: program for program in programs}
    assert len(by_name) == len(programs) == 4 + 4 * len(history)
    assert len(history) == report['passes_each_direction'] * 2
    previous_validation = None
    for row in history:
        step = row['step']
        if previous_validation:
            assert row['projection_source_programs'] == previous_validation
        source_states = [by_name[name]['native_registers'] for name in row['projection_source_programs']]
        expected_projection = [state['target'] for state in source_states] if row['extension_direction'] == 'x_to_y' else [[state['state'], state['relations']] for state in source_states]
        assert row['projected_values'] == expected_projection
        validation = [by_name[name] for name in row['validation_programs']]
        assert len(validation) == 4
        assert all(program['validates_extension_step'] == step for program in validation)
        assert [program['chain_sha256'] for program in validation] == row['post_extension_chain_hashes']
        assert [program['chain_values'] for program in validation] == row['lengths_after']
        assert [program['native_registers'] for program in validation] == row['validation_registers']
        assert [program['native_registers']['target'] for program in validation] == row['validation_target_vector']
        assert row['validation_passed']
        previous_validation = row['validation_programs']
    for program in programs:
        assert program['assembler_exit'] == program['linker_exit'] == program['native_exit'] == 0
        assert program['native_matches_reference']
        assert program['native_registers'] == program['reference_registers']
    # Independently verify the archived sources and executable identity/machine.
    with zipfile.ZipFile(root / 'assembled_sources.zip') as sources, zipfile.ZipFile(root / 'native_executables.zip') as binaries:
        assert len(sources.namelist()) == len(binaries.namelist()) == len(programs)
        for program in programs:
            source = sources.read(program['program'] + '.S')
            binary = binaries.read(program['program'] + '.elf')
            assert hashlib.sha256(source).hexdigest() == program['source_sha256']
            assert hashlib.sha256(binary).hexdigest() == program['executable_sha256']
            assert binary[:5] == b'\x7fELF\x02' and binary[18:20] == b'\x3e\x00'
    repo = Path(__file__).resolve().parents[2]
    table = numeral_table(repo / 'skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
    bands = load_archive(args.archive, table)
    chains = json.loads((root / 'final_chains.json').read_text())
    passes = report['passes_each_direction']
    for chain, band in zip(chains, bands):
        original = [frame['rounded'] for frame in band['frames']]
        assert chain[passes * 2:passes * 2 + len(original)] == original
        assert len(chain) == len(original) + passes * 3
    audit = {'result': 'passed', 'extension_steps_audited': len(history),
             'native_executables_audited': len(programs),
             'every_extension_reassembled_and_executed': True,
             'every_next_projection_from_preceding_native_validation': True,
             'all_chain_hashes_and_lengths_linked': True,
             'all_archived_sources_and_elf_hashes_verified': True,
             'original_chain_values_preserved': True,
             'validation_associated_with_preceding_extension': True}
    with (root / 'loop_integrity_audit.json').open('x', encoding='utf-8') as handle:
        json.dump(audit, handle, indent=2)
    print(json.dumps(audit))


if __name__ == '__main__':
    main()
