from __future__ import annotations

from pathlib import Path

import pytest

from robot.connectors.lusha.connector import LushaConnector
from robot.connectors.lusha.exceptions import LushaError


class DummyBrowser:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def open(self, url: str) -> None:
        self.calls.append(("open", url))

    def reconnect(self, session: object) -> None:
        self.calls.append(("reconnect", str(session)))

    def search(self, query: str, engine: str) -> list[dict[str, object]]:
        self.calls.append(("search", f"{query}|{engine}"))
        return [{"name": "Bob Dupont", "email": "bob@example.com", "phone": "0601020304"}]


def test_lusha_connector_executes_and_exports(tmp_path: Path) -> None:
    browser = DummyBrowser()
    connector = LushaConnector(browser_client=browser)

    result = connector.execute({"action": "search_contact", "query": "Bob Dupont"}, session={"id": "s3"})

    assert result["status"] == "ok"
    assert result["records"][0]["email"] == "bob@example.com"
    assert browser.calls[0][0] == "open"

    output_path = tmp_path / "lusha.json"
    exported_path = connector.export_json(result["records"], output_path)
    assert exported_path.exists()
    assert "bob@example.com" in exported_path.read_text()


def test_lusha_connector_requires_browser() -> None:
    connector = LushaConnector(browser_client=None)

    with pytest.raises(LushaError, match="browser client"):
        connector.execute({"action": "search_contact", "query": "Bob"})
