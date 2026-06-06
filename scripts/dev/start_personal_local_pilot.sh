#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/Lawyer-AI-Platform-App/backend"
FRONTEND_DIR="${ROOT_DIR}/Lawyer-AI-Platform-App/frontend"
BACKEND_PORT="${BACKEND_PORT:-8001}"
FRONTEND_PORT="${FRONTEND_PORT:-3001}"

check_port() {
  local port="$1"
  if lsof -iTCP:"${port}" -sTCP:LISTEN -Pn >/dev/null 2>&1; then
    printf 'Port %s is already in use. Stop the existing process or choose another port.\n' "${port}" >&2
    exit 1
  fi
}

check_port "${BACKEND_PORT}"
check_port "${FRONTEND_PORT}"

printf 'Starting AIHome.law Personal Local Pilot\n'
printf 'Backend:  http://127.0.0.1:%s\n' "${BACKEND_PORT}"
printf 'Frontend: http://127.0.0.1:%s\n' "${FRONTEND_PORT}"
printf 'Mode: mock-first, provider-gated, no live provider call by default\n'

(
  cd "${BACKEND_DIR}"
  if [ -d ".venv" ]; then
    # shellcheck disable=SC1091
    source .venv/bin/activate
  fi
  python -m uvicorn app.main:app --host 127.0.0.1 --port "${BACKEND_PORT}"
) &
BACKEND_PID="$!"

cleanup() {
  kill "${BACKEND_PID}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

printf 'Waiting for backend health check...\n'
for _ in $(seq 1 20); do
  if curl -fsS "http://127.0.0.1:${BACKEND_PORT}/health" >/dev/null 2>&1; then
    printf 'Backend health check passed.\n'
    break
  fi
  sleep 1
done

cd "${FRONTEND_DIR}"
NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:${BACKEND_PORT}" npm run dev -- -p "${FRONTEND_PORT}"
