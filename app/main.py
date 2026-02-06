from fastapi import FastAPI

app = FastAPI(title="Persons In A Video")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
