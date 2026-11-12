# Endpoint phase wiring experiment

This is an explicit candidate implementation of the endpoint-seeded test discussed on October 26, 2026. Existing repository files are unchanged.

For each aligned row, take its four rounded, pre-numeral input values as `x`, and the four values at the opposite row as `y`. Each channel has an eight-register bank. The initial assignment is `y1 -> state`, `y2 -> relations`, `y3 -> constraints`, `y4 -> observations`; remaining registers start at 1. These are experimental choices. The current channel's integer is encoded with the repository numeral table and dispatched through the archived operators after the endpoint values have been seeded.

**X to Y:** original command order; extract `target` from each other channel. Four channel outputs constitute the projected endpoint phase. Every active-channel view excludes itself.

**Y to X:** projected targets become the four current inputs, and the original `x` values become the opposite seeds. Reverse command order and extract `state` and `relations` from each other channel. Keep both values, rather than inventing a reduction. Compare each with original `x` and test forwarding each candidate plane again.

The runner also tries all 24 assignments of the four seeds to the chosen four register slots on the first endpoint pair. This checks placement sensitivity; it does not exhaust choices among eight slots. Independent channel banks and the use of original `x` as reverse seeds are explicit candidate wiring decisions. These need inspection against the intended shared-channel transform.

The assembly archive identifies ranked spectral stripes. Stripe identity can change frequency. Reverse command order follows the existing experiment convention and does not guarantee inverse arithmetic.

Run from the repository root (Python standard library only):

```powershell
python -B experiments/endpoint_phase_v1/endpoint_phase.py C:/Users/ccoulter/Downloads/3I_ATLAS_six_recordings_four_stripes_asm.zip --output experiments/endpoint_phase_v1/results_initial
```

The output directory must not already exist. The runner only creates new files. `first_row.json` is the smallest inspection artifact. `phases.csv` retains inputs, directional outputs and other-channel views. `register_trace.csv` retains all seeded and final registers. `mapping_comparison.json` lists placement trials; `report.json` records assumptions, source hashes and comparison counts.

Operator interpretation is checked against independent direct translations on boundary and deterministic randomized states. Original numerical encoding is checked for every source row. Native binaries are not executed. This portable execution uses archived operators because the repository's original runner depends on a missing `3I_ATLAS_four_lane_all_register_feedback.S` file.
