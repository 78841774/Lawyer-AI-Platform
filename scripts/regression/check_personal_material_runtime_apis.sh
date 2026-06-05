#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

assert_material_runtime_safe() {
  local body="$1"
  local label="$2"
  assert_absent "${body}" "${label}" 'raw OCR text'
  assert_absent "${body}" "${label}" 'raw material'
  assert_absent "${body}" "${label}" 'recognized source text value'
}

section "Personal Material Runtime APIs"

endpoints=(
  "/personal-material-runtime/status"
  "/personal-material-runtime/providers"
  "/personal-material-runtime/parse-jobs"
  "/personal-material-runtime/ocr-jobs"
  "/personal-material-runtime/ocr-review-queue"
  "/personal-material-runtime/source-traces"
  "/personal-material-runtime/audit"
  "/personal-material-runtime/safety"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_metadata_safe "${body}" "${endpoint}"
  assert_material_runtime_safe "${body}" "${endpoint}"
  assert_field_false_required "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_required "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_required "${body}" "${endpoint}" "final_report_generated"
  assert_field_false_if_present "${body}" "${endpoint}" "live_provider_call_enabled"
  if printf '%s' "${body}" | grep -Eq '"api_key_visible"[[:space:]]*:[[:space:]]*true'; then
    fail "${endpoint} expected api_key_visible=false"
  fi
done

parse_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_v55_approve_all",
      "material_id":"material_demo_001",
      "parser_provider_id":"mineru_file_parser_provider",
      "parse_type":"pdf_text_extract_preview",
      "manual_approval_confirmed":true,
      "mock_data_only_confirmation":true,
      "no_raw_content_confirmation":true,
      "no_external_upload_confirmation":true
    }' \
    "${API_BASE}/personal-material-runtime/parse-jobs/mock"
)"
assert_metadata_safe "${parse_body}" "parse-jobs/mock"
assert_material_runtime_safe "${parse_body}" "parse-jobs/mock"
assert_field_false_required "${parse_body}" "parse-jobs/mock" "would_call_provider"
assert_field_false_required "${parse_body}" "parse-jobs/mock" "live_call_executed"
assert_field_false_required "${parse_body}" "parse-jobs/mock" "raw_content_included"
assert_field_false_required "${parse_body}" "parse-jobs/mock" "raw_material_text_exposed"
assert_field_false_required "${parse_body}" "parse-jobs/mock" "raw_ocr_text_exposed"
require_true_field "${parse_body}" "parse-jobs/mock" "controlled_preview_only"
require_true_field "${parse_body}" "parse-jobs/mock" "requires_lawyer_review"
require_true_field "${parse_body}" "parse-jobs/mock" "source_trace_required"

ocr_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_v55_approve_all",
      "material_id":"material_demo_001",
      "ocr_provider_id":"paddleocr_provider",
      "ocr_job_type":"scanned_pdf_ocr_preview",
      "manual_approval_confirmed":true,
      "lawyer_review_required_confirmation":true,
      "source_trace_required_confirmation":true,
      "no_raw_ocr_exposure_confirmation":true,
      "no_final_legal_opinion_confirmation":true,
      "no_final_report_generation_confirmation":true
    }' \
    "${API_BASE}/personal-material-runtime/ocr-jobs/mock"
)"
assert_metadata_safe "${ocr_body}" "ocr-jobs/mock"
assert_material_runtime_safe "${ocr_body}" "ocr-jobs/mock"
assert_field_false_required "${ocr_body}" "ocr-jobs/mock" "would_call_provider"
assert_field_false_required "${ocr_body}" "ocr-jobs/mock" "live_call_executed"
assert_field_false_required "${ocr_body}" "ocr-jobs/mock" "raw_content_included"
assert_field_false_required "${ocr_body}" "ocr-jobs/mock" "raw_ocr_text_exposed"
assert_field_false_required "${ocr_body}" "ocr-jobs/mock" "used_in_ai_prompt"
assert_field_false_required "${ocr_body}" "ocr-jobs/mock" "used_in_final_output"
require_true_field "${ocr_body}" "ocr-jobs/mock" "controlled_preview_only"
require_true_field "${ocr_body}" "ocr-jobs/mock" "requires_lawyer_review"
require_true_field "${ocr_body}" "ocr-jobs/mock" "source_trace_required"

ocr_job_id="$(printf '%s' "${ocr_body}" | sed -n 's/.*"ocr_job_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${ocr_job_id}" ]; then
  fail "ocr-jobs/mock did not return ocr_job_id"
fi

preview_body="$(check_endpoint_200 "/personal-material-runtime/ocr-jobs/${ocr_job_id}/preview")"
assert_metadata_safe "${preview_body}" "ocr preview"
assert_material_runtime_safe "${preview_body}" "ocr preview"
assert_field_false_required "${preview_body}" "ocr preview" "raw_ocr_text_exposed"
assert_field_false_required "${preview_body}" "ocr preview" "used_in_ai_prompt"
assert_field_false_required "${preview_body}" "ocr preview" "used_in_final_output"
require_true_field "${preview_body}" "ocr preview" "controlled_preview_only"
require_true_field "${preview_body}" "ocr preview" "requires_lawyer_review"
require_true_field "${preview_body}" "ocr preview" "source_trace_required"

review_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"approve_preview_for_analysis",
      "reviewer_id":"local_demo_lawyer",
      "manual_review_confirmed":true,
      "no_raw_ocr_exposure_confirmation":true,
      "lawyer_review_required_confirmation":true
    }' \
    "${API_BASE}/personal-material-runtime/ocr-review-queue/${ocr_job_id}/actions"
)"
assert_metadata_safe "${review_body}" "ocr review action"
assert_material_runtime_safe "${review_body}" "ocr review action"
assert_field_false_required "${review_body}" "ocr review action" "raw_content_included"
assert_field_false_required "${review_body}" "ocr review action" "raw_ocr_text_exposed"
assert_field_false_required "${review_body}" "ocr review action" "used_in_ai_prompt"
assert_field_false_required "${review_body}" "ocr review action" "used_in_final_output"
require_true_field "${review_body}" "ocr review action" "controlled_preview_only"

queue_body="$(check_endpoint_200 "/personal-material-runtime/ocr-review-queue")"
traces_body="$(check_endpoint_200 "/personal-material-runtime/source-traces")"
audit_body="$(check_endpoint_200 "/personal-material-runtime/audit")"
assert_metadata_safe "${queue_body}" "ocr-review-queue"
assert_metadata_safe "${traces_body}" "source-traces"
assert_metadata_safe "${audit_body}" "audit"
assert_material_runtime_safe "${queue_body}" "ocr-review-queue"
assert_material_runtime_safe "${traces_body}" "source-traces"
assert_material_runtime_safe "${audit_body}" "audit"
assert_field_false_required "${traces_body}" "source-traces" "used_in_ai_prompt"
assert_field_false_required "${traces_body}" "source-traces" "used_in_final_output"

pass "personal material runtime APIs"
