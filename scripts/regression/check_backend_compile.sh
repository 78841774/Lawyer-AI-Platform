#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Backend Compile"
cd "${REPO_ROOT}/Lawyer-AI-Platform-App/backend"

if [ -f ".venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source ".venv/bin/activate"
else
  printf 'WARNING backend .venv not found; trying python from PATH.\n'
fi

PYTHON_BIN="${PYTHON:-python}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
  else
    fail "python is not available"
  fi
fi

"${PYTHON_BIN}" -m compileall \
  app \
  personal_alpha_workspace \
  personal_alpha_dashboard \
  personal_alpha_source_review \
  personal_alpha_final_readiness \
  personal_alpha_final_gate \
  personal_alpha_final_packet \
  personal_alpha_lawyer_final_review \
  personal_alpha_final_lock \
  personal_alpha_case_os

pass "backend compileall"
