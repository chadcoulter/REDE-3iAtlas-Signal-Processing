# Sigma Math and REDOE.Cartagraphy Complete Current Specification

> Supersession note: the Digamma section in this extracted document reflects
> the earlier equivalent-representation candidate. The current working
> canonical hypothesis is documented in `docs/digamma_reresolution_operator.md`:
> `Ϝ` means re-traverse / re-resolve an already closed Monad after change.

Transform language • Monad resolution • Lattice Cartagraphy • TAO traversal

20 August 2026

Scope

This specification consolidates the current Sigma Math transform vocabulary, its TAO execution semantics, the REDOE.Cartagraphy lattice model, preserved alternate transforms, closure behavior, and the active Digamma recovery candidate.

Contents

1. System boundary and purpose

2. Foundational objects and resolution substrate

3. Sigma Math principles and notation

4. Standard Greek transform alphabet

5. Core Cartagraphy transform

6. Transform contracts and state handoffs

7. Closure and terminal result semantics

8. Alternate transforms, selection, and permutation space

9. Extended / recovered operator space: Digamma

10. Named legacy transform: Stoic paradox resolution

11. Canonical composition patterns and worked examples

12. Conformance invariants

13. Current frontier / implementation-defined surfaces

Appendices: quick reference, formulas, terminology

Status vocabulary

1. System boundary and purpose

Sigma Math is a transform-oriented mathematical language for representing relational resolution. It treats states, relationships, constraints, branches, observations, and transformations as operations over Monads rather than as isolated symbols. Cartagraphy uses this language to establish and navigate a relational lattice. TAO supplies the permitted operation and resolution machinery underneath both.

The division of responsibility is deliberate: Sigma Math names and composes transforms; REDOE.Cartagraphy establishes the source-to-target relational space and orchestrates lattice resolution; TAO validates, operates, traces, and classifies the resolution. Cartagraphy does not replace TAO and does not define a second execution engine.

1.1 Governing principle

The governing principle carried across the transform family is to increase relational resolution before discarding apparently incompatible observations. Apparent contradiction is therefore an input to resolution, not an automatic instruction to delete one side of the relationship.

1.2 Assembly-equivalent resolution layer

TAO operates at an assembly-equivalent resolution layer: transformations expressible through primitive state operations should be representable as TAO resolution structures. Sigma Math provides a compact symbolic vocabulary above that substrate while preserving the trace needed to explain how one resolvable state became another.

2. Foundational objects and resolution substrate

2.1 Monad

A Monad is the relational unity admitted as an input, target, intermediate, or output of a transform. In Cartagraphy, the canonical endpoints are Source Monad and Target Monad. The notation does not require the Monad to be a permanently fixed object; it identifies the unity being resolved at the current operation boundary.

2.2 Theatre

The Theatre is the operative system boundary in which an act is evaluated. It determines which relationships, constraints, permissions, and operations are admitted for the resolution. Changing the theatre changes the object of examination and therefore requires re-evaluation rather than carrying conclusions across unchanged.

2.3 Lattice

The lattice is the relational resolution space between established Monads. It may contain branches, constraints, alternatives, costs, relationships, candidate paths, boundaries, and state transitions. A resolved lattice is not required to collapse to one geometric path; it contains enough resolved structure for TAO to perform a permitted traversal toward the Target Monad.

2.4 TAO

TAO is the operation and resolution substrate. At minimum, it receives or creates a Theatre, admits an Act, validates the Act against the Theatre, operates within the Theatre, emits outcome plus unresolved remainder and trace, and resolves the trace toward a prior state or explicit closure.

Minimal TAO engine loop expressed as an operational sequence.

Every permitted TAO operation resolves to exactly one terminal classification: Reversible Resolution, Closure, Logical Failure, or `KICK_FORWARD`. Reversibility is logical rather than necessarily physical; trace and checkpoint information are sufficient when they establish the prior resolvable state and how the resulting state was produced.

3. Sigma Math principles and notation

3.1 Transform grammar

Universal transform shape.

A Greek symbol represents an operation. Its meaning is therefore stated with a verb or operational phrase wherever possible. The operator transforms, establishes, observes, selects, relates, traverses, or returns a Monad or relational structure.

3.2 Standard notation

3.3 Representation is not resolved value

Sigma Math allows distinct representations to preserve the same resolved value when the theatre admits them as equivalent. This distinction is explicit in the active Digamma candidate and prevents identity of representation from being confused with identity of resolved value.

