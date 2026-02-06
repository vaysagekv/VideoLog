import logging

from fastapi import FastAPI

from app.api.reference import router as reference_router
from app.api.video import router as video_router
from app.db import init_db
from app.services.matcher import warm_up_models

logger = logging.getLogger(__name__)

app = FastAPI(title="Persons In A Video")

app.include_router(reference_router)
app.include_router(video_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    if not warm_up_models():
        logger.warning("InsightFace warm-up failed; model may be unavailable")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
