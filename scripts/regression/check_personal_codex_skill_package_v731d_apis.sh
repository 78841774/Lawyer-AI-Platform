#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Codex Skill Package v7.31d"
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

extract_id() {
  local body="$1"
  local field="$2"
  printf '%s' "${body}" | sed -n "s/.*\"${field}\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p" | head -n 1
}

assert_v731d_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "redacted_output_only"
  require_true_field "${body}" "${label}" "approved_experience_only"
  require_true_field "${body}" "${label}" "system_validation_required"
  require_true_field "${body}" "${label}" "system_validation_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "source_material_returned"
  require_false_field "${body}" "${label}" "unreviewed_experience_packaged"
  require_false_field "${body}" "${label}" "unsafe_experience_packaged"
  require_false_field "${body}" "${label}" "missing_source_trace_packaged"
  require_false_field "${body}" "${label}" "formal_training_set_generated"
  require_false_field "${body}" "${label}" "real_codex_training_triggered"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "skill_publishable"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

post_json() {
  local endpoint="$1"
  local payload="$2"
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "${payload}" \
    "${API_BASE}${endpoint}"
}

post_status() {
  local endpoint="$1"
  local payload="$2"
  curl -sS \
    -o /tmp/v731d_response_body.json \
    -w "%{http_code}" \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "${payload}" \
    "${API_BASE}${endpoint}"
}

ocr_body="$(post_json "/personal-skill-studio/training-artifacts/ocr-jobs" '{
  "material_label":"authorized_lawyer_work_product_metadata_001",
  "owner_user_id":"owner_local_demo",
  "document_type":"case_work_product",
  "page_count":8,
  "explicit_authorized_case_confirmation":true,
  "explicit_internal_processing_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_raw_return_confirmation":true
}')"
ocr_job_id="$(extract_id "${ocr_body}" "job_id")"
if [ -z "${ocr_job_id}" ]; then
  fail "setup ocr job missing job_id"
fi

retrieval_body="$(post_json "/personal-skill-studio/training-artifacts/legal-retrieval-jobs" "{
  \"source_ocr_job_id\":\"${ocr_job_id}\",
  \"query_label\":\"contract_dispute_experience_basis\",
  \"owner_user_id\":\"owner_local_demo\",
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_key_value_confirmation\":true,
  \"explicit_demo_safe_confirmation\":true
}")"
retrieval_job_id="$(extract_id "${retrieval_body}" "retrieval_job_id")"
if [ -z "${retrieval_job_id}" ]; then
  fail "setup legal retrieval missing retrieval_job_id"
fi

candidates_body="$(post_json "/personal-skill-studio/training-artifacts/experience-candidates/build" "{
  \"source_ocr_job_id\":\"${ocr_job_id}\",
  \"source_legal_retrieval_job_id\":\"${retrieval_job_id}\",
  \"owner_user_id\":\"owner_local_demo\",
  \"explicit_redaction_required_confirmation\":true,
  \"explicit_manual_review_required_confirmation\":true,
  \"explicit_no_skill_publish_confirmation\":true
}")"
candidate_id="$(extract_id "${candidates_body}" "candidate_id")"
if [ -z "${candidate_id}" ]; then
  fail "setup experience candidates missing candidate_id"
fi

post_json "/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/redact" '{}' >/dev/null
post_json "/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/review" '{
  "action":"approve",
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"experience candidate metadata review only",
  "explicit_manual_review_confirmation":true,
  "explicit_no_raw_return_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}' >/dev/null