3.4 Trace is part of resolution

A resolution is not only the final output. The path or checkpoint information required to establish provenance and logical reversibility is part of the operation contract. External effects do not need to be physically undone for a resolution to be logically reversible.

4. Standard Greek transform alphabet

The 24-letter Greek alphabet is the canonical standard transform vocabulary. Overlapping meanings are intentional where the operators act at different relational levels. For example, Ζ establishes connectivity while Ρ establishes the semantics of a relationship; Μ measures while Ε evaluates a threshold.

4.1 Important operator separations

5. Core Cartagraphy transform

Canonical REDOE.Cartagraphy transform.

5.1 Operational reading

Establish enough relational structure to identify the Source Monad.

Establish enough relational structure to identify the Target Monad.

Resolve the relational lattice connecting source and target through TAO.

Traverse the resolved lattice through TAO using the permitted operations.

Return the resulting Resolved State and terminal classification.

5.2 Cartagraphy does not prescribe the journey

The lattice represents available relationship space. It does not hard-code one journey. Λ resolves enough structure to make traversal possible, and Τ performs the permitted traversal. Alternative branches, costs, constraints, and paths may remain represented in the resolved lattice.

6. Transform contracts and state handoffs

6.1 Universal operator contract

Every standard Greek transform shares this contract. The operator semantics vary; the execution model does not. This avoids creating 24 separate runtimes or interface families.

6.2 Λ → Τ contract

The bracketed object is a handoff structure, not an additional operator.

Λ consumes the established Source Monad, Target Monad, and relevant Theatre context. It emits a Resolved Lattice: enough resolved relational structure for TAO to operate toward Ω from Α. Τ consumes that Resolved Lattice.

6.3 Τ → Ϲ contract

Traversal Outcome and Resolved State are handoff/result structures.

Τ performs the permitted traversal and emits a Traversal Outcome. Ϲ consumes that outcome and returns the Resolved State, including the terminal result classification, unresolved remainder when present, and trace/checkpoint information required by TAO.

6.4 Minimal result shape

The exact serialization is implementation-defined. The fields above express the current semantic minimum inherited from the TAO operating contract.

7. Closure and terminal result semantics

Closure classes are enums rather than additional Greek operators. Ϲ remains the common Return Resolved State operator; the enum records how the operation terminated.

No additional Cartagraphy enums are currently required. Other conditions remain relational state in the lattice until an operation demonstrates a finite state set that benefits from enumeration.

8. Alternate transforms, selection, and permutation space

8.1 Preserved whole-transform alternatives

These are not discarded drafts. They remain available when the canonical Α → Ω → Λ → Τ → Ϲ transform does not work, does not adequately resolve the Theatre, or is too computationally or operationally expensive.

8.2 Preserved endpoint / notation alternatives

Additional preserved endpoint pairs: Α₀→Ατ, Ω₀→Ωτ, Ξ₀→Ξτ, Φ₀→Φτ, Ψ₀→Ψτ, Γ₀→Γτ, Δ₀→Δτ. These remain available notation shapes but are not the canonical core endpoint notation.

8.3 Alternative selection through Υ

Υ is the standard Choice transform. When multiple admissible transforms, branches, or paths are available, Υ resolves which becomes operative against the current objective and Theatre. Cost may participate in the resolution, but choice is not defined as "pick the cheapest." Adequacy, permission, reversibility, constraints, and other lattice relationships may all participate.

8.4 Permutation space

The standard alphabet supplies a composable transform vocabulary. The meaningful permutation space is therefore the set of admissible operator sequences that TAO can resolve within a Theatre, not a blind enumeration of every syntactic ordering of Greek letters. Repetition, branching, and deeper composition remain available to the language where the Theatre and operator contracts admit them; a global composition grammar has not yet been frozen.

9. Extended operator space: Ϝ Digamma

Candidate Ϝ semantics: representation changes while relevant resolved value is preserved.

9.1 Candidate operation

9.2 Provenance and evidentiary boundary

The candidate arose through comparison of allographic substitution in Rongo Rongo, where differing graphic forms can share a reading value, with independent Greek evidence that the historical /w/ value associated with Digamma could be represented through other forms or spellings. These comparisons provide structural support for the substitution pattern.

Assigning this abstract operator semantics specifically to Ϝ is a Sigma / TAO formalization. It is not asserted here as an established ancient Greek mathematical meaning of Digamma.

10. Named legacy transform: Stoic paradox resolution

