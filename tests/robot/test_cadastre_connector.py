from __future__ import annotations

from pathlib import Path

from robot.connectors.cadastre.connector import CadastreConnector
from robot.connectors.cadastre.models import CadastreRecord
from robot.connectors.cadastre.exceptions import CadastreError


class DummyBrowserClient:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict]] = []

    def open(self, url: str) -> None:
        self.calls.append(("open", {"url": url}))

    def search(self, query: str, search_type: str) -> list[dict]:
        self.calls.append(("search", {"query": query, "search_type": search_type}))
        return [
            {
                "commune": "Lyon",
                "address": "1 rue de la République",
                "parcelle": "1234AB0001",
                "surface": 120.5,
                "coordinates": {"latitude": 45.7597, "longitude": 4.8422},
            }
        ]

    def reconnect(self, session: dict | None = None) -> None:
        self.calls.append(("reconnect", {"session": bool(session)}))


def test_cadastre_connector_search_commune_and_export_json(tmp_path: Path) -> None:
    browser = DummyBrowserClient()
    connector = CadastreConnector(browser_client=browser)

    result = connector.execute({"action": "search_commune", "query": "Lyon"}, session={})

    assert result["status"] == "ok"
    assert len(result["records"]) == 1
    assert result["records"][0]["commune"] == "Lyon"

    output_path = tmp_path / "cadastre.json"
    exported_path = connector.export_json(result["records"], output_path)

    assert exported_path == output_path
    assert output_path.exists()
    assert '"commune": "Lyon"' in output_path.read_text()


def test_cadastre_connector_search_parcel_and_export_csv(tmp_path: Path) -> None:
    browser = DummyBrowserClient()
    connector = CadastreConnector(browser_client=browser)

    result = connector.execute({"action": "search_parcel", "query": "1234AB0001"}, session={})

    assert result["status"] == "ok"
    assert result["records"][0]["parcelle"] == "1234AB0001"

    output_path = tmp_path / "cadastre.csv"
    exported_path = connector.export_csv(result["records"], output_path)

    assert exported_path == output_path
    assert output_path.exists()
    assert "parcelle" in output_path.read_text()


def test_cadastre_connector_raises_for_unknown_action() -> None:
    connector = CadastreConnector(browser_client=DummyBrowserClient())

    try:
        connector.execute({"action": "unknown", "query": "Lyon"}, session={})
    except CadastreError as exc:
        assert "unknown" in str(exc)
    else:
        raise AssertionError("CadastreError was expected")
