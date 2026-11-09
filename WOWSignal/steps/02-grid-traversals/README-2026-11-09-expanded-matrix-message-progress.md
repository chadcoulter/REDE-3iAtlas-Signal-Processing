# Wow! reconstruction progress — expanded matrix, ABRA, and continuing source relationships

Date: November 9, 2026

Branch: `codex/wow-signal`

Repository baseline: `bbc3beae7eafedd3af7a8b4b5e66697c777a5c47`

## Purpose and current state

This report captures the exploration after the [shared-center progress report](README-2026-11-09-shared-center-progress.md): returning to the horizontal source measurements; expanding the constructed relationship matrix; following its forward and reverse paths; exploring a remembered temporal/reflection hypothesis; returning to character and operator readings; deriving the candidate grouped sequence `ΑΒΡΑ`; following its next-source branches; and receiving Chad's composed interpretation.

The purpose is to recover where the original exploration went, including its assumptions and mistakes, while allowing the relationships to continue developing. Chad explicitly redirected the work away from making every intermediate relationship a proof exercise and back toward candidate messages. Missing historical transitions remain open rather than being replaced with an invented derivation.

**Step 2 and the message interpretation remain in progress.** Arithmetic identities, source occurrences, numerical encodings, grouping rules, and interpretive readings are distinguished below. The historical source-to-ΑΣΤΡΑ mapping, original horizontal transversal selection, and original triple-to-ΛΤϜ mapping have not been independently recovered. The new `ΑΒΡΑ` branch is an exploratory result of a stated grouping rule, not confirmation that the observation contains an intentional linguistic message.

All preceding experiments captured here were read-only inline calculations. This README is the only file added for this documentation request. No source, parser, earlier report, or generated run artifact was changed. No commit or push is included in this request.

## Sources, coordinates, and operator versions

- [Original process](../../ORIGINAL_PROCESS.md).
- [Historical narrative](../../sources/WowDecodeNarrative.md).
- [V8 resolver note](../../sources/v8-resolve-through-monads.md).
- [Versioned operator notes](../../sources/operator-notes/README.md).
- [Earlier checkpoint](README-2026-11-09-checkpoint.md).
- [Step 1 report](../01-source-data/run-001.md), [numeric grid](../01-source-data/run-001/numeric_grid.json), and [row metadata](../01-source-data/run-001/row_metadata.csv).
- [Character-transform skill](../../../skills/character-transform-reasoning/SKILL.md), [Book II](../../../skills/character-transform-reasoning/references/book-ii-alphabet.txt), and [resolution contract](../../../skills/character-transform-reasoning/references/resolution-contract.md).
- [Repository Greek numeral encoder](../../../skills/character-transform-reasoning/scripts/redsigma_band_extract.py).

All source rows and channels in tables are **one-based** unless explicitly identified otherwise. The stored grid is 82 time rows by 50 frequency-channel columns. Channel 02 contains the event in rows 58–63:

```text
Printed characters: 6 E Q U J 5
Numeric bins:       6 14 26 30 19 5
```

The input is the measurement transcription, not handwriting, circles, or the handwritten word “Wow!” These are normalized, quantized intensity labels; a blank is preserved in the raw representation and represented as bin zero numerically. A zero bin does not establish zero physical radio power.

The historical narrative supplies Trace / Traverse / Relate-or-Resolve / Admit interpretations and defines Ϝ as reverse traversal to recover direction. Later Book II supplies Origin, Branch, Boundary frame, Change, State, Context, Relation, Lattice resolution, Constraint, Threshold, and Stigma/unresolvedness roles. These are versioned interpretation resources, not a recovered August executable decoder. Historical Ϝ is retained for this reconstruction rather than silently replaced with its later retention definition.

## 1. Returning the shared edge to horizontal source paths

The shared source edge is between channel-02 values 26 and 30 in rows 60 and 61. Its temporal midpoint is 22:16:04.5 EST at the printed precision. The six event timestamps pair symmetrically around that midpoint.

The six actual horizontal rows form three mirrored pairs:

