#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Raw Training Material v7.35a"

post_json() {
  local endpoint="$1"
  local payload="${2:-{}}"
  local response body code
  response="$(curl -sS -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" -w '\n%{http_code}' --json "${payload}" "${API_BASE}${endpoint}")"
  code="${response##*$'\n'}"
  body="${response%$'\n'*}"
  if [[ ! "${code}" =~ ^2 ]]; then
    printf '%s\n' "${body}" >&2
    fail "POST ${endpoint} returned HTTP ${code}"
  fi
  printf '%s' "${body}"
}

assert_v735a_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
}

boundary="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-materials/raw-boundary/status")"
assert_v735a_safe "${boundary}" "raw boundary"

material="$(post_json "/personal-skill-studio/training-artifacts/training-materials/register" '{"material_kind":"lawyer_work_product","material_label":"regression metadata"}')"
assert_v735a_safe "${material}" "register material"

ocr="$(post_json "/personal-skill-studio/training-artifacts/training-materials/ocr-jobs/run" '{}')"
assert_v735a_safe "${ocr}" "ocr job"

parse="$(post_json "/personal-skill-studio/training-artifacts/training-materials/document-parse-jobs/run" '{}')"
assert_v735a_safe "${parse}" "parse job"

structures="$(post_json "/personal-skill-studio/training-artifacts/training-materials/structure-jobs/run" '{}')"
assert_v735a_safe "${structures}" "structure jobs"

legal="$(post_json "/personal-skill-studio/training-artifacts/training-materials/legal-retrieval-jobs/run" '{}')"
assert_v735a_safe "${legal}" "legal retrieval"

alignment="$(post_json "/personal-skill-studio/training-artifacts/training-materials/rule-alignment/run" '{}')"
assert_v735a_safe "${alignment}" "rule alignment"

gate="$(post_json "/personal-skill-studio/training-artifacts/training-materials/parse-quality-gate/run" '{}')"
assert_v735a_safe "${gate}" "parse gate"
printf '%s' "${gate}" | grep -Eq '"gate_status"[[:space:]]*:[[:space:]]*"passed"' || fail "parse gate did not pass"
printf '%s' "${gate}" | grep -Eq '"provider_call_executed"[[:space:]]*:[[:space:]]*false' || fail "provider call boundary missing"
printf '%s' "${gate}" | grep -Eq '"key_value_read"[[:space:]]*:[[:space:]]*false' || fail "credential boundary missing"

status="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-35a/status")"
assert_v735a_safe "${status}" "v735a status"

pass "personal raw training material v7.35a"
