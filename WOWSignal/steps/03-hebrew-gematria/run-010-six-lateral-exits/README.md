# Six lateral exits through the28-cell component — bidirectional record

2026-11-12. Status: IN-PROGRESS.

User-authorized scope: use the live Unified VRE harness and BookII character-transform skill to follow the six lateral exits in both directions, show coordinates and transforms, and preserve the data/process. No sentence construction, source changes, new message letters, commit, or push.

The component retains28 original nonzero cells,30 four-neighbor links,19 source-preserving corridors and3 independent cycles. The original source perimeter retains50 observed zero edges and2 outside-page edges. The six core cells remain a source spine; core-return route endpoints retain their onward neighbors rather than being declared terminal.

Route coverage:26 outward continuations:12 core returns and14 graph-leaf routes. Both directions yield52 primary route evaluations. A further26 explicitly separate full-glyph reversal comparisons retain the distinction between container order and internal glyph order. All78 machine trials start from explicitly declared all-ones registers; they are comparison trials, not recovered original source states. Every one of735 native operations matches the preserved original instruction interpreter. Native action and attributed BookII role remain separate fields. The live reasoning request contains the full graph, all26 routes, perimeter and original BookII definitions.

Method: traverse each crossing into the non-core forest; retain every branch until the next core re-entry or original graph leaf. Every branch is still explored when another branch re-enters the core. An independent BFS tree-path enumeration confirms the exact26 coordinate walks. All30 neighbor links appear once in the corridor decomposition. Three non-tree edges of a spanning tree define the independent cycle basis. A graph boundary is retained as a scoped observation, not a decoded message delimiter.

Exit accounting:
{"exit": "E1", "routes": ["P01"], "core_return_coordinates": [], "leaf_coordinates": [[59, 1]]}
{"exit": "E2", "routes": ["P02", "P03", "P04", "P05", "P06", "P07"], "core_return_coordinates": [[61, 2], [62, 2], [63, 2]], "leaf_coordinates": [[58, 4], [72, 5], [73, 4]]}
{"exit": "E3", "routes": ["P08", "P09", "P10", "P11", "P12", "P13"], "core_return_coordinates": [[59, 2], [62, 2], [63, 2]], "leaf_coordinates": [[58, 4], [72, 5], [73, 4]]}
{"exit": "E4", "routes": ["P14"], "core_return_coordinates": [], "leaf_coordinates": [[62, 1]]}
{"exit": "E5", "routes": ["P15", "P16", "P17", "P18", "P19", "P20"], "core_return_coordinates": [[61, 2], [59, 2], [63, 2]], "leaf_coordinates": [[58, 4], [72, 5], [73, 4]]}
{"exit": "E6", "routes": ["P21", "P22", "P23", "P24", "P25", "P26"], "core_return_coordinates": [[61, 2], [59, 2], [62, 2]], "leaf_coordinates": [[58, 4], [72, 5], [73, 4]]}

Coordinate-complete outward routes; reverse each complete cell list for the inward traversal while retaining each numeric container internally:

P01 E1 graph_leaf
Coordinates: r59c02 ↔ r59c01
Numeric: 14 | 1
Hebrew: יד | א
Greek: ΙΔ | Α

P02 E2 graph_leaf
Coordinates: r59c02 ↔ r59c03 ↔ r59c04 ↔ r58c04
Numeric: 14 | 2 | 4 | 2
Hebrew: יד | ב | ד | ב
Greek: ΙΔ | Β | Δ | Β

P03 E2 core_return
Coordinates: r59c02 ↔ r59c03 ↔ r59c04 ↔ r60c04 ↔ r61c04 ↔ r61c03 ↔ r61c02
Numeric: 14 | 2 | 4 | 1 | 1 | 3 | 30
Hebrew: יד | ב | ד | א | א | ג | ל
Greek: ΙΔ | Β | Δ | Α | Α | Γ | Λ

P04 E2 core_return
Coordinates: r59c02 ↔ r59c03 ↔ r59c04 ↔ r60c04 ↔ r61c04 ↔ r61c03 ↔ r62c03 ↔ r62c02
Numeric: 14 | 2 | 4 | 1 | 1 | 3 | 1 | 19
Hebrew: יד | ב | ד | א | א | ג | א | יט
Greek: ΙΔ | Β | Δ | Α | Α | Γ | Α | ΙΘ

P05 E2 core_return
Coordinates: r59c02 ↔ r59c03 ↔ r59c04 ↔ r60c04 ↔ r61c04 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r63c02
Numeric: 14 | 2 | 4 | 1 | 1 | 3 | 1 | 1 | 5
Hebrew: יד | ב | ד | א | א | ג | א | א | ה
Greek: ΙΔ | Β | Δ | Α | Α | Γ | Α | Α | Ε

