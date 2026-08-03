from __future__ import annotations

from pathlib import Path

import pytest

from robot.connectors.pappers.connector import PappersConnector
from robot.connectors.pappers.exceptions import PappersError


class DummyBrowser:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def open(self, url: str) -> None:
        self.calls.append(("open", url))

    def reconnect(self, session: object) -> None:
        self.calls.append(("reconnect", str(session)))

    def search(self, query: str, engine: str) -> list[dict[str, object]]:
        self.calls.append(("search", f"{query}|{engine}"))
        return [{"company": "Acme Immo", "website": "https://acme.example"}]


def test_pappers_connector_executes_and_exports(tmp_path: Path) -> None:
    browser = DummyBrowser()
    connector = PappersConnector(browser_client=browser)

    result = connector.execute({"action": "search_company", "query": "Acme"}, session={"id": "s1"})

    assert result["status"] == "ok"
    assert result["records"][0]["company"] == "Acme Immo"
    assert browser.calls[0][0] == "open"

    output_path = tmp_path / "pappers.json"
    exported_path = connector.export_json(result["records"], output_path)
    assert exported_path.exists()
    assert "Acme Immo" in exported_path.read_text()


def test_pappers_connector_exports_csv(tmp_path: Path) -> None:
    browser = DummyBrowser()
    connector = PappersConnector(browser_client=browser)

    result = connector.execute({"action": "search_contact", "query": "Acme"}, session={"id": "s2"})

    output_path = tmp_path / "pappers.csv"
    exported_path = connector.export_csv(result["records"], output_path)
    assert exported_path.exists()
    assert "company" in exported_path.read_text()


def test_pappers_connector_requires_browser() -> None:
    connector = PappersConnector(browser_client=None)

    with pytest.raises(PappersError, match="browser client"):
        connector.execute({"action": "search_company", "query": "Acme"})


def test_pappers_connector_rejects_unknown_action() -> None:
    connector = PappersConnector(browser_client=DummyBrowser())

    with pytest.raises(PappersError, match="Unsupported action"):
        connector.execute({"action": "unknown", "query": "Acme"})
