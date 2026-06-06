#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Codex Skill Training Run v7.38"

bash "${SCRIPT_DIR}/check_personal_codex_training_skill_v737_apis.sh" >/dev/null

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

assert_run_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
}

skill="$(post_json "/personal-skill-studio/training-artifacts/codex-training-skills/generate" '{"skill_target":"case_analysis_skill"}')"
skill_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("training_skill_id",""))' <<<"${skill}")"
post_json "/personal-skill-studio/training-artifacts/codex-training-skills/${skill_id}/gate/run" '{}' >/dev/null

run="$(post_json "/personal-skill-studio/training-artifacts/codex-skill-training-runs/start" "{\"training_skill_id\":\"${skill_id}\",\"run_mode\":\"dry_run\"}")"
assert_run_safe "${run}" "skill training run start"
run_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("training_run_id",""))' <<<"${run}")"
[ -n "${run_id}" ] || fail "missing training run id"
printf '%s' "${run}" | grep -Eq '"run_status"[[:space:]]*:[[:space:]]*"completed"' || fail "training run not completed"

for endpoint in \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/logs" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/metrics" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/gate-report" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/artifact" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/audit" \
  "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/source-trace" \
  "/personal-skill-studio/training-artifacts/v7-38/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_run_safe "${body}" "${endpoint}"
done

artifact="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/artifact")"
printf '%s' "${artifact}" | grep -Eq '"not_publishable"[[:space:]]*:[[:space:]]*true' || fail "artifact publish boundary missing"
printf '%s' "${artifact}" | grep -Eq '"not_runtime_loadable"[[:space:]]*:[[:space:]]*true' || fail "artifact runtime boundary missing"
printf '%s' "${artifact}" | grep -Eq '"requires_practice_load_review"[[:space:]]*:[[:space:]]*true' || fail "practice review boundary missing"
printf '%s' "${artifact}" | grep -Eq '"generated_experience_package"[[:space:]]*:' || fail "generated experience package missing"
printf '%s' "${artifact}" | grep -Eq '"case_cause_specific_fact_points"[[:space:]]*:' || fail "differentiated fact points missing"
printf '%s' "${artifact}" | grep -Eq '"procedural_profiles"[[:space:]]*:' || fail "procedural profiles missing"
printf '%s' "${artifact}" | grep -Eq '"substantive_experience_profiles"[[:space:]]*:' || fail "substantive experience profiles missing"
printf '%s' "${artifact}" | grep -Eq '"procedural_experience_profiles"[[:space:]]*:' || fail "procedural experience profiles missing"
printf '%s' "${artifact}" | grep -Eq '"runtime_reference_type"[[:space:]]*:[[:space:]]*"substantive_reference"' || fail "substantive reference type missing"
printf '%s' "${artifact}" | grep -Eq '"runtime_reference_type"[[:space:]]*:[[:space:]]*"procedural_exact_match"' || fail "procedural exact match type missing"
printf '%s' "${artifact}" | grep -Eq '"cross_stage_reference_allowed"[[:space:]]*:[[:space:]]*false' || fail "procedural cross-stage boundary missing"
printf '%s' "${artifact}" | grep -Eq '"substantive_impact_points"[[:space:]]*:' || fail "substantive impact points missing"
printf '%s' "${artifact}" | grep -Eq '"profile_loading_contract"[[:space:]]*:' || fail "profile loading contract missing"
printf '%s' "${artifact}" | grep -Eq '"legal_summary_validated"[[:space:]]*:[[:space:]]*true' || fail "legal summary validation missing"
printf '%s' "${artifact}" | grep -Eq '"case_cause_differentiation_validated"[[:space:]]*:[[:space:]]*true' || fail "case cause differentiation validation missing"
printf '%s' "${artifact}" | grep -Eq '"procedural_stage_differentiation_validated"[[:space:]]*:[[:space:]]*true' || fail "procedural stage differentiation validation missing"
printf '%s' "${artifact}" | grep -Eq '"substantive_procedural_split_validated"[[:space:]]*:[[:space:]]*true' || fail "substantive/procedural split validation missing"
printf '%s' "${artifact}" | grep -Eq '"procedural_exact_match_boundary_validated"[[:space:]]*:[[:space:]]*true' || fail "procedural exact match validation missing"
printf '%s' "${artifact}" | grep -Eq '"substantive_cross_procedure_boundary_validated"[[:space:]]*:[[:space:]]*true' || fail "substantive cross-procedure boundary validation missing"
printf '%s' "${artifact}" | grep -Eq '"substantive_impact_validated"[[:space:]]*:[[:space:]]*true' || fail "substantive impact validation missing"

gate="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/codex-skill-training-runs/${run_id}/gate-report")"
printf '%s' "${gate}" | grep -Eq '"facts_output_diff_check_passed"[[:space:]]*:[[:space:]]*true' || fail "facts diff check missing"
printf '%s' "${gate}" | grep -Eq '"procedural_stage_diff_check_passed"[[:space:]]*:[[:space:]]*true' || fail "procedural diff check missing"
printf '%s' "${gate}" | grep -Eq '"substantive_procedural_split_check_passed"[[:space:]]*:[[:space:]]*true' || fail "substantive/procedural split check missing"
printf '%s' "${gate}" | grep -Eq '"procedural_exact_match_check_passed"[[:space:]]*:[[:space:]]*true' || fail "procedural exact match check missing"
printf '%s' "${gate}" | grep -Eq '"substantive_impact_check_passed"[[:space:]]*:[[:space:]]*true' || fail "substantive impact check missing"
printf '%s' "${gate}" | grep -Eq '"legal_summary_check_passed"[[:space:]]*:[[:space:]]*true' || fail "legal summary check missing"
printf '%s' "${gate}" | grep -Eq '"readiness_check_passed"[[:space:]]*:[[:space:]]*true' || fail "readiness check missing"

pass "personal codex skill training run v7.38"
