from __future__ import annotations

from typing import Any, Optional

from robot.browser.browser_manager import BrowserManager
from robot.connectors.base_connector import BaseConnector
from robot.core.logger import Logger
from robot.core.retry_manager import RetryManager
from robot.screenshots.screenshot_manager import ScreenshotManager
from robot.sessions.session_manager import SessionManager


class AutomationEngine:
    """Orchestrates modular connectors for the IMMO DATA ROBOT automation workflow."""

    def __init__(
        self,
        logger: Optional[Logger] = None,
        browser_manager: Optional[BrowserManager] = None,
        session_manager: Optional[SessionManager] = None,
        retry_manager: Optional[RetryManager] = None,
        screenshot_manager: Optional[ScreenshotManager] = None,
    ) -> None:
        self.logger = logger or Logger(name="immo-robot")
        self.browser_manager = browser_manager or BrowserManager()
        self.session_manager = session_manager or SessionManager()
        self.retry_manager = retry_manager or RetryManager()
        self.screenshot_manager = screenshot_manager or ScreenshotManager()
        self.connectors: dict[str, BaseConnector] = {}

    def register_connector(self, connector: BaseConnector) -> None:
        if not isinstance(connector, BaseConnector):
            raise TypeError("connector must inherit from BaseConnector")
        self.connectors[connector.name] = connector
        self.logger.info("Registered connector %s", connector.name)

    def run(
        self,
        connector_name: str,
        context: Optional[dict[str, Any]] = None,
        session_id: Optional[str] = None,
        url: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        if context is None:
            context = {}
        session = None

        if session_id:
            session = self.session_manager.get_session(session_id)
            if session is None:
                raise KeyError(f"Session {session_id} not found")
        else:
            session = self.session_manager.create_session(name=connector_name)

        context.setdefault("session_id", session.session_id)
        context.setdefault("connector_name", connector_name)

        if url:
            self.logger.info("Opening URL %s", url)
            self.browser_manager.open_page(url)

        connector = self.connectors.get(connector_name)
        if connector is None:
            raise KeyError(f"Connector {connector_name} is not registered")

        result = self.retry_manager.run(connector.execute, context, session.to_dict())
        if context.get("take_screenshot"):
            self.screenshot_manager.capture(f"{connector_name}-run", data=b"automation run")

        self.session_manager.update_session(
            session.session_id,
            status="completed",
            metadata={"last_result": result, "connector": connector_name},
        )
        session_payload = session.to_dict()
        session_payload.setdefault("connector", connector_name)
        return session_payload
