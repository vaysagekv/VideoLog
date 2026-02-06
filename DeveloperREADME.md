# Developer README

This file documents how to create a virtual environment, install dependencies, configure the app, and run and test it locally.

## Prerequisites

- Python 3.11+
- System packages for OpenCV video IO (ffmpeg + libgl). On Debian-based systems:

```bash
sudo apt-get update
sudo apt-get install -y ffmpeg libgl1
```

## Environment variables

Set these before starting the app if you want to override defaults:

- `PIV_DATA_DIR`: base directory for all stored files (default: `data`)
- `PIV_MODEL_DIR`: InsightFace model directory (default: `$PIV_DATA_DIR/models/insightface`)
- `PIV_DB_URL`: database URL (default: `sqlite:///$PIV_DATA_DIR/app.db`)

## Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -e .
```

## Run the app

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Model download and warm-up

The app uses InsightFace (`buffalo_l`) and will download models on first startup into the model directory. Ensure the machine has internet access for the first run.

If you want to pre-download models, start the app once and wait for startup to complete. You should see the model files under:

- Default: `data/models/insightface`
- Custom: whatever `PIV_MODEL_DIR` points to
```

## Verify the health endpoint

```bash
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
```

## Test reference upload

```bash
curl -F "name=Alice" -F "file=@/path/to/alice.jpg" http://localhost:8000/references
```

## Test video processing

```bash
curl -F "file=@/path/to/video.mp4" http://localhost:8000/videos/process
```

Expected output is a JSON payload with a `results` list and a `csv_path` pointing to the generated CSV under the data directory.