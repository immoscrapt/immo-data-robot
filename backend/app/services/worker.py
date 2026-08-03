from __future__ import annotations

from typing import Any


class BackgroundWorker:
    def run_job(self, job_payload: dict[str, Any]) -> dict[str, Any]:
        return {"status": "queued", "payload": job_payload}
