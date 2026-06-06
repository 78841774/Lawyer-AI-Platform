#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Codex Training Skill v7.37"

bash "${SCRIPT_DIR}/check_personal_training_dataset_v736_apis.sh" >/dev/null

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

assert_skill_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
}

doc="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/codex-training-skills/interface-doc")"
assert_skill_safe "${doc}" "training skill interface doc"
printf '%s' "${doc}" | grep -Eq '"baseline_skill_ids"[[:space:]]*:' || fail "missing baseline skill refs"
printf '%s' "${doc}" | grep -Eq '"credential_alias"[[:space:]]*:' || fail "missing credential alias contract"

adapters="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/codex-training-skills/provider-adapters")"
assert_skill_safe "${adapters}" "provider adapters"
printf '%s' "${adapters}" | grep -Eq '"provider_type"[[:space:]]*:[[:space:]]*"OCR_API"' || fail "missing OCR adapter spec"

skill="$(post_json "/personal-skill-studio/training-artifacts/codex-training-skills/generate" '{"skill_target":"case_analysis_skill"}')"
assert_skill_safe "${skill}" "generate training skill"
skill_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("training_skill_id",""))' <<<"${skill}")"
[ -n "${skill_id}" ] || fail "missing training skill id"
printf '%s' "${skill}" | grep -Eq '"target_skill_ids"[[:space:]]*:' || fail "missing target skills"
printf '%s' "${skill}" | grep -Eq '"provider_specs"[[:space:]]*:' || fail "missing provider specs"
printf '%s' "${skill}" | grep -Eq '"value_stored_in_skill"[[:space:]]*:[[:space:]]*false' || fail "credential value storage boundary missing"
printf '%s' "${skill}" | grep -Eq '"common_fact_extraction_framework"[[:space:]]*:' || fail "missing common fact extraction framework"
printf '%s' "${skill}" | grep -Eq '"case_cause_specific_fact_points"[[:space:]]*:' || fail "missing differentiated fact points"
printf '%s' "${skill}" | grep -Eq '"case_cause_profiles"[[:space:]]*:' || fail "missing case cause profiles"
printf '%s' "${skill}" | grep -Eq '"substantive_experience_profiles"[[:space:]]*:' || fail "missing substantive experience profiles"
printf '%s' "${skill}" | grep -Eq '"procedural_experience_profiles"[[:space:]]*:' || fail "missing procedural experience profiles"
printf '%s' "${skill}" | grep -Eq '"runtime_reference_type"[[:space:]]*:[[:space:]]*"substantive_reference"' || fail "missing substantive runtime reference type"
printf '%s' "${skill}" | grep -Eq '"runtime_reference_type"[[:space:]]*:[[:space:]]*"procedural_exact_match"' || fail "missing procedural runtime reference type"
printf '%s' "${skill}" | grep -Eq '"cross_stage_reference_allowed"[[:space:]]*:[[:space:]]*false' || fail "procedural cross-stage boundary missing"
printf '%s' "${skill}" | grep -Eq '"source_stage_reference"[[:space:]]*:' || fail "missing source stage reference"
printf '%s' "${skill}" | grep -Eq '"procedural_profiles"[[:space:]]*:' || fail "missing procedural profiles"
printf '%s' "${skill}" | grep -Eq '"required_material_patterns"[[:space:]]*:' || fail "missing procedural material patterns"
printf '%s' "${skill}" | grep -Eq '"evidence_review_points"[[:space:]]*:' || fail "missing evidence review points"
printf '%s' "${skill}" | grep -Eq '"substantive_impact_points"[[:space:]]*:' || fail "missing substantive impact points"
printf '%s' "${skill}" | grep -Eq '"profile_loading_contract"[[:space:]]*:' || fail "missing profile loading contract"
printf '%s' "${skill}" | grep -Eq '"legal_summary"[[:space:]]*:' || fail "missing legal summary"
printf '%s' "${skill}" | grep -Eq '"diff_summary"[[:space:]]*:' || fail "missing fact output diff summary"

gate="$(post_json "/personal-skill-studio/training-artifacts/codex-training-skills/${skill_id}/gate/run" '{}')"
assert_skill_safe "${gate}" "training skill gate"
printf '%s' "${gate}" | grep -Eq '"not_publishable_by_default"[[:space:]]*:[[:space:]]*true' || fail "publish boundary missing"
printf '%s' "${gate}" | grep -Eq '"not_runtime_loadable_by_default"[[:space:]]*:[[:space:]]*true' || fail "runtime boundary missing"
printf '%s' "${gate}" | grep -Eq '"case_cause_differentiation_ready"[[:space:]]*:[[:space:]]*true' || fail "case cause differentiation gate missing"
printf '%s' "${gate}" | grep -Eq '"procedural_stage_differentiation_ready"[[:space:]]*:[[:space:]]*true' || fail "procedural differentiation gate missing"
printf '%s' "${gate}" | grep -Eq '"substantive_procedural_split_ready"[[:space:]]*:[[:space:]]*true' || fail "substantive/procedural split gate missing"
printf '%s' "${gate}" | grep -Eq '"procedural_exact_match_boundary_ready"[[:space:]]*:[[:space:]]*true' || fail "procedural exact match gate missing"
printf '%s' "${gate}" | grep -Eq '"substantive_cross_procedure_boundary_ready"[[:space:]]*:[[:space:]]*true' || fail "substantive cross-procedure boundary gate missing"
printf '%s' "${gate}" | grep -Eq '"substantive_impact_ready"[[:space:]]*:[[:space:]]*true' || fail "substantive impact gate missing"
printf '%s' "${gate}" | grep -Eq '"profile_loading_contract_ready"[[:space:]]*:[[:space:]]*true' || fail "profile loading contract gate missing"
printf '%s' "${gate}" | grep -Eq '"legal_summary_ready"[[:space:]]*:[[:space:]]*true' || fail "legal summary gate missing"

call="$(post_json "/personal-skill-studio/training-artifacts/codex-training-skills/${skill_id}/provider-call/mock" '{"provider_type":"Legal_API","method_name":"search_statutes"}')"
assert_skill_safe "${call}" "provider placeholder call"
printf '%s' "${call}" | grep -Eq '"live_call_executed"[[:space:]]*:[[:space:]]*false' || fail "provider call executed unexpectedly"
printf '%s' "${call}" | grep -Eq '"credential_value_returned"[[:space:]]*:[[:space:]]*false' || fail "credential value returned"

status="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-37/status")"
assert_skill_safe "${status}" "v737 training skill status"

pass "personal codex training skill v7.37"
