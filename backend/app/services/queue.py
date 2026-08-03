from __future__ import annotations

import json
from typing import Any

from redis import Redis


class RedisQueue:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        self.client = Redis(host=host, port=port, db=db, decode_responses=True)

    def enqueue(self, name: str, payload: dict[str, Any]) -> None:
        self.client.rpush(name, json.dumps(payload))

    def dequeue(self, name: str) -> dict[str, Any] | None:
        item = self.client.lpop(name)
        return json.loads(item) if item else None
