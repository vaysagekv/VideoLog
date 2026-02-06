# Implementation Plan: API Design

This plan turns the scaffold in docs/PLAN.md into concrete API endpoints, request/response schemas, and storage rules. It assumes synchronous video processing, local filesystem storage, JSON-only responses, and multiple reference images per person.

## Core Data
- Person: name + optional metadata JSON.
- Reference image: stored on disk, linked to a person.
- Video processing result: JSON response plus persisted CSV on disk.

## Storage Conventions
- Base data directory: `data/` (configurable).
- Reference images: `data/references/{person_id}/{uuid}.{ext}`.
- Uploaded videos: `data/videos/{uuid}.{ext}`.
- CSV outputs: `data/results/{uuid}.csv`.

## API Endpoints

### Health
- `GET /health`
  - Response: `{ "status": "ok" }`

### References
- `POST /references`
  - Multipart form fields:
    - `name` (string, required)
    - `file` (image file, required)
    - `metadata` (string JSON, optional)
  - Behavior:
    - Creates person if new.
    - Adds image to person.
  - Response:
    - `person_id`, `name`, `image_id`, `image_path`, `metadata`.

- `GET /references`
  - Response: list of persons with image counts.

- `GET /references/{person_id}`
  - Response: person details with all image paths.

- `DELETE /references/{person_id}`
  - Behavior: deletes person and all reference images.
  - Response: `{ "deleted": true }`

### Video Processing
- `POST /videos/process`
  - Multipart form fields:
    - `file` (video file, required)
    - `min_confidence` (float 0..1, optional, default 0.6)
    - `frame_interval_sec` (float, optional, default 1.0)
  - Behavior:
    - Saves the video to disk.
    - Loads reference images.
    - Runs synchronous detection + identification.
    - Writes CSV to disk.
  - Response:
    - `results`: list of `{ name, confidence, first_seen_sec }`.
    - `csv_path`: path to CSV relative to data dir.
    - `video_path`: path to video relative to data dir.

## CSV Format
- Columns: `name,confidence,first_seen_sec`.
- `confidence` is a percentage from 0 to 100.
- `first_seen_sec` is the earliest timestamp a person appears.

## Error Handling
- `400` for invalid JSON metadata or missing files.
- `404` for missing person id.
- `503` if ML models are unavailable.

## Next Implementation Steps
1. Add SQLAlchemy models and DB session helpers.
2. Build storage helpers for saving uploads and cleaning files.
3. Implement reference endpoints.
4. Implement video processing endpoint and CSV writer.
5. Wire routers into the FastAPI app and initialize DB.
