# Persons In A Video

This project will provide APIs to upload reference images and videos, run recognition with liveness checks, and output a CSV with the first time each person appears.

## Run with Docker (local)

### 1) Build the image

```
docker build -t persons-in-video .
```

### 2) Run the container

```
docker run --rm -p 8000:8000 \
  -v "%cd%\\data":/app/data \
  persons-in-video
```

Notes:
- The container exposes port 8000. Open http://localhost:8000/docs for the API UI.
- The volume mount stores uploaded files and generated CSVs under data/ on your machine.

### 3) Verify the API is up

```
curl http://localhost:8000/health
```

Expected output is a small JSON payload with status OK.

## Next Steps

- Add pyproject.toml and the FastAPI app code.
- Implement API endpoints and the processing pipeline.
