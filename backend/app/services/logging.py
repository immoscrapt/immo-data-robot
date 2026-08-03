from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("immo_data_robot")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)


def log_event(message: str, **context: Any) -> None:
    logger.info("%s | %s", message, context)
