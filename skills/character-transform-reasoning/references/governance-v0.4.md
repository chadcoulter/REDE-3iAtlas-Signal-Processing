# Governance-Driven Resolution Lattice v0.4 — Book II adaptation

Source: Chad Coulter, *Governance-Driven Resolution Lattice v0.4*; exact source retained as `governance-v0.4-source.docx`. This reference is an implementation mapping, not a replacement for the source text.

## Separation of concerns
- Human request **H**: intended purpose; humans govern alignment, allowable pivots, Enough acceptance and changes between cycles.
- Governance **G = (C, W, M, B)**: criteria, relative weights/priorities, measures/equivalence/materiality rules, and bounds. Freeze G during each cycle.
- **Generator**: produces transformed readings (candidate Rn) from a sequence of Book II operators, or revises, regenerates or combines candidates in response to feedback.
- **Evaluator**: applies only frozen G; measures candidate fit, material ambiguities, direction and eligibility. Evaluation does not rewrite operator definitions or governance.
- **Resolver**: manages candidate selection, relation traversal, feedback, reversal, stability, closure/Enough and stopping.

## Lattice records
- Node: candidate reading with occurrence trace and relational state.
- Transformation edge: edit / fresh regeneration / correction / recombination / reversal; index marks progression, not necessarily a parent edit.
- Contribution edge: links source characters, intermediate operators, assumptions, context, participants, witnesses and provenance to resulting claims.
- Retain alternate paths. The document's *lattice* is a connected resolution structure; do not promise formal mathematical meet/join unless implemented.

## Interpretation rules
- **Equivalence**: two candidates may differ in wording or glyph mappings yet be equivalent for H under G. Preserve the difference and provenance even if equivalent.
- **Materiality**: ask whether an ambiguity requires further resolution *for this request*. An unimportant orthographic variant may remain open; a change in actor, scope or closure may be material.
- **Direction**: Better/Same/Worse is governance-relative, can reflect multidimensional tradeoffs; do not overwrite mixed outcomes with a made-up aggregate score.
- **Reversal**: reopen a prior path, relocate its contributions, and maintain accounted residue; do not delete prior states.
- **Enough**: sufficient coherence for H according to G and any authorized human decision; may stop before stability verification.
- **Three-gate stability**: the concrete architecture establishes VALID TRANSFORM after three consecutive eligible Same transitions Rn ≡G Rn+1 ≡G Rn+2 ≡G Rn+3. Do not treat its optional implementation rule as a universal axiom of Book II.
- **Budget**: track iterations, cycles, compute or other configured limits; exhaustion is its own operational stop, not a successful validation.
- **Cohesion / Validity / Spirit**: injectable governing measures, not automatic numerical requirements or substitutes for the Book II transforms.
- **Collatz-relative measures**: optional measurements only; never make them a required part of transform reading.

## Canonical cycle
1. Register exact source H and freeze G.
2. Segment and execute Book II transforms, persist R0 and occurrences.
3. Generate alternative interpretations as supported by sequence/context.
4. Evaluate eligible candidates; judge materiality, equivalence, direction, and provenance.
5. Issue feedback and optionally revise/regenerate/reverse; append edges.
6. Test Enough, three eligible unchanged transitions, validation failure, and budget separately.
7. Return status and reading with inspectable trace and unresolved contributions.

For no actual iterative generation, report a composed reading with SUFFICIENT RESOLUTION only if Enough is truly satisfied; otherwise report IN-PROGRESS / UNRESOLVED, not fictitious stability.
