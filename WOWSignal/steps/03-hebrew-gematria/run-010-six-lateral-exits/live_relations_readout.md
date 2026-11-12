Applied Chad Coulter’s [character-transform-reasoning skill](C:/Users/ccoulter/.codex/skills/character-transform-reasoning/SKILL.md), using your supplied Book II as the glyph authority. This is a relational transform record, without sentence construction from the codes.

**Numeric observations.** The supplied component contains 28 vertices and 30 edges; its cycle rank is \(30-28+1=3\). Removing the six-cell core `r58..63c2` leaves two isolated cells and a 20-cell tree. The 26 outward routes comprise 12 core re-entries and 14 graph-leaf paths. These are scope boundaries, not message EOF.

The perimeter records 50 observed-zero incidences and two outside-page, unobserved incidences. Repeated references to one zero remain separate boundary incidences. Neither zero nor unobserved space supplies a Greek closure operator.

**Coordinate/container register.** Labels below abbreviate coordinates only. Every row remains one source cell; semicolons separate operator occurrences inside that cell.

| Label | [row,channel] | Value | Hebrew | Greek / occurrence order |
|---|---|---:|---|---|
| C0 | [58,2] | 6 | ו | Ϛ |
| C1 | [59,2] | 14 | יד | Ι;Δ |
| C2 | [60,2] | 26 | כו | Κ;Ϛ |
| C3 | [61,2] | 30 | ל | Λ |
| C4 | [62,2] | 19 | יט | Ι;Θ |
| C5 | [63,2] | 5 | ה | Ε |
| a | [59,1] | 1 | א | Α |
| b | [59,3] | 2 | ב | Β |
| c | [59,4] | 4 | ד | Δ |
| d | [58,4] | 2 | ב | Β |
| e | [60,4] | 1 | א | Α |
| f | [61,4] | 1 | א | Α |
| g | [61,3] | 3 | ג | Γ |
| h | [62,1] | 2 | ב | Β |
| i | [62,3] | 1 | א | Α |
| j | [63,3] | 1 | א | Α |
| k | [64,3] | 1 | א | Α |
| l | [64,4] | 4 | ד | Δ |
| m | [65,4] | 3 | ג | Γ |
| n | [66,4] | 4 | ד | Δ |
| o | [67,4] | 4 | ד | Δ |
| p | [68,4] | 1 | א | Α |
| q | [69,4] | 1 | א | Α |
| r | [70,4] | 1 | א | Α |
| s | [71,4] | 1 | א | Α |
| t | [72,4] | 1 | א | Α |
| u | [72,5] | 1 | א | Α |
| v | [73,4] | 1 | א | Α |

**Process and evolving context.** For each occurrence, retain `(route, direction, coordinate, container, glyph position, preceding relation, alternatives, remainder)`. Apply the next glyph to the relation produced by the preceding occurrence. Uppercase tells **how to resolve the observable**.

The following actions specify this application of Book II; they are conceptual operations, not asserted machine instructions:

- **Ι:** resolve the current relation’s particular instance; retain its source and alternatives.
- **Δ:** resolve change relative to that preceding relation; retain before/after distinctions.
- **Κ:** resolve the context governing the relation reached so far.
- **Ϛ:** resolve observable unresolvedness within that context, retaining unaccounted distinctions with provenance. It is Stigma, never Digamma.
- **Λ:** resolve the lattice relationships currently brought into scope, retaining unused connections.
- **Θ:** resolve constraints upon the instance just identified, preserving unresolved applicability.
- **Ε:** resolve the threshold between the current scope and its continuation.
- **Β:** resolve the current branching relationship, retaining every alternative.
- **Γ:** resolve the boundary frame/transform governing the accumulated relation.
- **Α:** resolve the origin of the relation now reached, retaining its incoming connection. Each occurrence adds its own provenance obligation; it does not erase previous origins.

Thus C1 executes **instance, then change of that instance’s relation**; C2 executes **context, then unresolvedness within that context**; C4 executes **instance, then its constraint**. Their glyphs never become separate graph vertices.

**Complete bidirectional route ledger.** Juxtaposition means successive adjacent containers. Define `Tu = klmnopqrstu` and `Tv = klmnopqrstv`. Each row’s inward counterpart is its exact reversed label list, retaining internal container order.

| Exit | Routes and ordered containers |
|---|---|
| E1 | P01 `C1 a` |
| E2 | P02 `C1 b c d`; P03 `C1 b c e f g C3`; P04 `C1 b c e f g i C4`; P05 `C1 b c e f g i j C5`; P06 `C1 b c e f g i j Tu`; P07 same prefix + `Tv` |
| E3 | P08 `C3 g f e c d`; P09 `C3 g f e c b C1`; P10 `C3 g i C4`; P11 `C3 g i j C5`; P12 `C3 g i j Tu`; P13 same prefix + `Tv` |
| E4 | P14 `C4 h` |
| E5 | P15 `C4 i g C3`; P16 `C4 i g f e c d`; P17 `C4 i g f e c b C1`; P18 `C4 i j C5`; P19 `C4 i j Tu`; P20 same prefix + `Tv` |
| E6 | P21 `C5 j i g C3`; P22 `C5 j i g f e c d`; P23 `C5 j i g f e c b C1`; P24 `C5 j i C4`; P25 `C5 j Tu`; P26 same prefix + `Tv` |

