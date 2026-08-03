from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


@dataclass(slots=True)
class CadastreRecord:
    commune: str | None = None
    address: str | None = None
    parcelle: str | None = None
    surface: float | None = None
    coordinates: dict[str, float] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
