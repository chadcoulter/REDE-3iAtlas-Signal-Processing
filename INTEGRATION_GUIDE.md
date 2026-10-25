# REDΣ 3I/ATLAS Signal Processing — Integration Guide

**Repository:** `chadcoulter/REDE-3iAtlas-Signal-Processing`  
**Component:** `skills/character-transform-reasoning/`  
**Purpose:** Integrate the existing SIGPROC signal extractors with REDΣ Book II Character Transform Reasoning and governed resolution.

## 1. Architecture

The integration consists of six sequential processing stages:

```text
SIGPROC .fil recording
        |
        v
[1] Signal extraction
    Spectral detection and band isolation
        |
        v
[2] Numerical encoding
    Measured values -> Greek numerals
        |
        v
[3] Character mapping
    Typed glyphs -> Book II operators
        |
        v
[4] REDΣ transformation
    Sequential relational-state operations
        |
        v
[5] Governed resolution
    Candidate comparison, reversal, Enough
        |
        v
[6] Validation and reporting
    Trace, provenance, residuals, status
```

Each stage preserves its inputs, outputs, transformation parameters, and relationship to the preceding stage.

## 2. Repository components

| File | Function |
|---|---|
| `SKILL.md` | Character transformation execution procedure |
| `references/book-ii-alphabet.txt` | Authoritative Book II operator definitions |
| `references/governance-v0.4.md` | Governance adaptation |
| `references/governance-v0.4-source.docx` | Original governance source |
| `references/resolution-contract.md` | State, trace, comparison, and validation contract |
| `references/signal-extraction.md` | Signal extraction interface documentation |
| `scripts/redsigma_band_extract.py` | Standard SIGPROC spectral-band extractor |
| `scripts/redsigma_band_extract_chunked.py` | Bounded-memory channel-chunked extractor |
| `scripts/validate_resolution.py` | Resolution trace validator |
| `requirements.txt` | NumPy and SciPy dependencies |

All paths in this table are relative to `skills/character-transform-reasoning/`.

## 3. Environment setup

From the repository root:

```bash
python -m venv .venv
python -m pip install -r skills/character-transform-reasoning/requirements.txt
```

Activate the virtual environment before installing packages if your environment requires it.

The existing extractors accept SIGPROC `.fil` recordings with supported 8-, 16-, 32-, or 64-bit sample representations.

## 4. Stage 1 — Signal extraction

### Standard extraction

```bash
python skills/character-transform-reasoning/scripts/redsigma_band_extract.py recording.fil -o output/bands
```

### Chunked extraction

```bash
python skills/character-transform-reasoning/scripts/redsigma_band_extract_chunked.py recording.fil -o output/bands --channel-chunk 65536
```

The chunked version processes channel tiles to reduce peak-detection memory requirements.

Both scripts produce:

```text
output/bands/
├── bands.csv
├── streams.csv
└── metadata.json
```

### Extraction controls

| Argument | Default | Purpose |
|---|---:|---|
| `--scan-frames` | 64 | Frames sampled for spectral detection |
| `--max-bands` | 16 | Maximum selected peaks per IF |
| `--threshold` | 5.0 | Peak prominence threshold in robust noise units |
| `--min-separation` | 32 | Minimum channel separation |
| `--half-width` | 8 | Channels on either side of a detected peak |
| `--max-frames` | All | Optional frame-processing limit |
| `--channel-chunk` | 65536 | Channel tile size in the chunked extractor only |

**`bands.csv`** records detected bands, channel boundaries, frequencies, peak measurements, and noise estimates.

**`streams.csv`** records measurements over time for each detected band: frame, elapsed seconds, stream ID, IF index, channel, frequency, amplitude, rounded integer, Greek numeral encoding (`gematria`), band sum, integer band sum, and Greek numeral band sum.

**`metadata.json`** records the source, SIGPROC header, processing counts, extraction settings, and encoding description.

## 5. Stage 2 — Greek numerical encoding

The extractors already perform numerical encoding through a Greek numeral lookup.

| Integer | Encoded value |
|---:|---|
| 1 | Α |
| 6 | Ϛ |
| 10 | Ι |
| 90 | Ϟ |
| 100 | Ρ |
| 900 | Ϡ |

Values above 999 use separated groups of three decimal digits. The scripts round measured values to integers before encoding, using round-half-away-from-zero.

Retain the original numerical value alongside each encoded glyph sequence. Encoding is a representation stage; character-transform execution is a subsequent stage.

## 6. Stage 3 — Character mapping

Read selected `streams.csv` records and preserve the source recording, frame, elapsed time, stream ID, channel, frequency, amplitude, rounded integer, and Greek numeral encoding.

A glyph can have different roles depending on its namespace:

- `Ϛ` represents numerical value 6 in the extractor's encoding.
- `Ϛ` is the observable unresolvedness operator in Book II.
- `Ϟ` represents numerical Koppa; its indexed relationship role is distinct from relational Koppa `Ϙ`.

Record whether each glyph is treated as a numerical symbol or explicitly invoked as a transformation operator. Preserve alternatives and provenance.

**Proposed output:** `mapped_occurrences.json`, containing source index, glyph, numerical value, selected operator, namespace, mapping rationale, and alternatives.

