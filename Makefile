.PHONY: install backend robot frontend test lint format

install:
	@if command -v uv >/dev/null 2>&1; then uv venv --python 3.12 .venv; else python3 -m venv .venv; fi
	./.venv/bin/python -m pip install --upgrade pip setuptools wheel
	./.venv/bin/python -m pip install -r backend/requirements.txt -r robot/requirements.txt
	./.venv/bin/python -m playwright install chromium || true

backend:
	cd backend && ../.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

robot:
	cd robot && ../.venv/bin/python main.py

frontend:
	cd frontend && npm install && npm run dev

test:
	./.venv/bin/python -m pytest -q tests/robot/test_automation_engine.py backend/app/tests/test_main.py

lint:
	./.venv/bin/python -m compileall backend robot

format:
	./.venv/bin/python -m black backend robot tests || true
