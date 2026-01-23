from __future__ import annotations

import argparse

from physicalai_av.intrinsics import load_camera_intrinsics
from physicalai_av.extrinsics import load_sensor_extrinsics


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunk", default="0000")
    ap.add_argument("--head", type=int, default=20)
    args = ap.parse_args()

    intr = load_camera_intrinsics(args.chunk)
    extr = load_sensor_extrinsics(args.chunk)

    intr = intr.rename(columns={"camera_name": "sensor_name"})
    merged = intr.merge(extr, how="left", on=["clip_id", "sensor_name"], indicator=True)

    total = len(merged)
    matched = int((merged["_merge"] == "both").sum())
    missing = total - matched

    print("CHUNK:", args.chunk)
    print("INTR_ROWS:", len(intr))
    print("EXTR_ROWS:", len(extr))
    print("JOIN_TOTAL:", total)
    print("JOIN_MATCHED:", matched)
    print("JOIN_MISSING_EXTR_FOR_INTR:", missing)

    bad = merged.loc[merged["_merge"] != "both", ["clip_id", "sensor_name"]].drop_duplicates()
    print("\nUNMATCHED_INTR_SENSOR_NAMES (sample):")
    print(bad.head(args.head).to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
