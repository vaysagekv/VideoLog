from __future__ import annotations

import os
from pathlib import Path
from typing import Iterable, Optional

import cv2
import numpy as np

from app.config import settings


class Matcher:
    def __init__(self) -> None:
        self.available = False
        self.app = None
        try:
            model_dir = Path(settings.resolved_model_dir())
            model_dir.mkdir(parents=True, exist_ok=True)
            os.environ.setdefault("INSIGHTFACE_HOME", str(model_dir))
            from insightface.app import FaceAnalysis

            self.app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
            self.app.prepare(ctx_id=0, det_size=(640, 640))
            self.available = True
        except Exception:
            self.app = None

    def detect_faces(self, frame: np.ndarray) -> list:
        if not self.available or self.app is None:
            return []
        return self.app.get(frame)

    def extract_embedding_from_image_path(self, image_path: str) -> Optional[np.ndarray]:
        image = cv2.imread(str(image_path))
        if image is None:
            return None
        faces = self.detect_faces(image)
        if not faces:
            return None
        face = max(faces, key=lambda f: getattr(f, "det_score", 0.0))
        return getattr(face, "embedding", None)

    def build_gallery(self, items: Iterable[tuple[str, str]]) -> list[dict]:
        gallery: list[dict] = []
        for name, image_path in items:
            embedding = self.extract_embedding_from_image_path(image_path)
            if embedding is None:
                continue
            gallery.append({"name": name, "embedding": embedding})
        return gallery

    def match(self, embedding: np.ndarray, gallery: list[dict]) -> tuple[Optional[dict], float]:
        best: Optional[dict] = None
        best_score = -1.0
        for item in gallery:
            score = cosine_similarity(embedding, item["embedding"])
            if score > best_score:
                best = item
                best_score = score
        return best, best_score


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b)) + 1e-8
    return float(np.dot(a, b) / denom)


def warm_up_models() -> bool:
    matcher = Matcher()
    return matcher.available
