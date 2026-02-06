from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Persons In A Video"
    data_dir: str = "data"
    db_url: str | None = None


settings = Settings()
