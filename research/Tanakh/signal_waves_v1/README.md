# Base signal and three child waves

The CSV contains one row per Hebrew gematria value from the complete supplied `tanakh_reconstructed.txt`, preserving the source's code-point positions. There are 1,172,332 base points. These are individual letter values, rather than the earlier ten-letter packed or summed samples.

The child waves use overlapping adjacent base points a and b:

- SUM: `(a + b) % 231`
- LINEAR: `(22 * a + b) % 231`
- PRODUCT: `(a * b) % 231`

Each child wave has 1,172,331 samples and is aligned to the first point of its pair. The last CSV row preserves the final base point and leaves child fields blank. There is no wraparound pair or padding. Indices are sequence positions, not timestamps.

## Functions

`src/signal_builder.py` adds `SignalBuilder`, a subclass of the existing `SignalParser`, without modifying the parser. It exposes `BuildSignal`, `BuildSumWave`, `BuildLinearWave`, and `BuildProductWave` as methods and as module functions.

```python
from signal_builder import SignalBuilder
builder = SignalBuilder()
signal = builder.BuildSignal([4, 2, 200, 10])
print(signal.base)
print(signal.sum_wave, signal.linear_wave, signal.product_wave)
signal.SaveCSV('new_signal_waves.csv')
```

`BuildSignal` accepts Hebrew text or an integer iterable. Text uses ordinary gematria, parser Hebrew overrides, and the parser's unknown-character policy. Structural characters are omitted from the numeric stream while their original index gaps remain. Integer inputs retain arbitrary integer precision. Modulus and linear multiplier are configurable. `SaveCSV` refuses to overwrite existing files.

`build_wave_rows.py` constructs the complete rows through `BuildSignal`; `export_waves.mjs` writes and checks batches through Artifact Tool before serializing the resulting grid to CSV. `verify_waves.py` independently checks every exported row against the source text and equations. `build_report.json` records the source hash and parameters; `verification.json` records full-file verification.

The CSV exceeds Excel's single-sheet row capacity. Read it as a CSV stream or with a data-analysis tool to include all points.
