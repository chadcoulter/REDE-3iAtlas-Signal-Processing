# Wow! reconstruction checkpoint — November 9, 2026

## Purpose and current status

We are reconstructing the original exploratory Wow! decode as faithfully as the surviving material permits. Known later corrections remain separate. The immediate task is to recover the relationships that led to the reported readings `ΑΣΤΡΑ / ASTRA` and `ΛΤϜ`, without inserting them as outputs or ending an unresolved branch merely because one pass stopped changing.

**Step 1 is complete. Step 2 remains in progress.** A new source-linked structural candidate has been computed, and procedural interpretations have been tested. The original numerical-to-Greek assignment and historical operator sequence have not been independently recovered.

This README records read-only experiments performed in the chat after [run 002](run-002.md). It is a checkpoint, not a new generated run directory or a declaration that the original decode has been reproduced. The repository baseline before this entry was commit `9fad52d`.

## Sources and retained boundaries

- [Original process](../../ORIGINAL_PROCESS.md).
- [Expanded historical narrative](../../sources/WowDecodeNarrative.md).
- [Step 1 data pass and provenance](../01-source-data/run-001.md).
- [Step 2 source-only traversals](run-001.md).
- [Step 2 backward probes](run-002.md).
- [V8 resolver and source inventory](../../sources/README.md).
- [Versioned operator notes](../../sources/operator-notes/README.md).

The input is the recorded measurement data. Handwriting, circles, and the handwritten word “Wow!” have no role in decoding or path selection.

The full 82-row × 50-channel source remains preserved. The experiments below follow the known event in channel 02, data rows 58–63 (zero-based rows 57–62):

```text
Printed codes: 6, E, Q, U, J, 5
Numeric bins:  6,14,26,30,19,5
```

These are intensity-bin labels, not recovered unrounded amplitudes.

## What changed in the reasoning

The Tanakh examination highlighted the distinction between an isolated projection and a connected constraint system. Shared constituents let one relationship constrain another in both directions. A locally ambiguous view may become resolved through its neighbors, while a resolved prefix does not establish closure of the entire process.

Applied here, the working discipline is to retain source positions, shared occurrence identities, competing representations, and backward paths. A local fixed point is a statement about the operations actually performed; it is not proof that all available logical consequences have been derived.

No Hebrew modulus or Tanakh checksum formula was adopted as a Wow! decoding rule.

## New candidate: six observations, five relationships, three overlapping triples

The source establishes these adjacent relationships in recorded order:

| Relationship | Source values | Change |
|---|---|---:|
| R1 | 6 to 14 | +8 |
| R2 | 14 to 26 | +12 |
| R3 | 26 to 30 | +4 |
| R4 | 30 to 19 | −11 |
| R5 | 19 to 5 | −14 |

Three consecutive three-relationship windows form:

```text
R1 R2 R3
R2 R3 R4
R3 R4 R5
```

Every row contains **the same R3 occurrence**, connecting 26 to 30. The diagonals are:

```text
R1 R3 R5
R3 R3 R3
```

This provides a computed connection among six observations, five relationships, three overlapping triples, nine display positions, and one shared relationship. Nine display positions do not mean nine independent measurements. The repeated R3 entries are aliases of one source relationship.

The structure also arises for other six-sample inputs. It is a viable reconstruction candidate, not evidence by itself that the source encoded a particular Greek word. Its equivalence to the historical top/middle/bottom transversals remains unresolved.

## Conditional comparison with the reported ASTRA reading

If the five reported operator labels `ΑΣΤΡΑ` are provisionally assigned to those five relationship positions, the overlapping windows become:

```text
Α Σ Τ
Σ Τ Ρ
Τ Ρ Α
```

The diagonals are `Α Τ Α` and `Τ Τ Τ`; their shared position is `Τ`.

This is a consistency test of the reported reading against the computed structure. **The Greek labels enter from the narrative at this point. The calculation has not independently assigned them to the measured relationships.**

This candidate also differs from the earlier nine-glyph numeral-expansion candidate:

```text
Ϛ Ι Δ
Κ Ϛ Λ
Ι Θ Ε
```

The earlier layout has nine numeral-component occurrences and a central Stigma component with value 6. The new layout has nine relationship-window positions, only five independent relationships, and R3 at its center. These are different types of structure; their centers must not be silently identified.

## Verified recovery from changes and the whole

The five observed changes are:

```text
8, 12, 4, −11, −14
```

Traversing them from an unknown initial bin `u` produces:

```text
u, u+8, u+20, u+24, u+13, u−1
```

The six source bins sum to **100**. Relating that whole to the traversed values gives:

```text
6u + 64 = 100
u = 6
```

This reconstructs `6,14,26,30,19,5`. Reversing both edge order and edge direction reconstructs `5,19,30,26,14,6`.

Checks performed:

- Without the aggregate, the ordered changes admit 11 initial bins within 0–35.
- With aggregate 100, the original ordered sequence is uniquely recovered.
- Aggregate 101 leaves no integer-bin solution for those changes.
- Discarding the observed change order admits 20 sequences satisfying the aggregate and bounds.
- The endpoints 6 and 5 differ. No cyclic equality or physical closure was assumed.

