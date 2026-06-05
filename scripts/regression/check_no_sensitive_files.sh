#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "No Sensitive Files"
repo_root
tracked_sensitive="$(git ls-files | grep -E '(^|/)(\.env|local\.db|\.DS_Store)$|(^|/)(storage/runtime|node_modules|__pycache__)(/|$)' || true)"
if [ -n "${tracked_sensitive}" ]; then
  printf '%s\n' "${tracked_sensitive}" >&2
  fail "tracked sensitive files found"
fi

tracked_case_paths="$(git ls-files | grep -E '(^|/)(real_cases|sandbox_cases)(/|$)' || true)"
if [ -n "${tracked_case_paths}" ]; then
  printf '%s\n' "${tracked_case_paths}" >&2
  fail "tracked real/sandbox case path found"
fi

pass "no sensitive tracked files"
