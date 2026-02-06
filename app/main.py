from fastapi import FastAPI

from app.api.reference import router as reference_router
from app.api.video import router as video_router
from app.db import init_db

app = FastAPI(title="Persons In A Video")

app.include_router(reference_router)
app.include_router(video_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