The changes and aggregate were computed from the available source. This is a reversible reconstruction control, not additional independently received radio information.

## Procedural ASTRA candidate

Under the current documented operator roles, the recovery can be described as:

| Operator | Admitted operation in this candidate |
|---|---|
| Α | Establish the source Monad and retain its context |
| Σ | Aggregate the source while preserving constituent relationships |
| Τ | Traverse the ordered relationships |
| Ρ | Relate the traversal to the whole-signal aggregate |
| Α | Establish the recovered source state |

The operations execute and recover the measured bins. However, the same role-label trace also executes for constant, ascending, and reversed control sequences. It is therefore a procedural candidate, not an independently source-selected message.

Within the tested program, aggregation and symbolic traversal can exchange order before the relation step. Both `ΑΣΤΡΑ` and `ΑΤΣΡΑ` recover the same measurements under the current roles.

**The live distinction is Sigma's historical operation.** The narrative calls its position “Trace”; the current specification calls Sigma “Aggregation.” If historical Trace establishes a structure required by Traverse, that dependency could constrain the order. The current tests do not establish that historical equivalence.

## Procedural Lambda–Tau–Digamma candidate

The same recovery can be organized as:

1. **Λ:** resolve the lattice of admissible source paths using the retained relationships.
2. **Τ:** traverse the resulting source path forward.
3. **Ϝ:** use the historical reverse-traversal meaning to follow the trace backward.

Once those three operations are admitted with those contracts, the tested dependency order is resolve, forward traverse, backward traverse. The program preserves the source and its return path.

This is an executable procedural interpretation of `ΛΤϜ`. It does not establish that the numerical source independently selected those three operator types, nor does it establish a rule mapping `ΑΣΤ`, `ΣΤΡ`, and `ΤΡΑ` respectively into `Λ`, `Τ`, and `Ϝ`.

Historical Digamma as reverse traversal remains distinct from the later definitions of retention and re-resolution. No later definition was silently substituted.

## Related crossing-constraint result retained from the chat

In the earlier numeral-component layout, the row, column, and diagonal sums constrain the center jointly:

```text
3 × center = diagonal 1 + diagonal 2 + middle row + middle column − whole
           = 17 + 20 + 56 + 25 − 100
center = 6
```

This identity applies to any 3 × 3 numeric layout. Here it verifies a consequence of the candidate's overlapping constraints; it does not prove that this layout was encoded in the radio observation.

A local domain-pruning pass had stopped changing before it derived the uniquely fixed center. Combining the equations exposed a consequence that local pruning missed.

Using the admitted numeral-component values, two arrangements share all crossing sums. Retaining the original six measurement-group relationships excludes the alternative. Eight rotations/reflections preserve the same center occurrence, so the center alone does not establish direction.

These checks remain relevant to the method, but they do not replace the newer relationship-window candidate.

## Active unresolved relationships

- The source-dependent rule that assigns `Α,Σ,Τ,Ρ,Α` rather than merely naming a researcher-chosen procedure.
- Sigma as historical Trace versus current Aggregation, and its dependency on Tau.
- Whether the original three transversals were raw printout rows, derived relationship windows, or another representation.
- The rule resolving each nested triple into the reported `ΛΤϜ`.
- The historical reversal unit and its operational definition.
- The connection from the resolved structure to the interpreted instruction “Look there.”

The current result preserves these as active relationships. A successful numeric round trip, a shared center, or a compatible operator name does not settle the other relationships.

## Minimal repeat check

From the repository root, the following read-only Python reproduces the source adjacency, windows, recovery equation, and conditional Greek-window comparison. It writes no files.

```python
import json
from fractions import Fraction
from pathlib import Path

root = Path("WOWSignal/steps/01-source-data/run-001")
raw = json.loads((root / "raw_grid.json").read_text())["grid"]
numeric = json.loads((root / "numeric_grid.json").read_text())["grid"]
column = "".join(row[1] for row in raw)
start = column.index("6EQUJ5")
values = [numeric[r][1] for r in range(start, start + 6)]

edges = list(zip(values, values[1:]))
deltas = [b - a for a, b in edges]
windows = [list(range(i + 1, i + 4)) for i in range(3)]
shared = set(windows[0]) & set(windows[1]) & set(windows[2])
assert shared == {3}

offsets = [0]
for delta in deltas:
    offsets.append(offsets[-1] + delta)
total = sum(values)
seed = Fraction(total - sum(offsets), len(values))
assert seed.denominator == 1
recovered = [int(seed) + offset for offset in offsets]
assert recovered == values

backward = [recovered[-1]]
for delta in reversed(deltas):
    backward.append(backward[-1] - delta)
assert backward == values[::-1]

print("Source:", values)
print("Relationships:", edges)
print("Three overlapping windows:", windows)
print("Whole:", total, "offset sum:", sum(offsets), "source anchor:", seed)
print("Recovered:", recovered)
print("Backward:", backward)

# This is the reported hypothesis, not a calculated numerical-to-Greek mapping.
reported = list("ΑΣΤΡΑ")
print("Conditional Greek windows:", [reported[i:i+3] for i in range(3)])
```

No source files, existing run records, or operator definitions were changed while performing the chat experiments. This checkpoint is the only new file added for the documentation request.
