from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


def save_upload(upload: UploadFile, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    suffix = Path(upload.filename or "").suffix
    filename = f"{uuid4().hex}{suffix}"
    target_path = target_dir / filename
    with target_path.open("wb") as handle:
        upload.file.seek(0)
        shutil.copyfileobj(upload.file, handle)
    return target_path


def to_relative_path(base_dir: Path, path: Path) -> str:
    return str(path.relative_to(base_dir))


def build_abs_path(base_dir: Path, relative_path: str) -> Path:
    return base_dir / relative_path
