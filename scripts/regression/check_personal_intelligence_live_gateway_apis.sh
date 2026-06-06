#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Intelligence Live Gateway APIs v7.14"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_intelligence_gateway/live"

assert_intelligence_live_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" 'raw_legal_content[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'raw_enterprise_content[[:space:]]*[:=]'
  assert_field_false_if_present "${body}" "${label}" "api_key_exposed"
  assert_field_false_if_present "${body}" "${label}" "live_call_executed"
  assert_field_false_if_present "${body}" "${label}" "raw_content_exposed"
  assert_field_false_if_present "${body}" "${label}" "legal_raw_content_exposed"
  assert_field_false_if_present "${body}" "${label}" "enterprise_raw_content_exposed"
  assert_field_false_if_present "${body}" "${label}" "ai_prompt_injected"
  assert_field_false_if_present "${body}" "${label}" "fact_extraction_triggered"
  assert_field_false_if_present "${body}" "${label}" "legal_analysis_triggered"
  assert_field_false_if_present "${body}" "${label}" "citation_finalized"
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
  "/personal-intelligence/live/status" \
  "/personal-intelligence/live/providers" \
  "/personal-intelligence/live/providers/kuaicha365_lawskills_provider" \
  "/personal-intelligence/live/legal-search/runs" \
  "/personal-intelligence/live/enterprise-query/runs" \
  "/personal-intelligence/live/review-queue" \
  "/personal-intelligence/live/source-traces" \
  "/personal-intelligence/live/audit" \
  "/personal-intelligence/live/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_intelligence_live_safe "${body}" "${endpoint}"
done

legal_dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"kuaicha365_lawskills_provider",
      "query_text":"买卖合同逾期付款责任",
      "query_type":"case_law_search",
      "case_id":"case_v55_approve_all",
      "jurisdiction":"中国大陆",
      "actor_id":"local_demo_lawyer",
      "dry_run":true,
      "explicit_live_confirmation":false,
      "query_owner_confirmation":false,
      "raw_content_handling_acknowledged":false,
      "no_ai_prompt_injection_acknowledged":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false,
      "no_final_citation_acknowledged":false
    }' \
    "${API_BASE}/personal-intelligence/live/legal-search/dry-run"
)"
assert_intelligence_live_safe "${legal_dry_run_body}" "legal dry-run"
require_true_field "${legal_dry_run_body}" "legal dry-run" "dry_run"
require_true_field "${legal_dry_run_body}" "legal dry-run" "query_metadata_only"
require_true_field "${legal_dry_run_body}" "legal dry-run" "citation_metadata_only"
require_true_field "${legal_dry_run_body}" "legal dry-run" "source_trace_required"
require_true_field "${legal_dry_run_body}" "legal dry-run" "lawyer_review_required"

enterprise_dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"tianyancha_ai_provider",
      "query_text":"示例科技有限公司",
      "query_type":"judicial_risk_preview",
      "case_id":"case_v55_approve_all",
      "jurisdiction":"中国大陆",
      "actor_id":"local_demo_lawyer",
      "dry_run":true,
      "explicit_live_confirmation":false,
      "query_owner_confirmation":false,
      "raw_content_handling_acknowledged":false,
      "no_ai_prompt_injection_acknowledged":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false,
      "no_final_citation_acknowledged":false
    }' \
    "${API_BASE}/personal-intelligence/live/enterprise-query/dry-run"
)"
assert_intelligence_live_safe "${enterprise_dry_run_body}" "enterprise dry-run"
require_true_field "${enterprise_dry_run_body}" "enterprise dry-run" "dry_run"
require_true_field "${enterprise_dry_run_body}" "enterprise dry-run" "query_metadata_only"
require_true_field "${enterprise_dry_run_body}" "enterprise dry-run" "source_trace_required"
require_true_field "${enterprise_dry_run_body}" "enterprise dry-run" "lawyer_review_required"

blocked_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"kuaicha365_lawskills_provider",
      "query_text":"买卖合同逾期付款责任",
      "query_type":"case_law_search",
      "case_id":"case_v55_approve_all",
      "jurisdiction":"中国大陆",
      "actor_id":"local_demo_lawyer",
      "dry_run":false,
      "explicit_live_confirmation":false,
      "query_owner_confirmation":false,
      "raw_content_handling_acknowledged":false,
      "no_ai_prompt_injection_acknowledged":false,
      "lawyer_review_acknowledged":false,
      "draft_only_acknowledged":false,
      "no_final_citation_acknowledged":false
    }' \
    "${API_BASE}/personal-intelligence/live/legal-search/runs"
)"
assert_intelligence_live_safe "${blocked_body}" "legal live blocked"
if ! printf '%s' "${blocked_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"live_call_blocked"'; then
  fail "legal live run without confirmations must be live_call_blocked"
fi
assert_field_false_required "${blocked_body}" "legal live blocked" "live_call_executed"

review_queue_body="$(check_endpoint_200 "/personal-intelligence/live/review-queue")"
assert_intelligence_live_safe "${review_queue_body}" "live review queue"
if ! printf '%s' "${review_queue_body}" | grep -Eq '"item_count"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "live review queue expected metadata item"
fi

source_trace_body="$(check_endpoint_200 "/personal-intelligence/live/source-traces")"
assert_intelligence_live_safe "${source_trace_body}" "live source traces"
if ! printf '%s' "${source_trace_body}" | grep -Eq '"source_trace_count"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "live source traces expected metadata item"
fi

audit_body="$(check_endpoint_200 "/personal-intelligence/live/audit")"
assert_intelligence_live_safe "${audit_body}" "live audit after runs"
if ! printf '%s' "${audit_body}" | grep -Eq '"event_count"[[:space:]]*:[[:space:]]*[1-9]'; then
  fail "live audit expected at least one audit event"
fi

pass "personal intelligence live gateway APIs v7.14"
