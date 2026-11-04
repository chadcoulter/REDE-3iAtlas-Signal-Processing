# WOWSignal

Workspace for the requested signal-to-gematria, instruction, and message-reading experiment in the 3I/ATLAS repository.

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
3. Encode the selected measurements as Greek numerals using the existing rounding and decimal-grouping rules.
4. Explicitly map numeral glyph occurrences to REDΣ Book II instructions, retaining measurement and glyph provenance.
5. Execute the instruction sequence and preserve complete register-state traces and feedback settings.
6. Develop the message reading from the resulting transformation trace, recording the interpretation alongside the numerical and instruction evidence.

Follow `../INTEGRATION_GUIDE.md` and the operator authority in `../skills/character-transform-reasoning/references/book-ii-alphabet.txt`. New experiment logic belongs in this folder; retain the existing extractors and operator definitions.

## Files

- `data/`: local recording location and acquisition notes; large recordings are ignored by Git.
- `results/`: generated extraction, instruction, state-trace, and interpretation artifacts.

This branch currently establishes the workspace only. No extraction, operator execution, or message reading has been run.
