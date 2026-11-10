# Wow! full-channel Hebrew gematria — run 001

Date: November 9, 2026

## Scope

This data pass encodes all 50 recorded channel streams, with 82 readings per stream: **4,100 source-linked records**. It does not select only the six event readings, threshold low bins, group nonzero runs, or apply the earlier Greek operator meanings to Hebrew characters.

The input is the preserved Step 1 printout transcription. These are normalized intensity-bin labels, not raw waveforms or recovered continuous amplitudes. Raw blanks and source coordinates remain in the CSV. A zero token preserves bin zero; it is not a word boundary, punctuation, or evidence of zero physical radio power.

## Outputs

- [streams.csv](streams.csv): one reading per line, ordered by stream ID and then source frame. Every channel has 82 lines; frame is zero-based and source row/channel are one-based.
- [hebrew_grid.json](hebrew_grid.json): the same Hebrew tokens in the original 82-row by 50-channel alignment.
- [manifest.json](manifest.json): input and script hashes, encoding table, conventions, coverage checks, and output hashes.

## Encoding and time conventions

Use ordinary Hebrew letter values 1–10, 20–90, and 100–400. This pass chooses descending additive numeral spelling; 15 and 16 use טו and טז. No final-form value extension, punctuation marks, word segmentation, or alternate spellings are selected. This is one value-preserving representation, not an inversion to unique Hebrew words.

The CSV field gematria contains Hebrew numerals, explicitly typed by encoding_namespace. It is not input to the existing Greek-only native operator runner without a separate Hebrew operator mapping. The copied V8 record scaffold likewise supplies no executable Hebrew transformation semantics.

Elapsed seconds come from the printed EST timestamps relative to the first row, preserving the recorded irregular intervals. The printed second local oscillator setting is retained as instrument metadata; no absolute per-channel sky frequency is inferred. Token order follows the source; visual right-to-left rendering must not reverse the time axis or channels.

## Examples from every channel

The following are six successive readings from **each** stream, at printed EST times 22:15:35, 22:15:47, 22:15:59, 22:16:10, 22:16:22, 22:16:34. These are examples only; all 82 readings per channel are in streams.csv.