P06 E2 graph_leaf
Coordinates: r59c02 ↔ r59c03 ↔ r59c04 ↔ r60c04 ↔ r61c04 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r72c05
Numeric: 14 | 2 | 4 | 1 | 1 | 3 | 1 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: יד | ב | ד | א | א | ג | א | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: ΙΔ | Β | Δ | Α | Α | Γ | Α | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P07 E2 graph_leaf
Coordinates: r59c02 ↔ r59c03 ↔ r59c04 ↔ r60c04 ↔ r61c04 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r73c04
Numeric: 14 | 2 | 4 | 1 | 1 | 3 | 1 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: יד | ב | ד | א | א | ג | א | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: ΙΔ | Β | Δ | Α | Α | Γ | Α | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P08 E3 graph_leaf
Coordinates: r61c02 ↔ r61c03 ↔ r61c04 ↔ r60c04 ↔ r59c04 ↔ r58c04
Numeric: 30 | 3 | 1 | 1 | 4 | 2
Hebrew: ל | ג | א | א | ד | ב
Greek: Λ | Γ | Α | Α | Δ | Β

P09 E3 core_return
Coordinates: r61c02 ↔ r61c03 ↔ r61c04 ↔ r60c04 ↔ r59c04 ↔ r59c03 ↔ r59c02
Numeric: 30 | 3 | 1 | 1 | 4 | 2 | 14
Hebrew: ל | ג | א | א | ד | ב | יד
Greek: Λ | Γ | Α | Α | Δ | Β | ΙΔ

P10 E3 core_return
Coordinates: r61c02 ↔ r61c03 ↔ r62c03 ↔ r62c02
Numeric: 30 | 3 | 1 | 19
Hebrew: ל | ג | א | יט
Greek: Λ | Γ | Α | ΙΘ

P11 E3 core_return
Coordinates: r61c02 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r63c02
Numeric: 30 | 3 | 1 | 1 | 5
Hebrew: ל | ג | א | א | ה
Greek: Λ | Γ | Α | Α | Ε

P12 E3 graph_leaf
Coordinates: r61c02 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r72c05
Numeric: 30 | 3 | 1 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: ל | ג | א | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: Λ | Γ | Α | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P13 E3 graph_leaf
Coordinates: r61c02 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r73c04
Numeric: 30 | 3 | 1 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: ל | ג | א | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: Λ | Γ | Α | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P14 E4 graph_leaf
Coordinates: r62c02 ↔ r62c01
Numeric: 19 | 2
Hebrew: יט | ב
Greek: ΙΘ | Β

P15 E5 core_return
Coordinates: r62c02 ↔ r62c03 ↔ r61c03 ↔ r61c02
Numeric: 19 | 1 | 3 | 30
Hebrew: יט | א | ג | ל
Greek: ΙΘ | Α | Γ | Λ

P16 E5 graph_leaf
Coordinates: r62c02 ↔ r62c03 ↔ r61c03 ↔ r61c04 ↔ r60c04 ↔ r59c04 ↔ r58c04
Numeric: 19 | 1 | 3 | 1 | 1 | 4 | 2
Hebrew: יט | א | ג | א | א | ד | ב
Greek: ΙΘ | Α | Γ | Α | Α | Δ | Β

P17 E5 core_return
Coordinates: r62c02 ↔ r62c03 ↔ r61c03 ↔ r61c04 ↔ r60c04 ↔ r59c04 ↔ r59c03 ↔ r59c02
Numeric: 19 | 1 | 3 | 1 | 1 | 4 | 2 | 14
Hebrew: יט | א | ג | א | א | ד | ב | יד
Greek: ΙΘ | Α | Γ | Α | Α | Δ | Β | ΙΔ

P18 E5 core_return
Coordinates: r62c02 ↔ r62c03 ↔ r63c03 ↔ r63c02
Numeric: 19 | 1 | 1 | 5
Hebrew: יט | א | א | ה
Greek: ΙΘ | Α | Α | Ε

P19 E5 graph_leaf
Coordinates: r62c02 ↔ r62c03 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r72c05
Numeric: 19 | 1 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: יט | א | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: ΙΘ | Α | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P20 E5 graph_leaf
Coordinates: r62c02 ↔ r62c03 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r73c04
Numeric: 19 | 1 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: יט | א | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: ΙΘ | Α | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P21 E6 core_return
Coordinates: r63c02 ↔ r63c03 ↔ r62c03 ↔ r61c03 ↔ r61c02
Numeric: 5 | 1 | 1 | 3 | 30
Hebrew: ה | א | א | ג | ל
Greek: Ε | Α | Α | Γ | Λ

