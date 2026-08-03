from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class DVFRecord:
    address: str | None = None
    city: str | None = None
    postal_code: str | None = None
    price: float | None = None
    surface: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
