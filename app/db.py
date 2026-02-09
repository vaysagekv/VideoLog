from __future__ import annotations

from pathlib import Path
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings
from app.models import Base


def build_db_url() -> str:
    if settings.db_url:
        return settings.db_url
    data_dir = Path(settings.data_dir)
    data_dir.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{data_dir / 'app.db'}"


engine = create_engine(build_db_url(), connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_reference_embedding_column()


def _ensure_reference_embedding_column() -> None:
    if engine.dialect.name != "sqlite":
        return
    with engine.connect() as connection:
        rows = connection.execute(text("PRAGMA table_info(reference_images)")).fetchall()
        columns = {row[1] for row in rows}
        if "embedding_json" not in columns and rows:
            connection.execute(text("ALTER TABLE reference_images ADD COLUMN embedding_json TEXT"))


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
