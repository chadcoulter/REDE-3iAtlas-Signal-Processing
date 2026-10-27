# Reading this run as transform phases

The user clarified after the initial run: the reverse step is not expected to return original measurement values. The original-value comparison counters in `results_initial/report.json`, `phases.csv`, and the seed-retention audit are diagnostic bookkeeping from an incorrect success criterion. They are not pass/fail criteria for the requested transform.

Read the phase sequence as:

1. Opposite-end four-value seeding, then current inputs, yields one `target` value per channel on X to Y.
2. Those four targets become the current reverse inputs. With opposite-side seeds, the reverse traversal yields `state` and `relations` per channel on Y to X.
3. For each active channel, select the other three channels' outputs. Preserve both leftward values as separate constituents; no averaging, concatenating integers, or selecting one is applied.

`results_initial/phase_values.csv` lists the rightward scalar, leftward pair, and each value's numeral-operator representation without original-value match columns. `results_initial/phases.csv` also preserves every active-channel exclusion view. `register_trace.csv` records the register provenance.

This first execution uses four separate eight-register banks, all seeded with the same opposite-end vector. The fixed initial assignment places those four seeds in `state`, `relations`, `constraints`, and `observations`; remaining registers start at one. This assignment and the independent-bank architecture are test choices. In particular, each bank processes its own current input; there is no hidden shared-memory propagation between banks. The experiment has not established that this is the intended shared four-channel layout.

The 24 first-row seed assignments produce 12 distinct four-channel target vectors. Consistent placement permits repeatable runs, but these operator bodies are placement-sensitive in this sample.

Original source files and earlier result files were not edited. This note records the corrected interpretation as an additional file.
