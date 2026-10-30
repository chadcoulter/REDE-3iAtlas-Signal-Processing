# Rotated one-register handoff results

Actual native reflection output is handed to projection channel 5-i. Only the named register is substituted; seven other slots are preserved. No endpoint reseeding occurs. Each scenario starts independently from the same four native reflection results.

Function output for this run: `target`. Native programs passed: 40/40.

Vectors below are ordered by projection destination channel 1, 2, 3, 4.

| Substitution | Projection state | Projection target | Changed channels vs control |
|---|---|---|---|
| none (control) | ["1", "1", "1", "1"] | ["1", "7913412885118562870", "2", "1"] | [] |
| state | ["1", "1", "1", "1"] | ["1", "14682301134823862838", "2", "1"] | [2] |
| relations | ["1", "1", "1", "1"] | ["1", "7913412885118562870", "2", "1"] | [1, 3, 4] |
| constraints | ["1", "1", "1", "1"] | ["1", "7913412885118562870", "2", "1"] | [4] |
| observations | ["1", "1", "1", "1"] | ["1", "11399613512586998326", "2", "1"] | [1, 2, 3, 4] |
| unresolved | ["1", "1", "1", "1"] | ["1", "7913412885118562870", "2", "1"] | [1, 2, 3, 4] |
| context | ["1", "1", "1", "1"] | ["1", "7913412885118562870", "2", "1"] | [3] |
| target | ["1", "1", "1", "1"] | ["1", "7913412885118562870", "2", "1"] | [] |
| events | ["1", "1", "1", "1"] | ["1", "1354582372535624446", "2", "1"] | [1, 2, 3, 4] |

`rotated_register_test.json` contains all eight input/output registers, source/destination links, the actual changed seed slots, native source and executable hashes, and comparison results. `case_readouts.json` provides a smaller per-case view. `assembled_sources.zip` and `native_executables.zip` preserve every newly compiled program.

The target-substitution case is an identity control when target is the selected function output. It must exactly match the no-substitution control. No original source, chain or previous result is edited.
