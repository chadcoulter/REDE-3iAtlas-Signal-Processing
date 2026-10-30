# Cyclic n+1 handoff with signal chains kept in place

This test changes only the handoff routing from the mirrored layout to `(n + 1) % 4` using zero-based positions: `0 -> 1`, `1 -> 2`, `2 -> 3`, `3 -> 0`. The equivalent existing one-based channel labels are `1 -> 2`, `2 -> 3`, `3 -> 4`, `4 -> 1`.

Each physical channel's captured core instruction sequence stays in place. The forward reflection baselines, core entry states, scalar output selection (`target`), backward projection traversal and register substitution sweep are unchanged from the mirrored test. A native reflection ending state is copied into the next channel, optionally replacing one selected slot with that reflection's target. The other slots remain untouched; there is no fresh endpoint seeding at the handoff.

The same nine cases are run: no substitution, then one separate substitution for each of eight register slots. All cases start independently from the same reflection outputs. Forty programs are freshly assembled, linked and executed: four reflection baselines and thirty-six projection runs. Target substituted with itself is the identity control.

`test_rotated_register_handoff.py` is an additive copy of the preceding runner; the sole computational routing change is `destination = source_channel % 4 + 1`. The original file is unchanged. New output lives in `rotated_register_test_results`.

`verify_and_compare.py` audits all native outputs and archived hashes, exact one-slot handoffs and modulo wrapping. It compares the complete `.text` assembly body for every destination and case against the mirrored run to confirm that the signal/code sequence was not moved or rewritten. The routes ending at zero-based positions 0 and 2 are unchanged between the two mappings; their full outputs and executable hashes must remain identical.

Readout vectors in the original case format are labelled with one-based destination channels 1–4. `comparison_to_mirrored.json` also explicitly labels the equivalent zero-based order 0–3. Only numeric pattern observations are reported; no extra success/failure interpretation is imposed.
