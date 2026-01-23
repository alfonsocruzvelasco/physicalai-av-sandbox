from __future__ import annotations

import os

from physicalai_av.intrinsics import load_camera_intrinsics
from physicalai_av.extrinsics import load_sensor_extrinsics


def test_intrinsics_extrinsics_join_chunk_0000() -> None:
    # This repo assumes PHYSICALAI_AV_ROOT points to your local dataset workspace.
    root = os.environ.get("PHYSICALAI_AV_ROOT", "").strip()
    assert root, "PHYSICALAI_AV_ROOT must be set (source scripts/env.local.sh)"

    intr = load_camera_intrinsics("0000").rename(columns={"camera_name": "sensor_name"})
    extr = load_sensor_extrinsics("0000")

    merged = intr.merge(extr, how="left", on=["clip_id", "sensor_name"], indicator=True)
    assert (merged["_merge"] == "both").all(), "All intrinsics rows should have matching extrinsics"
