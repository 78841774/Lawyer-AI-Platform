#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
FRONTEND_DIR="${APP_DIR}/frontend"

cd "${FRONTEND_DIR}"

echo "Installing frontend dependencies..."
npm install

echo "Starting frontend on http://localhost:3001"
npm run dev -- -p 3001
