# Whole-signal container transforms: complete preserved82x50 grid

{
  "paths": 132,
  "vertical_paths": 50,
  "horizontal_paths": 82,
  "branches": 792,
  "passes": 79200,
  "instruction_checks": 720388,
  "source_cells": 4100,
  "source_zero_bins": 2988,
  "source_nonzero_bins": 1112,
  "branches_with_repeats": 541,
  "repeat_period_counts": {
    "1": 479,
    "2": 62
  },
  "first_repeat_pass_counts": {
    "2": 258,
    "3": 215,
    "23": 4,
    "22": 3,
    "7": 15,
    "4": 4,
    "5": 24,
    "29": 3,
    "8": 9,
    "28": 1,
    "97": 1,
    "98": 2,
    "27": 1,
    "96": 1
  },
  "source_start_marker_identified": false,
  "source_end_marker_identified": false,
  "elapsed_seconds": 17.819
}

All4100 source cells are present in source_cells.csv. path_definitions.json maps every pass1 unit to its original coordinate. Fifty vertical and82 horizontal paths cover the grid in both axes. Intact input parts and whole-path sums are recorded as separate experiments; sums discard cell distinctions and are not the primary source representation. All-ones register initialization is an explicit new input adapter. The prior all-register-output feedback rule is unchanged. Every branch runs100 passes without output selection. Complete provenance, definitions, zero handling, and traversal details are in process.json.

source_boundaries.json records source edges and every contiguous nonzero run. The compressed instruction ledger stores all79200 pass records and every instruction before/after vector. register_passes.csv retains every program and eight-value result. hebrew_register_streams.txt retains all generated Hebrew numeric streams in one file. branch_summary.json records every first repeated full state and the period. A computational repeat is not a recovered source start/end marker. Source page bounds are not automatically message bounds. No word search or sentence coherence filter was used.

Reproduce before the run exists: python -X utf8 -B WOWSignal/scripts/step03_whole_signal_container_transforms.py
This command refuses an existing run directory and appends a checkpoint and the combined Hebrew outputs to the working Hebrew text.

Added the runner and run008 source_cells.csv, source_boundaries.json, path_definitions.json, process.json, instruction_trace.jsonl.gz, register_passes.csv, hebrew_register_streams.txt, branch_summary.json, summary.json, README.md, manifest.json. Appended data and process to the existing combined working Hebrew text. Added the runner byte-preserving .gitattributes rule. Earlier run records remain unchanged. No commit or push.


## Whole-source boundary relationships and validation

All4100 cells were processed in both axes; source_unit_execution.csv adds24600 cell-level records (4100cells x2axes x3orientations). Each records source order, traversal order, original coordinate, original character and numeric value, executed Greek glyphs, and all8 before/after registers. Zero cells are retained with no executed instruction. These records independently reproduce each intact path's first-pass final state.

Across both traversal sets there are1416 nonzero runs. None of the132 source paths is entirely blank. Nonzero-run boundaries describe transitions in the printed intensity bins; they do not establish message delimiters.

Of792 branches,479 reach period1 output repetitions and62 reach period2 cycles within100passes. The remaining251 have no repeated complete output within that window. Boundary_relationships.json retains groups of identical pass100 register vectors and every member path/branch. For example248branches have pass100 vector[1,1,1,1,1,3,1,1]. These shared outputs do not identify a unique source span or a unique start/end. All original coordinates remain available despite execution-state collisions.

Validation: all79200 compressed pass records were reopened and checked; all720388 per-instruction before/after connections and executed program strings were checked; every final pass matches its branch summary. The24600 cell-level records independently reproduce the intact-source first passes. Source input hashes, per-axis coverage, and append-only working text preservation are verified.

Added source_unit_execution.csv and boundary_relationships.json; appended this analysis to the report and combined working text; refreshed manifest hashes. No source-defined message beginning or ending was assigned. No commit or push.
