# Mirrored handoff, one register at a time

Test the stated routing: reflection 1 -> projection 4, 2 -> 3, 3 -> 2, and 4 -> 1. Each reverse executable receives the complete native ending register state of its paired forward executable. One register slot is replaced by the forward function output; the other seven remain unchanged. Register positions are not reversed and no fresh four-endpoint seed is applied at the turn.

This initial run selects `target` as the scalar function output, explicitly recorded in the result and configurable with `--output-register`. The test substitutes it into each of the eight logical register slots separately. A mirrored no-substitution case provides a control. Each case starts from the same independent forward outputs; it does not inherit another substitution case's result. Register 1 is `state`.

The input is the captured aligned core: 1,934 chain values per channel, initialized with its recorded core entry state. Forward runs must reproduce the existing native core output. Reverse runs traverse the mirrored destination's values and glyphs in reverse order. This is a single-turn routing test; chain extension is not performed in this experiment.

Every executable is freshly assembled, linked and run natively. Forty programs are executed: four forward baselines, four mirrored no-substitution controls and thirty-two one-slot substitution runs. Their actual native ending states are compared to the operator reference. Substituting target with itself provides an additional identity check and must match the no-substitution case exactly.

Results preserve all eight registers, exact uint64 strings, source and destination channel links, substituted values, changed output registers, and source/executable hashes. Readout vectors are labelled in destination-channel order so the mirrored routing cannot silently reverse their interpretation. Pattern matches are recorded without assigning a new success/failure definition.

Run `test_mirrored_register_handoff.py` inside WSL Ubuntu against the archived operators, passing a fresh `--output` directory. Existing files are not modified.
