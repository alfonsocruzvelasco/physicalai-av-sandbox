from __future__ import annotations

import argparse

import pandas as pd

# NOTE: run with PYTHONPATH=src
from physicalai_av.intrinsics import load_camera_intrinsics
from physicalai_av.extrinsics import load_sensor_extrinsics


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--intr-chunk", default="0000")
    ap.add_argument("--extr-chunk", default="0000")
    ap.add_argument("--limit-clip", default=None, help="Optional clip_id to filter for readability.")
    args = ap.parse_args()

    intr = load_camera_intrinsics(args.intr_chunk)
    extr = load_sensor_extrinsics(args.extr_chunk)

    # Align names for join
    intr2 = intr.rename(columns={"camera_name": "sensor_name"})

    if args.limit_clip:
        intr2 = intr2[intr2["clip_id"] == args.limit_clip]
        extr = extr[extr["clip_id"] == args.limit_clip]

    merged = intr2.merge(extr, on=["clip_id", "sensor_name"], how="inner", suffixes=("_intr", "_extr"))

    print("intr_rows:", len(intr2))
    print("extr_rows:", len(extr))
    print("inner_join_rows:", len(merged))

    # Coverage: how many intr rows matched extr?
    if len(intr2) > 0:
        print("intr_match_rate:", round(len(merged) / len(intr2), 6))

    # Show a tiny sample
    cols = ["clip_id", "sensor_name", "width", "height", "cx", "cy", "qx", "qy", "qz", "qw", "x", "y", "z"]
    cols = [c for c in cols if c in merged.columns]
    print("\nSAMPLE:")
    with pd.option_context("display.max_columns", 50, "display.width", 160):
        print(merged[cols].head(5))


if __name__ == "__main__":
    main()
