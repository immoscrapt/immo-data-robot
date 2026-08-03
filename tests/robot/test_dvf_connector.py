from __future__ import annotations

from pathlib import Path

import pytest

from robot.connectors.dvf.connector import DVFConnector
from robot.connectors.dvf.exceptions import DVFError


class DummyBrowser:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def open(self, url: str) -> None:
        self.calls.append(("open", url))

    def reconnect(self, session: object) -> None:
        self.calls.append(("reconnect", str(session)))

    def search(self, query: str, engine: str) -> list[dict[str, object]]:
        self.calls.append(("search", f"{query}|{engine}"))
        return [
            {
                "address": "12 Rue de Paris",
                "city": "Paris",
                "postal_code": "75010",
                "price": 420000.0,
                "surface": 80.0,
            }
        ]


def test_dvf_connector_executes_and_exports(tmp_path: Path) -> None:
    browser = DummyBrowser()
    connector = DVFConnector(browser_client=browser)

    result = connector.execute(
        {"action": "search", "query": "Paris 75010"},
        session={"id": "session-1"},
    )

    assert result["status"] == "ok"
    assert result["records"][0]["address"] == "12 Rue de Paris"
    assert browser.calls[0][0] == "open"

    output_path = tmp_path / "records.json"
    exported_path = connector.export_json(result["records"], output_path)
    assert exported_path.exists()
    assert "12 Rue de Paris" in exported_path.read_text()


def test_dvf_connector_requires_browser() -> None:
    connector = DVFConnector(browser_client=None)

    with pytest.raises(DVFError, match="browser client"):
        connector.execute({"action": "search", "query": "Paris"})