import_body="$(post_json "/personal-skill-studio/training-artifacts/skill-experience-pool/import-approved" "{\"source_candidate_ids\":[\"${candidate_id}\"],\"owner_user_id\":\"owner_local_demo\",\"explicit_approved_experience_only_confirmation\":true,\"explicit_redacted_output_only_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
experience_id="$(extract_id "${import_body}" "experience_id")"
if [ -z "${experience_id}" ]; then
  fail "skill-experience-pool/import-approved did not return experience_id"
fi

binding_body="$(post_json "/personal-skill-studio/training-artifacts/skill-experience-bindings" "{\"experience_ids\":[\"${experience_id}\"],\"skill_domain\":\"case_analysis\",\"skill_name_candidate\":\"案件经验提炼 Skill 草案\",\"case_cause_scope\":\"demo_safe_case_cause_scope\",\"experience_types\":[],\"draft_target_id\":\"codex_skill_draft_target_v731c\"}")"
binding_id="$(extract_id "${binding_body}" "binding_id")"
if [ -z "${binding_id}" ]; then
  fail "skill-experience-bindings create did not return binding_id"
fi

draft_body="$(post_json "/personal-skill-studio/training-artifacts/codex-skill-drafts/build" "{\"experience_ids\":[\"${experience_id}\"],\"binding_id\":\"${binding_id}\",\"draft_name\":\"Codex Skill 草案 v7.31c\",\"draft_target_id\":\"codex_skill_draft_target_v731c\",\"explicit_approved_experience_only_confirmation\":true,\"explicit_no_provider_confirmation\":true,\"explicit_no_real_training_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
draft_id="$(extract_id "${draft_body}" "draft_id")"
if [ -z "${draft_id}" ]; then
  fail "codex-skill-drafts/build did not return draft_id"
fi

unconfirmed_status="$(post_status "/personal-skill-studio/training-artifacts/skill-packages/build" "{\"source_draft_id\":\"${draft_id}\",\"package_name\":\"unconfirmed package\",\"package_version\":\"v7.31d-rejected\",\"explicit_system_validation_gate_confirmation\":true,\"explicit_no_manual_training_output_review_confirmation\":true,\"explicit_no_provider_confirmation\":true,\"explicit_no_real_training_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
if [ "${unconfirmed_status}" -lt 400 ]; then
  fail "unconfirmed draft should not build package"
fi
assert_no_stack_trace "$(cat /tmp/v731d_response_body.json)" "unconfirmed package build"

post_json "/personal-skill-studio/training-artifacts/codex-skill-drafts/${draft_id}/review" '{
  "action":"approve_draft_structure",
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"draft structure review only",
  "explicit_manual_confirmation":true,
  "explicit_no_skill_publish_confirmation":true,
  "explicit_no_real_training_confirmation":true
}' >/dev/null

build_body="$(post_json "/personal-skill-studio/training-artifacts/skill-packages/build" "{\"source_draft_id\":\"${draft_id}\",\"package_name\":\"案件经验提炼 Skill Package v7.31d\",\"package_version\":\"v7.31d.0\",\"explicit_system_validation_gate_confirmation\":true,\"explicit_no_manual_training_output_review_confirmation\":true,\"explicit_no_provider_confirmation\":true,\"explicit_no_real_training_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
assert_v731d_safe "${build_body}" "skill-packages/build"
package_id="$(extract_id "${build_body}" "package_id")"
if [ -z "${package_id}" ]; then
  fail "skill-packages/build did not return package_id"
fi
require_contains "${build_body}" "skill-packages/build" '"pre_publish_gate_status"[[:space:]]*:[[:space:]]*"draft"'
require_contains "${build_body}" "skill-packages/build" '"package_status"[[:space:]]*:[[:space:]]*"draft_package"'
require_contains "${build_body}" "skill-packages/build" '"final_review_status"[[:space:]]*:[[:space:]]*"not_applicable"'

for endpoint in \
  "/personal-skill-studio/training-artifacts/skill-packages" \
  "/personal-skill-studio/training-artifacts/skill-packages/${package_id}" \
  "/personal-skill-studio/training-artifacts/skill-packages/${package_id}/manifest" \
  "/personal-skill-studio/training-artifacts/skill-packages/${package_id}/audit" \
  "/personal-skill-studio/training-artifacts/skill-packages/${package_id}/source-trace"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731d_safe "${body}" "${endpoint}"
done

validate_body="$(post_json "/personal-skill-studio/training-artifacts/skill-packages/${package_id}/validate" '{}')"
assert_v731d_safe "${validate_body}" "skill-packages validate"
require_contains "${validate_body}" "skill-packages validate" '"pre_publish_gate_status"[[:space:]]*:[[:space:]]*"system_validated"'
require_contains "${validate_body}" "skill-packages validate" '"package_status"[[:space:]]*:[[:space:]]*"ready_for_training_package_build"'
require_true_field "${validate_body}" "skill-packages validate" "gate_passed"
require_true_field "${validate_body}" "skill-packages validate" "all_experiences_redacted"
require_true_field "${validate_body}" "skill-packages validate" "all_experiences_approved"
require_true_field "${validate_body}" "skill-packages validate" "all_source_traces_present"
require_true_field "${validate_body}" "skill-packages validate" "audit_complete"
require_true_field "${validate_body}" "skill-packages validate" "draft_structure_confirmed"
require_true_field "${validate_body}" "skill-packages validate" "manifest_generated"
require_true_field "${validate_body}" "skill-packages validate" "sensitive_field_scan_passed"
require_true_field "${validate_body}" "skill-packages validate" "ready_for_training_package_build"

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-31d/status")"
assert_v731d_safe "${status_body}" "v7-31d/status"
require_contains "${status_body}" "v7-31d/status" '"system_validated_count"[[:space:]]*:[[:space:]]*1'

pass "personal codex skill package v7.31d"
