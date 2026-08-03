from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


class PappersExporter:
    def export_json(self, records: list[dict[str, Any]], output_path: str | Path) -> Path:
        path = Path(output_path)
        payload = [dict(record) for record in records]
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
        return path

    def export_csv(self, records: list[dict[str, Any]], output_path: str | Path) -> Path:
        path = Path(output_path)
        if not records:
            path.write_text("")
            return path

        fieldnames = sorted({key for record in records for key in record.keys()})
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            for record in records:
                writer.writerow({key: record.get(key, "") for key in fieldnames})
        return path
