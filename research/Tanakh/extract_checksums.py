#!/usr/bin/env python3
"""Extract the existing SUM channel to recovery_data.npy for Dalet recovery."""
import csv
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "signal_waves_v1" / "signal_waves.csv"
OUTPUT = HERE / "recovery_data.npy"

with SOURCE.open("r", encoding="utf-8-sig", newline="") as stream:
    reader = csv.DictReader(stream)
    columns = reader.fieldnames or []
    sum_column = next(
        (name for name in columns if name.strip().lower() in ("sum", "sum_wave")),
        None,
    )
    if sum_column is None:
        raise ValueError(f"SUM channel not found. CSV columns: {columns}")
    checksums = [int(row[sum_column]) for row in reader if row[sum_column].strip()]

np.save(OUTPUT, np.asarray(checksums, dtype=np.uint8))
print(f"Saved {len(checksums)} checksums to {OUTPUT}")
