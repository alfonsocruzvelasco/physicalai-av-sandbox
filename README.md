# physicalai-av-sandbox

Sandbox utilities to **access, sanity-check, and prototype loaders** for the gated dataset:

- `nvidia/PhysicalAI-Autonomous-Vehicles` (Hugging Face datasets)

This repository **does not** contain the dataset files. It contains **scripts + minimal Python loaders** to:
- authenticate against a **public gated dataset**
- safely download **single files** with a hard size guard
- inspect Parquet/ZIP structures
- load calibration (intrinsics/extrinsics) and run simple join checks

---

## Requirements

- Python **>= 3.11**
- A virtual environment (recommended)
- Hugging Face token with:
  - **Read access**
  - **Enabled: “public gated repositories”**
  - Dataset terms accepted on the dataset page

---

## Setup

### 1) Create & activate venv
```bash
python -m venv ~/dev/venvs/physicalai-av
source ~/dev/venvs/physicalai-av/bin/activate
pip install -U pip
pip install -e .
````

### 2) Hugging Face login (gated token)

```bash
huggingface-cli login
huggingface-cli whoami
```

### 3) Configure local paths and HF cache redirection

This repo expects `scripts/env.local.sh` (ignored by git) defining:

* `PHYSICALAI_AV_ROOT`
* `HF_HOME`
* `HF_HUB_CACHE`

Example:

```bash
source scripts/env.local.sh
```

---

## Doctor check

Verify:

* env vars exist
* directories are writable
* token can access gated metadata

```bash
python scripts/doctor.py
```

---

## Download a single file safely

```bash
python scripts/download_one.py \
  --file calibration/camera_intrinsics/camera_intrinsics.chunk_0000.parquet \
  --max-mb 100
```

---

## Inspect downloaded files

### Parquet

```bash
python scripts/inspect_parquet.py \
  --file ~/datasets/physicalai-av/downloads/calibration/camera_intrinsics/camera_intrinsics.chunk_0000.parquet
```

### Zip

```bash
python scripts/inspect_zip.py \
  --file ~/datasets/physicalai-av/downloads/labels/egomotion/egomotion.chunk_0000.zip
```

---

## Calibration sanity join (intrinsics ↔ extrinsics)

```bash
python scripts/join_calibration.py --chunk 0000
```

---

## Egomotion sanity checks

Download one egomotion zip:

```bash
python scripts/download_one.py \
  --file labels/egomotion/egomotion.chunk_0000.zip \
  --max-mb 100
```

Inspect zip:

```bash
python scripts/inspect_zip.py \
  --file ~/datasets/physicalai-av/downloads/labels/egomotion/egomotion.chunk_0000.zip
```

Clip-level check:

```bash
python scripts/check_egomotion_clip.py \
  --chunk 0000 \
  --clip-id 25cd4769-5dcf-4b53-a351-bf2c5deb6124
```

---

## Repo principles

* **No dataset files** committed
* **No HF tokens** committed
* **No caches** committed
* Only a few curated logs under `reports/` are versioned for reproducibility

MD

````

Then:

```bash
git add README.md
git commit -m "Add README with setup and workflow documentation"
git push
````

---

## 2) One more thing (recommended): add LICENSE + short roadmap

This is optional but extremely cheap and increases repo professionalism. I recommend:

### `LICENSE` (MIT)

```bash
curl -fsSL https://raw.githubusercontent.com/github/choosealicense.com/gh-pages/_licenses/mit.txt \
  | sed "s/\[year\]/2026/; s/\[fullname\]/Alfonso Cruz Velasco/" \
  > LICENSE
```

Commit:

```bash
git add LICENSE
git commit -m "Add MIT license"
git push
```

### Add a tiny “Next steps” section in README

Append:

* loaders for more labels
* unify time axis / coordinate frames
* tiny visualization script

(If you want, I’ll add this in a tight professional form, but don’t overdo it.)

---

## 3) Repo hygiene check (1 command)

Before you call it “publicly polished”:

```bash
git grep -n "token\|HF_TOKEN\|hf_" || true
```


