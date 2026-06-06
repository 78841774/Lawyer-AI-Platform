#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
cd "${REPO_ROOT}"

fail() {
  printf 'FAIL %s\n' "$1" >&2
  exit 1
}

pass() {
  printf 'PASS %s\n' "$1"
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  fail "not inside a git worktree"
fi

patterns=(
  'sk-[A-Za-z0-9_-]{16,}'
  'Bearer[[:space:]]+[A-Za-z0-9._-]{16,}'
  '-----BEGIN[[:space:]]+(RSA[[:space:]]+|OPENSSH[[:space:]]+|EC[[:space:]]+)?PRIVATE[[:space:]]+KEY-----'
  '(api[_-]?key|private[_-]?key|access[_-]?token|refresh[_-]?token)[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{8,}["'\'']'
  '(raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|provider_response|provider_raw_response)[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{16,}["'\'']'
)

for pattern in "${patterns[@]}"; do
  matches="$(git grep -IlE -e "${pattern}" -- . ':!node_modules' ':!Lawyer-AI-Platform-App/backend/storage/runtime' ':!*.png' ':!*.jpg' || true)"
  if [ -n "${matches}" ]; then
    printf '%s\n' "${matches}" >&2
    fail "possible tracked secret or raw material payload found; file names only shown"
  fi
done

if git ls-files | grep -Eiq '(^|/)(\.env|local\.db|id_rsa|id_dsa|id_ecdsa|id_ed25519|.*private[_-]?key.*)$'; then
  git ls-files | grep -Ei '(^|/)(\.env|local\.db|id_rsa|id_dsa|id_ecdsa|id_ed25519|.*private[_-]?key.*)$' >&2
  fail "tracked filename suggests secret or local runtime material"
fi

pass "tracked files contain no high-confidence secret or raw material payload patterns"
