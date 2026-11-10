"""Encode every preserved Wow! channel reading as value-preserving Hebrew numerals."""

import argparse
import csv
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


LETTERS = "אבגדהוזחטיכלמנסעפצקרשת"
VALUES = list(range(1, 11)) + [20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400]
TABLE = list(zip(VALUES, LETTERS))
LETTER_VALUES = dict(zip(LETTERS, VALUES))
ENCODING = "hebrew_standard_additive_numerals"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def hebrew(number):
    require(isinstance(number, int) and 0 <= number <= 35, "Expected a preserved integer bin from 0 to 35")
    if number == 0:
        return "0"
    # Traditional numeral spellings avoid yod-he and yod-vav for 15 and 16.
    if number == 15:
        return "טו"
    if number == 16:
        return "טז"
    remainder = number
    result = ""
    for value, letter in reversed(TABLE):
        while remainder >= value:
            result += letter
            remainder -= value
    return result


def seconds(clock):
    hour, minute, second = map(int, clock.split())
    return 3600 * hour + 60 * minute + second


def run(output):
    wow = Path(__file__).resolve().parents[1]
    repo = wow.parent
    source = wow / "steps/01-source-data/run-001"
    require(not output.exists(), "Use a new output folder; existing runs are never overwritten")
    manifest_path = source / "manifest.json"
    original_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = {item["filename"]: item["sha256"] for item in original_manifest["artifacts"]}
    names = ["raw_grid.json", "numeric_grid.json", "cells.csv", "row_metadata.csv"]
    inputs = []
    for name in names:
        path = source / name
        actual = digest(path)
        require(actual == expected[name], f"Step 1 hash mismatch: {name}")
        inputs.append({"path": path.relative_to(repo).as_posix(), "sha256": actual, "bytes": path.stat().st_size})
    raw = json.loads((source / "raw_grid.json").read_text(encoding="utf-8"))["grid"]
    numeric = json.loads((source / "numeric_grid.json").read_text(encoding="utf-8"))["grid"]
    require(len(raw) == len(numeric) == 82, "Expected 82 rows")
    require(all(len(row) == 50 for row in raw + numeric), "Expected 50 channels in every row")
    with (source / "cells.csv").open(encoding="utf-8-sig", newline="") as handle:
        source_cells = list(csv.DictReader(handle))
    cells = {(int(item["row_0based"]), int(item["channel_0based"])): item for item in source_cells}
    require(len(source_cells) == len(cells) == 4100, "Expected 4100 unique source cells")
    with (source / "row_metadata.csv").open(encoding="utf-8-sig", newline="") as handle:
        metadata = list(csv.DictReader(handle))
    require(len(metadata) == 82, "Expected 82 metadata records")
    require([int(item["row_0based"]) for item in metadata] == list(range(82)), "Unexpected metadata order")
    clocks = [seconds(item["EASTERN STD TIME"]) for item in metadata]
    require(all(b > a for a, b in zip(clocks, clocks[1:])), "Expected increasing printed times on this page")
    elapsed = [clock - clocks[0] for clock in clocks]
    encoded = [[hebrew(value) for value in row] for row in numeric]
    records = []
    for channel in range(50):
        for row in range(82):
            item = cells[row, channel]
            value = numeric[row][channel]
            require(item["raw_character"] == raw[row][channel], "Raw source-cell disagreement")
            require(int(item["numeric_bin"]) == value, "Numeric source-cell disagreement")
            token = encoded[row][channel]
            decoded = 0 if token == "0" else sum(LETTER_VALUES[letter] for letter in token)
            require(decoded == value, "Hebrew numeral does not preserve the source value")
            records.append({
                "stream_id": f"WOW_CH{channel+1:02d}",
                "frame": row,
                "seconds": elapsed[row],
                "row_1based": row + 1,
                "channel_1based": channel + 1,
                "source_cell_id": row * 50 + channel,
                "source_csv_line": item["source_csv_line"],
                "source_csv_column_1based": item["source_csv_column_1based"],
                "source_txt_line": item["source_txt_line"],
                "source_txt_character_1based": item["source_txt_character_1based"],
                "printed_est": metadata[row]["EASTERN STD TIME"],
                "printed_second_lo_mhz": metadata[row]["2ND LO FREQ"],
                "raw_character": raw[row][channel],
                "is_blank": raw[row][channel] == " ",
                "numeric_bin": value,
                "gematria": token,
                "encoding_namespace": ENCODING,
                "measurement_kind": "normalized_intensity_bin_label",
            })
    counts = Counter(item["stream_id"] for item in records)
    require(len(counts) == 50 and set(counts.values()) == {82}, "Incomplete stream coverage")
    require(len({item["source_cell_id"] for item in records}) == 4100, "Duplicate or missing source occurrence")
    require([numeric[row][1] for row in range(57, 63)] == [6, 14, 26, 30, 19, 5], "Unexpected event sequence")
    require([encoded[row][1] for row in range(57, 63)] == ["ו", "יד", "כו", "ל", "יט", "ה"], "Unexpected event encoding")

    output.mkdir(parents=True, exist_ok=False)
    with (output / "streams.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)
    write_json(output / "hebrew_grid.json", {
        "axes": {"shape": [82, 50], "indexing": "grid[row_0based][channel_0based]",
                 "row_axis": "printed time order", "column_axis": "printed channels 01..50"},
        "encoding_namespace": ENCODING,
        "zero_policy": "String 0 retains numerical bin zero; it is not punctuation or closure",
        "grid": encoded,
    })
    example_times = ", ".join(metadata[row]["EASTERN STD TIME"].replace(" ", ":") for row in range(57, 63))
    preview = ["| Stream | Numeric bins, source rows 58–63 | Hebrew tokens, same order |",
               "|---|---|---|"]
    for channel in range(50):
        nums = ", ".join(str(numeric[row][channel]) for row in range(57, 63))
        glyphs = " / ".join(encoded[row][channel] for row in range(57, 63))
        preview.append(f"| WOW_CH{channel+1:02d} | {nums} | {glyphs} |")
    readme = "\n".join([
        "# Wow! full-channel Hebrew gematria — run 001", "",
        "Date: November 9, 2026", "",
        "## Scope", "",
        "This data pass encodes all 50 recorded channel streams, with 82 readings per stream: **4,100 source-linked records**. It does not select only the six event readings, threshold low bins, group nonzero runs, or apply the earlier Greek operator meanings to Hebrew characters.", "",
        "The input is the preserved Step 1 printout transcription. These are normalized intensity-bin labels, not raw waveforms or recovered continuous amplitudes. Raw blanks and source coordinates remain in the CSV. A zero token preserves bin zero; it is not a word boundary, punctuation, or evidence of zero physical radio power.", "",
        "## Outputs", "",
        "- [streams.csv](streams.csv): one reading per line, ordered by stream ID and then source frame. Every channel has 82 lines; frame is zero-based and source row/channel are one-based.",
        "- [hebrew_grid.json](hebrew_grid.json): the same Hebrew tokens in the original 82-row by 50-channel alignment.",
        "- [manifest.json](manifest.json): input and script hashes, encoding table, conventions, coverage checks, and output hashes.", "",
        "## Encoding and time conventions", "",
        "Use ordinary Hebrew letter values 1–10, 20–90, and 100–400. This pass chooses descending additive numeral spelling; 15 and 16 use טו and טז. No final-form value extension, punctuation marks, word segmentation, or alternate spellings are selected. This is one value-preserving representation, not an inversion to unique Hebrew words.", "",
        "The CSV field gematria contains Hebrew numerals, explicitly typed by encoding_namespace. It is not input to the existing Greek-only native operator runner without a separate Hebrew operator mapping. The copied V8 record scaffold likewise supplies no executable Hebrew transformation semantics.", "",
        "Elapsed seconds come from the printed EST timestamps relative to the first row, preserving the recorded irregular intervals. The printed second local oscillator setting is retained as instrument metadata; no absolute per-channel sky frequency is inferred. Token order follows the source; visual right-to-left rendering must not reverse the time axis or channels.", "",
        "## Examples from every channel", "",
        f"The following are six successive readings from **each** stream, at printed EST times {example_times}. These are examples only; all 82 readings per channel are in streams.csv.", "",
        *preview, "",
        "## Verification", "",
        "Before writing, the runner verifies all four Step 1 input hashes against their recorded manifest, matches raw and numeric cells to the source table, checks all 4,100 Hebrew value round trips, verifies unique source IDs and 82 readings in each of 50 streams, and checks the event conversion. Numerical identity checks do not establish a linguistic reading.", "",
        "## Repeat", "", "```powershell",
        "python -X utf8 -B WOWSignal/scripts/step03_hebrew_gematria.py --output WOWSignal/steps/03-hebrew-gematria/run-002",
        "```", "",
        "Use a new folder; existing runs are refused. Source files and prior reports are not modified. Numeric grids and CSV contents are deterministic; the manifest records its execution time separately.", "",
        "Source attribution: Ohio SETI Data, PHL @ UPR Arecibo; upstream credits MichaelHotaling's transcription. CC BY 4.0. Pinned upstream commit: " + original_manifest["source_commit"] + ".", "",
    ])
    (output / "README.md").write_text(readme, encoding="utf-8", newline="\n")
    script = Path(__file__).resolve()
    artifacts = [{"filename": path.name, "bytes": path.stat().st_size, "sha256": digest(path)}
                 for path in sorted(output.iterdir()) if path.is_file()]
    manifest = {
        "run_id": output.name,
        "step": "03-hebrew-gematria",
        "executed_at_utc": datetime.now(timezone.utc).isoformat(),
        "report_date_america_chicago": "2026-11-09",
        "input_manifest": {"path": manifest_path.relative_to(repo).as_posix(), "sha256": digest(manifest_path)},
        "inputs": inputs,
        "script": {"path": script.relative_to(repo).as_posix(), "sha256": digest(script)},
        "source_repository": original_manifest["source_repository"],
        "source_commit": original_manifest["source_commit"],
        "attribution": original_manifest["attribution"],
        "license": original_manifest["license"],
        "encoding": {"namespace": ENCODING, "letter_values": LETTER_VALUES,
                     "ordering": "descending additive numeral components",
                     "exceptions": {"15": "טו", "16": "טז"},
                     "zero_token": "0", "final_forms": "not selected",
                     "source_values": "preserved integer bins; no new rounding"},
        "stream_order": "channel ascending, then frame ascending",
        "time_reference": "printed EST relative to source row 1; not a corrected physical integration epoch",
        "operator_execution": "none; Hebrew operator mapping is not defined by this encoder",
        "validation": {"source_input_hashes_verified": 4, "records": len(records),
                       "streams": len(counts), "readings_per_stream": dict(sorted(counts.items())),
                       "unique_source_occurrences": 4100, "value_roundtrips": 4100,
                       "blank_cells_retained": sum(item["is_blank"] for item in records),
                       "zero_bins_retained": sum(item["numeric_bin"] == 0 for item in records)},
        "artifacts": artifacts,
    }
    write_json(output / "manifest.json", manifest)
    print(json.dumps({"output": str(output), "streams": 50, "readings_per_stream": 82,
                      "records": len(records), "event_hebrew_tokens": [encoded[row][1] for row in range(57, 63)]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="New output directory; existing paths are refused")
    args = parser.parse_args()
    run(args.output.resolve())
