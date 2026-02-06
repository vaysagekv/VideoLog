from __future__ import annotations

from typing import Iterable, Optional

import cv2
import numpy as np


class Matcher:
    def __init__(self) -> None:
        self.available = False
        self.app = None
        try:
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

    def build_gallery(self, items: Iterable[tuple[str, str]]) -> list[dict]:
        gallery: list[dict] = []
        for name, image_path in items:
            image = cv2.imread(str(image_path))
            if image is None:
                continue
            faces = self.detect_faces(image)
            if not faces:
                continue
            face = max(faces, key=lambda f: getattr(f, "det_score", 0.0))
            embedding = getattr(face, "embedding", None)
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
