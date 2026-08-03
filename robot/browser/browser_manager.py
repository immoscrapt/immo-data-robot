from __future__ import annotations

from pathlib import Path
from typing import Any, Optional


class BrowserManager:
    """Thin wrapper around Playwright to keep browser lifecycle isolated."""

    def __init__(self, headless: bool = True, slow_mo: int = 0, viewport: Optional[dict[str, int]] = None) -> None:
        self.headless = headless
        self.slow_mo = slow_mo
        self.viewport = viewport or {"width": 1400, "height": 900}
        self._playwright: Any = None
        self._browser: Any = None
        self._page: Any = None

    def start(self) -> Any:
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:  # pragma: no cover - import guard
            raise RuntimeError("Playwright is not installed. Install robot/requirements.txt first.") from exc

        if self._page is None:
            self._playwright = sync_playwright().start()
            self._browser = self._playwright.chromium.launch(headless=self.headless, slow_mo=self.slow_mo)
            self._page = self._browser.new_page(viewport=self.viewport)
        return self._page

    def open_page(self, url: str) -> Any:
        page = self.start()
        page.goto(url)
        return page

    def screenshot(self, output_path: str | Path) -> Path:
        page = self.start()
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(target), full_page=True)
        return target

    def stop(self) -> None:
        if self._browser is not None:
            self._browser.close()
        if self._playwright is not None:
            self._playwright.stop()
        self._browser = None
        self._page = None
        self._playwright = None
