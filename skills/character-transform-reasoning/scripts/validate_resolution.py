#!/usr/bin/env python3
"""Check structural invariants and three-gate accounting of saved resolution traces."""
import json
import sys
from pathlib import Path

TERMINAL = {"VALID TRANSFORM", "SUFFICIENT RESOLUTION", "INVALID VALIDATION", "BUDGET EXHAUSTED"}
STATUS = TERMINAL | {"IN-PROGRESS", "UNRESOLVED"}

def validate(data):
    errors = []
    if data.get("status") not in STATUS:
        errors.append("Unknown status")
    ids = [c.get("id") for c in data.get("candidates", [])]
    if len(ids) != len(set(ids)) or None in ids:
        errors.append("Candidate IDs must be present and unique")
    for t in data.get("transformations", []):
        if t.get("from") not in ids or t.get("to") not in ids:
            errors.append("Transformation refers to unknown candidate")
    comparisons = data.get("comparisons", [])
    streak = 0
    maximum = 0
    prev = None
    for c in comparisons:
        if c.get("from") not in ids or c.get("to") not in ids:
            errors.append("Comparison refers to unknown candidate")
        if (c.get("governance_id"), c.get("governance_version")) != (data.get("governance_id"), data.get("governance_version")):
            errors.append("Comparison changes frozen governance")
        valid = c.get("eligible") is True and c.get("material_change") is False and c.get("direction") == "Same"
        if not valid or (prev is not None and prev != c.get("from")):
            streak = 0
        if valid:
            streak += 1
            maximum = max(maximum, streak)
        prev = c.get("to")
    if data.get("status") == "VALID TRANSFORM" and maximum < 3:
        errors.append("VALID TRANSFORM requires three consecutive eligible Same transitions")
    if data.get("status") == "SUFFICIENT RESOLUTION" and not data.get("enough_met", False):
        errors.append("SUFFICIENT RESOLUTION requires documented Enough acceptance")
    for candidate in data.get("candidates", []):
        for idx in candidate.get("occurrence_indices", []):
            if not isinstance(idx, int) or idx < 0:
                errors.append("Invalid source occurrence index")
    return errors

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: validate_resolution.py <trace.json>")
    errors = validate(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    print("PASS" if not errors else "FAIL: " + "; ".join(errors))
    raise SystemExit(bool(errors))
