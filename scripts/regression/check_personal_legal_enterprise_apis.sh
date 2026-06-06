#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Legal / Enterprise API Live Connection v7.29"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_legal_enterprise_gateway"

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

assert_legal_enterprise_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR 原文|真实案件原文|raw provider response|客户姓名|身份证号|手机号'
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "dry_run"
  require_true_field "${body}" "${label}" "provider_gated"
  require_true_field "${body}" "${label}" "owner_confirmation_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "review_required"
  require_false_field "${body}" "${label}" "live_default_enabled"
  require_false_field "${body}" "${label}" "live_call_allowed"
  require_false_field "${body}" "${label}" "live_call_executed"
  require_false_field "${body}" "${label}" "network_call_executed"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "secret_value_returned"
  require_false_field "${body}" "${label}" "secret_logged"
  require_false_field "${body}" "${label}" "frontend_key_input_enabled"
  require_false_field "${body}" "${label}" "external_transfer_triggered"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "final_fact_finding"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "third_party_share_enabled"
  require_false_field "${body}" "${label}" "client_auto_delivery"
}

for endpoint in \
  "/personal-legal-enterprise/status" \
  "/personal-legal-enterprise/providers" \
  "/personal-legal-enterprise/categories" \
  "/personal-legal-enterprise/live-gates" \
  "/personal-legal-enterprise/legal-search/runs" \
  "/personal-legal-enterprise/enterprise-lookup/runs" \
  "/personal-legal-enterprise/review-queue" \
  "/personal-legal-enterprise/source-traces" \
  "/personal-legal-enterprise/audit" \
  "/personal-legal-enterprise/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_legal_enterprise_safe "${body}" "${endpoint}"
done

providers_body="$(check_endpoint_200 "/personal-legal-enterprise/providers")"
provider_id="$(printf '%s' "${providers_body}" | sed -n 's/.*"provider_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${provider_id}" ]; then
  fail "providers did not return provider_id"
fi

for endpoint in \
  "/personal-legal-enterprise/providers/${provider_id}" \
  "/personal-legal-enterprise/providers/${provider_id}/secret-boundary" \
  "/personal-legal-enterprise/providers/${provider_id}/live-gate" \
  "/personal-legal-enterprise/providers/${provider_id}/usage-policy" \
  "/personal-legal-enterprise/providers/${provider_id}/health/dry-run" \
  "/personal-legal-enterprise/categories/legal/providers" \
  "/personal-legal-enterprise/categories/enterprise/providers"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_legal_enterprise_safe "${body}" "${endpoint}"
done

gate_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"provider_id\":\"${provider_id}\",
      \"dry_run\":true,
      \"explicit_live_confirmation\":false,
      \"owner_authorized\":false,
      \"lawyer_review_acknowledged\":false,
      \"external_transfer_acknowledged\":false,
      \"source_trace_acknowledged\":true,
      \"no_training_use_acknowledged\":true,
      \"audit_acknowledged\":true
    }" \
    "${API_BASE}/personal-legal-enterprise/live-gates/mock"
)"
assert_legal_enterprise_safe "${gate_body}" "live-gates/mock"

legal_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"legal_search_placeholder",
      "query_type":"claim_basis_search",
      "query_text_metadata":"请求权基础检索 metadata",
      "case_id":"case_v55_approve_all",
      "dry_run":true,
      "source_trace_acknowledged":true,
      "no_training_use_acknowledged":true,
      "audit_acknowledged":true
    }' \
    "${API_BASE}/personal-legal-enterprise/legal-search/dry-run"
)"
assert_legal_enterprise_safe "${legal_body}" "legal-search/dry-run"
require_false_field "${legal_body}" "legal-search/dry-run" "final_citation_selected"

enterprise_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "provider_id":"enterprise_registry_placeholder",
      "lookup_type":"company_registry",
      "company_query_metadata":"企业主体核验 metadata",
      "case_id":"case_v55_approve_all",
      "dry_run":true,
      "source_trace_acknowledged":true,
      "no_training_use_acknowledged":true,
      "audit_acknowledged":true
    }' \
    "${API_BASE}/personal-legal-enterprise/enterprise-lookup/dry-run"
)"
assert_legal_enterprise_safe "${enterprise_body}" "enterprise-lookup/dry-run"
require_false_field "${enterprise_body}" "enterprise-lookup/dry-run" "final_fact_finding"

pass "personal legal / enterprise API live connection v7.29"

