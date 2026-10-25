# Signal extraction and character transformation

## Source files

- `scripts/redsigma_band_extract.py`: original SIGPROC filterbank spectral-band extractor.
- `scripts/redsigma_band_extract_chunked.py`: original channel-chunked extractor for bounded-memory processing.
- `scripts/validate_resolution.py`: validates structural invariants of a saved character-transform resolution trace.
- `references/book-ii-alphabet.txt`: authoritative REDΣ Book II operator definitions.

The two extraction scripts produce `bands.csv`, `streams.csv`, and `metadata.json`. They encode measurements as Greek numerals; they do **not** execute Book II character-transform reasoning.

## Processing sequence

1. Read a SIGPROC `.fil` recording using the original extraction script. Use the chunked version for large inputs.
2. Preserve `bands.csv`, `streams.csv`, and `metadata.json` together with the recording identifier and extraction parameters.
3. Treat Greek numeral output as a **typed numerical representation** of extracted measurements, not as a Book II operator sequence by default.
4. If character-transform analysis is requested, explicitly select and document the conversion from the extracted representation to a sequence of Book II operators. Retain the source values, mapping choices, alternatives, and provenance.
5. Execute the character transformation following `SKILL.md`, `references/book-ii-alphabet.txt`, and `references/resolution-contract.md`.
6. Save the resolution trace as JSON and validate its structural consistency with `scripts/validate_resolution.py`.

## Dependencies

Install the extractor dependencies from `requirements.txt` (NumPy and SciPy). Check each extractor's command-line help and options in its source before running it.

## Boundaries and reproducibility

Keep extraction, numerical encoding, character mapping, operator execution, and governance evaluation as separate stages. Record which stage produced each artifact. Preserve the original extraction scripts and Book II definitions unchanged; place new integration logic in separately named files.

The governance reference `references/governance-v0.4.md` is an adaptation. Its original source is retained in `references/governance-v0.4-source.docx`.
