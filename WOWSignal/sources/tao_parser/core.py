from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from tao_parser.types import (
    BackwardValidationStatus,
    InformationState,
    ResolutionKind,
)


ROLE_FUNCTION_PATTERN = re.compile(
    r"^\s*(?P<role>[A-Za-z][\w-]*)\s*:\s*(?P<function>[A-Za-z][\w-]*)"
    r"(?:\((?P<input>.*)\))?\s*$"
)


@dataclass(frozen=True)
class InformationItem:
    label: str
    value: Any
    state: InformationState
    source: str


@dataclass(frozen=True)
class Monad:
    name: str
    positions: tuple[str, ...]
    resolved_positions: frozenset[str] = frozenset()

    def resolve(self, *positions: str) -> "Monad":
        unknown = set(positions) - set(self.positions)
        if unknown:
            names = ", ".join(sorted(unknown))
            raise ValueError(f"positions are outside monad boundary: {names}")
        return Monad(
            name=self.name,
            positions=self.positions,
            resolved_positions=self.resolved_positions | frozenset(positions),
        )

    @property
    def unresolved_positions(self) -> tuple[str, ...]:
        return tuple(
            position
            for position in self.positions
            if position not in self.resolved_positions
        )

    @property
    def is_resolved(self) -> bool:
        return not self.unresolved_positions


PRIMARY_MONADS: tuple[Monad, ...] = (
    Monad("tao", ("Theatre", "Act", "Operate")),
    Monad(
        "geometry",
        ("Spirit", "Property", "Process Relation", "State", "Resolution"),
    ),
    Monad(
        "resolution_path",
        (
            "Entity",
            "State",
            "Union Spirit",
            "Understanding",
            "Resolution Possession",
            "Completeness",
            "Stability",
        ),
    ),
)


@dataclass(frozen=True)
class Theatre:
    boundary: str
    information: tuple[InformationItem, ...] = ()
    constraints: tuple[str, ...] = ()


@dataclass(frozen=True)
class Act:
    name: str
    permitted_transformation: str


@dataclass(frozen=True)
class Operation:
    name: str
    input_state: tuple[InformationItem, ...]
    output_state: tuple[InformationItem, ...]
    trace: str


@dataclass(frozen=True)
class BackwardValidation:
    status: BackwardValidationStatus
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class Resolution:
    outcome: Any
    unresolved_remainder: tuple[InformationItem, ...]
    trace: tuple[str, ...]
    enough: bool
    kind: ResolutionKind
    backward_validation: BackwardValidation


@dataclass(frozen=True)
class TAOExpression:
    theatre: str
    act: str
    operate: str


def parse_tao_expression(text: str) -> TAOExpression:
    normalized = text.replace("→", "->")
    parts = tuple(part.strip() for part in normalized.split("->"))
    if len(parts) != 3 or any(not part for part in parts):
        raise ValueError("TAO expression must be Theatre -> Act -> Operate")
    return TAOExpression(theatre=parts[0], act=parts[1], operate=parts[2])


def parse_resolution_function(text: str) -> tuple[str, str, str | None]:
    match = ROLE_FUNCTION_PATTERN.match(text)
    if not match:
        raise ValueError("resolution function must look like Role:Function(input)")
    return (
        match.group("role"),
        match.group("function"),
        match.group("input"),
    )


@dataclass
class TAOResolver:
    monads: tuple[Monad, ...] = field(default_factory=lambda: PRIMARY_MONADS)

    def resolve(
        self,
        theatre: Theatre,
        act: Act,
        operations: tuple[Operation, ...] = (),
    ) -> Resolution:
        trace = [f"Theatre:{theatre.boundary}", f"Act:{act.name}"]
        information = list(theatre.information)

        for operation in operations:
            trace.append(f"Operate:{operation.name}")
            information.extend(operation.output_state)

        unresolved = tuple(
            item
            for item in information
            if item.state in {InformationState.HYPOTHESIS, InformationState.QUESTION}
        )
        enough = not unresolved
        backward_validation = self.validate_backward(theatre, act, tuple(trace), information)

        if backward_validation.status == BackwardValidationStatus.FAILED:
            return Resolution(
                outcome="backward validation failed",
                unresolved_remainder=unresolved,
                trace=tuple(trace),
                enough=False,
                kind=ResolutionKind.LOGICAL_FAILURE,
                backward_validation=backward_validation,
            )

        if enough:
            return Resolution(
                outcome=tuple(
                    item
                    for item in information
                    if item.state == InformationState.RESOLUTION
                ),
                unresolved_remainder=(),
                trace=tuple(trace),
                enough=True,
                kind=ResolutionKind.CLOSURE,
                backward_validation=backward_validation,
            )

        return Resolution(
            outcome=tuple(
                item
                for item in information
                if item.state
                in {InformationState.OBSERVATION, InformationState.INFERENCE}
            ),
            unresolved_remainder=unresolved,
            trace=tuple(trace),
            enough=False,
            kind=ResolutionKind.REVERSIBLE_RESOLUTION,
            backward_validation=backward_validation,
        )

    def validate_backward(
        self,
        theatre: Theatre,
        act: Act,
        trace: tuple[str, ...],
        information: list[InformationItem],
    ) -> BackwardValidation:
        reasons: list[str] = []
        if f"Theatre:{theatre.boundary}" not in trace:
            reasons.append("reverse traversal cannot recover admitted Theatre")
        if f"Act:{act.name}" not in trace:
            reasons.append("reverse traversal cannot recover admitted Act")
        for item in information:
            if item.state == InformationState.RESOLUTION and not item.source:
                reasons.append(f"resolution item lacks resolving source: {item.label}")
        if reasons:
            return BackwardValidation(BackwardValidationStatus.FAILED, tuple(reasons))
        return BackwardValidation(BackwardValidationStatus.VALID)
