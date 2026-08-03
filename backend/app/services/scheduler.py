from __future__ import annotations

try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
except ImportError:  # pragma: no cover - fallback for minimal environments
    AsyncIOScheduler = None


class _FallbackScheduler:
    def __init__(self) -> None:
        self.running = False

    def start(self) -> None:
        self.running = True

    def shutdown(self, wait: bool = False) -> None:
        self.running = False


scheduler = AsyncIOScheduler() if AsyncIOScheduler is not None else _FallbackScheduler()


def start_scheduler() -> None:
    if hasattr(scheduler, "start") and not getattr(scheduler, "running", False):
        scheduler.start()


def stop_scheduler() -> None:
    if hasattr(scheduler, "shutdown") and getattr(scheduler, "running", False):
        scheduler.shutdown(wait=False)
