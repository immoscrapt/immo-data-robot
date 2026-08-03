from __future__ import annotations

from typing import Any

from robot.connectors.dvf.models import DVFRecord


class DVFParser:
    @staticmethod
    def parse(raw_results: list[dict[str, Any]]) -> list[DVFRecord]:
        return [
            DVFRecord(
                address=item.get("address"),
                city=item.get("city"),
                postal_code=item.get("postal_code"),
                price=item.get("price"),
                surface=item.get("surface"),
            )
            for item in raw_results
        ]