P22 E6 graph_leaf
Coordinates: r63c02 ↔ r63c03 ↔ r62c03 ↔ r61c03 ↔ r61c04 ↔ r60c04 ↔ r59c04 ↔ r58c04
Numeric: 5 | 1 | 1 | 3 | 1 | 1 | 4 | 2
Hebrew: ה | א | א | ג | א | א | ד | ב
Greek: Ε | Α | Α | Γ | Α | Α | Δ | Β

P23 E6 core_return
Coordinates: r63c02 ↔ r63c03 ↔ r62c03 ↔ r61c03 ↔ r61c04 ↔ r60c04 ↔ r59c04 ↔ r59c03 ↔ r59c02
Numeric: 5 | 1 | 1 | 3 | 1 | 1 | 4 | 2 | 14
Hebrew: ה | א | א | ג | א | א | ד | ב | יד
Greek: Ε | Α | Α | Γ | Α | Α | Δ | Β | ΙΔ

P24 E6 core_return
Coordinates: r63c02 ↔ r63c03 ↔ r62c03 ↔ r62c02
Numeric: 5 | 1 | 1 | 19
Hebrew: ה | א | א | יט
Greek: Ε | Α | Α | ΙΘ

P25 E6 graph_leaf
Coordinates: r63c02 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r72c05
Numeric: 5 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: ה | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: Ε | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α

P26 E6 graph_leaf
Coordinates: r63c02 ↔ r63c03 ↔ r64c03 ↔ r64c04 ↔ r65c04 ↔ r66c04 ↔ r67c04 ↔ r68c04 ↔ r69c04 ↔ r70c04 ↔ r71c04 ↔ r72c04 ↔ r73c04
Numeric: 5 | 1 | 1 | 4 | 3 | 4 | 4 | 1 | 1 | 1 | 1 | 1 | 1
Hebrew: ה | א | א | ד | ג | ד | ד | א | א | א | א | א | א
Greek: Ε | Α | Α | Δ | Γ | Δ | Δ | Α | Α | Α | Α | Α | Α


Independent cycle basis (repeated closing coordinate is an explicit revisit):
L1: r61c03 ↔ r61c02 ↔ r60c02 ↔ r59c02 ↔ r59c03 ↔ r59c04 ↔ r60c04 ↔ r61c04 ↔ r61c03; Greek Γ | Λ | ΚϚ | ΙΔ | Β | Δ | Α | Α | Γ
L2: r62c02 ↔ r61c02 ↔ r61c03 ↔ r62c03 ↔ r62c02; Greek ΙΘ | Λ | Γ | Α | ΙΘ
L3: r63c02 ↔ r62c02 ↔ r61c02 ↔ r61c03 ↔ r62c03 ↔ r63c03 ↔ r63c02; Greek Ε | ΙΘ | Λ | Γ | Α | Α | Ε

Measured relationships:

- E1 and E4 reach the single neighboring leaves r59c01 and r62c01. Their left neighbors are outside the source page, not zeros.
- E2,E3,E5,E6 connect to a common20-cell outer tree. Each has3 paths back to another core port and3 paths to leaves r58c04,r72c05,r73c04.
- Six reverse pairs of core-return routes are recorded rather than counted as independent confirmations.
- Four path pairs (P06/P07,P12/P13,P19/P20,P25/P26) have identical numeric/Greek sequences but different final coordinates: r72c05 versus r73c04. Both final cells are value1. Keep branch/coordinate provenance; do not reduce them to one endpoint.
- Outward versus reverse-container native final vectors differ for22 of26 routes under the declared comparison seed. Reverse-container versus full-glyph-reversal native final vectors happen to match in these26 trials; the actual instruction order remains different where a multi-glyph container is reversed.

The common lower branch includes distinct Alpha occurrences at r68c04,r69c04,r70c04,r71c04,r72c04 and the selected leaf r72c05 or r73c04. The fork is a graph relationship even though both source leaves encode Alpha. No repeated character is collapsed.

A live MCP relational response is pending. Original requests and responses are kept separately from locally computed data and independent checks. The MCP verification flag means structural checksum, not empirical correctness of an interpretation.

Reproduce into a fresh run path before this run exists: python -X utf8 -B WOWSignal/scripts/step03_six_lateral_exits.py
Validate existing records read-only except for its verification report: python -X utf8 -B WOWSignal/scripts/step03_six_lateral_exits_verify.py

Implementation issue: the first script invocation failed before producing run data because the preserved original_process import directory was not on the module path. The runner now explicitly adds that directory. A request-loading orchestration attempt also had a syntax error before execution and was retried. Neither failure reran a live reasoning request or changed source data.


## Occurrence-specific relationship pass

The first live reasoning step is step_1b8ef60fbc4400e3. Its readout retains all28 source cells, all26 routes, the common tail and a coordinate-complete return loop. Its generated critique correctly requests explicit incoming/action/output/remainder state per occurrence rather than only a role glossary.

