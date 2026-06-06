#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training Experience Pipeline v7.31b"
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

assert_v731b_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|local_path|file_path|absolute_path|api_key|secret|provider_response|private_key|access_token|refresh_token'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "redacted_output_only"
  require_true_field "${body}" "${label}" "manual_review_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

boundary_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/raw-work-product-boundary/status")"
assert_v731b_safe "${boundary_body}" "raw-work-product-boundary/status"
require_true_field "${boundary_body}" "raw-work-product-boundary/status" "skill_direct_ingest_blocked"

ocr_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "material_label":"authorized_lawyer_work_product_metadata_001",
      "owner_user_id":"owner_local_demo",
      "document_type":"case_work_product",
      "page_count":8,
      "explicit_authorized_case_confirmation":true,
      "explicit_internal_processing_confirmation":true,
      "explicit_no_provider_confirmation":true,
      "explicit_no_raw_return_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/ocr-jobs"
)"
assert_v731b_safe "${ocr_body}" "ocr-jobs create"
ocr_job_id="$(extract_id "${ocr_body}" "job_id")"
if [ -z "${ocr_job_id}" ]; then
  fail "ocr-jobs create did not return job_id"
fi
require_contains "${ocr_body}" "ocr-jobs create" '"parse_status"[[:space:]]*:[[:space:]]*"demo_safe_parse_completed"'

for endpoint in \
  "/personal-skill-studio/training-artifacts/ocr-jobs" \
  "/personal-skill-studio/training-artifacts/ocr-jobs/${ocr_job_id}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731b_safe "${body}" "${endpoint}"
done

retrieval_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"source_ocr_job_id\":\"${ocr_job_id}\",
      \"query_label\":\"contract_dispute_experience_basis\",
      \"owner_user_id\":\"owner_local_demo\",
      \"explicit_no_provider_confirmation\":true,
      \"explicit_no_key_value_confirmation\":true,
      \"explicit_demo_safe_confirmation\":true
    }" \
    "${API_BASE}/personal-skill-studio/training-artifacts/legal-retrieval-jobs"
)"
assert_v731b_safe "${retrieval_body}" "legal-retrieval-jobs create"
retrieval_job_id="$(extract_id "${retrieval_body}" "retrieval_job_id")"
if [ -z "${retrieval_job_id}" ]; then
  fail "legal-retrieval-jobs create did not return retrieval_job_id"
fi
require_contains "${retrieval_body}" "legal-retrieval-jobs create" '"retrieval_status"[[:space:]]*:[[:space:]]*"demo_safe_retrieval_completed"'

for endpoint in \
  "/personal-skill-studio/training-artifacts/legal-retrieval-jobs" \
  "/personal-skill-studio/training-artifacts/legal-retrieval-jobs/${retrieval_job_id}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731b_safe "${body}" "${endpoint}"
done

candidates_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"source_ocr_job_id\":\"${ocr_job_id}\",
      \"source_legal_retrieval_job_id\":\"${retrieval_job_id}\",
      \"owner_user_id\":\"owner_local_demo\",
      \"explicit_redaction_required_confirmation\":true,
      \"explicit_manual_review_required_confirmation\":true,
      \"explicit_no_skill_publish_confirmation\":true
    }" \
    "${API_BASE}/personal-skill-studio/training-artifacts/experience-candidates/build"
)"
assert_v731b_safe "${candidates_body}" "experience-candidates/build"
candidate_id="$(extract_id "${candidates_body}" "candidate_id")"
if [ -z "${candidate_id}" ]; then
  fail "experience-candidates/build did not return candidate_id"
fi
require_contains "${candidates_body}" "experience-candidates/build" '"redaction_status"[[:space:]]*:[[:space:]]*"requires_redaction"'

for endpoint in \
  "/personal-skill-studio/training-artifacts/experience-candidates" \
  "/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731b_safe "${body}" "${endpoint}"
done

redaction_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/redact"
)"
assert_v731b_safe "${redaction_body}" "experience-candidate redact"
require_contains "${redaction_body}" "experience-candidate redact" '"redaction_status"[[:space:]]*:[[:space:]]*"redacted_output_ready"'

review_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"approve",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"experience candidate metadata review only",
      "explicit_manual_review_confirmation":true,
      "explicit_no_raw_return_confirmation":true,
      "explicit_no_skill_publish_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/review"
)"
assert_v731b_safe "${review_body}" "experience-candidate review"
require_contains "${review_body}" "experience-candidate review" '"review_status"[[:space:]]*:[[:space:]]*"approved_for_skill_experience"'
require_true_field "${review_body}" "experience-candidate review" "skill_experience_ready"

for endpoint in \
  "/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/audit" \
  "/personal-skill-studio/training-artifacts/v7-31b/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731b_safe "${body}" "${endpoint}"
done

pass "personal training experience pipeline v7.31b"
