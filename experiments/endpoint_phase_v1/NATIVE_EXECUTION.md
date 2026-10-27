# Native executable criterion

The user specified that the test is whether new transform phases continue to produce machine executable code that works. Recovery of the original numerical values is not a criterion.

`native_execution_test.py` builds and executes three programs for each of four channels:

1. All projected rightward `target` values encoded as archived operator commands.
2. All projected leftward `state`, `relations` values encoded as archived operator commands.
3. The original chain extended with the first endpoint pair's two leftward values at the front and its one rightward value at the back.

The GNU assembler and linker produce actual Linux x86-64 ELF files. Each executable runs the archived operator bodies, emits all eight final registers as 64 binary bytes, and exits. The runner checks assembly, linking, native exit status and agreement of all registers with the portable interpreter. It does not expect output values to equal source amplitudes.

The output directory must be fresh. No existing files are modified. Full generated assembly is preserved in `assembled_sources.zip`; loose source, objects, ELF executables and binary register outputs remain in the ignored `build/` subdirectory. Reports include hashes and exact results for every executable.

Run on this Windows host with WSL Ubuntu:

```powershell
python -B experiments/endpoint_phase_v1/native_execution_test.py C:/Users/ccoulter/Downloads/3I_ATLAS_six_recordings_four_stripes_asm.zip --output experiments/endpoint_phase_v1/native_results_initial
```

Phase generation still uses the explicitly recorded candidate register wiring. This test checks actual native execution of its generated commands; it does not select among competing wiring assignments.
