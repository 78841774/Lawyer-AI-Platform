#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Material Live Gateway APIs v7.27"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_material_runtime/live"

assert_material_live_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'OPENAI_API_KEY'
  assert_absent "${body}" "${label}" 'DEEPSEEK_API_KEY'
  assert_absent "${body}" "${label}" 'API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'BEGIN PRIVATE KEY'
  assert_absent "${body}" "${label}" 'sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" 'raw_ocr_text[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'raw_document_content[[:space:]]*[:=]'
  assert_field_false_if_present "${body}" "${label}" "api_key_exposed"
  assert_field_false_if_present "${body}" "${label}" "secret_value_returned"
  assert_field_false_if_present "${body}" "${label}" "secret_logged"
  assert_field_false_if_present "${body}" "${label}" "frontend_key_input_enabled"
  assert_field_false_if_present "${body}" "${label}" "live_call_allowed"
  assert_field_false_if_present "${body}" "${label}" "live_call_executed"
  assert_field_false_if_present "${body}" "${label}" "raw_content_exposed"
  assert_field_false_if_present "${body}" "${label}" "raw_ocr_text_exposed"
  assert_field_false_if_present "${body}" "${label}" "raw_document_content_exposed"
  assert_field_false_if_present "${body}" "${label}" "ai_prompt_injected"
  assert_field_false_if_present "${body}" "${label}" "fact_extraction_triggered"
  assert_field_false_if_present "${body}" "${label}" "legal_analysis_triggered"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "real_pdf_generated"
  assert_field_false_if_present "${body}" "${label}" "real_docx_generated"
}

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

for endpoint in \
  "/personal-material-runtime/live/status" \
  "/personal-material-runtime/live/providers" \
  "/personal-material-runtime/live/providers/paddleocr" \
  "/personal-material-runtime/live/providers/paddleocr/secret-boundary" \
  "/personal-material-runtime/live/providers/paddleocr/live-gate" \
  "/personal-material-runtime/live/providers/paddleocr/health/dry-run" \
  "/personal-material-runtime/live-gates" \
  "/personal-material-runtime/live/document/runs" \
  "/personal-material-runtime/live/ocr/runs" \
  "/personal-material-runtime/live/review-queue" \
  "/personal-material-runtime/live/source-traces" \
  "/personal-material-runtime/live/audit" \
  "/personal-material-runtime/live/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_material_live_safe "${body}" "${endpoint}"
done

secret_body="$(check_endpoint_200 "/personal-material-runtime/live/providers/paddleocr/secret-boundary")"
assert_material_live_safe "${secret_body}" "material live secret boundary"
assert_field_false_required "${secret_body}" "material live secret boundary" "key_value_exposed"
assert_field_false_required "${secret_body}" "material live secret boundary" "key_prefix_returned"
assert_field_false_required "${secret_body}" "material live secret boundary" "key_suffix_returned"
assert_field_false_required "${secret_body}" "material live secret boundary" "masked_key_returned"
assert_field_false_required "${secret_body}" "material live secret boundary" "token_value_returned"
assert_field_false_required "${secret_body}" "material live secret boundary" "secret_value_stored"

gate_body="$(check_endpoint_200 "/personal-material-runtime/live/providers/paddleocr/live-gate")"
assert_material_live_safe "${gate_body}" "material live gate"
assert_field_false_required "${gate_body}" "material live gate" "global_live_enabled"
assert_field_false_required "${gate_body}" "material live gate" "provider_live_enabled"
assert_field_false_required "${gate_body}" "material live gate" "live_call_allowed"
assert_field_false_required "${gate_body}" "material live gate" "live_call_executed"

health_body="$(check_endpoint_200 "/personal-material-runtime/live/providers/paddleocr/health/dry-run")"
assert_material_live_safe "${health_body}" "material health dry-run"
require_true_field "${health_body}" "material health dry-run" "dry_run_ready"
assert_field_false_required "${health_body}" "material health dry-run" "network_call_executed"
assert_field_false_required "${health_body}" "material health dry-run" "upload_executed"
assert_field_false_required "${health_body}" "material health dry-run" "raw_content_uploaded"

