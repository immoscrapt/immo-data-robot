from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Optional
from uuid import uuid4


@dataclass
class AutomationSession:
    session_id: str
    name: str
    status: str = "created"
    created_at: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AutomationSession":
        return cls(**payload)


class SessionManager:
    """Persists automation sessions on disk for durable execution tracking."""

    def __init__(self, storage_dir: Optional[Path | str] = None) -> None:
        self.storage_dir = Path(storage_dir or Path("robot/sessions"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def create_session(self, name: str, metadata: Optional[dict[str, Any]] = None) -> AutomationSession:
        session = AutomationSession(session_id=str(uuid4()), name=name, metadata=metadata or {})
        self._persist(session)
        return session

    def get_session(self, session_id: str) -> Optional[AutomationSession]:
        path = self.storage_dir / f"{session_id}.json"
        if not path.exists():
            return None
        return AutomationSession.from_dict(json.loads(path.read_text()))

    def update_session(self, session_id: str, status: Optional[str] = None, metadata: Optional[dict[str, Any]] = None) -> AutomationSession:
        session = self.get_session(session_id)
        if session is None:
            raise KeyError(f"Session {session_id} not found")
        if status is not None:
            session.status = status
        if metadata is not None:
            session.metadata.update(metadata)
        self._persist(session)
        return session

    def _persist(self, session: AutomationSession) -> None:
        path = self.storage_dir / f"{session.session_id}.json"
        path.write_text(json.dumps(session.to_dict(), indent=2))
