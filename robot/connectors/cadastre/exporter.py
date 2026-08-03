from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


class CadastreExporter:
    """Exports Cadastre records as JSON or CSV files."""

    @staticmethod
    def export_json(records: list[dict[str, Any]], output_path: str | Path) -> Path:
        path = Path(output_path)
        path.write_text(json.dumps(records, indent=2, ensure_ascii=False))
        return path

    @staticmethod
    def export_csv(records: list[dict[str, Any]], output_path: str | Path) -> Path:
        path = Path(output_path)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["commune", "address", "parcelle", "surface", "coordinates"])
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        return path
