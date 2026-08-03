#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  cp .env.example .env
fi

if command -v uv >/dev/null 2>&1; then
  uv venv --python 3.12 .venv
  VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
elif command -v python3.12 >/dev/null 2>&1; then
  python3.12 -m venv .venv
  VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  python3 -m venv .venv
  VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
else
  echo "Python 3.12 or Python 3 is required." >&2
  exit 1
fi

"$VENV_PYTHON" -m pip install --upgrade pip setuptools wheel
"$VENV_PYTHON" -m pip install -r backend/requirements.txt -r robot/requirements.txt
"$VENV_PYTHON" -m playwright install chromium || true

if command -v docker >/dev/null 2>&1; then
  docker compose up -d db redis
else
  echo "Docker not found; skipping Docker startup." >&2
fi

cd backend
"$VENV_PYTHON" -m uvicorn app.main:app --host 0.0.0.0 --port 8000
