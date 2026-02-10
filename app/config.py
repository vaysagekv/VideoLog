import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Persons In A Video"
    data_dir: str = os.getenv("PIV_DATA_DIR", "data")
    model_dir: str = os.getenv("PIV_MODEL_DIR", "")
    db_url: str | None = os.getenv("PIV_DB_URL")
    yolo_model_path: str = os.getenv("PIV_YOLO_MODEL_PATH", "")
    yolo_confidence: float = float(os.getenv("PIV_YOLO_CONFIDENCE", "0.35"))
    yolo_iou: float = float(os.getenv("PIV_YOLO_IOU", "0.5"))

    def resolved_model_dir(self) -> str:
        if self.model_dir:
            return self.model_dir
        return os.path.join(self.data_dir, "models", "insightface")

    def resolved_yolo_model_path(self) -> str:
        if self.yolo_model_path:
            return self.yolo_model_path
        return os.path.join(self.data_dir, "models", "yolo", "yolov8n.pt")


settings = Settings()