Preserved five-stage Stoic paradox-resolution transform.

Ξ marks the encountered apparent contradiction or paradox. Ϲ is the terminal/resolved state. The middle stages Τ → Ω → Ι were derived from the Stoic resolution operation rather than assigned arbitrarily, and their named-transform semantics must be preserved.

11. Canonical composition patterns and worked examples

11.1 Measurement and threshold pattern

Observe → Determine/express change → Measure → Evaluate threshold.

This pattern separates observation, difference/change, measurement, and threshold evaluation. The separation prevents a measurement from silently becoming a decision boundary.

11.2 Relational navigation pattern

Frame → Context → Relation → Resolve Lattice → Traverse → Return Resolved State.

This pattern is useful when the Theatre boundary, context, and relational meaning must be established before the lattice can be resolved and traversed.

11.3 Branch and choice pattern

Branch generation/entry → candidate work → Choice → lattice resolution → traversal → return.

Β and Υ are deliberately not synonyms. A branch can exist without being chosen; a choice can be resolved among already existing branches without creating a new branch.

11.4 Equivalent representation substitution

Candidate substitution followed by continued resolution in the new representation.

If Ϝ is ultimately validated, a resolver may substitute an admitted equivalent representation to reduce cost, expose a relationship, or traverse a representation boundary while preserving the value that matters to the objective.

11.5 Canonical Cartagraphy execution

12. Conformance invariants

An implementation conforms to the current Sigma Math / Cartagraphy model when it preserves the following invariants:

Α and Ω establish Source Monad and Target Monad respectively; they are not merely labels for pre-existing endpoints.

Λ resolves relational space and emits a Resolved Lattice; Τ consumes that lattice and performs traversal.

Τ emits a Traversal Outcome; Ϲ is responsible for returning the Resolved State and its terminal classification.

Every permitted terminal resolution is exactly one of REVERSIBLE_RESOLUTION, CLOSURE, or LOGICAL_FAILURE.

Logical reversibility requires enough trace/state/relationship information to recover the prior resolvable state; physical reversal is not required.

Σ and Ϲ remain distinct: Aggregation is not terminal return.

Μ remains a valid standard Measure transform even though Mu was rejected for the core source/target notation.

Υ performs choice among admissible alternatives; it does not replace Λ lattice resolution.

Alternate transforms remain preserved options rather than being discarded because the core is preferred.

Ϝ remains an active candidate until its specific operator assignment and reversibility are sufficiently established.

13. Current frontier / implementation-defined surfaces

The conceptual core is resolved enough to exercise. The remaining surfaces are intentionally left open until implementation or further mathematical work forces additional structure.

Appendix A. Quick operator reference

Appendix B. Canonical formulas

Appendix C. Terminology

Appendix D. Provenance markers

Α → Ω → Λ → Τ → Ϲ

Establish. Resolve. Traverse. Return.

## Table 1

| Σ MATH / and REDOE.Cartagraphy / Complete Current Specification |
| --- |

## Table 2

| Canonical core / Α → Ω → Λ → Τ → Ϲ / Establish Source Monad → Establish Target Monad → Resolve Lattice → Traverse Resolved Lattice → Return Resolved State |
| --- |

## Table 3

| CONTENTS AND STATUS |
| --- |

## Table 4

| Canonical | Established as the current standard definition and used by default. |
| --- | --- |
| Preserved alternative | Retained as a valid transform option when the core is inadequate, inapplicable, or too expensive. |
| Active candidate | Structurally supported and usable for research, but not promoted to canonical semantics. |
| Implementation-defined | The abstract contract is established; concrete storage, weighting, or runtime representation remains open. |

## Table 5

| Critical notation distinction / Σ (capital sigma) is the standard Aggregation transform. Ϲ (capital lunate sigma) is the terminal Return Resolved State operator. They are intentionally distinct symbols with distinct semantics. |
| --- |

## Table 6

| PART I - SIGMA MATH |
| --- |

## Table 7

| Resolver discipline / Resolution is governed by the declared objective, theatre, relationships, and admitted constraints. Resolver preference is not itself a resolution criterion unless the theatre explicitly admits it. |
| --- |

## Table 8

| Receive/Create Theatre → Admit Act → Validate → Operate → Trace → Resolve |
| --- |

## Table 9

| Monadᵢ → Operator → Monadᵢ₊₁ |
| --- |

## Table 10

