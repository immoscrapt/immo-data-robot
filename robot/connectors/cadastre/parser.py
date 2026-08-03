from __future__ import annotations

from typing import Any

from robot.connectors.cadastre.models import CadastreRecord


class CadastreParser:
    """Transforms raw Cadastre payloads into structured records."""

    @staticmethod
    def parse(raw_results: list[dict[str, Any]]) -> list[CadastreRecord]:
        records: list[CadastreRecord] = []
        for item in raw_results:
            records.append(
                CadastreRecord(
                    commune=item.get("commune"),
                    address=item.get("address"),
                    parcelle=item.get("parcelle"),
                    surface=item.get("surface"),
                    coordinates=item.get("coordinates"),
                )
            )
        return records
