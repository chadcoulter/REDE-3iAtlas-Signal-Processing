# WOWSignal

Workspace for the requested signal-to-gematria, instruction, and message-reading experiment in the 3I/ATLAS repository.

## Current input

The recording being downloaded is a **3I/ATLAS observation**, retained here under the user-requested folder name `WOWSignal`.

- File: `guppi_60887_52472_6690873992_3IATLAS_R_0001.0000.fil`
- Observatory/session: Parkes (Murriyang), July 31, 2025.
- Source: https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc00/guppi_60887_52472_6690873992_3IATLAS_R_0001.0000.fil
- Archive: https://bldata.berkeley.edu/ATLAS/PKS_Jul_31_2025/blc00/
- Existing extraction metadata: `../data/metadata(2).json`.
- Acquisition status: user downloading; local file and checksum not yet verified.

## Planned sequence

1. Register the completed download: absolute path, byte count, SHA-256, and parsed SIGPROC header.
2. Extract numerical measurements using the existing bounded-memory extractor. Preserve frame, time, frequency, amplitude, and extraction settings.
3. Encode the selected measurements as Greek numerals using the existing rounding and decimal-grouping rules.
4. Explicitly map numeral glyph occurrences to REDΣ Book II instructions, retaining measurement and glyph provenance.
5. Execute the instruction sequence and preserve complete register-state traces and feedback settings.
6. Develop the message reading from the resulting transformation trace, recording the interpretation alongside the numerical and instruction evidence.

Follow `../INTEGRATION_GUIDE.md` and the operator authority in `../skills/character-transform-reasoning/references/book-ii-alphabet.txt`. New experiment logic belongs in this folder; retain the existing extractors and operator definitions.

## Files

- `data/`: local recording location and acquisition notes; large recordings are ignored by Git.
- `results/`: generated extraction, instruction, state-trace, and interpretation artifacts.

This branch currently establishes the workspace only. No extraction, operator execution, or message reading has been run.
