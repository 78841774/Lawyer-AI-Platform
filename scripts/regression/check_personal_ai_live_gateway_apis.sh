#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal AI Live Gateway APIs v7.12"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_ai_gateway/live"

assert_ai_live_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'OPENAI_API_KEY'
  assert_absent "${body}" "${label}" 'DEEPSEEK_API_KEY'
  assert_absent "${body}" "${label}" 'BEGIN PRIVATE KEY'
  assert_absent "${body}" "${label}" 'sk-[A-Za-z0-9_-]+'
  assert_field_false_if_present "${body}" "${label}" "api_key_exposed"
  assert_field_false_if_present "${body}" "${label}" "live_call_executed"
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
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
  "/personal-ai-gateway/live/status" \
  "/personal-ai-gateway/live/providers" \
  "/personal-ai-gateway/live/providers/openai" \
  "/personal-ai-gateway/live/runs" \
  "/personal-ai-gateway/live/audit" \
  "/personal-ai-gateway/live/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_ai_live_safe "${body}" "${endpoint}"
done

dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"openai",
      "model":"gpt-4.1-mini",
      "prompt_template_id":"fact_summary_draft",
      "prompt_purpose":"fact_summary_draft",
      "case_id":"case_v55_approve_all",
      "source_trace_ids":["trace_ai_live_demo"],
      "dry_run":true,
      "actor_id":"local_demo_lawyer",
      "explicit_live_confirmation":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false,
      "no_final_opinion_acknowledged":false,
      "no_final_report_acknowledged":false,
      "no_external_delivery_acknowledged":false,
      "raw_content_included":false,
      "final_legal_opinion_requested":false,
      "final_report_requested":false
    }' \
    "${API_BASE}/personal-ai-gateway/live/dry-run"
)"
assert_ai_live_safe "${dry_run_body}" "live/dry-run"
require_true_field "${dry_run_body}" "live/dry-run" "dry_run"
require_true_field "${dry_run_body}" "live/dry-run" "draft_only"
require_true_field "${dry_run_body}" "live/dry-run" "lawyer_review_required"
require_true_field "${dry_run_body}" "live/dry-run" "source_trace_required"
if ! printf '%s' "${dry_run_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"dry_run_completed"'; then
  fail "live/dry-run expected dry_run_completed"
fi

blocked_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"openai",
      "model":"gpt-4.1-mini",
      "prompt_template_id":"fact_summary_draft",
      "prompt_purpose":"fact_summary_draft",
      "case_id":"case_v55_approve_all",
      "source_trace_ids":["trace_ai_live_demo"],
      "dry_run":false,
      "actor_id":"local_demo_lawyer",
      "explicit_live_confirmation":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false,
      "no_final_opinion_acknowledged":false,
      "no_final_report_acknowledged":false,
      "no_external_delivery_acknowledged":false,
      "raw_content_included":false,
      "final_legal_opinion_requested":false,
      "final_report_requested":false
    }' \
    "${API_BASE}/personal-ai-gateway/live/runs"
)"
assert_ai_live_safe "${blocked_body}" "live/runs blocked"
if ! printf '%s' "${blocked_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"live_call_blocked"'; then
  fail "live/runs without confirmations must be live_call_blocked"
fi
assert_field_false_required "${blocked_body}" "live/runs blocked" "live_call_executed"

audit_body="$(check_endpoint_200 "/personal-ai-gateway/live/audit")"
assert_ai_live_safe "${audit_body}" "live/audit after runs"
if ! printf '%s' "${audit_body}" | grep -Eq '"event_count"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "live/audit expected at least one audit event"
fi

pass "personal AI live gateway APIs v7.12"
