from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import Person, ReferenceImage
from app.services.matcher import Matcher
from app.services.storage import build_abs_path, save_upload, to_relative_path

router = APIRouter(prefix="/references", tags=["references"])


def parse_metadata(raw: Optional[str]) -> Optional[dict[str, Any]]:
    if raw is None:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="metadata must be valid JSON") from exc


class ReferenceImageOut(BaseModel):
    image_id: int
    image_path: str


class PersonOut(BaseModel):
    person_id: int
    name: str
    metadata: Optional[dict[str, Any]]
    images: list[ReferenceImageOut]


class ReferenceCreateOut(BaseModel):
    person_id: int
    name: str
    image_id: int
    image_path: str
    metadata: Optional[dict[str, Any]]


@router.post("", response_model=ReferenceCreateOut)
def create_reference(
    name: str = Form(...),
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db),
) -> ReferenceCreateOut:
    metadata_dict = parse_metadata(metadata)

    person = db.execute(select(Person).where(Person.name == name)).scalar_one_or_none()
    if person is None:
        person = Person(name=name, metadata_json=json.dumps(metadata_dict) if metadata_dict else None)
        db.add(person)
        db.flush()
    elif metadata_dict is not None:
        person.metadata_json = json.dumps(metadata_dict)

    target_dir = Path(settings.data_dir) / "references" / str(person.id)
    saved_path = save_upload(file, target_dir)
    relative_path = to_relative_path(Path(settings.data_dir), saved_path)

    matcher = Matcher()
    if not matcher.available:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(status_code=503, detail="face model is not available")

    embedding = matcher.extract_embedding_from_image_path(str(saved_path))
    if embedding is None:
        saved_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail="no face detected in reference image")
    embedding_json = json.dumps(embedding.tolist())

    image = ReferenceImage(
        person_id=person.id,
        image_path=relative_path,
        embedding_json=embedding_json,
    )
    db.add(image)
    db.commit()

    return ReferenceCreateOut(
        person_id=person.id,
        name=person.name,
        image_id=image.id,
        image_path=relative_path,
        metadata=metadata_dict,
    )


@router.get("", response_model=list[PersonOut])
def list_references(db: Session = Depends(get_db)) -> list[PersonOut]:
    persons = db.execute(select(Person)).scalars().all()
    response: list[PersonOut] = []
    for person in persons:
        metadata = json.loads(person.metadata_json) if person.metadata_json else None
        images = [ReferenceImageOut(image_id=img.id, image_path=img.image_path) for img in person.images]
        response.append(
            PersonOut(
                person_id=person.id,
                name=person.name,
                metadata=metadata,
                images=images,
            )
        )
    return response


@router.get("/{person_id}", response_model=PersonOut)
def get_reference(person_id: int, db: Session = Depends(get_db)) -> PersonOut:
    person = db.get(Person, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="person not found")

    metadata = json.loads(person.metadata_json) if person.metadata_json else None
    images = [ReferenceImageOut(image_id=img.id, image_path=img.image_path) for img in person.images]
    return PersonOut(
        person_id=person.id,
        name=person.name,
        metadata=metadata,
        images=images,
    )


@router.delete("/{person_id}")
def delete_reference(person_id: int, db: Session = Depends(get_db)) -> dict:
    person = db.get(Person, person_id)
    if person is None:
        raise HTTPException(status_code=404, detail="person not found")

    data_dir = Path(settings.data_dir)
    for image in person.images:
        abs_path = build_abs_path(data_dir, image.image_path)
        if abs_path.exists():
            abs_path.unlink()

    db.delete(person)
    db.commit()
    return {"deleted": True}
