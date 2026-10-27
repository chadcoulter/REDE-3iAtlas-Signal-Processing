# Continuing an existing chain in 100-pass batches

`continue_100_passes.py` resumes the saved final chains rather than restarting the original recording. It preserves prior chain values and adds two front values and one back value per channel per round. The existing fixed register assignment and phase function are unchanged.

```powershell
python -B experiments/endpoint_phase_v1/continue_100_passes.py C:/Users/ccoulter/Downloads/3I_ATLAS_six_recordings_four_stripes_asm.zip --resume experiments/endpoint_phase_v1/extension_25_results --passes 100 --output experiments/endpoint_phase_v1/continuation_100_results
```

The output directory must be new. The new `final_chains.json` can be passed to a later invocation through its enclosing directory with `--resume`. Every batch saves complete history and register traces, exact zero observations, endpoint repeat observations and a full fixed-point check.

The batch prepares twelve native executable checks: the final full chain, newly prepended segment, and newly appended segment for every channel. Run `native_batch_runner.py` inside WSL against this output directory to assemble/link/execute those twelve programs. This avoids repeatedly compiling unchanged fixed-point steps while still checking the full chains and all new generated commands.

The current `phase()` implementation computes outputs from endpoint vectors only. It does not traverse the interior chain during phase generation. Its native executable checks do execute the full chains. If the endpoint vectors and both directional outputs repeat exactly, continued identical batches cannot escape that loop: chain length, pass number and interior data are absent from the phase function. Such a loop is not labelled a start or finish marker. Changing the wiring/state propagation or defining a termination interpretation is a separate decision, not a hidden alteration to this run.
