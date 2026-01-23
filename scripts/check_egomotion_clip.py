from __future__ import annotations

import argparse

import pandas as pd

from physicalai_av.egomotion import load_egomotion_clip
from physicalai_av.intrinsics import load_camera_intrinsics
from physicalai_av.extrinsics import load_sensor_extrinsics


def _guess_time_col(df: pd.DataFrame) -> str | None:
    # Common patterns; we’ll keep it pragmatic.
    candidates = [
        "timestamp_ns", "timestamp_us", "timestamp_ms", "timestamp_s",
        "timestamp", "t", "time",
        "frame_idx", "frame", "index",
    ]
    for c in candidates:
        if c in df.columns:
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", default="0000")
    ap.add_argument("--clip-id", required=True)
    args = ap.parse_args()

    ego = load_egomotion_clip(args.chunk, args.clip_id)
    print("CHUNK:", args.chunk)
    print("CLIP_ID:", args.clip_id)
    print("EGO_ROWS:", len(ego))
    print("EGO_COLS:", len(ego.columns))
    print("EGO_COLUMNS:", ", ".join(map(str, ego.columns)))

    # Join feasibility: calibration presence by clip_id
    intr = load_camera_intrinsics(args.chunk)
    extr = load_sensor_extrinsics(args.chunk)

    intr_n = int((intr["clip_id"] == args.clip_id).sum())
    extr_n = int((extr["clip_id"] == args.clip_id).sum())
    print("INTR_ROWS_FOR_CLIP:", intr_n)
    print("EXTR_ROWS_FOR_CLIP:", extr_n)

    # Basic quality checks
    nan_cols = [c for c in ego.columns if ego[c].isna().any()]
    print("EGO_HAS_NAN_COLS:", len(nan_cols))
    if nan_cols:
        print("EGO_NAN_COLS_SAMPLE:", nan_cols[:20])

    tcol = _guess_time_col(ego)
    print("TIME_COL_GUESS:", tcol)
    if tcol is not None:
        s = ego[tcol]
        if pd.api.types.is_numeric_dtype(s):
            mono = bool(s.is_monotonic_increasing)
            print("TIME_MONOTONIC_INCREASING:", mono)

    print("\nHEAD(3):")
    print(ego.head(3).to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
