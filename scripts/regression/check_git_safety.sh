#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Git Safety"
repo_root
git status --short
git diff --check

if git status --short | grep -E '(^|/)(\.env|local\.db|\.DS_Store)$|(^|/)(storage/runtime|node_modules|__pycache__)(/|$)' >/dev/null; then
  fail "git status includes sensitive path"
fi

pass "git safety checks"
