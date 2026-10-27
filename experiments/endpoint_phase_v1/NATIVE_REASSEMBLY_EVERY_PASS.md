# Reassemble and execute immediately after every extension

`native_reassemble_every_pass.py` corrects the earlier batch-only executable checks. It also makes the actual rebuilt native programs supply the next projection, rather than using endpoint-only interpreter calculations as feedback.

The loop is:

1. Bootstrap by assembling and executing the four original full chains.
2. Extract target for an X-to-Y extension, or state/relations for Y-to-X, from the actual native register outputs.
3. Append or prepend the raw values to the chains.
4. Immediately generate fresh assembly for the complete updated chains, assemble, link, and execute all four.
5. Record that execution as validation of the preceding extension; its actual outputs become the next pass's projection source.

The user identified `[1,1,1,7]` as validation of the previous pass. It is therefore recorded with the extension step validated, not labelled a chain termination marker. Every projection is linked to the exact native program that produced it. Source hashes link validation to the just-extended chain. No extension, including the last, is left unassembled.

Full native traversal replaces endpoint-only processing: the forward code executes every current chain value in order; reverse code executes all values and their glyphs in reverse order. The four opposite-end raw values seed the same named register slots before execution, and other register outputs retain feedback. Leftward pair order remains `[state, relations]`. Each active-channel exclusion view is preserved.

For 100 passes each way there are 200 extension steps and 804 freshly assembled/executed native programs: four bootstrap programs and four after each extension. The interpreter is only an independent operator-state execution check. All projections come from native output, and all eight returned registers must match the reference.

Run inside WSL Ubuntu Python, passing Linux paths to the archive and a fresh output directory. Only new files are created. Complete assembly and ELF executables are archived. New checkpoint files are emitted each round for progress recovery. Previous experiment files are not altered. The original recording is replayed because the corrected full-chain feedback invalidates continuation from the old endpoint-only results.
