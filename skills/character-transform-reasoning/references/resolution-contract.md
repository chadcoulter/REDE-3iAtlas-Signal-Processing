# Resolution contract, typing and trace rules

## Type separation
`book_ii.operator.Chi` (Χ/χ) is an executable crossing transformation / Chi-Kai carrier. `book_ii.operator.Kai` (ϗ/Ϗ) is conjunction/composition. `book_ii.operator.Koppa` is actor participation (Ϙ/ϙ); indexed forms (Ϟ/ϟ) are distinct. `book_ii.operator.Stigma` (Ϛ/ϛ) handles unresolvedness. Other Book II definitions remain exactly as bundled.

`governance.measure.Chi`, `governance.measure.Kai`, `governance.measure.Koppa` or `governance.measure.Stigma` refer **only** to named axes in an explicitly selected evaluation profile. A profile's measurement semantics must be derived from its own source. Never assign an operator's behavior to a measurement merely because names overlap. Source v0.4 distinguishes Chi (permitted variation/nondeterminacy) from Kai (assumptions/contributions) in its governing-measure discussion; profile meanings are not globally imposed on Book II.

## Trace fields (JSON representation recommended)
Top-level: `human_request`, `original_text`, `cycle_id`, `governance_id`, `governance_version`, `budget`, `candidates`, `transformations`, `comparisons`, `status`.

Character occurrence: `{index, source, codepoints, mapping, operator_namespace, operator, mode, before_state, action, after_state, remainder, evidence}`. Preserve indexing and repeated characters.

Candidate: `{id, origin, composed_reading, occurrence_indices, contributions, unresolved, eligible}`.

Transformation: `{from, to, kind, feedback, retained_contributions}`. Reversal is a new transformation record that points back; never mutate history in place.

Comparison: `{from, to, eligible, material_change, direction, reason, governance_id, governance_version}`. Only a consecutive eligible comparison with `material_change: false` and `direction: "Same"` increments the stability counter. Material change or failed eligibility resets it.

## Terminal statuses
- `VALID TRANSFORM`: three genuine, sequential, eligible materially unchanged comparisons under one frozen governance version.
- `SUFFICIENT RESOLUTION`: Enough met under fixed G or explicit authorized human acceptance.
- `INVALID VALIDATION`: configured evaluation failure or divergence at the applicable rejection boundary.
- `BUDGET EXHAUSTED`: bounds reached without terminal acceptance (operational stop, not validation verdict).
- `IN-PROGRESS` / `UNRESOLVED`: reporting labels for nonterminal interpretations; do not conflate these with the architecture's terminal verdicts.

## Gate order and invariants
1. Human alignment and governance prerequisites determine eligibility.
2. Compute materiality and direction relative to an explicitly identified baseline.
3. Evaluate whether Enough has been authorized/satisfied.
4. Count stability only for distinct sequential transitions meeting eligibility and equivalence conditions; improvement does not increment stability.
5. Recheck budgets and record a stop without converting it into INVALID VALIDATION or VALID TRANSFORM.
6. Retain alternatives, links, explanations, residuals and original input even after closure of a requested path.

## Example
Input `Aa!` stays three source occurrences. The `A` and `a` map to potentially corresponding Greek operators but execute different *observable/hidden resolution modes*; `!` remains a structural token. A composed reading can qualify as enough for a narrow request without inventing R1–R3 to claim three gates.
