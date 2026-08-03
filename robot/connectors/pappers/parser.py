from __future__ import annotations

from typing import Any

from robot.connectors.pappers.models import PappersRecord


class PappersParser:
    @staticmethod
    def parse(raw_results: list[dict[str, Any]]) -> list[PappersRecord]:
        return [
            PappersRecord(
                company=item.get("company"),
                website=item.get("website"),
            )
            for item in raw_results
        ]
