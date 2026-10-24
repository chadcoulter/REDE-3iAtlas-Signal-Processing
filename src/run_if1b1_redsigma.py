# REDΣ Signal Extraction and Return Analysis — 3I/ATLAS

**Research snapshot: 24 October 2026**  
**Recording:** `guppi_60887_52472_6690873992_3IATLAS_R_0001.0000.fil`  
**Scope:** extracted band IF1_B1 and exploratory eight-register operator-state analysis.

## Executive findings

A SIGPROC filterbank recording with 64,000,000 frequency channels and one IF stream was processed with a memory-bounded band extractor. The saved metadata reports **20 frames**, **15 seconds per frame**, **64 detected bands**, and a 64-band detection cap. Consequently, these results cover **300 seconds** and do not establish the number of distinct bands across the complete 12 GB recording.

Band **IF1_B1**, near **758.498 MHz**, was examined across 20 observations. Its peak-amplitude measurements range from 299,522,880 to 428,221,504, with the maximum at 165 seconds. The largest adjacent decline was **73,042,368** between 195 and 210 seconds. The observation at 240 seconds is within **428,640** (~0.129%) of the 0-second amplitude. These are near-returns of a scalar measurement, not complete state returns.

The numerical measurements were encoded in groups of three decimal digits as Greek numerals. Those numerals were also interpreted as sequences of REDΣ Book II operators for an exploratory state-machine execution. This is a defined experimental transformation of numeric measurements, **not evidence that the radio signal contains Greek writing or a linguistic transmission**.

## State-machine experiments

The supplied experiment scripts and reports describe six executions: three forward and three reverse, with each later pass seeded from the preceding pass's complete eight-register output. Reversal changes the order of frames and Greek glyph operators; it is **not an algebraic inverse**.

| Reported measurement | Value |
|---|---:|
| Frame-level snapshots | 120 |
| Operator-level snapshots | 960 |
| Exact repeated eight-register states | 57 |
| Adjacent stationary transitions | 51 |
| Genuine departure-and-return pairs | 27 |
| Returns spanning 2 operators | 11 |
| Returns spanning 3 operators | 10 |
| Returns spanning 4 operators | 6 |
| Exact forward/reverse full-state intersections | 0 |

The return analysis identifies short operator-level loops, but no demonstrated long-range recurring full-state cycle. The reports describe repeated returns around frame boundaries and different end states between forward and reverse traversals.

## Interpretation and limits

- **Observed:** spectral band measurements and numeric near-returns in the extracted 20-frame subset.
- **Computed in saved trace:** exact register-state repeats and short departure/return loops under the chosen operator implementation.
- **Still to establish:** whether the observed operator loops are caused by the signal, the Greek numeral encoding, or the operator rules. This requires control runs using shuffled, randomized, and other-band input under identical settings.
- **Coverage:** detection selects a limited set of bands from a sampled scan. It does not yet discover every transient band appearing later in the recording.
- **Reproducibility:** raw `.fil` recordings are not included. The analysis relies on the included extracted CSVs and original operator assembly source being available. Some scripts refer to local paths; inspect and configure them before running.

## Recommended next experiment

1. Scan all frames with a rolling, memory-bounded detector and preserve each band's onset, offset, and recurrence.
2. Re-run the operator trace for every band and retain full eight-register states after every glyph.
3. Separate unchanged-state runs from actual departure-and-return cycles.
4. Compare cycles against shuffled signals, synthetic amplitude sequences, and other detected bands to estimate signal specificity.
5. Publish machine-readable provenance: source file hashes, extractor version, exact invocation, seed state, and assembly build details.

## Repository layout

- `src/`: extractors and experimental analysis programs.
- `data/`: user-supplied extracted band, stream and metadata files.
- `results/`: state traces and analysis reports.
- `README.md`: this research summary.

**Provenance note:** Reported counts are drawn from the included analysis artifacts and should be independently regenerated before treating the implementation as validated across machines or recordings.