| Pair | Rows | Channel-02 values | Later minus earlier |
|---|---|---|---:|
| Outer | 58 ↔ 63 | 6 ↔ 5 | −1 |
| Middle | 59 ↔ 62 | 14 ↔ 19 | +5 |
| Inner | 60 ↔ 61 | 26 ↔ 30 | +4 |

Each pair extends across all 50 channels, producing three horizontal comparison sequences from six measured rows. The first three channel differences are respectively `[0,−1,1]`, `[1,5,−1]`, and `[0,4,3]`.

For adjacent channels c and c+1, the change between the two horizontal increments equals the difference between the two vertical increments. This was checked across all 49 channel intervals for each pair. For the inner pair at channels 02–03:

```text
Row 60: 26 → 0, horizontal change −26
Row 61: 30 → 3, horizontal change −27
Change between horizontal increments: −1
Vertical changes at the two channels: +4 and +3; difference −1
```

The channel-02 half imbalance is +8, whereas the complete six-row, 50-channel block has early-half total 121 and late-half total 126: imbalance +5. The other channels contribute −3. Horizontal context therefore changes the aggregate without changing the event's source occurrences.

One surveyed branch was channel 19: its three mirrored pairs are `(0,1)`, `(1,0)`, `(0,1)`. Their sums are all 1, while their differences are `+1,−1,+1`. This was the only channel in this six-row block with three equal nonzero pair sums. The recorded horizontal paths back to channel 02 recover pair sums 11, 33, and 56, totaling 100. No significance or instruction was independently established for channel 19.

These comparisons are candidate connections to the historical three transversals. They do not identify which horizontal paths were originally selected.

## 2. Stream counts and expanding the relationship matrix

The source has 50 channel sequences with 82 readings each. Nine originally described display positions in a three-by-three overlapping-window construction, not nine independent recorded streams. Thirteen had not been derived as a stream count.

Chad recalled that the structure also worked at 5, 7, and 9, and suggested 13 and possibly 17. He clarified expansion as adding a border in all directions. The tested relationship construction does retain its previous matrix inside each new border.

For odd size n, take 2n channel-02 samples centered on the edge between rows 60 and 61. Form their 2n−1 adjacent signed changes, then n overlapping windows of n changes. These windows form an n-by-n display. For this construction, both display axes index overlapping positions along the **same temporal edge sequence**; the horizontal display axis is not the native frequency-channel axis.

| Matrix size | Source rows | Source samples | Distinct edges | Display positions | Source-bin total |
|---:|---|---:|---:|---:|---:|
| 3 | 58–63 | 6 | 5 | 9 | 100 |
| 5 | 56–65 | 10 | 9 | 25 | 101 |
| 7 | 54–67 | 14 | 13 | 49 | 102 |
| 9 | 52–69 | 18 | 17 | 81 | 103 |
| 11 | 50–71 | 22 | 21 | 121 | 104 |
| 13 | 48–73 | 26 | 25 | 169 | 104 |
| 15 | 46–75 | 30 | 29 | 225 | 104 |
| 17 | 44–77 | 34 | 33 | 289 | 104 |

All retain the edge 26 → 30 at the central display position and throughout the other diagonal. This follows from the overlapping-window construction. Source-linked edge identity is retained rather than treating its repeated appearances as independent measurements.

The source boundary permits this symmetric construction through odd size 21. A native square time–frequency patch has different limits: channel 02 has only one recorded channel to its left. Time reversal preserves frequency-channel columns; the 180-degree rotation previously found describes the constructed relationship display with edge inversion, not a physical reversal of both native axes.

## 3. Traversing the 17 horizontal windows

The 34 source bins in rows 44–77 are:

```text
0,0,0,0,0,0,0,1,0,0,0,0,0,0,6,14,26,
30,19,5,0,1,1,0,0,1,0,0,0,0,0,0,0,0
```

Each horizontal window traverses 17 adjacent changes and therefore connects 18 source samples. Its sum telescopes to the difference between its endpoint bins.

