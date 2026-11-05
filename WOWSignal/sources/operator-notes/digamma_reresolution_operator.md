# Sigma Math - Digamma Re-Resolution Operator

## Status

Working canonical hypothesis.

Digamma (`Ϝ`) is the Sigma Math operator for re-traversing and re-resolving a
Monad that has already reached a resolved and closed state after something
subsequently changes.

The earlier candidate interpretation of `Ϝ` as equivalent-representation
substitution is superseded as the primary definition. Equivalent substitution
may still emerge as a special case or consequence of Digamma re-resolution, but
it is not currently considered the primitive operation.

## Core Definition

```text
Ϝ = Re-traverse / Re-resolve an already resolved and closed Monad after change.
```

Canonical form:

```text
Ϝ(Ϲ_n, Δ_n+1) -> Ϲ_n+1
```

Short form:

```text
Ϲ_n -> Ϝ -> Ϲ_n+1
```

## Operational Meaning

Digamma treats prior resolution as usable provenance. It should not discard a
valid resolved lattice simply because the Monad has changed.

Expected path:

```text
inherit -> invalidate selectively -> extend -> re-resolve -> re-traverse -> close
```

The central rule is:

```text
Do not resolve again what remains resolved.
```

## Primary Invariant

Preserve every previously resolved relationship that remains valid.

Digamma should re-resolve only the portion of the Monad whose resolution has
materially changed:

- unchanged resolved relationships are retained;
- invalidated relationships are re-resolved;
- changed relationships are re-resolved;
- new relationships are incorporated;
- dependent relationships are re-evaluated when necessary;
- unaffected resolution is not recomputed without cause.

## Relationship to Cartagraphy

The canonical Cartagraphy transform remains:

```text
Α -> Ω -> Λ -> Τ -> Ϲ
```

Digamma does not replace this transform. It provides a higher-order entry
condition for resolving a successor of something that has already passed
through it.

Fresh resolution:

```text
Α -> Ω -> Λ -> Τ -> Ϲ_0
```

Successor resolution:

```text
Ϲ_0 -> Ϝ -> Ϲ_1
```

## Relationship to TAO

TAO remains the underlying resolver. Digamma communicates this condition:

```text
This Monad has a valid prior resolution history. Use that prior closure and
trace as the basis for resolving its successor.
```

The prior closure is provenance, not authority over the successor Monad.

## Candidate Contracts

```text
DigammaInput {
    priorResolvedMonad
    priorResolvedLattice
    priorTrace
    priorClosureResult
    change
    currentContext
}
```

```text
DigammaResult {
    successorMonad
    successorResolvedLattice
    successorTrace
    closureResult
    retainedResolution
    changedResolution
    generation
}
```

## Open Evaluation Questions

Codex should test the model rather than assume additional machinery is
necessary. Do not add a new subsystem unless these evaluations demonstrate that
TAO's existing trace/checkpoint and lattice mechanisms cannot express the
required behavior.

1. What is the minimum closure state `Ϲ` must preserve for `Ϝ` to operate deterministically?
2. Can affected-lattice discovery be derived entirely from existing trace/checkpoint information?
3. Does Digamma require its own runtime mechanism, or can it compile cleanly into existing TAO primitives?
4. When does selective re-resolution become more expensive than complete `Λ` resolution?
5. What conditions invalidate the previous lattice entirely?
6. How should dependencies downstream of a changed relationship be discovered and re-resolved?
7. Can `LOGICAL_FAILURE` itself serve as a prior Digamma state if later information changes the Monad enough to make resolution possible?
8. Does equivalent-representation substitution emerge naturally as a special case of Digamma?
9. What algebraic composition rules does `Ϝ` have with `Δ`, `Λ`, `Τ`, `Ϲ`, `Ρ`, and other Sigma operators?
10. Does resolution-generation identity belong to the Monad, the trace, the Identity token, or solely the relationship between successive closures?

The working evaluation record for these questions is maintained in
[`digamma_evaluation.md`](digamma_evaluation.md).
