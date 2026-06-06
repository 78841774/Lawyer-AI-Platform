#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Redacted Experience Output v7.35b"

bash "${SCRIPT_DIR}/check_personal_raw_training_material_v735a_apis.sh" >/dev/null

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

assert_v735b_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
}

candidates="$(post_json "/personal-skill-studio/training-artifacts/training-materials/experience-candidates/build" '{}')"
assert_v735b_safe "${candidates}" "experience candidates"
printf '%s' "${candidates}" | grep -Eq '"candidate_count"[[:space:]]*:[[:space:]]*[1-9]' || fail "missing candidates"

package="$(post_json "/personal-skill-studio/training-artifacts/training-materials/redacted-experience-packages/build" '{}')"
assert_v735b_safe "${package}" "redacted package"
package_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("redacted_experience_package_id",""))' <<<"${package}")"
[ -n "${package_id}" ] || fail "missing package id"
printf '%s' "${package}" | grep -Eq '"package_status"[[:space:]]*:[[:space:]]*"ready_for_training_dataset"' || fail "package not ready"
printf '%s' "${package}" | grep -Eq '"facts_output"[[:space:]]*:' || fail "missing facts output"
printf '%s' "${package}" | grep -Eq '"common_fact_extraction_framework"[[:space:]]*:' || fail "missing common fact framework"
printf '%s' "${package}" | grep -Eq '"case_cause_specific_fact_points"[[:space:]]*:' || fail "missing case-cause fact points"
printf '%s' "${package}" | grep -Eq '"legal_output"[[:space:]]*:' || fail "missing legal output"
printf '%s' "${package}" | grep -Eq '"legal_summary"[[:space:]]*:' || fail "missing legal summary"
printf '%s' "${package}" | grep -Eq '"case_cause_profiles"[[:space:]]*:' || fail "missing case cause profiles"
printf '%s' "${package}" | grep -Eq '"substantive_experience_profiles"[[:space:]]*:' || fail "missing substantive experience profiles"
printf '%s' "${package}" | grep -Eq '"procedural_experience_profiles"[[:space:]]*:' || fail "missing procedural experience profiles"
printf '%s' "${package}" | grep -Eq '"runtime_reference_type"[[:space:]]*:[[:space:]]*"substantive_reference"' || fail "missing substantive reference type"
printf '%s' "${package}" | grep -Eq '"runtime_reference_type"[[:space:]]*:[[:space:]]*"procedural_exact_match"' || fail "missing procedural exact match type"
printf '%s' "${package}" | grep -Eq '"cross_stage_reference_allowed"[[:space:]]*:[[:space:]]*false' || fail "procedural cross-stage boundary missing"
printf '%s' "${package}" | grep -Eq '"source_stage_reference"[[:space:]]*:' || fail "missing source stage reference"
printf '%s' "${package}" | grep -Eq '"procedural_profiles"[[:space:]]*:' || fail "missing procedural profiles"
printf '%s' "${package}" | grep -Eq '"substantive_impact_points"[[:space:]]*:' || fail "missing substantive impact points"
printf '%s' "${package}" | grep -Eq '"profile_loading_contract"[[:space:]]*:' || fail "missing profile loading contract"
printf '%s' "${package}" | grep -Eq '"facts_output_diff_check"[[:space:]]*:[[:space:]]*true' || fail "facts diff readiness missing"
printf '%s' "${package}" | grep -Eq '"multi_procedure_stage_dry_run"[[:space:]]*:[[:space:]]*true' || fail "procedure stage readiness missing"

for endpoint in \
  "/personal-skill-studio/training-artifacts/training-materials/redacted-experience-packages/${package_id}/redaction-report" \
  "/personal-skill-studio/training-artifacts/training-materials/redacted-experience-packages/${package_id}/audit" \
  "/personal-skill-studio/training-artifacts/training-materials/redacted-experience-packages/${package_id}/source-trace" \
  "/personal-skill-studio/training-artifacts/v7-35b/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v735b_safe "${body}" "${endpoint}"
done

pass "personal redacted experience output v7.35b"