| → | Directed transform or handoff to the next operation/state. |
| --- | --- |
| ↔ | Reversible equivalence relationship between admitted representations. |
| Mᵢ / Mᵢ₊₁ | Input and output Monad positions in the universal contract. |
| V(A) | Resolved value of representation A within the relevant objective/theatre. |
| ₀ / τ | Preserved endpoint notation for source/target variants; not the canonical core notation. |
| prime (′) | Optional shorthand for a resulting or transformed state when the exact index is not important. |

## Table 11

| PART II - STANDARD TRANSFORM ALPHABET |
| --- |

## Table 12

| Symbol | Name | Standard transform | Operational distinction |
| --- | --- | --- | --- |
| Α | Alpha | Establish Source Monad | Establishes the source unity from which the resolution begins. |
| Β | Beta | Branch | Creates or enters a candidate branch in the lattice. |
| Γ | Gamma | Boundary / Frame | Establishes the theatre boundary or operative frame. |
| Δ | Delta | Change | Transforms state; change does not itself imply crossing a boundary. |
| Ε | Epsilon | Threshold | Evaluates whether a measured or observed difference crosses an operative threshold. |
| Ζ | Zeta | Link | Establishes connectivity between elements without fully specifying relational meaning. |
| Η | Eta | State | Establishes or reads an existing operative state. |
| Θ | Theta | Constraint | Applies a governing condition or limit inside an established frame. |
| Ι | Iota | Instance | Resolves a generalized structure into a specific instance. |
| Κ | Kappa | Context | Establishes or transforms contextual relationships relevant to resolution. |
| Λ | Lambda | Resolve Lattice | Allows TAO to resolve the relational lattice between established endpoints. |
| Μ | Mu | Measure | Measures or evaluates magnitude without itself deciding a threshold outcome. |

## Table 13

| Symbol | Name | Standard transform | Operational distinction |
| --- | --- | --- | --- |
| Ν | Nu | Novel State | Introduces or identifies a state not represented in the current lattice. |
| Ξ | Xi | Contradiction / Encounter | Marks an encountered apparent contradiction or incompatible observation requiring resolution. |
| Ο | Omicron | Observation | Observes or reads state without requiring a transformation. |
| Π | Pi | Projection | Projects a state, path, or relational consequence. |
| Ρ | Rho | Relation | Establishes what a connection means: the relational semantics between elements. |
| Σ | Sigma | Aggregation | Composes multiple resolved elements into a coherent whole. |
| Τ | Tau | Traverse Resolved Lattice | Uses TAO to traverse the lattice resolved by Λ. |
| Υ | Upsilon | Choice | Resolves a choice among admissible branches, transforms, or paths. |
| Φ | Phi | Form | Resolves the configuration or form of something treated as a unity. |
| Χ | Chi | Crossing | Crosses a defined boundary or interface; crossing is distinct from state change. |
| Ψ | Psi | Pattern | Resolves recurring or higher-order relationships across configurations. |
| Ω | Omega | Establish Target Monad | Establishes the target unity toward which the resolution is directed. |

## Table 14

| Β vs Υ | Β changes or enters branch topology; Υ selects among admissible alternatives. |
| --- | --- |
| Ζ vs Ρ | Ζ establishes connectivity; Ρ establishes relational meaning. |
| Η vs Ν | Η addresses an existing state; Ν introduces or identifies a novel state. |
| Γ vs Θ | Γ establishes the frame; Θ restricts what is permissible within it. |
| Φ vs Ψ | Φ resolves configuration as a unity; Ψ resolves higher-order pattern across configurations. |
| Δ vs Χ | Δ changes state; Χ crosses a boundary/interface. Either may occur without the other. |
| Μ vs Ε | Μ measures; Ε evaluates whether the measure reaches an operative threshold. |

## Table 15

| Mu status / Μ / Mu is part of the standard transform alphabet. It was rejected only as the symbol for the canonical core endpoint transform; it is not excluded from the design space. |
| --- |

## Table 16

| PART III - REDOE.CARTAGRAPHY |
| --- |

## Table 17

| Α → Ω → Λ → Τ → Ϲ |
| --- |

## Table 18

| Stage | Canonical meaning |
| --- | --- |
| Α | Establish Source Monad. |
| Ω | Establish Target Monad. |
| Λ | Allow TAO to resolve the lattice between the established Monads. |
| Τ | Use TAO to traverse the resolved lattice. |
| Ϲ | Return the Resolved State. |

## Table 19

| Transform { /   input_monad /   operator /   tao_operation /   output_monad /   trace / } |
| --- |

