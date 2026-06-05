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

expect_request_failure() {
  local label="$1"
  local endpoint="$2"
  local payload="$3"
  local status
  status="$(
    curl -sS -o /tmp/personal_intelligence_regression_error.json -w "%{http_code}" \
      -H "Content-Type: application/json" \
      -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
      -d "${payload}" \
      "${API_BASE}${endpoint}"
  )"
  if [ "${status}" -lt 400 ]; then
    fail "${label} expected failure status, got ${status}"
  fi
  pass "${label} returned ${status}"
}

assert_intelligence_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" '自动胜诉'
  assert_absent "${body}" "${label}" '替代律师'
  assert_absent "${body}" "${label}" '保证准确'
  assert_absent "${body}" "${label}" 'raw_external_content[[:space:]]*:[[:space:]]*true'
  assert_absent "${body}" "${label}" 'full_text[[:space:]]*:'
  assert_field_false_if_present "${body}" "${label}" "live_call_executed"
  assert_field_false_if_present "${body}" "${label}" "raw_external_content_included"
  assert_field_false_if_present "${body}" "${label}" "raw_external_content_returned"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "used_in_ai_prompt"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
}

section "Personal Intelligence Gateway APIs"

endpoints=(
  "/personal-intelligence/status"
  "/personal-intelligence/providers"
  "/personal-intelligence/providers/kuaicha365_lawskills_provider"
  "/personal-intelligence/providers/tianyancha_ai_provider"
  "/personal-intelligence/safety"
  "/personal-intelligence/legal-search"
  "/personal-intelligence/enterprise-query"
  "/personal-intelligence/source-traces"
  "/personal-intelligence/confirmation-queue"
  "/personal-intelligence/audit"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_intelligence_safe "${body}" "${endpoint}"
done

legal_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_v55_approve_all",
      "query":"买卖合同逾期付款责任",
      "search_scope":"case_law_search",
      "jurisdiction":"中国大陆",
      "legal_area":"合同纠纷",
      "provider_id":"kuaicha365_lawskills_provider",
      "explicit_mock_confirmation":true,
      "explicit_no_live_call_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-intelligence/legal-search/mock"
)"
assert_intelligence_safe "${legal_body}" "legal-search/mock"
assert_field_false_required "${legal_body}" "legal-search/mock" "live_call_executed"
assert_field_false_required "${legal_body}" "legal-search/mock" "raw_external_content_included"
assert_field_false_required "${legal_body}" "legal-search/mock" "used_in_ai_prompt"
assert_field_false_required "${legal_body}" "legal-search/mock" "final_legal_opinion_generated"
assert_field_false_required "${legal_body}" "legal-search/mock" "final_report_generated"
require_true_field "${legal_body}" "legal-search/mock" "requires_lawyer_confirmation"
require_true_field "${legal_body}" "legal-search/mock" "source_trace_required"

legal_search_id="$(printf '%s' "${legal_body}" | sed -n 's/.*"legal_search_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
legal_trace_id="$(printf '%s' "${legal_body}" | sed -n 's/.*"source_trace_ids"[[:space:]]*:[[:space:]]*\["\([^"]*\)".*/\1/p')"
if [ -z "${legal_search_id}" ] || [ -z "${legal_trace_id}" ]; then
  fail "legal-search/mock did not return ids"
fi

legal_detail="$(check_endpoint_200 "/personal-intelligence/legal-search/${legal_search_id}")"
trace_detail="$(check_endpoint_200 "/personal-intelligence/source-traces/${legal_trace_id}")"
assert_intelligence_safe "${legal_detail}" "legal-search detail"
assert_intelligence_safe "${trace_detail}" "source trace detail"

expect_request_failure "legal-search missing confirmation" "/personal-intelligence/legal-search/mock" '{
  "case_id":"case_v55_approve_all",
  "query":"买卖合同逾期付款责任",
  "search_scope":"case_law_search",
  "jurisdiction":"中国大陆",
  "legal_area":"合同纠纷",
  "provider_id":"kuaicha365_lawskills_provider"
}'

enterprise_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_v55_approve_all",
      "company_name":"示例科技有限公司",
      "unified_social_credit_code":null,
      "query_scope":"judicial_risk_preview",
      "provider_id":"tianyancha_ai_provider",
      "explicit_mock_confirmation":true,
      "explicit_no_live_call_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-intelligence/enterprise-query/mock"
)"
assert_intelligence_safe "${enterprise_body}" "enterprise-query/mock"
assert_field_false_required "${enterprise_body}" "enterprise-query/mock" "live_call_executed"
assert_field_false_required "${enterprise_body}" "enterprise-query/mock" "raw_external_content_included"
assert_field_false_required "${enterprise_body}" "enterprise-query/mock" "used_in_ai_prompt"
assert_field_false_required "${enterprise_body}" "enterprise-query/mock" "final_legal_opinion_generated"
assert_field_false_required "${enterprise_body}" "enterprise-query/mock" "final_report_generated"
require_true_field "${enterprise_body}" "enterprise-query/mock" "requires_lawyer_confirmation"
require_true_field "${enterprise_body}" "enterprise-query/mock" "source_trace_required"

enterprise_query_id="$(printf '%s' "${enterprise_body}" | sed -n 's/.*"enterprise_query_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${enterprise_query_id}" ]; then
  fail "enterprise-query/mock did not return enterprise_query_id"
fi

enterprise_detail="$(check_endpoint_200 "/personal-intelligence/enterprise-query/${enterprise_query_id}")"
assert_intelligence_safe "${enterprise_detail}" "enterprise-query detail"

expect_request_failure "enterprise-query missing confirmation" "/personal-intelligence/enterprise-query/mock" '{
  "case_id":"case_v55_approve_all",
  "company_name":"示例科技有限公司",
  "query_scope":"judicial_risk_preview",
  "provider_id":"tianyancha_ai_provider"
}'

confirmation_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"confirm",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"metadata only",
      "explicit_lawyer_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-intelligence/confirmation-queue/${legal_trace_id}/actions"
)"
assert_intelligence_safe "${confirmation_body}" "confirmation action"
assert_field_false_required "${confirmation_body}" "confirmation action" "live_call_executed"
assert_field_false_required "${confirmation_body}" "confirmation action" "raw_content_returned"
assert_field_false_required "${confirmation_body}" "confirmation action" "used_in_ai_prompt"
assert_field_false_required "${confirmation_body}" "confirmation action" "final_legal_opinion_generated"
assert_field_false_required "${confirmation_body}" "confirmation action" "final_report_generated"

expect_request_failure "confirmation invalid action" "/personal-intelligence/confirmation-queue/${legal_trace_id}/actions" '{
  "action":"invalid_action",
  "reviewer_id":"local_demo_lawyer",
  "explicit_lawyer_confirmation":true,
  "explicit_no_final_opinion_confirmation":true
}'

queue_body="$(check_endpoint_200 "/personal-intelligence/confirmation-queue")"
traces_body="$(check_endpoint_200 "/personal-intelligence/source-traces")"
audit_body="$(check_endpoint_200 "/personal-intelligence/audit")"
assert_intelligence_safe "${queue_body}" "confirmation queue"
assert_intelligence_safe "${traces_body}" "source-traces"
assert_intelligence_safe "${audit_body}" "audit"

pass "personal intelligence gateway APIs"
