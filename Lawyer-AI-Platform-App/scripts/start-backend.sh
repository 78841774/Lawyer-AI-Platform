#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKEND_DIR="${APP_DIR}/backend"

cd "${BACKEND_DIR}"

if [ ! -d ".venv" ]; then
  echo "Creating backend virtual environment..."
  python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing backend dependencies..."
python -m pip install -r requirements.txt

echo "Starting backend on http://127.0.0.1:8001"
python -m uvicorn app.main:app --reload --port 8001
