# Step-by-step investigation record

Authority: [Original process](../ORIGINAL_PROCESS.md).

Each step has its own folder. Its README records purpose, dependencies, and current status. Add a new numbered run record and uniquely named artifacts for each execution or recovery attempt; retain prior attempts.

| Step | Record | Status |
|---|---|---|
| 00 | [Recover method sources](00-source-recovery/README.md) | Partial: candidate sources located |
| 01 | [Recover the original signal data](01-source-data/README.md) | Not started |
| 02 | [Traverse the two-dimensional structure](02-grid-traversals/README.md) | Not started |
| 03 | [Apply V8 TAO](03-v8-tao/README.md) | Not started |
| 04 | [Process nested transversals](04-nested-reflections/README.md) | Not started |
| 05 | [Recover the interpreted instruction](05-message-reading/README.md) | Not started |
| 06 | [Examine directional relationships](06-directions/README.md) | Not started |
| 07 | [Audit transformation provenance](07-provenance/README.md) | Not started |
| 08 | [Validate the reproduction](08-reproduction-validation/README.md) | Not started |
| 09 | [Record implementation deliverables](09-delivery/README.md) | Not started |

## Recording an attempt

Copy [RUN_TEMPLATE.md](RUN_TEMPLATE.md) into the relevant step as `run-001.md`, then increment the number. Save supporting artifacts beside that run with the same prefix. Include input hashes and exact code revisions, settings, commands, output paths/hashes, result, and the parent run. A revised input or method starts a new attempt.

Keep observed measurements, computed transformations, historical reported readings, and current interpretations explicitly identified. Missing definitions remain unresolved. Do not execute a substitute transformation merely to fill a result.

