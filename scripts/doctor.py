from __future__ import annotations

import os
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_url

REPO_ID = "nvidia/PhysicalAI-Autonomous-Vehicles"
REPO_TYPE = "dataset"

def require_env(name: str) -> str:
    v = os.environ.get(name, "").strip()
    if not v:
        raise SystemExit(f"FAIL: missing env var {name} (did you 'source scripts/env.local.sh'?)")
    return v

def main() -> None:
    root = Path(require_env("PHYSICALAI_AV_ROOT")).expanduser().resolve()
    hf_home = Path(require_env("HF_HOME")).expanduser().resolve()
    hf_cache = Path(require_env("HF_HUB_CACHE")).expanduser().resolve()

    print("PHYSICALAI_AV_ROOT:", root)
    print("HF_HOME:", hf_home)
    print("HF_HUB_CACHE:", hf_cache)

    # Writable checks
    for p in (root, hf_home, hf_cache):
        p.mkdir(parents=True, exist_ok=True)
        test = p / ".write_test"
        test.write_text("ok\n", encoding="utf-8")
        test.unlink()
        print("OK writable:", p)

    # Auth + gated access check (metadata only)
    url = hf_hub_url(repo_id=REPO_ID, repo_type=REPO_TYPE, filename="README.md")
    meta = HfApi().get_hf_file_metadata(url=url, token=True)
    print("OK gated access: README.md size =", meta.size)

if __name__ == "__main__":
    main()
