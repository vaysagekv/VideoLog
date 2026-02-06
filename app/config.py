from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Persons In A Video"


settings = Settings()
