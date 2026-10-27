# Results of the 100-pass continuation and retained-state comparison

Only new files were added for these runs. Previous experiments and outputs remain unchanged.

## Continuing the recorded 25-pass chains

`continuation_100_results` adds 100 passes in each direction to the existing 25, reaching 125 total per direction. Every channel grows from 1,875 to 2,175 values, preserving every earlier value in order. Front/back endpoints remain `[1, 1, 1, 1]` throughout the batch. No new literal zero occurs. The endpoint-only phase function verifies this as an exact deterministic fixed point: further identical batches cannot change it.

All twelve native checks pass: four complete final chains, four newly added front segments, and four newly added back segments. Each actual Linux x86-64 executable assembles, links, exits zero, and returns all eight registers exactly as calculated by the interpreter.

## Retaining register feedback

The previous endpoint harness initializes unseeded registers to one on every call. The original repository experiment retained register state across passes. `stateful_100_comparison.py` therefore runs an additional, explicitly separate 100-pass experiment from the original recorded chains. It overwrites the same four opposite-end input slots, while retaining the other four register outputs between directions and rounds. Replaying from original inputs avoids inheriting a fixed point caused by the reset-mode run.

With retained state, front values settle to `[1, 1, 1, 1]` and back values to `[1, 1, 1, 7]`. The complete register and endpoint state at cycle 4 exactly repeats cycle 3. At cycle 3 and every later cycle, channel 4's left outputs are `[state=1, relations=0]`. The current prepend convention puts `state` first, so the zero is second in the chain rather than at its start. All twelve native checks also pass for this comparison.

No Y EOF marker is assigned. The repeated right value 7 is recorded as an output, not declared to mean EOF. The left output ordering remains a material wiring choice: prepending the pair as a unit gives `[state, relations]`; sequentially prepending state then relations would give `[relations, state]`. Changing that order consistently changes subsequent current inputs, so a different-order run must be recorded separately rather than merely relabelling these results.

Further identical batches cannot escape the observed deterministic loops. A new output-order or wiring choice should be recorded as a separate experiment before continuing. Numeric-original-value recovery is not a criterion; native executable functionality remains the check used here.
