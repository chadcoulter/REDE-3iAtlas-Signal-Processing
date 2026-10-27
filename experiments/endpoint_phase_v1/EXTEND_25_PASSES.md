# Twenty-five passes in each direction

This experiment reuses the recorded fixed wiring from `endpoint_phase.py`. It performs 25 alternating rounds. Every round:

1. Read the current four front values and four back values.
2. Seed with the back values, process the front values, and append the four `target` outputs, one per channel.
3. Use those updated endpoints in the reverse process and prepend each channel's `state`, `relations` pair, in that order.

The next round uses the updated chains. No original values are removed. At 25 rounds, each original 1,800-value chain has 50 new front values and 25 new back values, totaling 1,875. Every active channel's three-other-channel view is retained in the phase history. Seeds use the same named register mapping throughout; other registers start at one for each directional transform.

Literal numeric zeros are preserved and logged before encoding. Endpoints are compared for exact repeated states. Neither a zero nor a repeat stops the requested 25 rounds. No unknown Y termination is pre-labelled as EOF.

For the requested executable-code criterion, an actual native program is prepared for every channel after every directional extension: 25 rounds × 2 directions × 4 channels = 200 executable checks. Each program runs its entire extended chain. GNU as and ld assemble/link the sources in WSL; all eight native final registers are compared with the interpreter. Original measurement recovery is not a criterion.

All output paths must be new. Existing experiment files are not modified.

```powershell
python -B experiments/endpoint_phase_v1/extend_25_passes.py C:/Users/ccoulter/Downloads/3I_ATLAS_six_recordings_four_stripes_asm.zip --output experiments/endpoint_phase_v1/extension_25_results
```

Then execute `native_batch_runner.py` inside WSL Python with the Linux path to `extension_25_results`. `phase_history.csv` is the compact front/back sequence; `phase_history.json` preserves other-channel views; `final_chains.json` contains the complete extended chains; `register_trace.csv` records directional transforms. Native reports and compressed source are added by the batch runner.
