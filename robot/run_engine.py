from __future__ import annotations

from robot.automation_engine import AutomationEngine
from robot.core.logger import Logger


def main() -> None:
    engine = AutomationEngine(logger=Logger(name="immo-robot"))
    print("Automation engine ready. Register connectors to start a run.")
    print(engine)


if __name__ == "__main__":
    main()
