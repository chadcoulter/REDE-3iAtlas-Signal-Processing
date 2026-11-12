# Expanded Hebrew streams — container and orientation parser pass

November 10, 2026. This pass uses the actual projected chains in [run 003](../run-003-growing-container/results.json), restricted to the original scoped parts `וידכ | ול`. It does not extend into the surrounding `יטה` or replace the observed source streams.

**Working result:** the generated candidate `הגה` connects to steering/control or speech/utterance. Container-preserving reversal also exposes `וידא` in two lanes. These support an orientation–control–verification hypothesis, while the speech interpretation remains open. No complete grammatical Hebrew sentence or intended transmitted message is established.

**Execution and boundaries**

1. Rebuild all 3,612 numeric tokens from the saved projection history: three cases, four lanes each, 301 values per lane. Every original input or generated value retains its identity.
2. Attribute each generated value to its cycle, extension step, program, and output register. Preserve the original `[state, relations]` pairs and original numeral-token boundaries.
3. Render values through the existing Hebrew encoder, retaining all glyphs, repeated letters and zeros.
4. Examine source order, full glyph reversal, and container-order reversal with internal token letters preserved. These produce 36 explicitly labelled stream views.
5. Find all overlapping exact matches in the displayed 13-entry lexical candidate bank. Keep all unmatched ranges. This is a finite lexical parser, not an exhaustive Hebrew dictionary or grammatical decoder.
6. Record computed relationships and supplied semantic alternatives through the V8 TAO scaffold. Its backward-record status is provenance bookkeeping, not semantic validation. Its result remains unresolved.

**הגה**

| Item | Result |
|---|---|
| Origin | Generated values `[5,3,5]` in primary lane 4. |
| Literal form | ה · ג · ה = הגה. |
| Boundary | Crosses two adjacent generated `[state,relations]` pairs; it is not one original pair or one observed source token. |
| Meanings retained | Steering wheel/rudder/control; speech sound/utterance; an alternate verbal vocalization can mean he uttered/pondered. |
| Reverse test | הגה is a palindrome. Full reversal preserves the form and therefore does not select its meaning or direction. |
| Count | 96 overlapping occurrences per orientation in lane 4, arising from a repeated generated pattern—not 96 independent messages. |
| Relationship | Steering/control can qualify the earlier orientation/container hypothesis. Speech/utterance can instead connect to expression and verification. Neither sense is selected by the source. |

Sources: [steering/control](https://www.pealim.com/dict/7234-hege/), [speech/utterance meanings](https://milononline.net/מקרא/הגה), [Hebrew Academy steering terminology](https://terms.hebrew-academy.org.il/munnah/9111_2/steering).

**וידא**

| Item | Result |
|---|---|
| Primary orientation | Appears only under container-order reversal among the three tested views of the primary lanes. |
| Lane 1 | Chain position 201: retained source value 6, ו; position 200: generated relations value 14, יד; position 199: generated state value 1, א. |
| Result | ו · יד · א = וידא, candidate “he/it verified or made sure.” |
| Full-glyph counterpart | The same numeric units give ו · די · א = ודיא when their internal glyphs are also reversed. |
| Lane 3 | The final ו inside retained כו participates with generated יד and א, yielding כ[וידא]. The leading כ remains present; it has not been omitted to produce a standalone word. |
| Dependency | Both generated relations values 14 derive from the same endpoint-seeding/feedback mechanism; they are not independent source confirmations. |

Source: [וידא conjugation and meaning](https://www.pealim.com/he/dict/479-levade/). Complete occurrence traces are in [orientation_followup.json](orientation_followup.json).

**גג**

| Item | Result |
|---|---|
| Origin | Generated `[3,3]` pairs in primary lane 2. |
| Meaning candidate | Roof/top/maximum. |
| Count | 196 overlapping exact matches per orientation; 98 align with a generated `[state,relations]` pair and 98 cross a pair boundary. |
| Orientation | Palindromic; does not choose a direction. |
| Container relationship | A roof/top can be interpreted as a boundary of a containing structure. No “lid,” roof instruction, or containing object was recovered from observed measurements. |

Source: [גג](https://www.pealim.com/dict/7066-gag/).

**Other candidates and remainder**

`אבא` occurs in primary lanes 1 and 3; it is generated, palindromic, and crosses pair boundaries. Its dictionary reading “father” does not establish a speaker or actor. `ידו` occurs in source-order lane 1, mixing generated `יד` with retained original `ו`. The finite scan preserves these alternatives without forcing a father/hand/steering narrative.

The prior candidate vessel word `כדיו` is not a new lexical hit in this scoped expansion. A connection from it to generated steering/control is an analyst-supplied relationship across different paths. The Hebrew container noun has not been redefined as a boat or spacecraft by the English word “vessel.”

**Provisional synthesis to test**

“Orient the containers; verify.”

This is an operational paraphrase connecting the earlier tilt/container reading, generated steering/control candidate, and orientation-dependent verification candidate. It is not a contiguous Hebrew translation. Imperative grammar, punctuation, and the join between paths are supplied. The competing expression/utterance–verification interpretation remains active.

**Artifacts and repeat**

- [results.json](results.json): all 36 exact stream views, token/cycle/register provenance, every candidate occurrence, unmatched ranges, the complete finite lexicon, and TAO record.
- [orientation_followup.json](orientation_followup.json): two orientation-sensitive verification spans and their proposed relationship.
- [manifest.json](manifest.json): hashes, counts and checks for this checkpoint.
- [Continuing Hebrew text](../run-001/hebrew_streams_updated.txt): appended candidate readings, exact occurrence traces and unresolved relationships; original full 50-stream export remains its exact prefix.
- [Parser runner](../../../scripts/step03_expanded_hebrew_relations.py): the explicit finite lexical scanner and relation-recording procedure.

The runner requires a new output directory and records one versioned appended marker. It does not overwrite a previous run. A future independent trial should use a new trial marker and preserve all earlier text.

```powershell
python -X utf8 -B WOWSignal/scripts/step03_expanded_hebrew_relations.py --output WOWSignal/steps/03-hebrew-gematria/NEW-PARSER-RUN
```

This pass adds the parser script and four run artifacts (`results.json`, `orientation_followup.json`, this README, and `manifest.json`). It modifies only the continuing text and the script byte-preservation rule in `WOWSignal/.gitattributes`. Earlier pending work from the previous run remains pending. No commit or push was requested or performed for this pass.
