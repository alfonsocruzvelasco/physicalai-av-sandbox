from __future__ import annotations

import argparse
from pathlib import Path
import zipfile


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--head", type=int, default=50)
    args = ap.parse_args()

    p = Path(args.file).expanduser().resolve()
    if not p.exists():
        raise SystemExit(f"FAIL: file not found: {p}")

    with zipfile.ZipFile(p, "r") as z:
        infos = z.infolist()
        print("FILE:", str(p))
        print("ENTRIES:", len(infos))

        total_uncompressed = sum(i.file_size for i in infos)
        total_compressed = sum(i.compress_size for i in infos)
        print("TOTAL_UNCOMPRESSED_BYTES:", total_uncompressed)
        print("TOTAL_COMPRESSED_BYTES:", total_compressed)

        print("\nHEAD_ENTRIES:")
        for i, info in enumerate(infos[: args.head], start=1):
            print(f"{i:03d}  {info.file_size:12d}  {info.compress_size:12d}  {info.filename}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
