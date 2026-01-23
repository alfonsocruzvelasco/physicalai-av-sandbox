from __future__ import annotations

import os
from pathlib import Path
import zipfile
from typing import Iterable

import pandas as pd
import pyarrow.parquet as pq


EGOMOTION_ZIP_REL = Path("downloads/labels/egomotion")  # under PHYSICALAI_AV_ROOT
EGOMOTION_ZIP_NAME = "egomotion.chunk_{chunk}.zip"


def _physical_root() -> Path:
    root = os.environ.get("PHYSICALAI_AV_ROOT", "").strip()
    if not root:
        raise RuntimeError("Missing PHYSICALAI_AV_ROOT (did you 'source scripts/env.local.sh'?)")
    return Path(root).expanduser().resolve()


def _zip_path(chunk: str) -> Path:
    root = _physical_root()
    return root / EGOMOTION_ZIP_REL / EGOMOTION_ZIP_NAME.format(chunk=chunk)


def list_clip_ids_in_egomotion_zip(chunk: str = "0000") -> list[str]:
    zp = _zip_path(chunk)
    if not zp.exists():
        raise FileNotFoundError(str(zp))

    with zipfile.ZipFile(zp, "r") as z:
        out: list[str] = []
        for name in z.namelist():
            if name.endswith(".egomotion.parquet"):
                out.append(name.split(".egomotion.parquet")[0])
        return out


def load_egomotion_clip(chunk: str, clip_id: str) -> pd.DataFrame:
    """
    Load egomotion for a single clip_id from a chunk zip.

    Returns a DataFrame with an added `clip_id` column.
    """
    zp = _zip_path(chunk)
    if not zp.exists():
        raise FileNotFoundError(str(zp))

    member = f"{clip_id}.egomotion.parquet"
    with zipfile.ZipFile(zp, "r") as z:
        try:
            with z.open(member) as f:
                table = pq.read_table(f)
        except KeyError:
            raise FileNotFoundError(f"{member} not found in {zp}") from None

    df = table.to_pandas()
    if "clip_id" not in df.columns:
        df.insert(0, "clip_id", clip_id)
    return df


def load_egomotion_many(chunk: str, clip_ids: Iterable[str], *, limit: int | None = None) -> pd.DataFrame:
    """
    Load multiple clip_ids and concatenate.
    Use limit to cap number of clips loaded (safety for experimentation).
    """
    frames: list[pd.DataFrame] = []
    n = 0
    for cid in clip_ids:
        frames.append(load_egomotion_clip(chunk, cid))
        n += 1
        if limit is not None and n >= limit:
            break
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
