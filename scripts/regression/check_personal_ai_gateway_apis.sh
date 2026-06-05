#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal AI Gateway APIs"

endpoints=(
  "/personal-ai-gateway/status"
  "/personal-ai-gateway/providers"
  "/personal-ai-gateway/prompt-templates"
  "/personal-ai-gateway/audit"
  "/personal-ai-gateway/token-usage/summary"
  "/personal-ai-gateway/safety"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_metadata_safe "${body}" "${endpoint}"
  assert_field_false_required "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_required "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_required "${body}" "${endpoint}" "final_report_generated"
  assert_field_false_if_present "${body}" "${endpoint}" "live_provider_call_enabled"
  assert_field_false_if_present "${body}" "${endpoint}" "live_usage_available"
  if printf '%s' "${body}" | grep -Eq '"api_key_visible"[[:space:]]*:[[:space:]]*true'; then
    fail "${endpoint} expected api_key_visible=false"
  fi
done

preview_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "template_id":"fact_summary_draft",
      "case_id":"case_v55_approve_all",
      "variables":{"case_type":"civil","task":"fact summary"},
      "manual_review_confirmed":true,
      "mock_data_only_confirmation":true,
      "no_raw_content_confirmation":true
    }' \
    "${API_BASE}/personal-ai-gateway/prompt-render-preview"
)"
assert_metadata_safe "${preview_body}" "prompt-render-preview"
assert_field_false_required "${preview_body}" "prompt-render-preview" "would_call_provider"
assert_field_false_required "${preview_body}" "prompt-render-preview" "raw_content_included"
assert_field_false_required "${preview_body}" "prompt-render-preview" "final_legal_opinion_generated"
assert_field_false_required "${preview_body}" "prompt-render-preview" "final_report_generated"
if ! printf '%s' "${preview_body}" | grep -Eq '"draft_only"[[:space:]]*:[[:space:]]*true'; then
  fail "prompt-render-preview expected draft_only=true"
fi
if ! printf '%s' "${preview_body}" | grep -Eq '"requires_lawyer_review"[[:space:]]*:[[:space:]]*true'; then
  fail "prompt-render-preview expected requires_lawyer_review=true"
fi

run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"openai_provider",
      "template_id":"fact_summary_draft",
      "case_id":"case_v55_approve_all",
      "manual_approval_confirmed":true,
      "lawyer_review_required_confirmation":true,
      "draft_only_confirmation":true,
      "source_trace_required_confirmation":true,
      "no_final_legal_opinion_confirmation":true,
      "no_final_report_generation_confirmation":true
    }' \
    "${API_BASE}/personal-ai-gateway/runs/mock"
)"
assert_metadata_safe "${run_body}" "runs/mock"
assert_field_false_required "${run_body}" "runs/mock" "would_call_provider"
assert_field_false_required "${run_body}" "runs/mock" "live_call_executed"
assert_field_false_required "${run_body}" "runs/mock" "raw_content_included"
assert_field_false_required "${run_body}" "runs/mock" "final_legal_opinion_generated"
assert_field_false_required "${run_body}" "runs/mock" "final_report_generated"
if ! printf '%s' "${run_body}" | grep -Eq '"draft_only"[[:space:]]*:[[:space:]]*true'; then
  fail "runs/mock expected draft_only=true"
fi
if ! printf '%s' "${run_body}" | grep -Eq '"requires_lawyer_review"[[:space:]]*:[[:space:]]*true'; then
  fail "runs/mock expected requires_lawyer_review=true"
fi

runs_body="$(check_endpoint_200 "/personal-ai-gateway/runs")"
audit_body="$(check_endpoint_200 "/personal-ai-gateway/audit")"
assert_metadata_safe "${runs_body}" "/personal-ai-gateway/runs"
assert_metadata_safe "${audit_body}" "/personal-ai-gateway/audit"

pass "personal AI gateway APIs"
