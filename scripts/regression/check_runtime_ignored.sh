#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Runtime Ignored"
repo_root
paths=(
  "Lawyer-AI-Platform-App/backend/storage/runtime"
  "Lawyer-AI-Platform-App/backend/storage/runtime/personal_alpha_case_os"
  "Lawyer-AI-Platform-App/backend/storage/runtime/personal_alpha_case_os/export_packages"
)

for path in "${paths[@]}"; do
  if ! git check-ignore -q "${path}"; then
    fail "runtime storage ignore check failed: ${path}"
  fi
  pass "ignored ${path}"
done

pass "runtime ignored checks"
