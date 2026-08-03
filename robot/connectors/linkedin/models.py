from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class LinkedInRecord:
    name: str | None = None
    title: str | None = None
    company: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
