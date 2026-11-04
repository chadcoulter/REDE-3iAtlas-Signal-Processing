#!/usr/bin/env python3
"""Step 1 only: preserve and validate the archived Wow! printout data."""
from __future__ import annotations

import argparse
import collections
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

SOURCE_COMMIT = "28624a1eaf955ced940db347684cee61c8e4fd61"
SOURCE_REPO = "https://github.com/planetaryhablab/Ohio-SETI"
FILES = {
    "oseti_19770815_220410.csv": ("oseti_19770815_220410.csv", "7f340d309ebb6a9b5c52eea125c13fa8160465dd"),
    "oseti_19770815_220410.txt": ("oseti_19770815_220410.txt", "093658ac810e4165200ca41e93e2a2710fb76375"),
    "oseti_19770815_220410.jpg": ("oseti_19770815_220410.jpg", None),
    "UPSTREAM_README.md": ("README.md", "c92b837b651ed4c0ddd97350fd8dc1ff4aebe256"),
}
CHANNELS = [f"{i:02d}" for i in range(1, 51)]
METADATA = ["RT. ASCEN", "DECLIN", "2ND LO FREQ", "GAL LAT", "GAL LON", "EASTERN STD TIME"]
CODING_SOURCE = "https://bigear.org/6equj5.htm"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def blob_sha(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()


def decode(character):
    # The stored integer is the printed bin label, not an exact measured amplitude.
    if character == " ":
        return 0
    if character in "0123456789":
        return int(character)
    if character in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return ord(character) - ord("A") + 10
    raise ValueError(f"Unexpected intensity character: {character!r}")


def encode(value):
    return " " if value == 0 else str(value) if value < 10 else chr(ord("A") + value - 10)


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run(source_dir, output):
    require(not output.exists(), "Output already exists; use a new run directory to retain prior attempts.")
    inventory = []
    for local, (original, expected) in FILES.items():
        path = source_dir / local
        require(path.is_file(), f"Missing source: {path}")
        raw = path.read_bytes()
        actual = blob_sha(raw)
        require(expected is None or actual == expected, f"Source blob mismatch: {local}")
        inventory.append({
            "local_path": path.relative_to(source_dir.parent.parent).as_posix(),
            "original_filename": original,
            "source_url": f"{SOURCE_REPO}/blob/{SOURCE_COMMIT}/{original}",
            "retrieved_utc_date": "2026-11-04",
            "bytes": len(raw), "sha256": sha256(path), "git_blob_sha1": actual,
            "expected_git_blob_sha1": expected,
            "verification": "matches connector-returned blob" if expected else "downloaded from pinned commit; SHA-256 recorded",
        })
    require((source_dir / "oseti_19770815_220410.jpg").read_bytes().startswith(bytes.fromhex("ffd8")), "Scan is not a JPEG")
    with (source_dir / "oseti_19770815_220410.csv").open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == CHANNELS + METADATA, "Unexpected CSV header or orientation")
        rows = list(reader)
    require(len(rows) == 82, "Expected 82 data rows")
    require(all(None not in r and all(v is not None for v in r.values()) for r in rows), "Malformed CSV row")
    grid = [[row[c] for c in CHANNELS] for row in rows]
    require(all(len(cell) == 1 for row in grid for cell in row), "Each intensity cell must contain exactly one character")
    txt = (source_dir / "oseti_19770815_220410.txt").read_text(encoding="utf-8").splitlines()
    require(len(txt) == len(rows), "CSV/TXT row counts differ")
    differences = [(r, c + 1) for r, row in enumerate(grid) for c, raw in enumerate(row) if len(txt[r]) <= c or txt[r][c] != raw]
    require(not differences, f"CSV/TXT intensity differences: {differences[:10]}")
    # Fixed-width intensity region is the first 50 characters; retain original metadata strings.
    metadata_pattern = re.compile(
        r"^\s*(\d{2}\s+\d{2}\s+\d{2})\s+([+-]?)\s*(\d{2}\s+\d{2})"
        r"\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)\s+([+-]?\d+\.\d+)"
        r"\s+(\d{2}\s+\d{2}\s+\d{2})\s*$")
    for index, (row, line) in enumerate(zip(rows, txt)):
        match = metadata_pattern.fullmatch(line[50:])
        require(match is not None, f"Unparsed TXT metadata at row {index}")
        ra, sign, decl, lo, lat, lon, time = match.groups()
        values = [" ".join(ra.split()), sign + " ".join(decl.split()), lo, lat, lon, " ".join(time.split())]
        require(values == [row[k] for k in METADATA], f"CSV/TXT metadata differs at row {index}")
    numeric = [[decode(cell) for cell in row] for row in grid]
    require(all(encode(n) == raw for row, nrow in zip(grid, numeric) for raw, n in zip(row, nrow)), "Character/bin round trip failed")
    counts = collections.Counter(raw for row in grid for raw in row)
    anomalies = []
    parsed_times = []
    for index, row in enumerate(rows):
        parts = [int(v) for v in row["EASTERN STD TIME"].split()]
        h, m, s = parts
        if not (0 <= h < 24 and 0 <= m < 60 and 0 <= s < 60):
            anomalies.append({"row_0based": index, "source_csv_line": index + 2, "field": "EASTERN STD TIME", "value": row["EASTERN STD TIME"], "issue": "not a valid clock time; source retained unchanged"})
            parsed_times.append(None)
        else:
            parsed_times.append(h * 3600 + m * 60 + s)
    deltas = []
    for index in range(1, len(rows)):
        if parsed_times[index - 1] is None or parsed_times[index] is None:
            continue
        delta = parsed_times[index] - parsed_times[index - 1]
        deltas.append(delta)
        if delta not in (11, 12, 13):
            anomalies.append({"row_0based": index, "previous_row_0based": index - 1, "field": "EASTERN STD TIME", "issue": "printed interval outside 11–13 seconds; no resampling or correction", "delta_seconds": delta})
    sequence = "".join(row[1] for row in grid)
    positions = [i for i in range(len(sequence) - 5) if sequence[i:i + 6] == "6EQUJ5"]
    require(len(positions) == 1, "Expected exactly one 6EQUJ5 occurrence in channel 02")
    start = positions[0]
    reference = [{
        "row_0based": r, "row_1based": r + 1, "channel_1based": 2,
        "source_csv_line": r + 2, "raw_character": grid[r][1], "numeric_bin": numeric[r][1],
        "eastern_std_time_printed": rows[r]["EASTERN STD TIME"],
    } for r in range(start, start + 6)]
    require([r["numeric_bin"] for r in reference] == [6, 14, 26, 30, 19, 5], "Reference-bin mismatch")
    output.mkdir(parents=True)
    metadata_rows = [{"row_0based": i, "row_1based": i + 1, "source_csv_line": i + 2, "source_txt_line": i + 1, **row} for i, row in enumerate(rows)]
    # Emit only row metadata here; the original CSV remains unchanged.
    meta_fields = ["row_0based", "row_1based", "source_csv_line", "source_txt_line"] + METADATA
    with (output / "row_metadata.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=meta_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(metadata_rows)
    axes = {
        "array_shape": [82, 50],
        "array_indexing": "grid[row_0based][channel_0based]",
        "axis_0": "time rows, top to bottom in source order",
        "axis_1": "frequency-channel columns, left to right as printed labels 01..50",
        "channel_number": "channel_0based + 1",
        "absolute_frequency_policy": "not reconstructed; retain the printed second LO frequency as metadata",
        "timing_policy": "preserve printed EASTERN STD TIME strings; no uniform-time assumption or automatic repairs",
    }
    write_json(output / "raw_grid.json", {"axes": axes, "blank_character": " ", "grid": grid})
    write_json(output / "numeric_grid.json", {
        "axes": axes, "representation": "integer intensity-bin labels",
        "coding_source": CODING_SOURCE,
        "blank_policy": "space becomes bin 0; original space retained in raw_grid and cells.csv",
        "precision": "bins represent truncated baseline-subtracted/rms-scaled intensities; no sub-bin measurement is recovered",
        "rollover_policy": "use ordinary 0..35 printed labels; no rollover reconstructed",
        "grid": numeric,
    })
    fields = ["row_0based", "channel_0based", "row_1based", "channel_1based", "source_csv_line", "source_csv_column_1based", "source_txt_line", "source_txt_character_1based", "raw_character", "is_blank", "numeric_bin", "nominal_bin_lower_inclusive", "nominal_bin_upper_exclusive"] + METADATA
    with (output / "cells.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for r, row in enumerate(grid):
            for c, raw in enumerate(row):
                n = numeric[r][c]
                writer.writerow({
                    "row_0based": r, "channel_0based": c, "row_1based": r + 1, "channel_1based": c + 1,
                    "source_csv_line": r + 2, "source_csv_column_1based": c + 1,
                    "source_txt_line": r + 1, "source_txt_character_1based": c + 1,
                    "raw_character": raw, "is_blank": raw == " ", "numeric_bin": n,
                    "nominal_bin_lower_inclusive": n, "nominal_bin_upper_exclusive": n + 1,
                    **{key: rows[r][key] for key in METADATA},
                })
    validation = {
        "status": "PASS_WITH_SOURCE_METADATA_FLAGS",
        "intensity_cells": 4100, "csv_txt_intensity_matches": 4100, "csv_txt_intensity_differences": 0,
        "csv_txt_metadata_rows_matched": 82, "all_cells_character_bin_round_trip": True,
        "blank_cells": counts[" "], "nonblank_cells": 4100 - counts[" "],
        "character_distribution": dict(sorted(counts.items())),
        "printed_first_time": rows[0]["EASTERN STD TIME"], "printed_last_time": rows[-1]["EASTERN STD TIME"],
        "valid_adjacent_printed_time_delta_counts": dict(sorted(collections.Counter(deltas).items())),
        "source_metadata_flags": anomalies,
        "known_sequence_spot_check": reference,
        "scan_review": "human-style visual inspection by assistant: orientation and visible 6EQUJ5 spot-checked; not a cell-by-cell transcription audit",
        "independence_limit": "CSV and TXT belong to the same published transcription; agreement does not independently validate all cells against the scan",
        "historical_identity_limit": "archive matches narrative dimensions and sequence; exact identity with the file used in the earlier investigation is unconfirmed",
        "later_steps_executed": False,
    }
    write_json(output / "validation.json", validation)
    now = datetime.now(timezone.utc)
    try:
        client_time = now.astimezone(ZoneInfo("America/Chicago")).isoformat()
    except Exception:
        client_time = "America/Chicago; execution UTC timestamp retained separately"
    script = Path(__file__).resolve()
    artifacts = [{"filename": p.name, "bytes": p.stat().st_size, "sha256": sha256(p)} for p in sorted(output.iterdir()) if p.is_file()]
    manifest = {
        "run_id": output.name, "step": 1, "executed_at_utc": now.isoformat(),
        "executed_at_america_chicago": client_time, "source_repository": SOURCE_REPO, "source_commit": SOURCE_COMMIT,
        "attribution": "Ohio SETI Data, PHL @ UPR Arecibo; source credits MichaelHotaling for original transcription",
        "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/",
        "sources": inventory, "script": {"path": "WOWSignal/scripts/step01_data_pass.py", "sha256": sha256(script)},
        "python_version": __import__("sys").version, "artifacts": artifacts,
    }
    write_json(output / "manifest.json", manifest)
    print(json.dumps({"output": str(output), "shape": [82,50], "matched_intensity_cells": 4100,
        "matched_metadata_rows": 82, "blank_cells": counts[" "], "flags": anomalies,
        "reference_sequence": reference, "manifest": str(output / "manifest.json")}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="A new result folder; existing folders are never overwritten")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    run(root / "data/ohio-seti", args.output.resolve())


if __name__ == "__main__":
    main()