**Outbound and back.**

- **E1/P01:** `[59,2](ΙΔ) ↔ [59,1](Α)`. Outbound, resolve instance/change, then that changed relation’s origin. Inward, resolve origin first, then its returning instance/change. `[58,1]` and `[60,1]` are recorded zeros; `[59,0]` is unobserved outside-page space.
- **E2/P02–P07:** C1’s instance/change enters b’s branch and c’s change. At c, preserve d versus e. P02 is exactly `[59,2](ΙΔ) ↔ [59,3](Β) ↔ [59,4](Δ) ↔ [58,4](Β)`. The other routes resolve separate origins at e and f, then g’s boundary frame. P03 re-enters C3’s lattice; P04 reaches i’s origin then C4’s instance/constraint; P05 additionally resolves j’s origin then C5’s threshold. P06/P07 retain both tail leaves. Backward, these endpoint relations successively supply the context for g, f, e, c, b, and C1; returning does not undo their operations.
- **E3/P08–P13:** C3’s lattice enters g’s boundary frame. Its upper continuation resolves f-origin, e-origin, c-change, then d-branch (P08) or b-branch and C1-instance/change (P09). Its lower continuation resolves i-origin, reaching C4 (P10), or j-origin and C5 (P11), or the tail (P12/P13). Inward, the selected continuation is retained when g resolves its boundary and C3 resolves the returning lattice.
- **E4/P14:** `[62,2](ΙΘ) ↔ [62,1](Β)`. Outbound resolves instance, its constraint, then branching; inward resolves branching before the returning instance/constraint. `[61,1]` and `[63,1]` are zeros; `[62,0]` remains unobserved.
- **E5/P15–P20:** C4’s constrained instance reaches i-origin. The upper branch reaches g-boundary: C3-lattice (P15), the upper leaf (P16), or C1 (P17). The lower branch reaches j-origin: C5-threshold (P18) or either tail leaf (P19/P20). Inward, i resolves origin against the arriving upper/lower history before C4 resolves its instance/constraint.
- **E6/P21–P26:** C5’s threshold reaches j-origin. Upward, i-origin then g-boundary reaches C3 (P21), d (P22), or C1 (P23); i also reconnects C4 (P24). Downward, P25/P26 share the tail. Inward, j resolves origin against the selected arriving history before C5 resolves the return threshold.

Graph junctions c, g, i, j, t retain their full-component degrees of three; topology supplies branching even where the glyph is not Β.

**Shared tail occurrence record.** P06/P07, P12/P13, P19/P20, P25/P26 join at j `[63,3]`. Each separately executes:

`[64,3] Α; [64,4] Δ; [65,4] Γ; [66,4] Δ; [67,4] Δ; [68,4] Α; [69,4] Α; [70,4] Α; [71,4] Α; [72,4] Α;` then `[72,5] Α` **or** `[73,4] Α`.

Each Alpha resolves origin relative to its accumulated preceding history. Inward, the leaf-origin precedes t-origin, s-origin, r-origin, q-origin, p-origin, o-change, n-change, m-boundary, l-change, k-origin, j-origin. Identical glyph sequences preserve distinct coordinates and endpoints.

**Coordinate-complete return loop.** P03 closes geometrically through the original core spine:

`[59,2]ΙΔ ↔ [59,3]Β ↔ [59,4]Δ ↔ [60,4]Α ↔ [61,4]Α ↔ [61,3]Γ ↔ [61,2]Λ ↔ [60,2]ΚϚ ↔ [59,2]ΙΔ`.

This is L1 with changed starting point/orientation. The final C1 occurrence acts on the returned context. L2 and L3 preserve their supplied spine connections; other return cycles compose through those actual edges. C0 `[58,2]Ϛ` remains attached to C1 and outside this loop.

**Comparison record.** Forward replay preserves the ledger order. Container reversal preserves `ΙΔ`, `ΚϚ`, `ΙΘ`; full glyph reversal instead gives `ΔΙ`, `ϚΚ`, `ΘΙ`, a distinct trial. Reverse traversal is neither an inverse operator nor evidence of restored state.

Independent native all-ones trials have no supplied outputs here; none were executed in this response. They cannot establish original source states. The conceptual record retains all boundaries, alternatives, and re-entries. No ς occurs; direction, message boundaries, source-zero meaning, outside-page continuation, and remaining relational resolution stay open.
