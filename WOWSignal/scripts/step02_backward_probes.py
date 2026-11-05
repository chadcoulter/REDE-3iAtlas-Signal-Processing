#!/usr/bin/env python3
"""Backward reconstruction probes; every proposed connection remains typed."""
import argparse
import ast
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
WOW = Path(__file__).resolve().parents[1]
REPO = WOW.parent
sys.path.insert(0, str(WOW / "sources"))
from tao_parser import Act, InformationItem, InformationState, Operation, TAOResolver, Theatre, to_plain


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def run(output):
    if output.exists():
        raise ValueError("Use a new output directory.")
    source = WOW / "steps/01-source-data/run-001"
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    expected = {x["filename"]: x["sha256"] for x in manifest["artifacts"]}
    for name in ("raw_grid.json", "numeric_grid.json"):
        if digest(source / name) != expected[name]:
            raise ValueError("Source artifact hash mismatch.")
    raw = json.loads((source / "raw_grid.json").read_text(encoding="utf-8"))["grid"]
    numeric = json.loads((source / "numeric_grid.json").read_text(encoding="utf-8"))["grid"]
    # The known recorded event is a source reference, not an output selected by interpretation.
    column = "".join(row[1] for row in raw)
    starts = [i for i in range(len(column) - 5) if column[i:i + 6] == "6EQUJ5"]
    assert len(starts) == 1
    start = starts[0]
    measurements = [{"source_row_0based": r, "source_channel_0based": 1, "source_cell_id": r * 50 + 1,
                     "character": raw[r][1], "numeric_bin": numeric[r][1]} for r in range(start, start + 6)]
    extractor = REPO / "skills/character-transform-reasoning/scripts/redsigma_band_extract.py"
    tree = ast.parse(extractor.read_text(encoding="utf-8-sig"))
    selected = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "greek"
                or isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "VALUES" for t in n.targets)]
    namespace = {}
    exec(compile(ast.Module(body=selected, type_ignores=[]), str(extractor), "exec"), namespace)
    glyph_values = {glyph: n for n, glyph in namespace["VALUES"]}
    occurrences = []
    encoded = []
    for index, item in enumerate(measurements):
        group = namespace["greek"](item["numeric_bin"])
        encoded.append(group)
        for offset, glyph in enumerate(group):
            occurrences.append({"occurrence": len(occurrences), "glyph": glyph,
                                "numeral_component": glyph_values[glyph],
                                "measurement_index": index, "offset_within_group": offset,
                                "source_cell_id": item["source_cell_id"]})
    assert len(occurrences) == 9
    recovered = [sum(x["numeral_component"] for x in occurrences if x["measurement_index"] == i) for i in range(6)]
    assert recovered == [x["numeric_bin"] for x in measurements]
    row_major = [[occurrences[r * 3 + c]["occurrence"] for c in range(3)] for r in range(3)]
    column_major = [[occurrences[c * 3 + r]["occurrence"] for c in range(3)] for r in range(3)]
    layouts = []
    for name, layout in (("row_major", row_major), ("column_major", column_major)):
        glyph_grid = [[occurrences[i]["glyph"] for i in row] for row in layout]
        layouts.append({"candidate": name, "occurrence_grid": layout, "glyph_grid": glyph_grid,
                        "diagonal_1": [glyph_grid[i][i] for i in range(3)],
                        "diagonal_2": [glyph_grid[i][2 - i] for i in range(3)],
                        "center_occurrence": layout[1][1], "center_glyph": glyph_grid[1][1]})
    rows = [sum(occurrences[i]["numeral_component"] for i in row) for row in row_major]
    columns = [sum(occurrences[row_major[r][c]]["numeral_component"] for r in range(3)) for c in range(3)]
    matrix_probe = {
        "status": "COMPUTED_CANDIDATE_HISTORICAL_EQUIVALENCE_UNCONFIRMED",
        "encoding_authority": "existing Atlas extractor greek()/VALUES, not a recovered August Wow implementation",
        "encoded_measurements": encoded, "glyph_occurrences": occurrences, "layouts": layouts,
        "row_sums": rows, "column_sums": columns,
        "source_sum": sum(recovered), "sum_as_existing_greek_numeral": namespace["greek"](sum(recovered)),
        "provenance_round_trip": recovered,
        "fits": ["nine glyph occurrences from six measurements without adding or removing numeral components",
                 "three groups of three and two diagonals with one shared position are available under explicit layout"],
        "does_not_establish": ["the original horizontal measurement paths", "why row-major or column-major layout was chosen",
                              "a transformation yielding ASTRA or ΛΤϜ", "a historical role for the shared Stigma center"],
    }
    # Stylized E geometry: a declared typographic model, not image extraction or source handwriting.
    # Vertical trunk x=0, y=0..2; top/middle/bottom bars run to x=1.
    edges = [((0, 0), (0, 1)), ((0, 1), (0, 2)),
             ((0, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 2), (1, 2))]
    degree = {}
    for a, b in edges:
        degree[a] = degree.get(a, 0) + 1
        degree[b] = degree.get(b, 0) + 1
    intersections = [{"node": [0, y], "degree": degree[(0, y)]} for y in range(3)]
    assert [x["degree"] for x in intersections] == [2, 3, 2]
    glyph_probe = {
        "status": "TYPOGRAPHIC_HYPOTHESIS",
        "source": measurements[1], "input_type": "printed intensity code E, representing bin 14",
        "declared_model": "upright block-capital E: one vertical trunk and three horizontal bars",
        "model_edges": edges, "bar_trunk_intersections": intersections,
        "fits": ["exact structural match to V + H_T + H_M + H_B at the glyph-model level"],
        "reverse_tests": {"top_bottom_reflection": "same geometric E", "left_right_reflection": "backward E, not Digamma",
                          "double_left_right_reflection": "original geometry restored"},
        "does_not_establish": ["that the original exploration used glyph strokes rather than neighboring cells",
                              "a source-measurement 3x3 matrix", "three degree-three junctions",
                              "Lambda/Tau/Digamma outputs"],
        "boundary": "A printed measurement symbol is being examined as a representation; it is not evidence of transmitted writing.",
    }
    constraints = {
        "three_event_rows_possible_choices": len(list(itertools.combinations(range(start, start + 6), 3))),
        "no_unique_middle_event_sample": "six samples have two central positions, not one",
        "simple_sum_probe": {
            "scope": "three raw bins added without scaling or other transforms",
            "max_dataset_bin": max(max(row) for row in numeric), "upper_bound": 3 * max(max(row) for row in numeric),
            "Tau_numeral_value": 300, "can_reach_Tau_by_this_rule": False,
            "note": "This excludes only this particular arithmetic rule, not a semantic Tau operation.",
        },
        "numeral_identity": "Existing encoder uses Stigma Ϛ for 6; it does not use Digamma Ϝ. No substitution is admitted.",
        "meaning_of_ASTRA": "The narrative describes a candidate operational reading; a one-sample-to-one-letter substitution is not supplied.",
    }
    observation = InformationItem("recorded_event", measurements, InformationState.OBSERVATION, "Step 1 preserved cells")
    context = InformationItem("whole_source_context", {"raw_grid": str(source / "raw_grid.json"), "sha256": digest(source / "raw_grid.json"),
                                                     "shape": [82, 50]}, InformationState.OBSERVATION, "Step 1 complete grid retained")
    question = InformationItem("historical_grouping", "not recovered", InformationState.QUESTION, "source narrative explicitly omits exact derivations")
    theatre = Theatre("Backward reconstruction from recorded source measurements and versioned historical constraints",
                      (context, observation, question),
                      ("no handwriting or annotation selection", "no target phrase used as an encoding criterion",
                       "historical and newer operator definitions remain distinct"))
    act = Act("test-reconstruction-candidates", "compute source-linked candidates, retain contradictions, and leave historical equivalence unresolved")
    ops = (
        Operation("numerical-expansion", (observation,), (InformationItem("nine_glyph_candidate", matrix_probe, InformationState.HYPOTHESIS, "existing numerical encoder plus declared layout choices"),), "Numerical expansion verified; proposed historical connection remains a hypothesis"),
        Operation("source-symbol-geometry", (observation,), (InformationItem("E_geometry_candidate", glyph_probe, InformationState.HYPOTHESIS, "explicit block-E geometric model"),), "Typographic model fits four-stroke formula but does not identify source-row transversals"),
        Operation("check-backward-constraints", (observation,), (InformationItem("constraint_results", constraints, InformationState.INFERENCE, "arithmetic and geometry checks"),), "No unsupported Greek or semantic output admitted"),
    )
    result = TAOResolver().resolve(theatre, act, ops)
    assert not result.enough and result.kind.value == "reversible_resolution"
    output.mkdir(parents=True)
    dump(output / "candidate_results.json", {"measurements": measurements, "numeric_expansion": matrix_probe, "source_glyph_geometry": glyph_probe, "constraints": constraints})
    dump(output / "tao_trace.json", {"theatre": to_plain(theatre), "act": to_plain(act), "operations": to_plain(ops), "result": to_plain(result),
                                     "validation_limit": "The parser backward check is structural; source provenance and arithmetic are checked independently above."})
    sources = [source / name for name in ("raw_grid.json", "numeric_grid.json", "manifest.json")]
    sources += [extractor, WOW / "sources/WowDecodeNarrative.md", WOW / "sources/v8-resolve-through-monads.md"]
    sources += list((WOW / "sources/operator-notes").glob("*.md"))
    dump(output / "manifest.json", {"run_id": output.name, "kind": "backward-reconstruction-probes", "executed_at_utc": datetime.now(timezone.utc).isoformat(),
                                    "inputs": [{"path": str(p.relative_to(REPO)).replace("\\", "/"), "sha256": digest(p)} for p in sources],
                                    "script_sha256": digest(Path(__file__)),
                                    "artifacts": [{"file": p.name, "sha256": digest(p)} for p in sorted(output.iterdir())],
                                    "historical_decode_reproduced": False})
    print(json.dumps({"encoded_groups": encoded, "row_major_grid": layouts[0]["glyph_grid"],
                      "diagonals": [layouts[0]["diagonal_1"], layouts[0]["diagonal_2"]], "center": layouts[0]["center_glyph"],
                      "source_sum": sum(recovered), "sum_numeral": namespace["greek"](sum(recovered)),
                      "E_intersection_degrees": [x["degree"] for x in intersections],
                      "resolver": result.kind.value, "enough": result.enough,
                      "historical_decode_reproduced": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
