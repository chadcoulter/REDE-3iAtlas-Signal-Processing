#!/usr/bin/env python3
"""Step 2: deterministic traversals of the preserved measurement grid only."""
import argparse
import collections
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def require(value, message):
    if not value:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8", newline="\n")


def run(output):
    wow = Path(__file__).resolve().parents[1]
    previous = wow / "steps/01-source-data/run-001"
    require(not output.exists(), "Use a new output directory; existing runs are preserved.")
    old_manifest = json.loads((previous / "manifest.json").read_text(encoding="utf-8"))
    expected = {x["filename"]: x["sha256"] for x in old_manifest["artifacts"]}
    inputs = ["raw_grid.json", "numeric_grid.json", "cells.csv"]
    for name in inputs:
        require(digest(previous / name) == expected[name], f"Step 1 artifact hash mismatch: {name}")
    raw = json.loads((previous / "raw_grid.json").read_text(encoding="utf-8"))["grid"]
    numeric = json.loads((previous / "numeric_grid.json").read_text(encoding="utf-8"))["grid"]
    height, width = len(raw), len(raw[0])
    require((height, width) == (82, 50), "Unexpected source dimensions.")
    with (previous / "cells.csv").open(encoding="utf-8", newline="") as f:
        source_cells = list(csv.DictReader(f))
    cells = {(int(x["row_0based"]), int(x["channel_0based"])): x for x in source_cells}
    require(len(cells) == height * width, "Incomplete source-cell coordinates.")
    for (r, c), item in cells.items():
        require(item["raw_character"] == raw[r][c] and int(item["numeric_bin"]) == numeric[r][c], "Step 1 representations disagree.")
    families = {"H": [], "V": [], "DR": [], "DL": []}
    for r in range(height):
        families["H"].append([(r, c) for c in range(width)])
    for c in range(width):
        families["V"].append([(r, c) for r in range(height)])
    for family, dc in [("DR", 1), ("DL", -1)]:
        starts = [(0, c) for c in range(width)] + [(r, 0 if dc == 1 else width - 1) for r in range(1, height)]
        for r, c in starts:
            coordinates = []
            while r < height and 0 <= c < width:
                coordinates.append((r, c))
                r, c = r + 1, c + dc
            families[family].append(coordinates)
    paths = []
    memberships = collections.defaultdict(list)
    triples = []
    triple_counts = collections.Counter()
    coverage = {name: collections.Counter() for name in families}
    deltas = {"H": (0, 1), "V": (1, 0), "DR": (1, 1), "DL": (1, -1)}
    for family, group in families.items():
        for index, coordinates in enumerate(group):
            base_id = f"{family}-{index:03d}"
            forward_ids = [r * width + c for r, c in coordinates]
            forward_values = [numeric[r][c] for r, c in coordinates]
            for r, c in coordinates:
                coverage[family][r, c] += 1
            for reverse in (False, True):
                ordered = coordinates[::-1] if reverse else coordinates
                path_id = base_id + ("-R" if reverse else "-F")
                ids = [r * width + c for r, c in ordered]
                values = [numeric[r][c] for r, c in ordered]
                chars = "".join(raw[r][c] for r, c in ordered)
                dr, dc = deltas[family]
                paths.append({
                    "id": path_id, "family": family, "order": "reverse" if reverse else "forward",
                    "reverse_partner": base_id + ("-F" if reverse else "-R"),
                    "start_0based": list(ordered[0]), "end_0based": list(ordered[-1]),
                    "direction_delta": [-dr, -dc] if reverse else [dr, dc],
                    "direction_changes_within_path": 0, "cell_ids": ids,
                    "raw_characters": chars, "numeric_bins": values,
                })
                for offset, (r, c) in enumerate(ordered):
                    memberships[r, c].append((path_id, offset))
                if reverse:
                    require(ids == forward_ids[::-1] and values == forward_values[::-1], "Reverse path mismatch.")
                for offset in range(max(0, len(ordered) - 2)):
                    selected = ids[offset:offset + 3]
                    ns = values[offset:offset + 3]
                    triples.append([path_id, offset, *selected, *ns])
                    if not reverse:
                        triple_counts[tuple(ns)] += 1
    for family, counts in coverage.items():
        require(len(counts) == height * width and set(counts.values()) == {1}, f"Coverage failure: {family}")
    require(all(len(v) == 8 for v in memberships.values()), "Each cell should have four forward and four reverse memberships.")
    lookup = {p["id"]: p for p in paths}
    for (r, c), entries in memberships.items():
        for path_id, offset in entries:
            p = lookup[path_id]
            require(p["cell_ids"][offset] == r * width + c, "Intersection provenance mismatch.")
            require(p["numeric_bins"][offset] == numeric[r][c] and p["raw_characters"][offset] == raw[r][c], "Path/source mismatch.")
    output.mkdir(parents=True)
    dump(output / "paths.json", {
        "scope": "source measurements only; no handwriting, scan annotations, narrative-derived row selection, threshold filtering, Greek mapping, or semantic interpretation",
        "source_shape": [height, width], "cell_id_rule": "row_0based * 50 + channel_0based",
        "family_rules": {"H": "all rows left to right", "V": "all columns top to bottom", "DR": "all maximal down-right diagonals", "DL": "all maximal down-left diagonals"},
        "blank_policy": "preserve spaces and their numeric bin zero; never drop cells",
        "diagonal_start_order": "top edge left to right, then remaining rows along the applicable side",
        "singleton_policy": "retain length-one diagonals and their reverse partners; count them explicitly",
        "paths": paths,
    })
    with (output / "intersections.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        fields = ["cell_id", "row_0based", "channel_0based", "row_1based", "channel_1based", "raw_character", "numeric_bin"]
        for family in families:
            fields += [family + "_forward_path", family + "_forward_offset", family + "_reverse_path", family + "_reverse_offset"]
        writer.writerow(fields)
        for r in range(height):
            for c in range(width):
                row = [r * width + c, r, c, r + 1, c + 1, raw[r][c], numeric[r][c]]
                entries = dict(memberships[r, c])
                for family in families:
                    for suffix in ("-F", "-R"):
                        matching = [(key, value) for key, value in entries.items() if key.startswith(family + "-") and key.endswith(suffix)]
                        require(len(matching) == 1, "Ambiguous family membership.")
                        row += list(matching[0])
                writer.writerow(row)
    with (output / "triples.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["path_id", "start_offset", "cell_id_1", "cell_id_2", "cell_id_3", "bin_1", "bin_2", "bin_3"])
        writer.writerows(triples)
    with (output / "triple_counts.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["bin_1", "bin_2", "bin_3", "forward_occurrences"])
        writer.writerows([*key, count] for key, count in sorted(triple_counts.items()))
    summary = {
        "status": "TRAVERSAL_EXTRACTION_COMPLETE_HISTORICAL_SELECTION_UNRESOLVED",
        "shape": [height, width], "cells": height * width,
        "forward_paths_by_family": {name: len(v) for name, v in families.items()},
        "forward_paths": len(paths) // 2, "including_reverse_paths": len(paths),
        "singleton_forward_paths": sum(len(p["cell_ids"]) == 1 for p in paths if p["order"] == "forward"),
        "source_cell_visits_forward": sum(len(p["cell_ids"]) for p in paths if p["order"] == "forward"),
        "source_cell_visits_with_reverse": sum(len(p["cell_ids"]) for p in paths),
        "intersections": len(memberships), "memberships_per_cell": 8,
        "three_cell_windows_with_reverse": len(triples),
        "three_cell_windows_forward": sum(triple_counts.values()),
        "distinct_numeric_triples_forward": len(triple_counts),
        "most_common_forward_triples": [{"bins": list(key), "count": count} for key, count in triple_counts.most_common(5)],
        "validation": {"step1_hashes": True, "all_cells_preserved_once_per_forward_family": True, "all_reverse_partners_exact": True, "all_path_and_intersection_values_match_source": True},
        "interpretation": "Three-cell windows are exhaustive candidate windows, not the historical three nested triples. Shared cell positions are geometric intersections, not proof of a semantic center.",
        "unresolved": ["selection of the original top/middle/bottom horizontal paths", "historical nested grouping and path switching", "historical 3x3 reduction", "original Greek transformation rules"],
        "later_transform_steps_executed": False,
    }
    dump(output / "summary.json", summary)
    manifest = {
        "step": 2, "run_id": output.name, "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "parent": "../01-source-data/run-001", "source_commit": old_manifest["source_commit"],
        "inputs": [{"path": str((previous / name).relative_to(wow)).replace("\\", "/"), "sha256": digest(previous / name)} for name in inputs + ["manifest.json"]],
        "script": {"path": "scripts/step02_grid_traversals.py", "sha256": digest(Path(__file__))},
        "artifacts": [{"file": p.name, "bytes": p.stat().st_size, "sha256": digest(p)} for p in sorted(output.iterdir()) if p.is_file()],
        "annotation_policy": "no image or annotation file is opened by this script",
    }
    dump(output / "manifest.json", manifest)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.output.resolve())
