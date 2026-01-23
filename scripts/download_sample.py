from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download, hf_hub_url
from huggingface_hub.utils import HfHubHTTPError

REPO_ID = "nvidia/PhysicalAI-Autonomous-Vehicles"
REPO_TYPE = "dataset"

TARGET_FILE = "calibration/camera_intrinsics/camera_intrinsics.chunk_0000.parquet"
MAX_BYTES = 100 * 1024 * 1024  # 100 MiB

def require_env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        raise RuntimeError(f"Missing env var: {name}. Did you 'source scripts/env.local.sh'?")
    return v

def main() -> int:
    physical_root = Path(require_env("PHYSICALAI_AV_ROOT")).expanduser().resolve()
    out_dir = physical_root / "downloads"
    out_dir.mkdir(parents=True, exist_ok=True)

    api = HfApi()

    url = hf_hub_url(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        filename=TARGET_FILE,
    )

    # Authenticated metadata fetch (works even when HEAD is 401)
    try:
        meta = api.get_hf_file_metadata(url=url, token=True)
    except HfHubHTTPError as e:
        print("ERROR: Could not fetch authenticated file metadata:", e)
        print("If this is gating/terms, accept terms on the dataset page and rerun.")
        return 2

    size = getattr(meta, "size", None)
    print("TARGET_FILE:", TARGET_FILE)
    print("REMOTE_SIZE_BYTES:", size)
    print("MAX_BYTES:", MAX_BYTES)

    if size is None:
        print("ERROR: No size in metadata; refusing to download.")
        return 3

    if size > MAX_BYTES:
        print("REFUSE: File exceeds MAX_BYTES. No download performed.")
        return 4

    # Download exactly one file
    try:
        local_path = hf_hub_download(
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            filename=TARGET_FILE,
            local_dir=str(out_dir),
        )
    except HfHubHTTPError as e:
        print("ERROR: Download failed:", e)
        print("If this is gating/terms, accept terms on the dataset page and rerun.")
        return 5

    p = Path(local_path)
    print("DOWNLOADED_TO:", str(p))
    print("LOCAL_SIZE_BYTES:", p.stat().st_size)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