The follow-up therefore instantiates490 separate primary-direction occurrence records across52 route evaluations. Each retains the exact incoming source/path context, prior same-role occurrences, current glyph and source container, resulting role-tagged provenance, branch alternatives, indexed perimeter references, and actual native register before/after vectors. These structured records describe measured arrival/source relationships and explicitly labeled BookII contextual applications. They do not invent a unique semantic transition function beyond the provided definitions.

For example, P25 outward reaches r68c04 Α with native state4 and sets it1. Subsequent Α occurrences at r69c04,r70c04,r71c04,r72c04 and r72c05 each preserve native state1 while advancing the distinct source occurrence and previous-origin reference. P26 has the same glyph/value sequence but ends at r73c04 instead. Inward traversal begins at the selected leaf, so r72c04 receives r72c05 or r73c04 as its prior origin, and r69c04 receives r70c04 rather than r68c04. All branch alternatives remain retained. Distinct source/context progression and unchanged native value are recorded separately.

The short E1 path P01 executes ΙΔ | Α outward and Α | ΙΔ inward. Under the declared independent all-ones seed, outward final state is1 and inward final state is2; both have events2. The terminal position of Α in the outward sequence accounts for the difference. E4 path P14 is ΙΘ | Β outward and Β | ΙΘ inward; both give the same full native vector[1,1,2,1,1,2,1,2] in these trials. No statement about general commutativity follows from those vectors.

boundary_register.json indexes all52 perimeter incidences, keyed by originating cell and neighboring coordinate. This retains duplicate incidences to the same source zero and the distinction between observed zeros and outside-page space.

The second live request receives the explicit tail occurrence records in both directions, all52 primary native initial/final vectors, and the original reasoning and critique. Its response will be appended unchanged. No source values or letters are replaced. Status: IN-PROGRESS.


## Completed live occurrence follow-up

The second live step is step_be6c499af4b04c46. The original reply and feedback are saved unchanged. Both live response texts follow below. The pass is IN-PROGRESS as research, with the requested six-exit tracing checkpoint recorded.

Measured result: the four right-side crossings do not lead to four independent streams. They join one20-cell outer tree and can reconnect to one another through12 directed core-return routes. The two left-side crossings lead to single leaf cells adjacent to the page edge. Six paired core-return paths are exact reversals of one another. Their distinct route/source identities remain recorded.

All8 long-tail routes share the lower sequence:
r64c03 Α | r64c04 Δ | r65c04 Γ | r66c04 Δ | r67c04 Δ | r68c04 Α | r69c04 Α | r70c04 Α | r71c04 Α | r72c04 Α | either r72c05 Α or r73c04 Α.
The two leaf alternatives encode the same value/glyph. Four distinct route pairs therefore have the same numeric/Greek stream while retaining different final coordinates. The coordinate graph preserves information that the character string alone does not identify.

At r63c03 the complete source neighbors are r62c03,r63c02,r64c03. From the tail, a return can enter the core at r63c02 or continue upward to r62c03. At r61c03 the neighbors are r61c02,r61c04,r62c03. A returning path can re-enter the core at r61c02 or continue toward the upper branch. Every such choice remains recorded rather than collapsed into a single reading.

BookII contextual applications and native operations remain distinct. The Alpha provenance ledger records the chosen source occurrence and its incoming history; it does not establish an additional source-authored meaning. The native recovered Alpha sets the trial's state register to1. At r68c04 it changes state4 to1 in the displayed outward tail trials; subsequent source Alphas still have distinct coordinates even when the register stays1. shared_tail_arrivals.json preserves actual intermediate vectors for all8 long-tail routes in both directions.

Correction retained separately from original MCP replies: r72c04 carries Alpha, not Gamma. Its neighbor frame is measured adjacency data. The second reply's phrase attributing that frame to Gamma is an interpretive overreach and is not adopted as source data. Whole-route native outputs are not automatically attributed to their last glyph; actual per-operation changes are available in transform_trials.json. Reverse-container trials restart from their declared all-ones seed and are not carried-state inverses of the outward execution.

No character, repetition, source coordinate, zero-boundary incidence, or outside-page distinction was removed. The pass records26 outward continuations,52 primary bidirectional trials,26 additional explicit full-glyph reversal comparisons,735 checked native operations, and490 concrete primary relational occurrence records. Three independent graph cycles and19 source-preserving corridors retain all30 component edges. Core re-entry and graph leaves remain typed scope boundaries, with onward connections/remainders retained.

Validation: an independent outer-tree BFS enumerates exactly the same26 paths; the corridor edge partition covers all30 links once; source values match the frozen grid; every native operation matches the original interpreter; every primary relation output equals the next occurrence's input in each of52 separate chains; all52 perimeter incidences retain zero versus outside-page types. No decoded sentence or additional source letters were inserted. No commit or push.