mock_gate_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"paddleocr",
      "explicit_live_confirmation":false,
      "owner_authorized":false,
      "raw_content_boundary_acknowledged":true,
      "no_ai_prompt_injection_acknowledged":true,
      "audit_acknowledged":true
    }' \
    "${API_BASE}/personal-material-runtime/live-gates/mock"
)"
assert_material_live_safe "${mock_gate_body}" "material live-gates/mock"
assert_field_false_required "${mock_gate_body}" "material live-gates/mock" "live_call_allowed"
assert_field_false_required "${mock_gate_body}" "material live-gates/mock" "live_call_executed"

document_dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"mineru",
      "case_id":"case_v55_approve_all",
      "material_id":"material_demo_001",
      "file_name":"controlled_demo_material.pdf",
      "file_type":"pdf",
      "byte_size":1200000,
      "page_range":"1-2",
      "actor_id":"local_demo_lawyer",
      "dry_run":true,
      "explicit_live_confirmation":false,
      "material_owner_confirmation":false,
      "raw_content_handling_acknowledged":false,
      "no_ai_prompt_injection_acknowledged":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false
    }' \
    "${API_BASE}/personal-material-runtime/live/document/dry-run"
)"
assert_material_live_safe "${document_dry_run_body}" "document dry-run"
require_true_field "${document_dry_run_body}" "document dry-run" "dry_run"
require_true_field "${document_dry_run_body}" "document dry-run" "file_metadata_only"
require_true_field "${document_dry_run_body}" "document dry-run" "source_trace_required"
require_true_field "${document_dry_run_body}" "document dry-run" "lawyer_review_required"
if ! printf '%s' "${document_dry_run_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"dry_run_completed"'; then
  fail "document dry-run expected dry_run_completed"
fi

ocr_dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"paddleocr",
      "case_id":"case_v55_approve_all",
      "material_id":"material_demo_001",
      "file_name":"controlled_demo_scan.pdf",
      "file_type":"pdf",
      "byte_size":900000,
      "page_range":"1",
      "actor_id":"local_demo_lawyer",
      "dry_run":true,
      "explicit_live_confirmation":false,
      "material_owner_confirmation":false,
      "raw_content_handling_acknowledged":false,
      "no_ai_prompt_injection_acknowledged":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false
    }' \
    "${API_BASE}/personal-material-runtime/live/ocr/dry-run"
)"
assert_material_live_safe "${ocr_dry_run_body}" "ocr dry-run"
require_true_field "${ocr_dry_run_body}" "ocr dry-run" "dry_run"
require_true_field "${ocr_dry_run_body}" "ocr dry-run" "source_trace_required"
require_true_field "${ocr_dry_run_body}" "ocr dry-run" "lawyer_review_required"
if ! printf '%s' "${ocr_dry_run_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"dry_run_completed"'; then
  fail "ocr dry-run expected dry_run_completed"
fi
if ! printf '%s' "${ocr_dry_run_body}" | grep -Eq '"page_count_estimate"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "ocr dry-run expected page_count_estimate metadata"
fi

blocked_document_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"mineru",
      "case_id":"case_v55_approve_all",
      "material_id":"material_demo_001",
      "file_name":"controlled_demo_material.pdf",
      "file_type":"pdf",
      "byte_size":1200000,
      "page_range":"1-2",
      "actor_id":"local_demo_lawyer",
      "dry_run":false,
      "explicit_live_confirmation":false,
      "material_owner_confirmation":false,
      "raw_content_handling_acknowledged":false,
      "no_ai_prompt_injection_acknowledged":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false
    }' \
    "${API_BASE}/personal-material-runtime/live/document/runs"
)"
assert_material_live_safe "${blocked_document_body}" "document live blocked"
if ! printf '%s' "${blocked_document_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"live_call_blocked"'; then
  fail "document live run without confirmations must be live_call_blocked"
fi
assert_field_false_required "${blocked_document_body}" "document live blocked" "live_call_executed"

review_queue_body="$(check_endpoint_200 "/personal-material-runtime/live/review-queue")"
assert_material_live_safe "${review_queue_body}" "live review queue"
if ! printf '%s' "${review_queue_body}" | grep -Eq '"item_count"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "live review queue expected metadata item"
fi

audit_body="$(check_endpoint_200 "/personal-material-runtime/live/audit")"
assert_material_live_safe "${audit_body}" "live audit after runs"
if ! printf '%s' "${audit_body}" | grep -Eq '"event_count"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "live audit expected at least one audit event"
fi

pass "personal material live gateway APIs v7.27"
