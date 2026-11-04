from __future__ import annotations

from enum import StrEnum


class InformationState(StrEnum):
    OBSERVATION = "observation"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"
    QUESTION = "question"
    RESOLUTION = "resolution"


class ResolutionKind(StrEnum):
    REVERSIBLE_RESOLUTION = "reversible_resolution"
    CLOSURE = "closure"
    LOGICAL_FAILURE = "logical_failure"
    REOPENED = "reopened"


class BackwardValidationStatus(StrEnum):
    VALID = "valid"
    FAILED = "failed"