| Path | Source endpoints, rows | Net | Greek numeral |
|---|---|---:|---|
| H01 | 44 → 61 | 30 | Λ |
| H02 | 45 → 62 | 19 | ΙΘ |
| H03 | 46 → 63 | 5 | Ε |
| H04 | 47 → 64 | 0 | 0 |
| H05 | 48 → 65 | 1 | Α |
| H06 | 49 → 66 | 1 | Α |
| H07 | 50 → 67 | 0 | 0 |
| H08 | 51 → 68 | −1 | −Α |
| H09 | 52 → 69 | 1 | Α |
| H10 | 53 → 70 | 0 | 0 |
| H11 | 54 → 71 | 0 | 0 |
| H12 | 55 → 72 | 0 | 0 |
| H13 | 56 → 73 | 0 | 0 |
| H14 | 57 → 74 | 0 | 0 |
| H15 | 58 → 75 | −6 | −Ϛ |
| H16 | 59 → 76 | −14 | −ΙΔ |
| H17 | 60 → 77 | −26 | −ΚϚ |

There are ten nonzero net results. A net-zero path can still traverse the event and nonzero contextual changes. Zeros were not assigned punctuation or terminal closure; minus signs are numerical orientation markers, not a newly defined inverse-operator grammar.

Reversing H15, H16, and H17 recovers 6, 14, and 26. Joining these in their source order to the first three positive results gives the original six bins. Pairing opposite horizontal nets gives `+4,+5,−1` for H01+H17, H02+H16, and H03+H15: the original central, middle, and outer event-pair differences encountered from the display borders.

The central path H09 includes:

```text
0,0,0,0,0,0,6,14,26,30,19,5,0,1,1,0,0,1
```

Its net is +1. In reverse, its source checkpoints are `1 → … → 30 → 26 → … → 0`, with net −1. All reverse windows encounter that same central edge, though their endpoint bins differ.

The main diagonal sums to zero. Its alternating source-position totals are 52 and 52. The other diagonal repeats the same +4 edge in 17 display positions; its numerical display sum is 68, not 17 independent detections of a new signal.

## 4. Candidate instruction before the temporal branch

The operational candidate was first expressed as following the trace backward through the shared crossing toward its origin. This was an interpretation of retained paths, not a decoded quotation. Relating that operation to the sky introduced two different branches:

- Retrace incoming propagation toward the source-facing sky direction.
- Reflect the source-facing direction to its antipode.

Using the historical narrative's coordinates, antipodal conversion `(RA + 12 hours) mod 24`, with declination sign reversed, gives:

| Historical source direction | Antipode |
|---|---|
| 19h25m31s, −26°57′ | 7h25m31s, +26°57′ |
| 19h28m22s, −26°57′ | 7h28m22s, +26°57′ |

The narrative identifies the opposite field as Gemini after an earlier Taurus prediction. The matrix does not itself select a sky antipode or a geographic destination. Its temporal center is not automatically the physical observer. The inward interpretation followed the transformation trace back to the instrument, observation time, pointing, and admitted Theatre, consistent with the V8 backward chain.

## 5. Remembered departure, degradation, and geographical hypotheses

Chad recalled trials at approximately 15,000, 25,000, and 80,000 years, with Gemini associated with the 15,000-year trial. He clarified that 15,000 years referred to **departure from Earth**, and recalled a possible origin in Chile or Turkey followed by a stellar reflection. He also recalled tracing the signal's degradation to constrain where the reflector would have needed to be. These are historical recollections to investigate, not outputs recovered from this matrix pass.

The repository copies contain CSV, TXT, JPG, and the upstream README. The README also describes an upstream calibrated `.sav` file, but that file is not in this checkout. Its listed flux estimates assumed a 54 Jy maximum. Describing that schema did not supply those arrays to this analysis.

### Read-only degradation probes

Using the printed event-time offsets `[0,12,24,35,47,59]` seconds and bin midpoints `[6.5,14.5,26.5,30.5,19.5,5.5]`, a descriptive point-sampled Gaussian fit gave:

