from __future__ import annotations

from typing import Any

from robot.connectors.lusha.models import LushaRecord


class LushaParser:
    @staticmethod
    def parse(raw_results: list[dict[str, Any]]) -> list[LushaRecord]:
        return [
            LushaRecord(
                name=item.get("name"),
                email=item.get("email"),
                phone=item.get("phone"),
            )
            for item in raw_results
        ]
