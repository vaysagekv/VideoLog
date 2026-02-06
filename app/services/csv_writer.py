from __future__ import annotations

import csv
from pathlib import Path


def write_results_csv(path: Path, results: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["name", "confidence", "first_seen_sec"])
        writer.writeheader()
        for item in results:
            writer.writerow(item)
