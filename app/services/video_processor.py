from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.services.matcher import Matcher


def process_video(
    video_path: Path,
    reference_items: list[dict],
    min_confidence: float = 0.6,
    frame_interval_sec: float = 1.0,
) -> list[dict]:
    matcher = Matcher()
    if not matcher.available:
        raise RuntimeError("face model is not available")

    gallery = build_reference_gallery(matcher, reference_items)
    if not gallery:
        return []

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError("unable to open video")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    frame_interval = max(1, int(round(frame_interval_sec * fps)))

    results: dict[str, dict] = {}
    frame_index = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_index % frame_interval == 0:
            faces = matcher.detect_faces(frame)
            for face in faces:
                embedding = getattr(face, "embedding", None)
                if embedding is None:
                    continue
                best, score = matcher.match(embedding, gallery)
                if best is None:
                    continue
                confidence = (score + 1.0) / 2.0
                if confidence < min_confidence:
                    continue
                name = best["name"]
                if name not in results:
                    results[name] = {
                        "name": name,
                        "confidence": confidence,
                        "first_seen_sec": frame_index / fps,
                    }
        frame_index += 1

    cap.release()

    output = []
    for item in results.values():
        output.append(
            {
                "name": item["name"],
                "confidence": round(item["confidence"] * 100.0, 2),
                "first_seen_sec": round(item["first_seen_sec"], 2),
            }
        )

    output.sort(key=lambda x: x["first_seen_sec"])
    return output


def build_reference_gallery(matcher: Matcher, reference_items: list[dict]) -> list[dict]:
    gallery: list[dict] = []
    for item in reference_items:
        name = item.get("name")
        if not name:
            continue
        embedding = item.get("embedding")
        if embedding is None:
            image_path = item.get("image_path")
            if image_path is None:
                continue
            embedding = matcher.extract_embedding_from_image_path(str(image_path))
        if embedding is None:
            continue
        if not isinstance(embedding, np.ndarray):
            embedding = np.array(embedding, dtype=np.float32)
        gallery.append({"name": name, "embedding": embedding})
    return gallery
