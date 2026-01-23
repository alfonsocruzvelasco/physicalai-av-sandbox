# physicalai-av-sandbox

Sandbox utilities to **access, sanity-check, and prototype loaders** for the gated Hugging Face dataset:

- `nvidia/PhysicalAI-Autonomous-Vehicles`

This repository **does not** contain dataset files. It contains **scripts + minimal Python loaders** to:

- authenticate against a **public gated dataset**
- safely download **single files** with a hard size guard
- inspect Parquet / ZIP structures
- load calibration (intrinsics / extrinsics) and run a simple join sanity-check

---

## Requirements

- Python **3.11** (recommended and CI target)
- A virtual environment (recommended)
- A Hugging Face token with:
  - **Read access**
  - access to **public gated repositories**
  - dataset terms accepted on the dataset page

---

## Setup

### 1) Create & activate venv

```bash
python3.11 -m venv ~/dev/venvs/physicalai-av
source ~/dev/venvs/physicalai-av/bin/activate

python -m pip install -U pip
python -m pip install -e ".[dev]"
```

### 2) Hugging Face login (gated token)

```bash
huggingface-cli login
huggingface-cli whoami
```

### 3) Configure local paths (and optional HF cache redirection)

This repo expects `scripts/env.local.sh` (ignored by git) defining:

- `PHYSICALAI_AV_ROOT`  (required)
- `HF_HOME`             (optional)
- `HF_HUB_CACHE`        (optional)

Sanity check:

```bash
source scripts/env.local.sh
echo "$PHYSICALAI_AV_ROOT"
ls -lah "$PHYSICALAI_AV_ROOT"
```

---

## Doctor check

Verifies:

- env vars exist
- directories are writable
- token can access gated metadata

```bash
python -u scripts/doctor.py
```

---

## Discover files on Hugging Face

Prefix listing:

```bash
python -u scripts/find_files.py --prefix calibration/ --limit 80
```

Keyword search:

```bash
python -u scripts/search_files.py --contains extrinsics --limit 80
python -u scripts/search_files.py --contains egomotion --limit 80
```

---

## Download a single file safely

```bash
python -u scripts/download_one.py   --file calibration/camera_intrinsics/camera_intrinsics.chunk_0000.parquet   --max-mb 100
```

---

## Inspect downloaded files

### Parquet

```bash
python -u scripts/inspect_parquet.py   --file ~/datasets/physicalai-av/downloads/calibration/camera_intrinsics/camera_intrinsics.chunk_0000.parquet
```

### ZIP

```bash
python -u scripts/inspect_zip.py   --file ~/datasets/physicalai-av/downloads/labels/egomotion/egomotion.chunk_0000.zip
```

---

## Calibration sanity join (intrinsics ↔ extrinsics)

```bash
python -u scripts/join_calibration.py --chunk 0000
python -m pytest -q
```

---

## Egomotion sanity checks

Download one egomotion zip:

```bash
python -u scripts/download_one.py   --file labels/egomotion/egomotion.chunk_0000.zip   --max-mb 100
```

Inspect zip:

```bash
python -u scripts/inspect_zip.py   --file ~/datasets/physicalai-av/downloads/labels/egomotion/egomotion.chunk_0000.zip
```

Clip-level check:

```bash
python -u scripts/check_egomotion_clip.py   --chunk 0000   --clip-id 25cd4769-5dcf-4b53-a351-bf2c5deb6124
```

---

## Repo principles

- **No dataset files** committed
- **No HF tokens** committed
- **No caches** committed
- Only curated logs under `reports/` may be versioned for reproducibility

---

## Commit workflow

After updating docs or scripts:

```bash
python -m pytest -q
git status

git add README.md
git commit -m "docs: polish README and workflows"
git push
```
