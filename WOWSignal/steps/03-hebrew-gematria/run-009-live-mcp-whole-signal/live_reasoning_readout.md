**The grid supports several scoped start/end relationships, but it does not establish a unique message beginning or ending.** Applying Chad Coulter’s Book II definitions preserves those candidates together with their neighboring continuations. The strongest distinction is between a boundary of a chosen traversal and a delimiter evidenced by the source.

**1. Whole-source accounting and encoding**

The source scope is **r01–r82 × c01–c50: 4,100 numeric containers**. Coordinates below are one-based. From the supplied histogram, the calculated totals are 1,112 nonzero containers, 2,988 preserved zero containers, and a numeric sum of 1,487. These calculations use the supplied summary; they are not an independent verification of that summary.

The complete encoding vocabulary required by this grid is:

| Numeric container | Greek encoding | Book II operation sequence: resolve the observable… |
|---|---|---|
| 0 | Preserved `0` structural token | No Greek numeral operator assigned |
| 1 | Α | Origin |
| 2 | Β | Branch |
| 3 | Γ | Boundary frame / transform operator |
| 4 | Δ | Change |
| 5 | Ε | Threshold |
| 6 | Ϛ | Unresolvedness |
| 7 | Ζ | Link |
| 14 | ΙΔ | Instance; change |
| 19 | ΙΘ | Instance; constraint |
| 26 | ΚϚ | Context; unresolvedness |
| 30 | Λ | Lattice resolution |

Thus the nonzero encoding contains **1,115 glyph occurrences within 1,112 containers**. Including one structural record for each zero gives 4,103 occurrence/token records, still belonging to exactly 4,100 original containers.

`14 = ΙΔ = 10 + 4`; the Hebrew additive representation `יד` likewise remains **one numeric-14 container**. Neither representation creates two source cells. Uppercase specifies **how to resolve the observable**; it does not establish that a cell’s source meaning is “origin,” “constraint,” or another operator concept.

**2. Coordinate-specific execution: the c02 concentration**

Select this vertical scope because it contains all three multi-letter values and the maximum value, independently of any desired phrase:

`r57c02=0 | r58c02=6 | r59c02=14 | r60c02=26 | r61c02=30 | r62c02=19 | r63c02=5 | r64c02=0`

Each row below is a distinct glyph occurrence. Actions are Book II applications to the evolving analytical relation; the retained remainder prevents that application from replacing the source.

| Occurrence | Source container / glyph | Operator action on the current relation | Resulting relation / retained remainder |
|---|---|---|---|
| r58c02.1 | 6 / Ϛ | Resolve observable unresolvedness concerning the proposed entry after r57c02=0. | Retain 6, its coordinate, the preceding zero, and uncertainty about entry direction. |
| r59c02.1 | 14 / Ι | Resolve the observable instance of container r59c02 within the continuing vertical scope. | Retain the whole value 14; Δ remains pending within this same container. |
| r59c02.2 | 14 / Δ | Resolve observable change relative to the preceding scoped state, without splitting 14. | Retain Ι and Δ in order, value 14, and lateral neighbors r59c01=1 and r59c03=2. |
| r60c02.1 | 26 / Κ | Resolve observable context for this instance’s relation to its neighbors. | Retain whole value 26, preceding 14, following 30, and pending Ϛ. Κ is Kappa, not Koppa. |
| r60c02.2 | 26 / Ϛ | Resolve observable unresolvedness remaining within that contextual relation. | Retain both Κ and Ϛ, value 26, and r60c01=0 / r60c03=0; no delimiter follows from unresolvedness. |
| r61c02.1 | 30 / Λ | Resolve observable lattice relationships at this position. | Retain 30’s vertical links and the lateral connection r61c03=3; lattice resolution does not terminate the path. |
| r62c02.1 | 19 / Ι | Resolve the observable instance at r62c02 in the continuing relation. | Retain whole value 19 and pending Θ; keep it distinct from r59c02’s Ι occurrence. |
| r62c02.2 | 19 / Θ | Resolve observable constraints on this scoped candidate, including adjacency and container integrity. | Retain ΙΘ, value 19, and lateral neighbors r62c01=2 / r62c03=1. |
| r63c02.1 | 5 / Ε | Resolve the observable threshold between this nonzero vertical run and r64c02=0. | Retain the zero below and the continuing lateral relation r63c03=1; a threshold is not terminal closure. |

Observed arithmetic for this scope is:

`6 + 14 + 26 + 30 + 19 + 5 = 100`.

The alternative first-three-container calculation is `6 + 14 + 26 = 46`. The contextual input `[6,14,1]` sums to 21, but **that is not this vertical triple**: the supplied grid has r60c02=26. Substituting 1 there would manufacture a source sample.

**3. Actual boundary traces and their alternatives**

