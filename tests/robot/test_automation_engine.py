from __future__ import annotations

import tempfile
from pathlib import Path

from robot.automation_engine import AutomationEngine
from robot.connectors.base_connector import BaseConnector
from robot.core.logger import Logger
from robot.core.retry_manager import RetryManager
from robot.screenshots.screenshot_manager import ScreenshotManager
from robot.sessions.session_manager import SessionManager


class DummyConnector(BaseConnector):
    name = "dummy"

    def execute(self, context: dict, session: dict | None = None) -> dict:
        context["executed"] = True
        if session is not None:
            session["connector"] = self.name
        return {"status": "ok"}


def test_session_manager_creates_and_retrieves_session() -> None:
    manager = SessionManager(storage_dir=Path(tempfile.mkdtemp()))
    session = manager.create_session("demo")

    assert session.session_id
    assert session.name == "demo"
    assert manager.get_session(session.session_id) is not None


def test_retry_manager_retries_until_success() -> None:
    attempts = {"count": 0}

    def flaky() -> str:
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RuntimeError("temporary failure")
        return "ok"

    manager = RetryManager(max_attempts=3, delay_seconds=0)
    assert manager.run(flaky) == "ok"
    assert attempts["count"] == 3


def test_screenshot_manager_writes_file() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        manager = ScreenshotManager(output_dir=Path(tmp_dir))
        file_path = manager.capture("demo", data=b"abc")

        assert file_path.exists()
        assert file_path.read_bytes() == b"abc"


def test_automation_engine_executes_registered_connector() -> None:
    engine = AutomationEngine(logger=Logger(name="test"))
    engine.register_connector(DummyConnector())

    context: dict = {}
    session = engine.run("dummy", context=context)

    assert session is not None
    assert context["executed"] is True
    assert session["connector"] == "dummy"
