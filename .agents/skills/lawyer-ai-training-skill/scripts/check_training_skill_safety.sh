#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

fail() {
  printf 'FAIL %s\n' "$1" >&2
  exit 1
}

pass() {
  printf 'PASS %s\n' "$1"
}

secret_value_patterns=(
  'sk-[A-Za-z0-9_-]{16,}'
  'Bearer[[:space:]]+[A-Za-z0-9._-]{16,}'
  '-----BEGIN[[:space:]]+(RSA[[:space:]]+|OPENSSH[[:space:]]+|EC[[:space:]]+)?PRIVATE[[:space:]]+KEY-----'
  '(api[_-]?key|private[_-]?key|access[_-]?token|refresh[_-]?token)[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']{8,}["'\'']'
)

for pattern in "${secret_value_patterns[@]}"; do
  if grep -RIEq --exclude-dir=.git --exclude='*.png' --exclude='*.jpg' -e "${pattern}" "${SKILL_DIR}"; then
    fail "possible secret value pattern found in Codex training Skill directory"
  fi
done

forbidden_assignment_pattern='(raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|absolute_path|provider_response|provider_raw_response|unredacted)[[:space:]]*[:=][[:space:]]*["'\''][^"'\'']+["'\'']'
if grep -RIEq --exclude-dir=.git -e "${forbidden_assignment_pattern}" "${SKILL_DIR}"; then
  fail "possible raw material or provider payload assignment found in Codex training Skill directory"
fi

pass "lawyer-ai-training-skill contains no secret values or raw payload assignments"
