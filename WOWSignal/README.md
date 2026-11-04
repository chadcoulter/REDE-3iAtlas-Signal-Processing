# WOWSignal

Workspace for reconstructing the original Wow! signal investigation using V8 TAO in the 3I/ATLAS repository. The [original process](ORIGINAL_PROCESS.md) is preserved verbatim. Follow the [step-by-step investigation record](steps/README.md) for methods, inputs, attempts, and results.

## Current input

The intended input is the **Wow! signal observation from Big Ear on August 15, 1977**. The earlier Parkes 3I/ATLAS download link was supplied in error and is not the input to this experiment.

- Source archive: https://github.com/planetaryhablab/Ohio-SETI
- CSV transcription: `oseti_19770815_220410.csv`.
- TXT transcription: `oseti_19770815_220410.txt`.
- Printout scan: `oseti_19770815_220410.jpg`.
- Reanalysis data: `oseti_19770815_220410.sav` (IDL Save format).
- Available printout measurements: 50 frequency channels by 82 rows.
- Provenance: Arecibo Wow! project, Planetary Habitability Laboratory, University of Puerto Rico at Arecibo; original transcription credited to MichaelHotaling.
- Archive license: Creative Commons Attribution 4.0 International.
- Acquisition status: source located; local download and checksum not yet verified.

The CSV/TXT files transcribe the historical computer printout. They are not waveform or raw-voltage recordings. Keep those transcribed values distinct from the calibrated quantities in the reanalysis file.

## Planned sequence

1. Register the downloaded scan and transcription: source revision, absolute path, byte count, and SHA-256.
2. Parse and verify the transcription against the scan. Preserve spaces, channel positions, row ordering, time fields, and original intensity characters. Convert intensity codes to their recorded numeric bins, retaining the originals. The existing SIGPROC extractor is not applicable to this printout dataset.
3. Recover the historical grid traversals and V8 TAO definitions, including any numerical/gematria mapping. Record the original rules before applying them.
4. Apply documented V8 TAO transformations and nested/reflected traversals, preserving every intermediate state and coordinate.
5. Reconstruct the message reading and directional calculations with links to the measurement and operation evidence.
6. Compare with the original investigation and record reproduced results, recovered operations, and unresolved definitions at each step.

Use the original V8 TAO source as the method authority once recovered. The repository's newer REDΣ integration is available as context, but has not been established as equivalent to the historical Wow! method. New experiment logic belongs in this folder; retain the existing extractors and operator definitions.

## Files

- `data/`: local recording location and acquisition notes; large recordings are ignored by Git.
- `results/`: generated extraction, instruction, state-trace, and interpretation artifacts.
- `steps/`: numbered step folders, current findings, dependencies, and a template for recording each attempt.

This branch currently establishes the workspace only. No extraction, operator execution, or message reading has been run.
