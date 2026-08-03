from __future__ import annotations

import time
from typing import Any, Callable, Optional

from robot.core.logger import Logger


class RetryManager:
    """Retries flaky operations without coupling the engine to business logic."""

    def __init__(self, max_attempts: int = 3, delay_seconds: float = 1.0, logger: Optional[Logger] = None) -> None:
        self.max_attempts = max_attempts
        self.delay_seconds = delay_seconds
        self.logger = logger

    def run(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        last_error: Optional[Exception] = None
        for attempt in range(1, self.max_attempts + 1):
            try:
                return func(*args, **kwargs)
            except Exception as exc:  # pragma: no cover - exercised in tests
                last_error = exc
                if self.logger:
                    self.logger.warning("Attempt %s/%s failed: %s", attempt, self.max_attempts, exc)
                if attempt == self.max_attempts:
                    raise
                if self.delay_seconds:
                    time.sleep(self.delay_seconds)
        raise RuntimeError("RetryManager exhausted") from last_error
