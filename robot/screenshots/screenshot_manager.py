from __future__ import annotations

from pathlib import Path
from typing import Optional


class ScreenshotManager:
    """Stores screenshots and other artifacts locally for each run."""

    def __init__(self, output_dir: Optional[Path | str] = None) -> None:
        self.output_dir = Path(output_dir or Path("robot/screenshots"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def capture(self, name: str, data: bytes | None = None) -> Path:
        target = self.output_dir / f"{name}.png"
        if data is None:
            target.write_bytes(b"")
        else:
            target.write_bytes(data)
        return target
