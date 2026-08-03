from __future__ import annotations

from pathlib import Path

import pytest

from robot.connectors.linkedin.connector import LinkedInConnector
from robot.connectors.linkedin.exceptions import LinkedInError


class DummyBrowser:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def open(self, url: str) -> None:
        self.calls.append(("open", url))

    def reconnect(self, session: object) -> None:
        self.calls.append(("reconnect", str(session)))

    def search(self, query: str, engine: str) -> list[dict[str, object]]:
        self.calls.append(("search", f"{query}|{engine}"))
        return [{"name": "Alice Martin", "title": "Directrice", "company": "Acme Immo"}]


def test_linkedin_connector_executes_and_exports(tmp_path: Path) -> None:
    browser = DummyBrowser()
    connector = LinkedInConnector(browser_client=browser)

    result = connector.execute({"action": "search_profile", "query": "Alice Martin"}, session={"id": "s2"})

    assert result["status"] == "ok"
    assert result["records"][0]["name"] == "Alice Martin"
    assert browser.calls[0][0] == "open"

    output_path = tmp_path / "linkedin.json"
    exported_path = connector.export_json(result["records"], output_path)
    assert exported_path.exists()
    assert "Alice Martin" in exported_path.read_text()


def test_linkedin_connector_requires_browser() -> None:
    connector = LinkedInConnector(browser_client=None)

    with pytest.raises(LinkedInError, match="browser client"):
        connector.execute({"action": "search_profile", "query": "Alice"})
