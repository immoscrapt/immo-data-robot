from __future__ import annotations

from typing import Any

from robot.connectors.linkedin.models import LinkedInRecord


class LinkedInParser:
    @staticmethod
    def parse(raw_results: list[dict[str, Any]]) -> list[LinkedInRecord]:
        return [
            LinkedInRecord(
                name=item.get("name"),
                title=item.get("title"),
                company=item.get("company"),
            )
            for item in raw_results
        ]
