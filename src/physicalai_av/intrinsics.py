from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq


INTRINSICS_REL = Path("downloads/calibration/camera_intrinsics")

VALUE_COLS = [
    "width", "height", "cx", "cy",
    "bw_poly_0", "bw_poly_1", "bw_poly_2", "bw_poly_3", "bw_poly_4",
    "fw_poly_0", "fw_poly_1", "fw_poly_2", "fw_poly_3", "fw_poly_4",
]
KEY_COLS = ["clip_id", "camera_name"]
EXPECTED_COLS = VALUE_COLS + KEY_COLS


def _physical_root() -> Path:
    root = os.environ.get("PHYSICALAI_AV_ROOT", "").strip()
    if not root:
        raise RuntimeError("Missing PHYSICALAI_AV_ROOT (did you 'source scripts/env.local.sh'?)")
    return Path(root).expanduser().resolve()


def load_camera_intrinsics(chunk: str = "0000") -> pd.DataFrame:
    """
    Load one intrinsics parquet chunk into a DataFrame with explicit key columns:
    clip_id, camera_name.
    """
    root = _physical_root()
    p = root / INTRINSICS_REL / f"camera_intrinsics.chunk_{chunk}.parquet"
    if not p.exists():
        raise FileNotFoundError(str(p))

    table = pq.read_table(p)
    df = table.to_pandas()

    # If clip_id/camera_name are index columns, normalize them back into columns.
    if any(k not in df.columns for k in KEY_COLS):
        if list(df.index.names) == KEY_COLS:
            df = df.reset_index()
        else:
            # Defensive: handle partial index naming
            df = df.reset_index()

    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing expected columns after normalization: {missing}")

    return df[EXPECTED_COLS].copy()