- Peak: approximately 30.47 in the normalized representation.
- Center: approximately 31.31 seconds after the first printed event time.
- Sigma: approximately 16.12 seconds; FWHM approximately 37.95 seconds.
- RMS residual: approximately 1.14 bin units.

This is not a calibrated beam deconvolution or an estimate of a millennial propagation time. An exponential fitted only to the three falling-side points gave a roughly 14-second e-folding time. A Gaussian beam multiplied by exponential fading can reproduce another Gaussian with a shifted center; illustrative fading times of 14, 60, and 600 seconds all reproduced the same fitted profile by changing the unmeasured beam-center parameter. Independent instrument constraints would be needed to distinguish them.

Neighboring channels 01, 03, and 04 did not contain a comparable large event envelope. Their six-reading maxima were 2, 3, and 4, versus channel 02's 30. This did not establish an intrinsic spectral width or a propagation-scattering tail.

The printed oscillator setting changed from 120.184 to 120.185 MHz across the event. It is a receiver setting, not a direct measurement of source line drift. Instrument documentation describes integration, baseline/noise normalization, threshold-dependent freezing of updates, and truncation. The original waveform, phase, emitted reference, transmitter power, scattering cross-section, and frequency-dependent delay are not supplied by these printout arrays.

For an illustrative equal-leg Earth–reflector–Earth model, assumed elapsed times of 15,000, 25,000, and 80,000 years correspond approximately to one-leg distances of 7,500, 12,500, and 40,000 light-years. With received strength held fixed, a simple inverse-fourth-power echo model can accommodate these distances by scaling the unknown transmitter-strength × scattering factor by 1, 7.716, and 809.086. These are conditional model comparisons, not ages inferred from the data.

A separate illustrative calculation used 54 Jy averaged over 10 kHz. The isotropic-equivalent radiating powers at those assumed one-leg distances were approximately 3.42×10^20, 9.49×10^20, and 9.72×10^21 W. This treats an effective radiating point, not a completed reflection model. Changing calibration from 54 to 212 Jy changes a fixed-power inferred distance by a factor approximately 0.505.

### Historical material actually recovered