**Implementation status:** The extractors already produce Greek numerical symbols. A dedicated typed mapping adapter is still required to connect these outputs to Book II execution.

## 7. Stage 4 — REDΣ Character Transformation

The Character Transform Reasoning skill governs execution. Pass the selected character sequence and its provenance into the skill and follow `SKILL.md`:

1. Register the original input and human request.
2. Freeze governance for the resolution cycle.
3. Segment exact Unicode occurrences.
4. Select and record character-to-operator mappings.
5. Execute Book II operators sequentially against evolving relational state.
6. Compose candidate readings while retaining contributions and unresolved relationships.
7. Preserve the transformation trace.

Book II capitalization rule:

- **UPPERCASE:** How to resolve the observable.
- **lowercase:** How to resolve the hidden.

Preserve original capitalization. Any selection of observable or hidden operator mode must be recorded.

The authoritative operator definitions remain in `references/book-ii-alphabet.txt` and must not be changed by integration work.

## 8. Stage 5 — Governed resolution

Governance-Driven Resolution Lattice v0.4 applies:

- **H — Human request:** Purpose and scope of the analysis.
- **G — Governance:** Criteria, priorities, materiality, equivalence, and bounds.
- **Rn — Candidate state:** A transformation result with source contributions and retained alternatives.

Evaluate candidate changes under frozen governance. Record Better, Same, Worse, or an explicitly mixed/unresolved result. Reversal creates a new transformation record without deleting earlier states.

| Status | Meaning |
|---|---|
| `VALID TRANSFORM` | Three consecutive eligible materially unchanged transitions |
| `SUFFICIENT RESOLUTION` | Authorized Enough Boundary satisfied |
| `INVALID VALIDATION` | Applicable governance validation failed |
| `BUDGET EXHAUSTED` | Bounds reached without acceptance |
| `IN-PROGRESS` | Continuing resolution |
| `UNRESOLVED` | Outstanding material relationships |

## 9. Stage 6 — Trace validation

Validate saved JSON resolution traces with:

```bash
python skills/character-transform-reasoning/scripts/validate_resolution.py output/resolution_trace.json
```

The validator checks candidate identifiers, transformation references, frozen-governance consistency, comparison accounting, and declared terminal-status requirements.

The JSON contract is documented in `references/resolution-contract.md`. Successful structural validation prints `PASS`.

## 10. Proposed integrated output structure

```text
output/
└── recording_id/
    ├── extraction/
    │   ├── bands.csv
    │   ├── streams.csv
    │   └── metadata.json
    ├── mapping/
    │   └── mapped_occurrences.json
    ├── resolution/
    │   ├── resolution_trace.json
    │   └── transformed_reading.md
    └── validation/
        └── validation_result.json
```

Extraction outputs are implemented. Mapping, resolution, and validation output directories are proposed integration artifacts.

## 11. Integration development requirements

Three new components complete the automated pipeline:

### A. Signal-to-character adapter

**Proposed:** `scripts/signal_to_character.py`

Read `streams.csv`, select source sequences, preserve measurements, and emit typed character occurrences.

### B. Transformation runner

**Proposed:** `scripts/run_character_transform.py`

Load mappings and Book II authority, apply governance, and record candidate transformations. Execute the skill's actual relational-state and trace requirements rather than substituting glyph names.

### C. Pipeline orchestrator

**Proposed:** `scripts/run_pipeline.py`

Coordinate extraction, mapping, transformation, and validation. Record inputs, parameters, outputs, and execution results in a manifest.

These are proposed new files, separate from the recovered originals.

## 12. Reproducibility sequence

1. Identify the exact `.fil` recording.
2. Record its checksum and SIGPROC header.
3. Execute the chosen extractor with recorded arguments.
4. Preserve all three extraction outputs.
5. Select stream, frames, and numerical representation for mapping.
6. Record each glyph mapping and source occurrence.
7. Execute Book II transforms under identified governance.
8. Preserve candidates, alternatives, contribution edges, and reversal history.
9. Validate the saved trace.
10. Record final resolution status and open relationships.

## 13. Acceptance criteria

- Both original extractors remain available and executable.
- Extraction outputs trace to their input recordings and parameters.
- Every mapped character retains its source numerical measurement.
- Book II execution produces an inspectable relational-state trace.
- Governance remains fixed within each cycle.
- Reversal and alternatives retain their history.
- The trace validator passes applicable structural tests.
- A single pipeline command reproduces the complete process.

## 14. Implementation status

| Component | Status |
|---|---|
| SIGPROC extraction | Existing implementation |
| Chunked signal extraction | Existing implementation |
| Greek numeral encoding | Existing implementation |
| Book II operator reference | Existing |
| Character Transform Reasoning skill | Existing |
| Governance and resolution contract | Existing |
| Resolution trace validator | Existing implementation |
| Signal-to-character adapter | To implement |
| Automated Book II transformation runner | To implement |
| End-to-end pipeline orchestrator | To implement |
| End-to-end integration test | To execute |

**Integration objective:** Establish a reproducible processing path from measured radio-signal states through Greek character representations into REDΣ relational transformation and governed resolution, preserving original measurements, operator definitions, provenance, and transformation history.

**Source authority:** The original REDΣ Book II skill and signal extraction scripts in this repository.
