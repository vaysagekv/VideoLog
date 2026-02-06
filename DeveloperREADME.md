# Developer README

This file documents how to create a virtual environment, install dependencies, and run the app locally.

## Prerequisites

- Python 3.11+

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

## Verify the health endpoint

```bash
python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/health').read().decode())"
```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://YOUR_HOST/YOUR_USER/YOUR_REPO.git
git push -u origin main