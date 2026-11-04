# WOWSignal

## Project purpose

Workspace for reconstructing the original Wow! signal investigation using V8 TAO in the 3I/ATLAS repository. The [original process](ORIGINAL_PROCESS.md) is preserved verbatim. Follow the [step-by-step investigation record](steps/README.md) for methods, inputs, attempts, and results.

The project proceeds one step at a time: recover the surviving signal measurements, examine their two-dimensional structure, recover and apply the original transformation definitions, and trace any resulting interpretation back to its source data. Each step preserves its inputs, operations, intermediate states, results, and unresolved questions. Historical readings such as `ASTRA` and “Look there” are comparison targets to reconstruct through documented operations.

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
- Acquisition status: source acquired and hashed at pinned revision; see [Step 1, run 001](steps/01-source-data/run-001.md).

The CSV/TXT files transcribe the historical computer printout. They are not waveform or raw-voltage recordings. Keep those transcribed values distinct from the calibrated quantities in the reanalysis file.

## Step 1 narrative — data acquisition and reconstruction

I began by fixing the source to a specific version of the Ohio SETI archive so we could repeat the data pass later against exactly the same files. I saved the CSV transcription, fixed-width TXT transcription, original printout scan, and the archive's README. I recorded their source links, file sizes, and hashes.

Next, I established the grid's orientation. The files contain **82 time rows and 50 channel columns**, giving us **4,100 intensity cells**. I retained the original ordering, including spaces. Each cell now has a record connecting its original character and numeric intensity bin to its row, channel, source-file position, and printed metadata.

I compared every intensity cell between the CSV and TXT. **All 4,100 matched.** The metadata also matched across all 82 rows after accounting for formatting spaces. I then checked that converting each character to its numeric bin and back reproduced the original character. All cells passed, including the **2,988 blanks**.

As a recognizable spot-check, I located `6EQUJ5` in channel 2, at data rows 58–63. Its numeric bins are `6, 14, 26, 30, 19, 5`. I also visually inspected the scan to check the layout and visible sequence. The complete grid remains our input; those six samples are only a check within it.

Finally, I saved the structured data and validation results, repeated the process independently, and confirmed that it produced identical data files. Everything is recorded in the [Step 1 report](steps/01-source-data/run-001.md).

### Issues and limits

- **Timing:** the first two printed timestamps are 15 seconds apart. Most later intervals are 12 seconds, with four at 11 seconds. I preserved them without correction or resampling.
- **Transcription confidence:** CSV and TXT agree, but they come from the same published transcription. I have not checked every cell individually against the scan.
- **Historical identity:** this archive matches the dimensions and sequence described in the original process, but we have not confirmed it is the exact file used in that earlier investigation.
- **Measurement precision:** the numbers are intensity-bin labels. They preserve the information in the printout; they do not recover finer measurements or a raw waveform.

Step 1 gives us a reproducible, traceable data foundation. I stopped before traversals, gematria, or interpretation.

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
- `sources/`: preserved V8 TAO resolver note and Python package with original source URLs and content identifiers.

Step 1 has reconstructed and checked the archived printout data. The [data-pass record](steps/01-source-data/run-001.md) includes results and retained source flags. No later traversal analysis, gematria conversion, operator execution, or message reading has been run as part of this recorded workflow.
