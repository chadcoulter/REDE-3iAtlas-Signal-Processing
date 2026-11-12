# WOW! Signal — Alpha Return Findings

**Progress captured: November12,2026.** Research remains in progress. This entry collects the relationships identified through run011 using the live Unified VRE harness and Chad Coulter’s character-transform-reasoning skill.

## What we found

The return paths preserve distinct origins while sharing execution states. Traversal order changes what Gamma records; Alpha can reset one register while retaining another; and the shared return can enter four different core cells with different recorded results.

These are concrete relationships tied to original coordinates and recorded operations. They provide the next connections to follow without constructing a sentence from the codes.

## 1. Two Alpha origins share a path without becoming one source cell

The endpoints are **r72c05 Α** and **r73c04 Α**, both numeric1 / Hebrew א.

They meet spatially at r72c04, then share11 positions through r63c03:

```text
[r72c05 Α OR r73c04 Α]
 ↔ r72c04 Α
 ↔ r71c04 Α
 ↔ r70c04 Α
 ↔ r69c04 Α
 ↔ r68c04 Α
 ↔ r67c04 Δ
 ↔ r66c04 Δ
 ↔ r65c04 Γ
 ↔ r64c04 Δ
 ↔ r64c03 Α
 ↔ r63c03 Α
```

For each of the four core destinations, both origins have identical numeric streams, Greek instruction streams, and native before/after vectors. Their initial coordinates and complete arrival histories remain different.

**Relationship retained:** the numeric trace alone does not distinguish these two source origins. The coordinate and provenance records do. Every repeated Alpha remains a separate occurrence.

## 2. Reversal changes the condition Gamma records

The same source Gamma, r65c04, receives different states according to the surrounding Delta order.

```text
Outward order:
r64c04 Δ ↔ r65c04 Γ ↔ r66c04 Δ ↔ r67c04 Δ

Return order:
r67c04 Δ ↔ r66c04 Δ ↔ r65c04 Γ ↔ r64c04 Δ
```

| Traversal | State when Γ is encountered | Constraints after Γ |
| --- | ---: | ---: |
| Outward | 2 | 2 |
| Return | 3 | 3 |

The return encounters two Delta operations before Gamma. In the recorded native implementation, Gamma copies the current state’s low byte into constraints. **Order changes the retained value at the same coordinate.**

## 3. Alpha changes state while a prior condition survives

During the return:

| Source operation | State before | State after | Constraints after |
| --- | ---: | ---: | ---: |
| r67c04 Δ | 1 | 2 | 1 |
| r66c04 Δ | 2 | 3 | 1 |
| r65c04 Γ | 3 | 3 | 3 |
| r64c04 Δ | 3 | 4 | 3 |
| r64c03 Α | 4 | 1 | 3 |
| r63c03 Α | 1 | 1 | 3 |

**The state reset does not reset all recorded conditions.** Constraints3 survive the Alpha at r64c03. The contextual BookII reading follows an origin occurrence reached with retained arrival conditions. Endpoint history is retained separately in the provenance records; it is not an additional distinction inside the equal register vectors.

## 4. The shared return has four different core outcomes

The routes branch from r63c03 through the following entries:

| Core coordinate | Intact Hebrew / Greek container | State | Constraints | Context | Events |
| --- | --- | ---: | ---: | ---: | ---: |
| r63c02 | ה / Ε | 1 | 3 | 1 | 1 |
| r62c02 | יט / ΙΘ | 1 | 4 | 1 | 2 |
| r61c02 | ל / Λ | 0 | 1 | 1 | 1 |
| r59c02 | יד / ΙΔ | 3 | 1 | 2 | 2 |

Relations, observations, unresolved, and target remain1 in these inherited traces.

- **Ε:** the direct entry retains constraints3 without another register change.
- **ΙΘ:** instance increments events to2; the following constraint operation increments constraints to4. Both glyphs remain inside the original numeric19 container.
- **Λ:** the route first reaches r61c03 Γ, changing constraints3 to1. At the core’s Lambda, state1 XOR relations1 gives state0.
- **ΙΔ:** the upper route retains two separate Alpha occurrences at r61c04 and r60c04, then reaches r59c04 Δ and r59c03 Β. State reaches2 and context2 before the intact numeric14 container’s Ι increments events and Δ changes state to3.

Each destination’s result is identical for the two endpoint origins. The four destination relationships remain different.

## 5. Re-entry retains onward relationships

The returns remain connected to the core:

- r63c02 retains r62c02.
- r62c02 retains r61c02, r63c02, and the r62c01 branch.
- r61c02 retains r60c02 and r62c02.
- r59c02 retains r58c02, r60c02, and the r59c01 branch.

The upper r58c04 branch remains available at r59c04. Graph leaves, source-page edges, scope returns, and whole-message boundaries remain separately recorded.

## Evidence and process

This capture reuses **8 return routes,126 occurrence records,11 shared positions, and4 core re-entries** from run011. Native comparisons inherit run010’s explicitly declared independent all-ones initializations. No new decode pass, seed, machine execution, source letter, or sentence was introduced for this report.

Measured coordinates, source values, and native register changes are recorded separately from contextual BookII interpretation. The live MCP’s structural checksum flag is not substituted for those checks.

Source evidence:

- `run-011-alpha-endpoint-return/pair_comparisons.json`
- `run-011-alpha-endpoint-return/shared_tail.json`
- `run-011-alpha-endpoint-return/core_reentries.json`
- `run-011-alpha-endpoint-return/inherited_orientation_comparison.json`
- `run-011-alpha-endpoint-return/inherited_relational_occurrences.json`
- `run-011-alpha-endpoint-return/verification.json`
- `run-011-alpha-endpoint-return/response-live-return.json`

The next proposed work is to follow the onward core connections with each arrival history retained. This capture does not execute that pass.

## File changes for this capture

- Added this focused findings report.
- Added `run-011-alpha-endpoint-return/findings-capture/harness-response.json`.
- Added `run-011-alpha-endpoint-return/findings-capture/manifest.json`.
- Appended this report to `run-001/hebrew_streams_updated.txt`.

Prior source and run evidence remain unchanged. No commit or push.