## Table 20

| Λ → [Resolved Lattice] → Τ |
| --- |

## Table 21

| Boundary rule / Λ produces what Τ traverses. Resolution of relational space and traversal of that space are separate responsibilities. |
| --- |

## Table 22

| Τ → [Traversal Outcome] → Ϲ → [Resolved State] |
| --- |

## Table 23

| Boundary rule / Τ produces what Ϲ resolves and returns. Traversal is not the same operation as terminal return. |
| --- |

## Table 24

| ResolvedState { /   monad /   result /   unresolved_remainder /   trace /   enough / } |
| --- |

## Table 25

| result ∈ { /   REVERSIBLE_RESOLUTION, /   CLOSURE, /   LOGICAL_FAILURE / } |
| --- |

## Table 26

| REVERSIBLE_RESOLUTION | The operation resolves while preserving enough state, relationship, and trace information to traverse logically back to the prior resolvable state. |
| --- | --- |
| CLOSURE | The operation reaches an explicit valid terminal boundary. Further traversal is not required for the objective. |
| LOGICAL_FAILURE | Neither a prior resolvable state nor a valid closure can be established. |

## Table 27

| PART IV - COMPOSITION AND ALTERNATIVES |
| --- |

## Table 28

| Ρ → Φ → Λ → Τ → Ϲ |
| --- |

## Table 29

| Α → Β → Λ → Δ → Ϲ |
| --- |

## Table 30

| Π → Ρ → Λ → Τ → Ϲ |
| --- |

## Table 31

| Θ → Φ → Λ → Τ → Ϲ |
| --- |

## Table 32

| Σ₀ → Στ → Λ → Τ → Ϲ |
| --- |

## Table 33

| Ρ₀ → Ρτ → Λ → Τ → Ϲ |
| --- |

## Table 34

| Selection / resolution separation / Υ selects among admissible alternatives. Λ resolves the relational lattice for the selected operation/path. These are distinct transforms. |
| --- |

## Table 35

| PART V - EXTENDED AND RECOVERED TRANSFORMS |
| --- |

## Table 36

| Status: Active candidate / Strong current candidate for equivalent-representation substitution. Working confidence: approximately 0.8, pending stronger evidence for reversibility and the operator assignment itself. |
| --- |

## Table 37

| A ↔ B  when  A ≠ B  and  V(A) = V(B) |
| --- |

## Table 38

| Symbol | Ϝ (Digamma) |
| --- | --- |
| Candidate role | Equivalent-representation substitution. |
| Input relationship | A and B are distinct admitted representations. |
| Invariant | The relevant resolved value is preserved: V(A)=V(B). |
| Directionality | Intended to be reversible between admitted equivalent representations. |
| Effect | Changes representation without changing the resolved value relevant to the current objective. |

## Table 39

| Ξ → Τ → Ω → Ι → Ϲ |
| --- |

## Table 40

| Namespace reconciliation required / The standard Cartagraphy alphabet now gives Τ, Ω, and Ι general transform meanings (Traverse, Establish Target Monad, Instance). Until the legacy Stoic derivation is explicitly reconciled with those general meanings, this five-stage sequence should be treated as a preserved named transform rather than automatically expanded through the standard Cartagraphy definitions. |
| --- |

## Table 41

| PART VI - COMPOSITION PATTERNS |
| --- |

## Table 42

| Ο → Δ → Μ → Ε |
| --- |

## Table 43

| Γ → Κ → Ρ → Λ → Τ → Ϲ |
| --- |

## Table 44

| Β → … → Υ → Λ → Τ → Ϲ |
| --- |

## Table 45

| A —Ϝ→ B  ;  V(A) = V(B) |
| --- |

## Table 46

| Α  establish Source Monad / Ω  establish Target Monad / Λ  TAO resolves lattice  -> Resolved Lattice / Τ  TAO traverses lattice -> Traversal Outcome / Ϲ  return Resolved State -> terminal result enum |
| --- |

## Table 47

