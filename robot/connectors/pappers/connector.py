from __future__ import annotations

from pathlib import Path
from typing import Any

from robot.connectors.base_connector import BaseConnector
from robot.connectors.pappers.exceptions import PappersError
from robot.connectors.pappers.exporter import PappersExporter
from robot.connectors.pappers.parser import PappersParser


class PappersConnector(BaseConnector):
    name = "pappers"

    def __init__(self, browser_client: Any | None = None) -> None:
        self.browser_client = browser_client
        self.parser = PappersParser()
        self.exporter = PappersExporter()

    def execute(self, context: dict[str, Any], session: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.browser_client:
            raise PappersError("A browser client is required")

        action = context.get("action")
        query = context.get("query")
        if not action or not query:
            raise PappersError("action and query are required")

        try:
            self.browser_client.open("https://www.pappers.fr")
            self.browser_client.reconnect(session)
            search_type = self._resolve_search_type(action)
            raw_results = self.browser_client.search(str(query), search_type)
            records = [record.to_dict() for record in self.parser.parse(raw_results)]
        except Exception as exc:  # pragma: no cover - defensive integration path
            raise PappersError(str(exc)) from exc

        return {"status": "ok", "records": records, "session": session or {}}

    def export_json(self, records: list[dict[str, Any]], output_path: str | Path) -> Path:
        return self.exporter.export_json(records, output_path)

    def export_csv(self, records: list[dict[str, Any]], output_path: str | Path) -> Path:
        return self.exporter.export_csv(records, output_path)

    def _resolve_search_type(self, action: str) -> str:
        mapping = {
            "search_company": "company",
            "search_contact": "contact",
        }
        if action not in mapping:
            raise PappersError(f"Unsupported action: {action}")
        return mapping[action]
