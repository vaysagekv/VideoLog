import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Persons In A Video"
    data_dir: str = os.getenv("PIV_DATA_DIR", "data")
    model_dir: str = os.getenv("PIV_MODEL_DIR", "")
    db_url: str | None = os.getenv("PIV_DB_URL")

    def resolved_model_dir(self) -> str:
        if self.model_dir:
            return self.model_dir
        return os.path.join(self.data_dir, "models", "insightface")


settings = Settings()
