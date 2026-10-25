# REDSigma Signal Extraction Integration

This package preserves the installed Character Transform Reasoning skill, including its original `SKILL.md`, reference texts, governance source DOCX, validation script, and icon. The two signal extraction scripts are copied from the user's Library without modifying their source.

## Inputs and outputs

Run either `scripts/redsigma_band_extract.py` or `scripts/redsigma_band_extract_chunked.py` against a SIGPROC `.fil` file. Each writes `bands.csv`, `streams.csv`, and `metadata.json` in an output directory. Use `--help` for supported options. Install the dependencies in `requirements.txt` first.

The scripts detect spectral bands, extract numerical measurements and encode rounded integers into Greek numeral sequences. They do not execute Book II operator transformations. Treat numerical measurements and Book II operators as separate typed stages. Use `references/book-ii-alphabet.txt` for authoritative operator meanings and `scripts/validate_resolution.py` for checking saved resolution trace structure.

The chunked script bounds channel memory for large `.fil` recordings. No raw recording or experimental data is included in this package.