| Scope and actual neighbors | Per-occurrence actions for additional nonzero cells | Boundary relationship supported |
|---|---|---|
| Top edge: r01c03=0, **r01c04=2**, r01c05=0; below, r02c04=1 | r01c04 Β: resolve the observable branch between available spatial continuations. r02c04 Α: resolve the observable origin of that distinct instance, retaining its link above. | r01c04 is the first nonzero cell in forward row-major order and a horizontal singleton. It has a downward nonzero continuation. Its upper neighbor is outside the page, not an observed zero. |
| Horizontal run: r59c01–c05 = **1,14,2,4,0** | r59c01 Α: resolve this scoped origin while retaining the page edge. r59c02 Ι then Δ: retain both actions detailed above. r59c03 Β: resolve the observable branch while retaining links to c02/c04 and r61–r64 through other cells. r59c04 Δ: resolve observable change while retaining c03 and the zero at c05. | The run has a page-limited left edge and a zero-bounded right edge. Above c04 is r58c04=2; below is r60c04=1. The rightmost run cell therefore continues vertically. |
| Vertical scope exit: r63c02=5, r64c02=0; alongside, **r63c03=1, r64c03=1, r64c04=4** | r63c03 Α: resolve this continuation’s observable origin, retaining its connection to Ε at c02. r64c03 Α: resolve a separate instance’s origin, retaining the vertical connection. r64c04 Δ: resolve observable change, retaining its horizontal connection and r65c04=3 below. | r63c02 ends the selected c02 run, but not the connected nonzero structure. The path continues through c03 and c04. |
| Bottom edge: r82c43=0, **r82c44=1**, r82c45=0; above, r81c44=0 | r82c44 Α: resolve the observable origin of this isolated instance while retaining all observed zero neighbors and the lower page edge. | This is the last nonzero cell in forward row-major order and a four-neighbor singleton. Its isolation does not establish an end-of-message marker. |

Zeros in these traces retain their coordinates and adjacency. A zero separates nonzero runs in a chosen direction; it does not erase the relation between the containers on either side.

**4. Reverse traversal preserves two different operations**

For the selected c02 scope:

| Operation | Ordered, container-preserving encoding |
|---|---|
| Forward containers, canonical glyph order | `[Ϛ] [ΙΔ] [ΚϚ] [Λ] [ΙΘ] [Ε]` |
| Reverse containers, canonical glyph order retained | `[Ε] [ΙΘ] [Λ] [ΚϚ] [ΙΔ] [Ϛ]` |
| Reverse glyphs inside each container, forward containers retained | `[Ϛ] [ΔΙ] [ϚΚ] [Λ] [ΘΙ] [Ε]` |
| Reverse containers and their internal glyphs | `[Ε] [ΘΙ] [Λ] [ϚΚ] [ΔΙ] [Ϛ]` |

The reversed internal sequences remain attributed to their original containers. For example, `[ΔΙ]` is an explicitly reversed traversal of r59c02’s encoding, not a replacement canonical encoding of 14.

Book II reconsideration, **Ͻ**, can reopen the traversal choice while retaining its history; accounted reversal, **Ͼ**, can retain the changed order as an explicit analytical condition. These are invoked analytical operators, not additional glyphs recovered from the numeric source.

**5. Boundary alternatives compatible with the full grid**

- **Page/traversal bounds:** Forward row-major traversal begins at r01c01=0 and ends at r82c50=0. Its first and last nonzero occurrences are r01c04 and r82c44. Reverse traversal exchanges those roles. These are consequences of the chosen enumeration.
- **Spatial run bounds:** r58c02 and r63c02 delimit the maximal nonzero c02 run between r57c02=0 and r64c02=0. Either can be a scoped entry under opposite traversal directions. Lateral connections prevent treating those run bounds as component bounds.
- **Connected-region bounds:** The supplied summary places r58c02–r63c02 in the same component and reports 395 four-neighbor nonzero components, including 230 singletons. Component boundaries remain useful spatial distinctions, but the grid supplies no rule selecting one component as the message.
- **Computational cycles:** The reported 479 fixed-point, 62 period-2, and 251 unrepeated branches total 792 experimental branches. Their classification depends on the all-ones seeds, eight-register implementation, and 100-pass horizon. Fixed points and cycles do not establish source endpoints; “unrepeated after 100 passes” does not establish permanent nonperiodicity.
- **Actual message delimiters:** No supplied delimiter rule distinguishes one of these page edges, zero transitions, values, or cycles as a message delimiter. A delimiter interpretation remains conditional on additional evidence. A unique start/end pair is therefore unresolved.

Book II roles remain conceptual relational definitions throughout; they are not identified with the recovered machine’s registers. The MCP `verified` field is a **structural checksum**, not external verification of the interpretation.

**6. Partial closure and a concrete further comparison**

Partial closure can retain the finding **“r58c02–r63c02 is the maximal nonzero vertical run at c02, bounded by the observed zeros at r57c02 and r64c02”** together with its nine glyph actions, reverse alternatives, and lateral exits. That resolves the requested local relationship while leaving message order, component selection, and the rest of the grid open. It does not insert source **ς**, nor claim terminal closure of the whole Set.

A concrete next comparison is to enumerate **every maximal horizontal and vertical nonzero run** in the complete grid, comparing endpoint zeros/page edges, lateral nonzero exits, sums, and forward/reverse container signatures. Include the c02 candidate and r59c01–c04 by the same rule. Test how often their boundary features recur elsewhere before assigning either a delimiter role. This comparison preserves all zero bins and repeated occurrences and requires no phrase selection, generated sentences, or hidden samples.
