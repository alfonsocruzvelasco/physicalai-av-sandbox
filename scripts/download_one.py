from __future__ import annotations

import argparse
import os
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download, hf_hub_url
from huggingface_hub.utils import HfHubHTTPError

REPO_ID = "nvidia/PhysicalAI-Autonomous-Vehicles"
REPO_TYPE = "dataset"

DEFAULT_MAX_MB = 100

def require_env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        raise SystemExit(f"FAIL: missing env var {name} (did you 'source scripts/env.local.sh'?)")
    return v

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Exact path_in_repo to download (one file only).")
    ap.add_argument("--max-mb", type=int, default=DEFAULT_MAX_MB, help="Hard size cap in MiB.")
    args = ap.parse_args()

    target_file = args.file.strip()
    max_bytes = args.max_mb * 1024 * 1024

    physical_root = Path(require_env("PHYSICALAI_AV_ROOT")).expanduser().resolve()
    out_dir = physical_root / "downloads"
    out_dir.mkdir(parents=True, exist_ok=True)

    api = HfApi()
    url = hf_hub_url(repo_id=REPO_ID, repo_type=REPO_TYPE, filename=target_file)

    try:
        meta = api.get_hf_file_metadata(url=url, token=True)
    except HfHubHTTPError as e:
        print("ERROR: Could not fetch authenticated file metadata:", e)
        return 2

    size = getattr(meta, "size", None)
    print("TARGET_FILE:", target_file)
    print("REMOTE_SIZE_BYTES:", size)
    print("MAX_BYTES:", max_bytes)

    if size is None:
        print("ERROR: No size in metadata; refusing to download.")
        return 3

    if size > max_bytes:
        print("REFUSE: File exceeds MAX_BYTES. No download performed.")
        return 4

    try:
        local_path = hf_hub_download(
            repo_id=REPO_ID,
            repo_type=REPO_TYPE,
            filename=target_file,
            local_dir=str(out_dir),
        )
    except HfHubHTTPError as e:
        print("ERROR: Download failed:", e)
        return 5

    p = Path(local_path)
    print("DOWNLOADED_TO:", str(p))
    print("LOCAL_SIZE_BYTES:", p.stat().st_size)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
