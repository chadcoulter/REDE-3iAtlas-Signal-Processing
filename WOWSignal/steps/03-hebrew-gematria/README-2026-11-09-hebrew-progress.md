# Wow! progress report — full-channel Hebrew gematria and text streams

Date: November 9, 2026

Branch: `codex/wow-signal`

Repository baseline before this commit: `ba3b1396a74764d6bb012b28def5419ffb8d2ed4`

## Purpose and current state

Chad requested trying the 3I/ATLAS-style processing approach with Hebrew gematria, then clarified that the input should contain multiple readings from every channel, rather than just the six event readings. He subsequently requested the Hebrew as text streams, combined in one file.

The completed pass preserves **all 50 recorded channel streams, each with 82 readings: 4,100 source-linked measurements**. It supplies both a structured numerical-to-Hebrew representation and a single UTF-8 text export containing every stream. No intensity threshold, run grouping, word selection, or Greek operator execution was applied in this pass.

The preceding [return and 5 × 5 / 7 × 7 report](../02-grid-traversals/README-2026-11-09-return-and-5x5-7x7-progress.md) was already captured locally and is included with these changes for preservation. Its source-linked paths and candidate readings remain a separate exploratory branch.

## 1. Existing parser and 3I/ATLAS workflow review

The [repository summary](../../../README.md), [integration guide](../../../INTEGRATION_GUIDE.md), and existing source programs were inspected before selecting the Hebrew pass.

The recorded 3I/ATLAS experiment used extracted filterbank measurements, Greek numeral encoding, native eight-register operator bodies, three forward and three reverse passes with state feedback, and recurrence analysis. Its native runner expects Greek glyphs and an external assembly dependency. The integration guide also identifies typed mapping and automated Book II execution as integration work, rather than an already complete generic language decoder.

The copied V8 TAO implementation records declared operations but does not supply executable Hebrew letter semantics. No Hebrew encoder was found in the inspected parser files. Accordingly, the current work implements the **numerical encoding stage** for the already preserved Wow! printout data. It does not claim to have run a Hebrew version of the native state machine or to have extracted a Hebrew-language instruction.

## 2. Initial six-reading conversion and scope correction

The first read-only conversion examined the known event in channel 02, source rows 58–63:

| Row, one-based | Recorded bin | Additive components | Hebrew numeral |
|---:|---:|---|---|
| 58 | 6 | 6 | ו |
| 59 | 14 | 10 + 4 | יד |
| 60 | 26 | 20 + 6 | כו |
| 61 | 30 | 30 | ל |
| 62 | 19 | 10 + 9 | יט |
| 63 | 5 | 5 | ה |

Source token order is:

```text
ו | יד | כו | ל | יט | ה
```

Reversing measurement order while preserving each numeral's component order gives:

```text
ה | יט | ל | כו | יד | ו
```

The core total is 100, encoded ק. The earlier 34-reading context total is 104, encoded קד. These totals are arithmetic on the preserved bin labels, not calibrated energy estimates.

Chad then clarified: the output should have several lines from **each channel**. The next pass therefore covered the complete 82 × 50 source grid. It did not promote the six-reading example into the full input specification.

## 3. Value-preserving encoding conventions

The new [encoding script](../../scripts/step03_hebrew_gematria.py) uses ordinary Hebrew values 1–10, 20–90, and 100–400. Its selected spelling is descending additive numeral components, with traditional 15/16 spellings טו and טז. No special final-form values, punctuation, alternative letter combinations, or word segmentation are chosen.

Zero is retained as the literal token `0`. It is not silently omitted, mapped to a Hebrew letter, or treated as punctuation or closure. Raw blank source characters and their coordinates remain available in the structured CSV. A numerical zero bin does not establish zero physical radio power.

The chosen convention is one value-preserving spelling of a number. Gematria values do not determine unique words. Numerical conversion also differs from phonetic transliteration:

| Grouped numerical values | Earlier Greek numerals | Hebrew numerals |
|---|---|---|
| 1, 2, 100, 1 | Α Β Ρ Α | א ב ק א |
| 2, 3, 1, 8, 1, 4, 1 | Β Γ Α Η Α Δ Α | ב ג א ח א ד א |

