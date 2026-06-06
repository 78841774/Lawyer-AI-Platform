#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Codex Training Runs v7.31"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/training_artifacts"

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

require_false_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*false"; then
    fail "${label} expected ${field}=false"
  fi
}

require_contains() {
  local body="$1"
  local label="$2"
  local pattern="$3"
  if ! printf '%s' "${body}" | grep -Eq "${pattern}"; then
    fail "${label} expected pattern: ${pattern}"
  fi
}

assert_codex_training_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR content|raw case content|raw provider response|customer name|ID number|phone number|客户姓名|身份证号|手机号'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "training_artifact_only"
  require_true_field "${body}" "${label}" "codex_training"
  require_true_field "${body}" "${label}" "training_run_generated"
  require_true_field "${body}" "${label}" "closed_case_only"
  require_true_field "${body}" "${label}" "load_dry_run"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "fine_tune_model_training"
  require_false_field "${body}" "${label}" "open_case_data_used"
  require_false_field "${body}" "${label}" "raw_content_included"
  require_false_field "${body}" "${label}" "raw_ocr_content_included"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "secret_value_returned"
  require_false_field "${body}" "${label}" "local_path_exposed"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "skill_auto_published"
  require_false_field "${body}" "${label}" "load_executed"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "blocks_next_stage"
}

list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-runs")"
assert_codex_training_safe "${list_body}" "training-runs"

create_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "source_case_mode":"synthetic_closed_case",
      "target_case_cause_paths":[
        ["civil","contract_dispute","sales_contract_dispute"],
        ["civil","contract_dispute","loan_contract_dispute"],
        ["civil","tort_dispute","traffic_accident_dispute"],
        ["civil","marriage_inheritance","divorce_dispute"],
        ["civil","labor_dispute","labor_contract_dispute"]
      ],
      "target_skill_ids":["case_fact_extraction_skill","case_legal_analysis_skill"],
      "explicit_closed_case_only_confirmation":true,
      "explicit_redaction_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_open_case_training_confirmation":true,
      "explicit_no_auto_publish_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/training-runs/mock"
)"
assert_codex_training_safe "${create_body}" "training-runs/mock"
require_contains "${create_body}" "training-runs/mock" '"source_case_mode"[[:space:]]*:[[:space:]]*"synthetic_closed_case"'
require_contains "${create_body}" "training-runs/mock" '"case_fact_extraction_skill"'
require_contains "${create_body}" "training-runs/mock" '"case_legal_analysis_skill"'

training_run_id="$(printf '%s' "${create_body}" | sed -n 's/.*"training_run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${training_run_id}" ]; then
  fail "training-runs/mock did not return training_run_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/summary" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/case-cause-packages" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/generated-skills" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/evaluations" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/gates" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/test-cases" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/loading-manifest" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/audit" \
  "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_codex_training_safe "${body}" "${endpoint}"
done

packages_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/case-cause-packages")"
require_contains "${packages_body}" "case-cause-packages" '"source_case_mode"[[:space:]]*:[[:space:]]*"synthetic_closed_case"'
require_contains "${packages_body}" "case-cause-packages" '"case_cause_scope"'

skills_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/generated-skills")"
require_contains "${skills_body}" "generated-skills" '"skill_published"[[:space:]]*:[[:space:]]*false'
require_contains "${skills_body}" "generated-skills" '"baseline_complete"'

loading_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/loading-manifest")"
require_contains "${loading_body}" "loading-manifest" '"case_cause_match_strategy"'
require_contains "${loading_body}" "loading-manifest" '"exact_then_ancestor_then_common_with_evidence_overlay"'
require_contains "${loading_body}" "loading-manifest" '"case_fact_extraction_skill"'
require_contains "${loading_body}" "loading-manifest" '"case_legal_analysis_skill"'

load_dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-skill-studio/training-artifacts/training-runs/${training_run_id}/load-dry-run/mock"
)"
assert_codex_training_safe "${load_dry_run_body}" "training-run load-dry-run/mock"
require_contains "${load_dry_run_body}" "training-run load-dry-run/mock" '"load_dry_run_result"'

detail_after_load="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-runs/${training_run_id}")"
assert_codex_training_safe "${detail_after_load}" "training-run detail after load"
require_contains "${detail_after_load}" "training-run detail after load" '"load_dry_run_result"'

pass "personal codex training runs v7.31"