| Monad schema | The minimum semantic role is established; a universal machine schema has not been frozen. |
| --- | --- |
| Lattice storage model | Resolved Lattice semantics are established; concrete node/edge representation, weights, persistence, and indexing remain implementation-defined. |
| Traversal Outcome schema | Its position and responsibility are established; concrete fields beyond TAO-required outcome/trace/remainder are not frozen. |
| Cost function | Cost may influence Υ and TAO resolution, but no universal scalar cost equation has been adopted. |
| Composition grammar | Operators are composable, but global rules for repetition, recursion, nesting, concurrency, and precedence are not yet standardized. |
| Stoic transform reconciliation | The preserved named transform Ξ→Τ→Ω→Ι→Ϲ needs an explicit namespace/semantic reconciliation with the standard alphabet if the two are to share automatic expansion. |
| Digamma validation | Ϝ equivalent-representation substitution remains a strong candidate rather than a canonical operator. |
| Additional extended symbols | No requirement currently exists to assign further archaic/non-24-letter Greek symbols until a distinct operation is discovered. |
| Conformance tests | The invariants are defined; executable test vectors and formal proofs are the next validation surface. |

## Table 48

| Completion criterion / New architecture should be added only when exercising the existing transforms exposes an actual unresolved relationship, unreachable state, contradiction, or cost problem. The current model should be tested before it is expanded. |
| --- |

## Table 49

| APPENDICES |
| --- |

## Table 50

| Symbol | Meaning |
| --- | --- |
| Α | Establish Source Monad |
| Β | Branch |
| Γ | Boundary / Frame |
| Δ | Change |
| Ε | Threshold |
| Ζ | Link |
| Η | State |
| Θ | Constraint |
| Ι | Instance |
| Κ | Context |
| Λ | Resolve Lattice |
| Μ | Measure |
| Ν | Novel State |
| Ξ | Contradiction / Encounter |
| Ο | Observation |
| Π | Projection |
| Ρ | Relation |
| Σ | Aggregation |
| Τ | Traverse Resolved Lattice |
| Υ | Choice |
| Φ | Form |
| Χ | Crossing |
| Ψ | Pattern |
| Ω | Establish Target Monad |
| Ϲ | Return Resolved State |
| Ϝ | Equivalent-representation substitution (candidate) |

## Table 51

| Pattern | Notation |
| --- | --- |
| Core Cartagraphy | Α → Ω → Λ → Τ → Ϲ |
| Universal transform | Monadᵢ → Operator → Monadᵢ₊₁ |
| Λ/Τ handoff | Λ → [Resolved Lattice] → Τ |
| Τ/Ϲ handoff | Τ → [Traversal Outcome] → Ϲ → [Resolved State] |
| Terminal enum | result ∈ { REVERSIBLE_RESOLUTION, CLOSURE, LOGICAL_FAILURE } |
| Digamma candidate | A ↔ B when A ≠ B and V(A)=V(B) |
| Stoic named transform | Ξ → Τ → Ω → Ι → Ϲ |
| Measurement pattern | Ο → Δ → Μ → Ε |
| Relational navigation | Γ → Κ → Ρ → Λ → Τ → Ϲ |

## Table 52

| Term | Current definition |
| --- | --- |
| Cartagraphy | The REDOE lattice-oriented layer that establishes source/target Monads, resolves relational space through TAO, traverses that space, and returns the resolved state. |
| Monad | The relational unity admitted at an operation boundary. |
| Resolved Lattice | Enough resolved relational structure for TAO to perform permitted traversal toward the Target Monad. |
| Traversal Outcome | The result emitted by Τ after traversing a Resolved Lattice and before terminal return by Ϲ. |
| Resolved State | The state returned by Ϲ together with TAO terminal classification and required trace/remainder information. |
| Trace | Provenance/checkpoint information establishing how a state was produced and, where applicable, its prior resolvable state. |
| Reversible Resolution | Successful logical resolution with enough information to traverse back to the prior resolvable state. |
| Closure | Explicit valid terminal boundary. |
| Logical Failure | Terminal condition in which neither prior resolvable state nor valid closure can be established. |
| Permutation space | The admissible transform sequences resolvable within a Theatre, rather than every possible syntactic ordering. |

## Table 53

| Core Cartagraphy transform | Α → Ω → Λ → Τ → Ϲ established as the preferred core; alternate transforms preserved for inadequacy or excessive cost. |
| --- | --- |
| Source/Target correction | Canonical endpoint semantics are Source Monad and Target Monad; “Meta” was discarded as the endpoint object name. |
| Mu correction | Μ remains valid in the alphabet; only its use as the core endpoint symbol was rejected. |
| Closure correction | Closure classes became enums; Ϲ remained the terminal Return Resolved State operator. |
| Digamma recovery | Ϝ candidate: equivalent-representation substitution with value preservation and intended reversibility; working confidence approximately 0.8. |
