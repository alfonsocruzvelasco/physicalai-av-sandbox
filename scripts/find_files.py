from __future__ import annotations

import argparse
from huggingface_hub import HfApi

REPO_ID = "nvidia/PhysicalAI-Autonomous-Vehicles"

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", required=True)
    ap.add_argument("--limit", type=int, default=100)
    args = ap.parse_args()

    api = HfApi()
    files = api.list_repo_files(repo_id=REPO_ID, repo_type="dataset")

    n = 0
    for f in files:
        if f.startswith(args.prefix):
            print(f)
            n += 1
            if n >= args.limit:
                break
    print("shown:", n)

if __name__ == "__main__":
    main()
