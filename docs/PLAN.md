# Plan: Scaffold ML Video Recognition Service

This plan adds a devcontainer, Dockerfile, and README guidance first, then scaffolds the FastAPI + InsightFace app with liveness checking and CSV output. Defaults are Python 3.11, CPU-only inference, and a plan file at docs/PLAN.md. The project will support reference image upload APIs, video upload/testing APIs, and produce a CSV listing name, confidence, and first appearance time.

## Steps
1. Create devcontainer essentials in .devcontainer/devcontainer.json and .devcontainer/Dockerfile: base on Python 3.11, install system deps (ffmpeg, libgl), configure VS Code extensions (Python, Docker), and set workspace mount.
2. Add runtime Dockerfile for local execution in Dockerfile: slim Python 3.11, install system deps for OpenCV, install Python deps, copy app, expose port, run uvicorn.
3. Draft project structure and dependencies in pyproject.toml, with FastAPI, Uvicorn, SQLAlchemy, Pydantic, OpenCV, InsightFace, ONNXRuntime (CPU), pandas.
4. Implement core app skeleton in app/main.py with router registration, app/config.py for settings, and app/db.py for SQLite setup.
5. Add API endpoints and services: reference upload in app/api/reference.py, video upload and status/results in app/api/video.py, video processing in app/services/video_processor.py, matching in app/services/matcher.py, CSV generation in app/services/csv_writer.py, and background job handler in app/services/jobs.py.
6. Document full local Docker run guide in README.md: build/run commands, volume mounts for data, sample curl requests, where CSV results land.

## Verification
- Build devcontainer and ensure workspace opens without errors.
- docker build -t persons-in-video . then docker run -p 8000:8000 ... and verify /docs loads.
- Upload references and a short test video; confirm CSV contains name, confidence, first_seen_sec.

## Decisions
- Python 3.11, CPU-only Docker image.
- Plan file path: docs/PLAN.md.
