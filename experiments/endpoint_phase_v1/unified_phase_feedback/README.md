# Unified signal transform

`atlas_phase_feedback.S` is a self-contained GNU x86-64 assembly program for Linux/WSL. It contains all four channel chains in both traversal directions, the initial phase and register banks, and the runtime feedback loop. It requires no input files, Python runtime, or external libraries.

Build and run from this directory:

```sh
as --64 atlas_phase_feedback.S -o atlas_phase_feedback.o
ld --build-id=none atlas_phase_feedback.o -o atlas_phase_feedback.elf
./atlas_phase_feedback.elf > execution_registers.bin
```

The `CYCLES` constant at the top is 100. Each cycle reflects channels 1,2,3,4, then projects to destinations 2,3,4,1. Reflection loads the current four phase values into state, relations, constraints and observations; the remaining cells retain the previous projection state. Each turn transfers all eight cells to the next channel and replaces state with target. Projection targets in destination order 1,2,3,4 become the next phase. The signal chains stay fixed, as in the saved cyclic phase-feedback experiment.

Output is binary: eight little-endian unsigned 64-bit words per execution, in the order state, relations, constraints, observations, unresolved, context, target, events. There are eight executions per cycle and 51,200 bytes for 100 cycles. Partial writes and interrupted writes are handled; an output error exits with status 1.

`verification.json` records an exact comparison of all 6,400 register words against the earlier 800 independently assembled executions. All match. The final phase is `[1,15275004092359177936,2,1]`.

The eight instruction routines were extracted without changing their operator bodies from cycle 1 of the saved source archive; `source_provenance.json` records the members and body hashes. The new outer assembly loop performs the orchestration previously done by Python. `../build_unified_phase_feedback.py` records how the source was constructed, and `../verify_unified_phase_feedback.py` verifies native output against the saved execution trace.
