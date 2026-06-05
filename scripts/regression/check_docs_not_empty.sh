#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Docs Not Empty"
repo_root
empty_files="$(find docs 09-Change-Logs -name "*.md" -size 0)"
if [ -n "${empty_files}" ]; then
  printf '%s\n' "${empty_files}" >&2
  fail "empty markdown files found"
fi

pass "docs and changelog markdown files are non-empty"
