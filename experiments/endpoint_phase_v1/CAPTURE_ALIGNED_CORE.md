# Capturing the code between the repeating regions

`capture_aligned_core.py` creates a separate four-channel core capture. It preserves channel alignment and every original recorded value. It removes only the shared repeating boundary regions: 37 complete two-value left pairs (74 values) and 92 right values from every 2,100-value channel.

The retained interval is original zero-based indices 74 through 2007 inclusive: 1,934 values per channel. It contains all 1,800 recorded values plus 134 generated transient or alignment values. Additional per-channel repetition is retained where cutting it would break common four-channel alignment. This is a boundary-based code selection, not a claim that every remaining instruction has independent semantic significance.

The exact retained assembly body is preserved. Its entry state is captured after the removed prefix, and that state initializes the standalone core ELF. Native execution must reproduce the expected core exit state. Applying the removed suffix to that native state must reproduce all eight original final register values. The suffix contribution is recorded rather than silently discarded.

Each channel has:

- `.S`: retained assembly with captured initial state and a small output/exit wrapper.
- `.o`: assembled object with symbols/relocations.
- `.elf`: tested standalone Linux x86-64 executable.
- `.code.bin`: raw retained machine instructions, excluding the output/exit wrapper.
- `.data.bin`: the 64-byte captured entry state.
- `.context.json`: input/output states, hashes, original boundaries and code/data layout.

Use the ELF for direct execution. The raw code body uses RIP-relative memory references and falls through at its end; loading it independently requires its paired data and the recorded relative placement. It is not a standalone executable file. The object and assembly support linking/reassembly into another layout.

All files are new. Original complete programs, source measurements and earlier results are unchanged. `core_manifest.json` summarizes the four native tests and the shared boundary choice.
