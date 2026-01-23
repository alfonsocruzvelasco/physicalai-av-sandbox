from __future__ import annotations

import argparse
from pathlib import Path

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="Path to a local parquet file.")
    ap.add_argument("--head", type=int, default=5)
    args = ap.parse_args()

    p = Path(args.file).expanduser().resolve()
    if not p.exists():
        raise SystemExit(f"FAIL: file not found: {p}")

    try:
        import pyarrow.parquet as pq  # type: ignore
    except Exception:
        raise SystemExit("FAIL: pyarrow not installed in this venv. Install it: pip install pyarrow")

    tbl = pq.read_table(p)
    print("FILE:", str(p))
    print("ROWS:", tbl.num_rows)
    print("COLUMNS:", tbl.num_columns)
    print("SCHEMA:")
    print(tbl.schema)

    n = min(args.head, tbl.num_rows)
    print(f"\nHEAD({n}):")
    print(tbl.slice(0, n).to_pandas())

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
