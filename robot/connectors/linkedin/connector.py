from __future__ import annotations

from pathlib import Path
from typing import Any

from robot.connectors.base_connector import BaseConnector
from robot.connectors.linkedin.exceptions import LinkedInError
from robot.connectors.linkedin.parser import LinkedInParser


class LinkedInConnector(BaseConnector):
    name = "linkedin"

    def __init__(self, browser_client: Any | None = None) -> None:
        self.browser_client = browser_client
        self.parser = LinkedInParser()

    def execute(self, context: dict[str, Any], session: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.browser_client:
            raise LinkedInError("A browser client is required")

        action = context.get("action")
        query = context.get("query")
        if not action or not query:
            raise LinkedInError("action and query are required")

        try:
            self.browser_client.open("https://www.linkedin.com")
            self.browser_client.reconnect(session)
            raw_results = self.browser_client.search(str(query), "linkedin")
            records = [record.to_dict() for record in self.parser.parse(raw_results)]
        except Exception as exc:  # pragma: no cover - defensive integration path
            raise LinkedInError(str(exc)) from exc

        return {"status": "ok", "records": records, "session": session or {}}

    def export_json(self, records: list[dict[str, Any]], output_path: str | Path) -> Path:
        path = Path(output_path)
        path.write_text(str(records))
        return path
