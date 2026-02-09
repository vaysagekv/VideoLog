import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.reference import router as reference_router
from app.api.video import router as video_router
from app.db import init_db
from app.services.matcher import warm_up_models

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    if not warm_up_models():
        logger.warning("InsightFace warm-up failed; model may be unavailable")
    yield


app = FastAPI(title="Persons In A Video", lifespan=lifespan)

app.include_router(reference_router)
app.include_router(video_router)

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