Greek Ρ and Hebrew ק both represent 100. Hebrew ר represents 200. Consequently, writing ABRA phonetically as אברא would total 204 and would not preserve the earlier grouped total of 104. No pronunciation or word meaning was selected for the value-preserving Hebrew sequence.

The [Hebcal value table](https://www.hebcal.com/home/1824/numerical-values-of-hebrew-letters) and [Chabad alphabet reference](https://www.chabad.org/library/article_cdo/aid/4084597/jewish/The-Hebrew-Alphabet.htm) were consulted for the value convention. The source remains the repo's preserved measurements, not those references.

## 4. Full-channel run

The script reads [Step 1 run 001](../01-source-data/run-001.md), verifies the recorded hashes of raw_grid.json, numeric_grid.json, cells.csv, and row_metadata.csv, and checks their source-cell agreement before writing a new output directory.

The [new run README](run-001/README.md) describes the saved outputs:

- [streams.csv](run-001/streams.csv): 4,100 records, ordered by channel and then time. Stream IDs are WOW_CH01 through WOW_CH50, each with frames 0–81.
- [hebrew_grid.json](run-001/hebrew_grid.json): the same Hebrew tokens in their original 82-row × 50-channel alignment.
- [manifest.json](run-001/manifest.json): source and script hashes, encoding table and conventions, coverage results, and hashes of the generated README, CSV, and grid.

Each CSV reading retains its source row, channel, cell ID, original CSV/TXT position, printed EST time, elapsed seconds, raw character, blank flag, numeric bin, and Hebrew token. The field `gematria` is explicitly typed as `hebrew_standard_additive_numerals`. It must not be mistaken for the Greek input expected by the existing native runner.

Elapsed seconds preserve the printed time intervals rather than assuming uniform sampling. The printed second local oscillator setting is retained as instrument metadata; no absolute per-channel sky frequency was synthesized. Visual Hebrew right-to-left rendering does not change logical source order.

The run README includes six successive readings from every one of the 50 streams, at source rows 58–63. Those are examples; the CSV and grid preserve all 82 readings per channel.

## 5. Single-file Hebrew text export

Chad requested one combined file instead of separate channel files. The resulting [hebrew_streams.txt](run-001/hebrew_streams.txt) is a UTF-8 text file with:

- One introductory block explaining the conventions and identifying the source CSV hash.
- Fifty labeled Hebrew channel blocks, ערוץ 01 through ערוץ 50.
- All 82 chronological Hebrew numeral tokens in each block.
- Up to twelve tokens per line; line wrapping is for display only.
- All numerical zero tokens retained.

Tokens remain separated so that each source reading can be recovered. No new word boundaries, spacing interpretation, translation, or linguistic meaning was introduced. No separate per-channel files were created.

The export was generated after the original encoding run's manifest. That manifest remains unchanged and does not inventory this later text export. Export provenance is recorded here and in the text header:

```text
File: run-001/hebrew_streams.txt
Bytes: 10355
SHA-256: 9b096e25385b0c9289e0335ae28c04733d848061ef899b60aa720c9035bcf99a
```

## 6. Verification completed

The saved outputs were read back and checked independently against the source:

- All 4,100 Hebrew tokens sum to their original numerical bins.
- Exactly 50 streams each contain 82 chronological records.
- Source IDs are unique; the CSV and aligned grid agree at every source position.
- All run-manifest output hashes match the saved files.
- The encoder was checked across every possible printout bin, 0–35, including the explicit 15/16 spellings.
- All 50 channels appear in the README preview.
- A rerun into the existing output folder was refused, and the files' hashes remained unchanged.
- The combined text was parsed back into its 50 channel blocks; every one of its 4,100 tokens matches the corresponding CSV token exactly.

Before pushing, Git reported that automatic Windows line-ending conversion could change the hashed script and run files on a later checkout. The existing [WOWSignal attributes](../../.gitattributes) were extended to preserve those bytes, following the existing policy for source acquisitions and prior generated runs. The files were checked again against their hashes after applying that rule.

These checks establish numerical fidelity and reproducibility of the representation. Hebrew word interpretation, operator-state execution, directional feedback passes, and recurrence analysis remain subsequent work.

## 7. Reproduce the numerical encoding

From the repository root, choose a new output directory:

```powershell
python -X utf8 -B WOWSignal/scripts/step03_hebrew_gematria.py --output WOWSignal/steps/03-hebrew-gematria/run-002
```

Existing output directories are refused. No package installation is required; the encoder uses the Python standard library.

## 8. Reproduce the combined text from the saved CSV

The following Python block reproduces the text in memory and checks the existing export byte-for-byte. It writes no files. To create a future export elsewhere, use the resulting `rendered` string with an explicitly selected new destination.

```python
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

base = Path('WOWSignal/steps/03-hebrew-gematria/run-001')
source = base / 'streams.csv'
manifest = json.loads((base / 'manifest.json').read_text(encoding='utf-8'))
expected = next(a['sha256'] for a in manifest['artifacts']
                if a['filename'] == 'streams.csv')
assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
streams = defaultdict(list)
with source.open(encoding='utf-8', newline='') as handle:
    for row in csv.DictReader(handle):
        streams[int(row['channel_1based'])].append(row)
assert sorted(streams) == list(range(1,51))

blocks = [
    'זרמי גימטריה בעברית\n50 ערוצים; 82 קריאות בכל ערוץ.\n'
    '0 מציין ערך מספרי אפס. סדר הקריאות נשמר לפי המקור.\n'
    'כל שורת טקסט מכילה עד 12 קריאות; מעבר שורה הוא לצורכי תצוגה בלבד.\n'
    'מקור: streams.csv\nSHA-256: ' + expected
]
for channel in range(1,51):
    rows = streams[channel]
    assert len(rows) == 82
    assert [int(r['frame']) for r in rows] == list(range(82))
    tokens = [r['gematria'] for r in rows]
    lines = [f'ערוץ {channel:02d}']
    lines.extend(' '.join(tokens[i:i+12]) for i in range(0,82,12))
    blocks.append('\n'.join(lines))
rendered = '\n\n'.join(blocks) + '\n'
assert rendered.encode('utf-8') == (base / 'hebrew_streams.txt').read_bytes()
assert hashlib.sha256(rendered.encode('utf-8')).hexdigest() == (
    '9b096e25385b0c9289e0335ae28c04733d848061ef899b60aa720c9035bcf99a'
)
print('Combined Hebrew text reproduced: 50 streams, 82 readings each.')
```

## 9. Complete file inventory included with this progress push

Eight files are additions. One previously tracked file, WOWSignal/.gitattributes, is modified to preserve hashed bytes across checkouts. No file is deleted or renamed.

| Added file | Purpose |
|---|---|
| [Return and 5 × 5 / 7 × 7 report](../02-grid-traversals/README-2026-11-09-return-and-5x5-7x7-progress.md) | Previously captured, uncommitted status report |
| [step03_hebrew_gematria.py](../../scripts/step03_hebrew_gematria.py) | Full-channel Hebrew numerical encoder |
| [This Hebrew progress report](README-2026-11-09-hebrew-progress.md) | Scope, method, verification, export provenance, and reproduction |
| [Run README](run-001/README.md) | Run description and examples from all 50 channels |
| [streams.csv](run-001/streams.csv) | All 4,100 source-linked encoded readings |
| [hebrew_grid.json](run-001/hebrew_grid.json) | Original grid alignment with Hebrew tokens |
| [manifest.json](run-001/manifest.json) | Input, script, and original run-output provenance |
| [hebrew_streams.txt](run-001/hebrew_streams.txt) | All Hebrew channel streams in one text file |

| Modified file | Purpose |
|---|---|
| [WOWSignal/.gitattributes](../../.gitattributes) | Preserve the Hebrew script and generated run bytes across checkouts |

Source attribution remains Ohio SETI Data, PHL @ UPR Arecibo, with the upstream credit to MichaelHotaling's transcription; CC BY 4.0. The preserved upstream source commit is `28624a1eaf955ced940db347684cee61c8e4fd61`.
