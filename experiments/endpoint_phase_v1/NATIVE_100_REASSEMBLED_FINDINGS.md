# Corrected native-driven 100-pass results

The replay completed 100 X-to-Y extensions and 100 Y-to-X extensions. Each extension was immediately followed by fresh assembly, linking and execution of all four complete updated chains. The resulting native registers supplied the next extension. There were 804 native programs: four bootstrap programs plus four after each of the 200 extensions. All 804 assembled, linked, exited zero and matched all eight reference registers.

The integrity audit links every projected value to its native source program, verifies that each validation used the just-extended chain hashes and lengths, verifies both archived sources and ELF hashes, and checks that the original recording values remain intact in the final chains.

## Outputs

- Final fronts: `[1, 1, 1, 1]`.
- Final backs: `[2, 1, 5, 1]`.
- Final lengths: 2,100 values per channel (1,800 original, 200 prepended, 100 appended).
- The validation target vector `[2,1,5,1]` first appears after extension step 16, at the end of round 8. That execution validates step 16. Its output is then used to append those values at step 17, in round 9.
- Channel 1 yields `[state=1, relations=0]` on the left from round 9 onward: 92 recorded zeros, all in the second left position. No projected chain-front zero was observed under state-first prepend order.
- The earlier `[1,1,1,7]` pattern from the endpoint-only harness was not observed in this full-chain native replay. That earlier run is preserved separately and should not be substituted for the corrected loop's results.

Validation of the previous extension and new chain values are linked but separately recorded. No repeated vector is labelled EOF. The user-specified executable-functionality criterion passes for every compiled chain.

Only new files were added on `codex/atlas-endpoint-phase-test`; earlier scripts and results were not edited. `native_reassembly_100_results/phase_history.csv` is the compact inspection view. `program_manifest.json` and `native_execution_summary.csv` record every execution. `assembled_sources.zip` and `native_executables.zip` preserve all native artifacts.