| Stream | Numeric bins, source rows 58–63 | Hebrew tokens, same order |
|---|---|---|
| WOW_CH01 | 0, 1, 0, 0, 2, 0 | 0 / א / 0 / 0 / ב / 0 |
| WOW_CH02 | 6, 14, 26, 30, 19, 5 | ו / יד / כו / ל / יט / ה |
| WOW_CH03 | 0, 2, 0, 3, 1, 1 | 0 / ב / 0 / ג / א / א |
| WOW_CH04 | 2, 4, 1, 1, 0, 0 | ב / ד / א / א / 0 / 0 |
| WOW_CH05 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH06 | 0, 0, 1, 0, 0, 0 | 0 / 0 / א / 0 / 0 / 0 |
| WOW_CH07 | 0, 3, 6, 1, 3, 0 | 0 / ג / ו / א / ג / 0 |
| WOW_CH08 | 0, 0, 0, 0, 1, 0 | 0 / 0 / 0 / 0 / א / 0 |
| WOW_CH09 | 0, 0, 1, 0, 0, 0 | 0 / 0 / א / 0 / 0 / 0 |
| WOW_CH10 | 0, 1, 0, 0, 3, 0 | 0 / א / 0 / 0 / ג / 0 |
| WOW_CH11 | 0, 2, 2, 0, 0, 0 | 0 / ב / ב / 0 / 0 / 0 |
| WOW_CH12 | 0, 0, 0, 0, 1, 0 | 0 / 0 / 0 / 0 / א / 0 |
| WOW_CH13 | 0, 0, 0, 0, 1, 0 | 0 / 0 / 0 / 0 / א / 0 |
| WOW_CH14 | 0, 1, 1, 3, 1, 0 | 0 / א / א / ג / א / 0 |
| WOW_CH15 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH16 | 3, 2, 0, 7, 0, 1 | ג / ב / 0 / ז / 0 / א |
| WOW_CH17 | 1, 1, 1, 0, 1, 0 | א / א / א / 0 / א / 0 |
| WOW_CH18 | 0, 0, 0, 0, 1, 0 | 0 / 0 / 0 / 0 / א / 0 |
| WOW_CH19 | 0, 1, 0, 1, 0, 1 | 0 / א / 0 / א / 0 / א |
| WOW_CH20 | 0, 0, 0, 0, 1, 0 | 0 / 0 / 0 / 0 / א / 0 |
| WOW_CH21 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH22 | 0, 0, 1, 0, 1, 0 | 0 / 0 / א / 0 / א / 0 |
| WOW_CH23 | 0, 0, 0, 0, 2, 0 | 0 / 0 / 0 / 0 / ב / 0 |
| WOW_CH24 | 1, 0, 0, 0, 0, 0 | א / 0 / 0 / 0 / 0 / 0 |
| WOW_CH25 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH26 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH27 | 2, 0, 0, 0, 0, 0 | ב / 0 / 0 / 0 / 0 / 0 |
| WOW_CH28 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH29 | 1, 1, 0, 0, 0, 0 | א / א / 0 / 0 / 0 / 0 |
| WOW_CH30 | 1, 0, 0, 0, 0, 0 | א / 0 / 0 / 0 / 0 / 0 |
| WOW_CH31 | 0, 3, 0, 0, 2, 1 | 0 / ג / 0 / 0 / ב / א |
| WOW_CH32 | 1, 0, 0, 0, 0, 0 | א / 0 / 0 / 0 / 0 / 0 |
| WOW_CH33 | 0, 0, 0, 0, 1, 1 | 0 / 0 / 0 / 0 / א / א |
| WOW_CH34 | 0, 1, 0, 1, 2, 0 | 0 / א / 0 / א / ב / 0 |
| WOW_CH35 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH36 | 0, 1, 0, 0, 0, 0 | 0 / א / 0 / 0 / 0 / 0 |
| WOW_CH37 | 0, 0, 0, 0, 2, 1 | 0 / 0 / 0 / 0 / ב / א |
| WOW_CH38 | 0, 0, 1, 0, 0, 0 | 0 / 0 / א / 0 / 0 / 0 |
| WOW_CH39 | 0, 0, 1, 2, 1, 0 | 0 / 0 / א / ב / א / 0 |
| WOW_CH40 | 0, 0, 0, 0, 0, 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| WOW_CH41 | 0, 0, 1, 0, 2, 1 | 0 / 0 / א / 0 / ב / א |
| WOW_CH42 | 3, 3, 1, 1, 1, 2 | ג / ג / א / א / א / ב |
| WOW_CH43 | 1, 0, 0, 1, 1, 1 | א / 0 / 0 / א / א / א |
| WOW_CH44 | 1, 1, 0, 0, 1, 0 | א / א / 0 / 0 / א / 0 |
| WOW_CH45 | 1, 0, 1, 0, 0, 0 | א / 0 / א / 0 / 0 / 0 |
| WOW_CH46 | 2, 1, 0, 0, 1, 0 | ב / א / 0 / 0 / א / 0 |
| WOW_CH47 | 2, 1, 1, 0, 1, 1 | ב / א / א / 0 / א / א |
| WOW_CH48 | 1, 0, 0, 1, 2, 0 | א / 0 / 0 / א / ב / 0 |
| WOW_CH49 | 0, 1, 0, 0, 1, 1 | 0 / א / 0 / 0 / א / א |
| WOW_CH50 | 1, 0, 0, 0, 1, 0 | א / 0 / 0 / 0 / א / 0 |

## Verification

Before writing, the runner verifies all four Step 1 input hashes against their recorded manifest, matches raw and numeric cells to the source table, checks all 4,100 Hebrew value round trips, verifies unique source IDs and 82 readings in each of 50 streams, and checks the event conversion. Numerical identity checks do not establish a linguistic reading.

## Repeat

```powershell
python -X utf8 -B WOWSignal/scripts/step03_hebrew_gematria.py --output WOWSignal/steps/03-hebrew-gematria/run-002
```

Use a new folder; existing runs are refused. Source files and prior reports are not modified. Numeric grids and CSV contents are deterministic; the manifest records its execution time separately.

Source attribution: Ohio SETI Data, PHL @ UPR Arecibo; upstream credits MichaelHotaling's transcription. CC BY 4.0. Pinned upstream commit: 28624a1eaf955ced940db347684cee61c8e4fd61.
