from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class LushaRecord:
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
