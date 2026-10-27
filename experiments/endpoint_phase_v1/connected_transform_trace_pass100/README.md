# Connected register and transform trace

`transform_trace.json` contains the complete recorded 100-pass native-driven run and the captured core. `projection_example.json` is a smaller example of the first projection step; references not expanded in that subset resolve in the complete file.

## Contents

- `executions`: 804 native runs, with all eight logical registers before seeding, after seeding and after execution. Each has the 64-byte output as hex, executable/source hashes, input-chain revision and feedback source.
- `transforms`: 200 extension steps. X to Y is **reflection**, selecting `target`. Y to X is **projection**, selecting `state` and `relations`. Each step links source executions, emitted data, insertion order, other-channel readouts and the native execution that validated the extension.
- `data`: 8,400 individually identified values: 7,200 archived extracted measurements and 1,200 generated values. Equal numbers retain different IDs when they arise at different positions or passes. Generated values identify their producer execution and register; measurements retain recorded amplitude, frequency and elapsed second.
- `chains`: the ordered original and final value IDs for each channel. Intermediate revisions are reconstructed by applying each transform's `chain_updates` to the original order.
- `captured_cores`: entry/output/boundary states and core artifacts, linked to their source executions and retained data IDs.
- `core_value_trace`: all eight cells after each of the 7,736 retained core values, linked to those values' origins. These intermediate snapshots come from the operator-reference trace; each channel's final snapshot is reconciled with its actual native core output.

## Precision and references

Unsigned 64-bit words are **decimal strings**, with hex available where useful. They must be read as BigInt or another exact unsigned/integer type. Counts and indices remain normal JSON integers. No machine word has been serialized as a JavaScript-unsafe JSON number.

IDs connect records, for example:

```json
{
  "id": "data/c4/step0002/state",
  "value_decimal": "829335579365792083",
  "origin": {
    "kind": "projection",
    "transform_id": "transform/0002",
    "source_execution_id": "program0008_validates001_y_to_x_channel4",
    "source_register": "state",
    "emitted_order": 0,
    "insertion_end": "front"
  }
}
```

This value is read from the native `state` output, inserted at the front of channel 4 by transform 2, and included in the chain that the next compiled execution validates. Subsequent seeding and feedback explicitly identify which prior data or register supplies each cell.

Validation follows the preceding extension: execution after step N validates N and supplies the next transform. Its target vector is retained separately from insertion records. Other-channel views are readout selections; actual seed loads and chain insertions are recorded separately, without inventing additional feedback connections.

Artifact paths are relative to `experiments/endpoint_phase_v1`. Assembly/ELF archives remain unchanged. Original frequency-ranked channel identity is preserved; the data does not silently relabel stripes as fixed frequencies.

The trace preserves the implementation and observed outputs; it does not change the seed assignment, direction rules, pair order or boundary selection. No earlier files were edited.
