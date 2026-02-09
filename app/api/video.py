from __future__ import annotations

import json
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import Person, ReferenceImage
from app.services.csv_writer import write_results_csv
from app.services.storage import save_upload, to_relative_path
from app.services.video_processor import process_video

router = APIRouter(prefix="/videos", tags=["videos"])


class ResultItem(BaseModel):
    name: str
    confidence: float
    first_seen_sec: float


class ProcessResponse(BaseModel):
    results: list[ResultItem]
    csv_path: str
    video_path: str


@router.post("/process", response_model=ProcessResponse)
def process_video_api(
    file: UploadFile = File(...),
    min_confidence: float = Form(0.6),
    frame_interval_sec: float = Form(1.0),
    db: Session = Depends(get_db),
) -> ProcessResponse:
    if min_confidence < 0 or min_confidence > 1:
        raise HTTPException(status_code=400, detail="min_confidence must be between 0 and 1")
    if frame_interval_sec <= 0:
        raise HTTPException(status_code=400, detail="frame_interval_sec must be > 0")

    data_dir = Path(settings.data_dir)
    video_dir = data_dir / "videos"
    video_path = save_upload(file, video_dir)
    video_rel = to_relative_path(data_dir, video_path)

    reference_items: list[dict] = []
    images = db.execute(select(ReferenceImage, Person).join(Person)).all()
    for image, person in images:
        embedding = json.loads(image.embedding_json) if image.embedding_json else None
        reference_items.append(
            {
                "name": person.name,
                "embedding": embedding,
                "image_path": data_dir / image.image_path,
            }
        )

    try:
        results = process_video(
            video_path,
            reference_items,
            min_confidence=min_confidence,
            frame_interval_sec=frame_interval_sec,
        )
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    result_dir = data_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    csv_path = result_dir / f"{video_path.stem}.csv"
    write_results_csv(csv_path, results)

    return ProcessResponse(
        results=[ResultItem(**item) for item in results],
        csv_path=to_relative_path(data_dir, csv_path),
        video_path=video_rel,
    )
