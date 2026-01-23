from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


EXTRINSICS_REL = Path("downloads/calibration/sensor_extrinsics")

VALUE_COLS = ["qx", "qy", "qz", "qw", "x", "y", "z"]
KEY_COLS = ["clip_id", "sensor_name"]
EXPECTED_COLS = VALUE_COLS + KEY_COLS


def _physical_root() -> Path:
    root = os.environ.get("PHYSICALAI_AV_ROOT", "").strip()
    if not root:
        raise RuntimeError("Missing PHYSICALAI_AV_ROOT (did you 'source scripts/env.local.sh'?)")
    return Path(root).expanduser().resolve()


def load_sensor_extrinsics(chunk: str = "0000") -> pd.DataFrame:
    """
    Load one sensor extrinsics parquet chunk into a DataFrame with explicit key columns:
    clip_id, sensor_name.
    """
    root = _physical_root()
    p = root / EXTRINSICS_REL / f"sensor_extrinsics.chunk_{chunk}.parquet"
    if not p.exists():
        raise FileNotFoundError(str(p))

    table = pq.read_table(p)
    df = table.to_pandas()

    # Normalize index columns -> regular columns (HF Parquet keeps keys as pandas index).
    if any(k not in df.columns for k in KEY_COLS):
        df = df.reset_index()

    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns after normalization: {missing}")

    return df[EXPECTED_COLS].copy()
