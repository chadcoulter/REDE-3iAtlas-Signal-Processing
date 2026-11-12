# Container-as-transform feedback experiment 001

This run tests the user's proposal to treat the container as transform information. It executes the recovered original Greek machine operators on intact candidate numeric units, then follows their output through a newly specified feedback rule.


Container-as-transform follow-up: orientation changes target writes

Execution order below is left-to-right Greek instruction order. Hebrew labels identify the intact numeric units, not a sentence. The eight output registers are state, relations, constraints, observations, unresolved, context, target, events.

Rule used in this new experiment: execute the candidate in its generating-program register context; encode all eight output registers with the recovered original Greek numeric encoder; execute that output as the next program while carrying the state. This is an explicit experimental feedback rule, distinct from run003's recovered append/prepend growth rule.

Forward seed32 הגה: [5,3,5] -> ΕΓΕ. Ε increments observations only if constraints=0; Γ sets constraints=state &255. From the recorded seed state (state5, constraints4), the execution leaves observations4 and sets constraints5. It emits [5,3,5,4,1,5,1,13], or Ε ‖ Γ ‖ Ε ‖ Δ ‖ Α ‖ Ε ‖ Α ‖ ΙΓ. The next executed program is ΕΓΕΔΑΕΑΙΓ, producing [1,3,1,4,1,5,1,14]. Thus additional instructions are explicitly generated from the register projection.

Forward וידא: intact parts [6,14,1] -> ϚΙΔΑ. Ϛ increments unresolved, Ι increments events, Δ increments state, Α resets state to1. Starting from program5 output [1,14,26,30,3,1,1,1], pass1 produces [1,14,26,30,4,1,1,2]. Re-encoding gives Α ‖ ΙΔ ‖ ΚϚ ‖ Λ ‖ Δ ‖ Α ‖ Α ‖ Β. Pass2 executes ΑΙΔΚϚΛΔΑΑΒ and produces [1,14,26,30,5,3,1,3]. The leading כ retained in כוידא instead supplies Κ before ϚΙΔΑ and changes context.

Reverse numeric-container traversal for וידא (Greek units execute in listed order):
Pass1 ΑΙΔϚ -> state2, target1, events2.
Pass2 ΒΑΑΔΛΚϚΙΔΒ -> state13, target1, events3.
Pass3 ΓΑΔΕΛΚϚΙΔΙΓ -> state13, target1, events5.
Pass4 ΕΑΕϚΛΙΓΙΔΙΓ -> state16, target1, events8.
Pass5 ΗΑΕΖΛΙϚΙΔΙϚ -> state15, target16, events11.
The event value8 from pass4 becomes the leading Η in pass5. Η copies incoming state16 into target, before Α resets state. This is the first target-changing operation in that branch.

Intact כוידא under the same container-reversal rule:
Pass1 ΑΙΔΚϚ -> state2, target1, events2.
Pass2 ΒΑΔΔΛΚϚΙΔΒ -> state14, target1, events3.
Pass3 ΓΑΖΕΛΚϚΙΔΙΔ -> state16, target1, events5.
Pass4 ΕΑΗϚΛΙΔΙΕΙϚ -> state15, target1, events8.
Pass5 ΗΑΗΗΛΙΔΙΕΙΕ -> state15, target1, events11.
Pass5 instruction1 Η writes target15; instruction2 Α resets state1; instruction3 Η overwrites target1. Instruction4 Η repeats that write without changing its value. The first write is not the final result. At the preceding pass the context value8 also generates Η for the next program. The extra prefix's effects propagate into subsequent programs.

Whole-container totals are separate alternatives: הגה total13 -> ΙΓ; וידא total21 -> ΚΑ; כוידא total41 -> ΜΑ. They do not execute the same instruction sequence as the intact parts despite having the same summed numeric value.

Finding: within this explicit feedback rule, orientation and preserved container boundaries affect generated instruction order and later target writes. Target is the machine register name; no physical direction, astronomical coordinate, or decoded sentence is established by its value. Five passes are a bounded exploration, not evidence of convergence. Full glyph reversal and numeric-container reversal happen to reach the same five-pass final states for the two verification candidates; their instruction sequences remain distinct.

No observed letters were added. Source channels, original blanks, and surrounding יטה are unchanged. The generated Hebrew remains numeric register output, with boundaries retained. Status: IN-PROGRESS.

## Reproduce

From the repository root, use a NEW output directory:

```powershell
python -X utf8 -B WOWSignal/scripts/step03_container_transform_feedback.py --rounds 5 --output NEW_OUTPUT_DIRECTORY
```

The saving mode appends its ledger once to the working Hebrew text and refuses an existing run directory or repeated append marker. For a read-only recomputation, omit `--output` (the full JSON ledger is printed). The new feedback rule is in the runner and results, rather than claimed as an original 3i-Atlas decompressor.

## Coverage and checks

24 branches, five iterations each: three intact candidate containers, two generating contexts for הגה, original numeric parts versus whole sums, and three orientations. Every executed operation is compared with the preserved original instruction interpreter. The ledger retains every input, output, instruction, intermediate register vector, and candidate provenance. A separate read-only recomputation must reproduce the entire saved JSON result. The original frozen Hebrew export remains an exact prefix of the updated working text.

## Files changed in this experiment

- Added `WOWSignal/scripts/step03_container_transform_feedback.py`.
- Added this run's `results.json`, `README.md`, and `manifest.json`.
- Appended experiment output and this causal follow-up to `run-001/hebrew_streams_updated.txt`.
- Added the runner's byte-preserving rule to `WOWSignal/.gitattributes`.

Earlier uncommitted runs002–004 and original-source recovery remain separate work. No commit or push was made in this experiment.


## Reporting scope correction — 2026-11-11

User direction: stop trying to build sentences; obtain and report the data, and record both the data and the process.

Subsequent passes will retain exact numeric units, source/generating-program provenance, container boundaries, execution direction, encoder and operator definitions, seed state, feedback rule, every intermediate state, and final register outputs. Report numerical changes and operation dependencies. Do not optimize for grammatical phrases or use sentence coherence to select outputs. Existing sentence-oriented interpretations remain historical entries, not acceptance criteria for this experiment.

The current container selection was inherited from earlier lexical exploration; it is a selected subset, not an exhaustive scan of the signal. The output-register feedback rule is an investigator-defined experimental choice. Source observations, generated values, and process choices must remain identifiable separately.

Data: `results.json` retains all 24 branches, 120 pass records, and 977 per-instruction records. `register_passes.csv` provides the same pass-level data as 120 rows, including input units, exact executed program, all eight before/after register values, and Greek/Hebrew numeric renderings. No numeric result or machine operation was changed for this correction.

Computed findings under the recorded rule: reverse numeric-container traversal of [6,14,1] yields pass5 target16; the intact [26,14,1] branch yields pass5 target1 after successive writes15 then1. These are register results of the recorded programs. Equal total values and intact-part encodings generate different instruction sequences. The complete data include all tested orientations and whole-total alternatives.

Changes for this correction: added `register_passes.csv`; appended this scope/process record to this README and the combined working Hebrew text; refreshed `manifest.json` to cover the added CSV and updated documentation. No commit or push.
