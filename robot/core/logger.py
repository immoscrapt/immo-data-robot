from __future__ import annotations

import logging
from typing import Any


class Logger:
    """Small structured logger wrapper used by the automation engine."""

    def __init__(self, name: str = "immo-robot", level: int = logging.INFO) -> None:
        self._logger = logging.getLogger(name)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s"))
            self._logger.addHandler(handler)
        self._logger.setLevel(level)
        self._logger.propagate = False

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(message, *args, **kwargs)

    def debug(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.debug(message, *args, **kwargs)
