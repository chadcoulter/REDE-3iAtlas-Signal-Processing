**The supplied full-grid comparisons support `[58,2]..[63,2]` as a scoped start/end candidate: a maximal vertical run that also becomes an entire connected component at thresholds 4 and 5. They do not establish a unique message boundary or direction.** Expanding Γ’s frame to the 28-cell component changes which relationships are internal and which constitute its boundary.

**Computed boundary facts — from the supplied results**

These are reported input computations, not an independent rerun against the raw grid. The retained source comprises 82×50 = **4,100 containers**, including **1,112 nonzeros and 2,988 zeros**, totaling **1,487**. The supplied tokenizer check independently regrouped all Hebrew numeral containers into their source values. Greek 6 uses **Ϛ**, not Ϝ; multi-glyph encodings remain single numeric containers.

The uniform horizontal/vertical enumeration reports **1,416 maximal nonzero runs**: 664 vertical and 752 horizontal.

| Length | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Runs | 948 | 292 | 99 | 38 | 19 | 7 | 7 | 1 | 2 | 2 | 1 |

Endpoint types are **1,360 zero/zero**, **31 zero/page-edge**, and **25 page-edge/zero**, in the enumeration’s order. **876** runs have lateral nonzero exits; **540** do not. Thus zero-bounded runs and lateral continuation recur throughout the signal.

The complete c02 boundary trace is:

`r57c02=0 | r58c02=6 | r59c02=14 | r60c02=26 | r61c02=30 | r62c02=19 | r63c02=5 | r64c02=0`

Its sum is **100**; its first three containers total **46**. Among enumerated runs, seven share its length, one its sum, one its ordered signature, and none its reversed signature. These uniqueness claims concern that comparison population.

All six lateral nonzero exits remain:

| From | To=value |
|---|---|
| r59c02 | r59c01=1; r59c03=2 |
| r61c02 | r61c03=3 |
| r62c02 | r62c01=2; r62c03=1 |
| r63c02 | r63c03=1 |

The supplied 28-cell component is recorded below as `row: column=value`; every listed container retains its coordinate:

```text
58: 2=6, 4=2
59: 1=1, 2=14, 3=2, 4=4
60: 2=26, 4=1
61: 2=30, 3=3, 4=1
62: 1=2, 2=19, 3=1
63: 2=5, 3=1
64: 3=1, 4=4
65: 4=3
66: 4=4
67: 4=4
68: 4=1
69: 4=1
70: 4=1
71: 4=1
72: 4=1, 5=1
73: 4=1
```

This preserves horizontal links across each listed row and vertical links between adjacent listed rows. In particular, the continuation from r63c02 passes through r63c03, r64c03, r64c04 and onward down c04 despite r64c02=0.

The supplied whole-grid threshold sweep reports:

| Inclusive threshold | Retained cells | Components | Core-intersecting component |
|---:|---:|---:|---|
| 1 | 1,112 | 395 | 28 cells |
| 2 | 215 | 153 | 11 cells |
| 3 | 52 | 39 | Six-cell core plus r61c03=3 |
| 4 | 21 | 15 | Exactly six-cell core |
| 5 | 12 | 7 | Exactly six-cell core |
| 6 | 9 | 5 | r58–r62c02 |
| 7 | 5 | 2 | r59–r62c02 |
| 14 | 4 | 1 | r59–r62c02 |
| 19 | 3 | 1 | r60–r62c02 |
| 26 | 2 | 1 | r60–r61c02 |
| 30 | 1 | 1 | r61c02 |

Thresholding changes derived membership only; all original containers, zeros and connections remain in the primary record.

**Candidate interpretation — applying Book II**

In Chad Coulter’s Book II, uppercase specifies **how to resolve the observable**.

- **Γ, boundary frame / transform operator:** With the six-cell frame, the two axial zeros bound the run while six lateral edges cross its frame. With the 28-cell frame, those edges become internal relationships. Its boundary is the component’s full external adjacency perimeter; r58c02 and r63c02 no longer constitute the component’s start/end pair.
- **Θ, constraint:** Keep container integrity, coordinates, four-neighbor adjacency, traversal choice and threshold policy explicit. The discovered constraint is that the core is connected to additional cells at lower thresholds.
- **Ε, threshold:** The observed facts are the `5→0` axial transition and isolation of the core at thresholds 4 and 5. Ε supplies the conceptual operation; neither observation makes the investigator’s threshold a source instruction.
- **Λ, lattice resolution:** Account for the axial and lateral relationships together. The lattice establishes continuation beyond the run’s frame at lower thresholds.
- **Ϛ, unresolvedness:** Preserve the unresolved selection of frame, direction and message boundary with provenance. These conceptual roles are not native machine instructions.

**Inference:** Persistence at 4 and 5 strengthens the six-cell candidate as a locally stable component under this specified filter. It preserves, rather than cancels, the lower-threshold lateral exits.

**Reverse and partial closure**

Forward containers encode `[Ϛ][ΙΔ][ΚϚ][Λ][ΙΘ][Ε]`; reverse containers encode `[Ε][ΙΘ][Λ][ΚϚ][ΙΔ][Ϛ]`. Both traverse the **same bounded object**. Reversing internal glyph order is a separate operation, producing, for example, `[ΘΙ]` within container 19. Zero reverse-signature matches elsewhere establish occurrence asymmetry, not a privileged direction.

Partial closure resolves the scoped run/component relationship while retaining open paths and remainders. The unresolved boundary is **whether this candidate bounds a source message**, including its orientation.

A further operation is to build the **complete component-inclusion hierarchy across all thresholds**, comparing every component’s persistence and attachment changes with the core’s. Retain coordinate-level edges and zeros, and evaluate directional features symmetrically. This tests structural distinctiveness without promoting a glyph to delimiter or selecting a desired phrase.

The earlier `[6,14,1]` belongs to generated-chain provenance; it is distinct from the raw triple, not demonstrated source corruption.