The accessible August chat [“Branch · Check Recursion Pattern”](https://chatgpt.com/c/6a8bf7c0-006c-83ea-85f2-8a72be6d131e) contains Chad's proposed South American origin and time-buffer/ice-age hypothesis. The reply assumed a departure interval and calculated a relay distance using `d = ct/2`. It discussed departure ages of approximately 26,500–33,000 years and a corresponding reflector range roughly 13,000–16,500 light-years, plus another proposed period and range. These are statements preserved from that chat, not archaeological chronology established here.

This recovers a documented route connecting South America, ancient departure, reflection, and a number near 15,000. In that passage, the number near 15,000 is a distance derived from a proposed age. It does not recover the separate degradation calculation or the Turkey selection. Other inspected recent excerpts of August chats did not supply those missing details; this was not an exhaustive review of every original turn.

An exploratory constant-rate precession calculation also exposed a possible route to the Gemini label. The historical directions have approximate J2000 ecliptic longitudes 289.035° and 289.666°. A 26,000-year constant cycle gives a 15,000-year phase of 207.692°. Subtraction yields 81.343° and 81.973°, in the equal-width Gemini zodiac sector, 60°–90°. The opposite sign gives 136.727° and 137.358°. Both signs were tested; neither was recovered as the historical convention. At 25,000 years the minus-phase results are approximately 302.881°–303.512°; at 80,000 years approximately 261.343°–261.973°.

This is a toy phase model, not a valid long-term astrometric solution. An equal-width zodiac sector is not an IAU constellation classification. Precessing a coordinate frame does not alone move a fixed celestial direction into a different modern constellation. Mixing coordinate epochs, years, and light-years remains a possible historical mistake to investigate rather than an established account of what happened.

Mapping any historical sky direction to Chile or Turkey would additionally require an Earth-orientation/time assumption and an alignment rule, such as overhead, horizon, or specified pointing. None was recovered. Chad then redirected the immediate work toward messages, leaving these branches available rather than requiring them to resolve first.

External references consulted for this side branch:

- [Ehman's instrument and beam-fit report](https://www.bigear.org/Wow30th/wow30th.htm).
- [Archival reanalysis, version 1](https://arxiv.org/html/2508.10657v1), retained as a versioned comparison rather than silently substituting its coordinates.
- [PHL current data summary](https://phl.upr.edu/wow/data), whose revised positions also remain separate from the historical reconstruction.
- [JPL radar propagation derivation](https://descanso.jpl.nasa.gov/SciTechBook/series2/SAR_Polarimetry_compressed.pdf).
- [NASA reference systems and approximate precession cycle](https://science.nasa.gov/learn/basics-of-space-flight/chapter2-1/).
- [USNO sky-to-local direction transformation](https://aa.usno.navy.mil/faq/alt_az).

## 6. Reading numerical characters through the matrix

The repo encoder maps magnitudes by additive Greek numeral components. Numerical encoding is deterministic; reading those numeral glyphs as operators is an additional exploratory interpretation. A numeral such as ΙΔ represents 14; it does not by itself establish that the measurement commands an Instance–Change operation.

The recovered six-reading core encodes:

```text
6     14    26    30    19    5
Ϛ  |  ΙΔ |  ΚϚ |  Λ  | ΙΘ | Ε
```

A provisional forward operator reading linked unresolvedness, a particular change, contextual unresolvedness, lattice resolution, a particular constraint, and a threshold:

> Resolve the unresolved change in its context. Resolve its connections, identify the applicable constraint, and evaluate the threshold.

Reversing source chunks, while preserving each numeral's internal component order, gives:

```text
Ε | ΙΘ | Λ | ΚϚ | ΙΔ | Ϛ
```

The provisional reverse reading was:

> Examine the threshold and its constraint. Follow the resolved connections back through context to the particular change that remains unresolved.

Displaying each nine-glyph sequence row-major gives two distinct representations:

```text
Forward                    Source reversed
Ϛ Ι Δ                      Ε Ι Θ
Κ Ϛ Λ                      Λ Κ Ϛ
Ι Θ Ε                      Ι Δ Ϛ
```

Forward diagonals are `ϚϚΕ` and `ΔϚΙ`; reversed diagonals are `ΕΚϚ` and `ΘΚΙ`. Their centers are respectively Ϛ and Κ. Neither display center is automatically the shared temporal source edge of the 17-by-17 construction. The candidate synthesis was to return a result to context and identify the particular unresolved change before applying constraints and thresholds.

## 7. Applying that candidate instruction to its own context

The 34 source readings were decomposed into the original six-reading core and the surrounding measurements. This is an accounting decomposition, not a classification of intentional signal versus noise. Because adjacent differencing and matrix construction are linear, the corresponding matrices add exactly.

The four surrounding bin-one occurrences are rows 51, 65, 66, and 69. They induce six nonzero adjacent changes and affect 56 of the 289 matrix positions.

| Quantity | Core contribution | Context contribution | Combined |
|---|---:|---:|---:|
| Source-bin total | 100 | 4 | 104 |
| Sum of horizontal nets | 8 | 2 | 10 |
| Main diagonal sum | −2 | +2 | 0 |
| Shared central edge | +4 | 0 | +4 |
| H09 net | 0 | +1 | +1 |

Alternating source-position totals decompose as `[51,49] + [1,3] = [52,52]`. Thus a zero diagonal total contains distinct cancelling contributions; it is not absence of internal change. The four source-context units also should not be equated with the +4 central edge merely because their numerical values agree.

H09's Alpha comes from its endpoint at row 69: `1 − 0 = +1` between rows 52 and 69. It is a different source relationship from the original event endpoint difference `6 − 5 = +1`.

The candidate continuation became:

> Look through the balance to the changes that compose it. Recover their origins, retain their context, and continue from those distinctions.

## 8. Central Alpha, complete excursions, and ABRA

The surrounding readings form three excursions:

```text
Rows 50–52: 0,1,0
Rows 64–67: 0,1,1,0
Rows 68–70: 0,1,0
```

Their net adjacent change is zero, although their source-bin sum is four. Reversing the contextual changes with the retained anchor reconstructs every occurrence. Their local shapes are palindromic; shape alone does not distinguish chronology.

H09 ends inside the last excursion at row 69. Extending its reverse path one reading, from row 70 rather than row 69, adds `0 → 1` before `1 → 0`. The reverse path's net changes from −1 to zero while retaining the same shared edge. This extension is a separate path using already available source data, not a silent modification of H09.

The next grouping choice was **maximal contiguous nonzero source runs**, with all zero-bin samples retained as separators. Within rows 44–77 this produces:

| Run | Source rows | Values | Sum | Numeral |
|---|---|---|---:|---|
| Earlier context | 51 | 1 | 1 | Α |
| Event core | 58–63 | 6,14,26,30,19,5 | 100 | Ρ |
| Paired context | 65–66 | 1,1 | 2 | Β |
| Later context | 69 | 1 | 1 | Α |

```text
Forward grouped reading: Α | Ρ | Β | Α
Reverse grouped reading: Α | Β | Ρ | Α
```

The reverse sequence is transliterated **ABRA**. No ancient word meaning was established. Contiguous-positive grouping, summing each run, and switching from numeral to operator interpretation are explicit researcher choices, not a recovered universal decoder.

At the operator layer the reverse candidate was: establish an origin, branch, resolve relation, establish the next origin. The context-only grouped sequence `ΑΒΑ` is unchanged by reversal; adding the event Ρ distinguishes the forward and reverse orders. The four run totals still sum to 104, but preserving their order carries information lost by the single total `ΡΔ`.

## 9. Following ABRA through the center into a next source

The reverse source chain is:

```text
Α at row 69
Β at rows 65–66
Ρ at rows 58–63, traversed as 5,19,30,26,14,6
Α at row 51
```

Inside Ρ, the shared edge is traversed as 30 → 26. The final Alpha supplies a particular next source cell: **row 51, channel 02**. No rule was found that uniquely selects a continuation from it. Both chronological and horizontal branches were followed.

### Horizontal branch from row 51

At channels 02–03, the cell read vertically as Α participates in a horizontal run `[1,1]`, whose sum encodes Β. Its source occurrence is retained while its grouping changes. Applying the same maximal-nonzero-run rule across the entire row gives:

| Channels | Values | Sum | Numeral |
|---|---|---:|---|
| 02–03 | 1,1 | 2 | Β |
| 07–08 | 1,2 | 3 | Γ |
| 11 | 1 | 1 | Α |
| 15–21 | 1,1,1,1,1,1,2 | 8 | Η |
| 38 | 1 | 1 | Α |
| 44–46 | 2,1,1 | 4 | Δ |
| 49 | 1 | 1 | Α |

```text
Β | Γ | Α | Η | Α | Δ | Α
```

The row total is 20, encoded Κ, which supplied an additional candidate enclosing Context reading. This row-total reduction is another interpretation choice, not independent confirmation of the operator sentence.

The provisional composition was:

> Branch within a frame. Establish a source and resolve its state. Establish a source for the change, then establish the next source.

### Continuing backward in channel 02

Before row 51, the next complete runs are row 40 `[1]`, rows 31–32 `[1,2]`, row 20 `[2]`, row 12 `[1]`, and row 5 `[1]`. Their reverse-order continuation is:

```text
Α | Γ | Β | Α | Α
```

A provisional reading was to establish a source, resolve its frame, branch, and establish the following sources. The repeated Alphas remain different source occurrences unless a further relationship identifies them.

### Wider-window context retained

Expanding the original centered relationship matrix further changes the scope of the run sequence:

```text
17 × 17, rows 44–77: Α | Β | Ρ | Α
19 × 19, rows 42–79: Γ | Α | Β | Ρ | Α
21 × 21, rows 40–81: Γ | Α | Β | Ρ | Α | Α
```

The new leading Γ comes from rows 78–79, `[2,1]`. The additional trailing Α comes from row 40. Across the full 82-row page, the reverse channel-02 run sequence is:

```text
Γ | Α | Β | Ρ | Α | Α | Γ | Β | Α | Α
```

These wider sequences prevent treating ABRA as an independently established word boundary or a uniquely selected complete message. Their relation to a larger reading remains available for continuation.

## 10. Requested syllabic notation

Chad requested the characters in a Sumerian-style `ak-ka-da` format. The response supplied proposed hyphenated phonetic renderings, not Sumerian translations or identified ancient words:

| Characters | Proposed rendering |
|---|---|
| ΑΒΡΑ | ab-ra |
| ΒΓΑΗΑΔΑ | ba-ga-e-a-da |
| ΑΓΒΑΑ | ag-ba-a |

For the second rendering, an `a` was added after the initial `b`, and Eta was approximated as `e`. These choices do not define a canonical conversion from Greek operator characters to Sumerian signs. [Oxford's transliteration principles](https://etcsl.orinst.ox.ac.uk/edition2/pdf/transliterationprinciples.pdf) were consulted for the syllabic notation convention.

## 11. Chad's composed interpretation, preserved verbatim

> An origin produces a branch, and the branch establishes a relationship with its source.
>
> The branch establishes boundaries within which a state can form. The originating structure initiates change, and the resulting transformation returns to its source.
>
> Through that return, the originating state is preserved, while the branch remains connected to the structure from which it emerged.

This is Chad's proposed relational reading of the sequences together. The response associated `ΑΒΡΑ` with origin, branch, and relation to source; and `ΒΓΑΗΑΔΑ` with branch, frame, originating state, change, and a subsequent origin. His final paragraph makes preservation and continuing source connection explicit.

The resulting candidate instruction was:

> Branch from the source, establish the frame for change, and carry the source relationship through the transformation and return.

The interpretation that a later Alpha refers back to the originating structure is retained as a candidate relationship. The glyph sequence alone does not equate different source occurrences. Reverse traversal demonstrates recovery of retained source data; it does not by itself establish that a physical source state was unchanged by a hypothetical transmission or reflection.

## 12. Where to continue

Continue from the explicit source groups and contribution links. Keep the horizontal and chronological branches, the expanded-window prefixes and suffixes, and Chad's composed reading available together. Candidate instructions can guide the next exploratory pass while remaining distinct from measured content.

Open relationships include the run-boundary rule's role in the historical process, the numeral-to-operator bridge, which next-source branch is selected, how repeated Alphas are related, and whether the wider glyph sequences support a less generic instruction. The physical age, reflection, and geographical branches remain separate and unresolved. Neither a repeated numerical identity nor a zero aggregate establishes a global stopping boundary.

## Reproduction of the source and character calculations

Run this Python block from the repository root. It writes no files and uses only the standard library. It extracts the encoder's literal table and function without importing its signal-processing dependencies. The assertions check the recorded calculations; they do not validate the message interpretation.

```python
import ast
import json
from pathlib import Path

base = Path('WOWSignal/steps/01-source-data/run-001')
grid = json.loads((base / 'numeric_grid.json').read_text(encoding='utf-8'))['grid']
source = [row[1] for row in grid]
encoder = Path('skills/character-transform-reasoning/scripts/redsigma_band_extract.py')
tree = ast.parse(encoder.read_text(encoding='utf-8'))
selected = [node for node in tree.body if (
    isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == 'VALUES' for t in node.targets)
) or (isinstance(node, ast.FunctionDef) and node.name == 'greek')]
namespace = {}
exec(compile(ast.Module(body=selected, type_ignores=[]), str(encoder), 'exec'), namespace)
greek = namespace['greek']

previous = None
for n in range(3, 18, 2):
    values = source[60-n:60+n]
    edges = [b-a for a, b in zip(values, values[1:])]
    matrix = [edges[i:i+n] for i in range(n)]
    assert matrix[n//2][n//2] == 4
    if previous is not None:
        assert [row[1:-1] for row in matrix[1:-1]] == previous
    previous = matrix

s = source[43:77]
def matrix17(values):
    edges = [b-a for a, b in zip(values, values[1:])]
    return [edges[i:i+17] for i in range(17)]
matrix = matrix17(s)
nets = list(map(sum, matrix))
assert nets == [30,19,5,0,1,1,0,-1,1,0,0,0,0,0,-6,-14,-26]
assert [-nets[14], -nets[15], -nets[16], *nets[:3]] == source[57:63]
assert sum(matrix[i][i] for i in range(17)) == 0
assert all(matrix[i][16-i] == 4 for i in range(17))
assert sum(s[::2]) == sum(s[1::2]) == 52

core = [v if 14 <= i < 20 else 0 for i, v in enumerate(s)]
context = [v-c for v, c in zip(s, core)]
cm, bm = matrix17(core), matrix17(context)
assert all(matrix[i][j] == cm[i][j] + bm[i][j]
           for i in range(17) for j in range(17))
assert [sum(core), sum(context), sum(s)] == [100, 4, 104]
assert sum(cm[i][i] for i in range(17)) == -2
assert sum(bm[i][i] for i in range(17)) == 2
assert sum(value != 0 for row in bm for value in row) == 56
assert [(44+i, v) for i, v in enumerate(context) if v] == [
    (51,1), (65,1), (66,1), (69,1)]
assert source[68] - source[51] == 1
assert source[69] - source[51] == 0

def runs(values, offset=1):
    result = []
    i = 0
    while i < len(values):
        if values[i] == 0:
            i += 1
            continue
        j = i
        while j < len(values) and values[j] != 0:
            j += 1
        total = sum(values[i:j])
        result.append((i+offset, j-1+offset, total, greek(total)))
        i = j
    return result

assert runs(s, 44) == [(51,51,1,'Α'), (58,63,100,'Ρ'),
                       (65,66,2,'Β'), (69,69,1,'Α')]
assert [r[3] for r in runs(s, 44)[::-1]] == list('ΑΒΡΑ')
assert [r[3] for r in runs(grid[50])] == list('ΒΓΑΗΑΔΑ')
assert sum(grid[50]) == 20 and greek(20) == 'Κ'
assert [r[3] for r in runs(source[:50])[::-1]] == list('ΑΓΒΑΑ')
assert [r[3] for r in runs(source)[::-1]] == list('ΓΑΒΡΑΑΓΒΑΑ')
assert [greek(v) for v in source[57:63]] == ['Ϛ','ΙΔ','ΚϚ','Λ','ΙΘ','Ε']
print('Source, matrix, context, and grouped-character calculations reproduced.')
print('Operator sentences and historical derivations remain candidate interpretations.')
```

Optional reproduction of the descriptive Gaussian probe requires the already available NumPy and SciPy packages. No package installation or source modification is required:

```python
import csv
import numpy as np
from scipy.optimize import least_squares

with (base / 'row_metadata.csv').open(encoding='utf-8-sig', newline='') as f:
    rows = list(csv.DictReader(f))[57:63]
def seconds(text):
    h, m, sec = map(int, text.split())
    return 3600*h + 60*m + sec
x = np.array([seconds(row['EASTERN STD TIME']) for row in rows], dtype=float)
x -= x[0]
y = np.array(source[57:63], dtype=float) + 0.5
def gaussian(q):
    amplitude, center, sigma = q
    return amplitude * np.exp(-0.5*((x-center)/sigma)**2)
fit = least_squares(lambda q: gaussian(q)-y, [31,30,17],
                    bounds=([0,-60,1], [200,120,200]))
print('Descriptive Gaussian parameters:', fit.x)
print('FWHM seconds:', 2*np.sqrt(2*np.log(2))*fit.x[2])
print('RMS residual:', np.sqrt(np.mean((y-gaussian(fit.x))**2)))
```
