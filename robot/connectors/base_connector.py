from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """Base class for all connectors in the modular automation engine."""

    name: str = ""

    @abstractmethod
    def execute(self, context: dict[str, Any], session: dict[str, Any] | None = None) -> dict[str, Any]:
        raise NotImplementedError
