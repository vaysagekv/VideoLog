from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np

from app.config import settings


@dataclass
class YoloConfig:
    confidence: float
    iou: float


class YoloDetector:
    def __init__(
        self,
        model_path: Optional[str] = None,
        config: Optional[YoloConfig] = None,
    ) -> None:
        self.available = False
        self.model = None
        self.config = config or YoloConfig(
            confidence=settings.yolo_confidence,
            iou=settings.yolo_iou,
        )
        try:
            from ultralytics import YOLO

            resolved_path = Path(model_path or settings.resolved_yolo_model_path())
            resolved_path.parent.mkdir(parents=True, exist_ok=True)
            self.model = YOLO(str(resolved_path))
            self.available = True
        except Exception:
            self.model = None

    def detect_person_boxes(self, frame: np.ndarray) -> list[tuple[int, int, int, int]]:
        if not self.available or self.model is None:
            return []

        results = self.model.predict(
            frame,
            verbose=False,
            conf=self.config.confidence,
            iou=self.config.iou,
            classes=[0],
        )
        if not results:
            return []
        boxes = results[0].boxes
        if boxes is None:
            return []

        xyxy = boxes.xyxy.cpu().numpy()
        output: list[tuple[int, int, int, int]] = []
        for x1, y1, x2, y2 in xyxy:
            output.append((int(x1), int(y1), int(x2), int(y2)))
        return output


def warm_up_yolo() -> bool:
    detector = YoloDetector()
    return detector.available
