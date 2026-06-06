#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Provider Live Readiness & Secret Boundary APIs v7.26"
cd "${REPO_ROOT}"

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

assert_provider_readiness_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR 原文|真实案件原文|真实案件材料|客户姓名|身份证号|手机号|银行卡号'
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "dry_run"
  require_true_field "${body}" "${label}" "provider_gated"
  require_true_field "${body}" "${label}" "owner_confirmation_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "live_default_enabled"
  require_false_field "${body}" "${label}" "live_call_allowed"
  require_false_field "${body}" "${label}" "live_call_executed"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "secret_value_returned"
  require_false_field "${body}" "${label}" "secret_logged"
  require_false_field "${body}" "${label}" "frontend_key_input_enabled"
  require_false_field "${body}" "${label}" "external_transfer_triggered"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

for endpoint in \
  "/personal-provider-readiness/status" \
  "/personal-provider-readiness/providers" \
  "/personal-provider-readiness/categories" \
  "/personal-provider-readiness/live-gates" \
  "/personal-provider-readiness/audit" \
  "/personal-provider-readiness/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_provider_readiness_safe "${body}" "${endpoint}"
done

providers_body="$(check_endpoint_200 "/personal-provider-readiness/providers")"
assert_provider_readiness_safe "${providers_body}" "/personal-provider-readiness/providers"
provider_id="$(printf '%s' "${providers_body}" | sed -n 's/.*"provider_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${provider_id}" ]; then
  fail "providers did not return provider_id"
fi

for endpoint in \
  "/personal-provider-readiness/providers/${provider_id}" \
  "/personal-provider-readiness/providers/${provider_id}/secret-boundary" \
  "/personal-provider-readiness/providers/${provider_id}/live-gate" \
  "/personal-provider-readiness/providers/${provider_id}/usage-policy" \
  "/personal-provider-readiness/providers/${provider_id}/health/dry-run"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_provider_readiness_safe "${body}" "${endpoint}"
done

secret_body="$(check_endpoint_200 "/personal-provider-readiness/providers/${provider_id}/secret-boundary")"
assert_provider_readiness_safe "${secret_body}" "secret boundary"
require_false_field "${secret_body}" "secret boundary" "key_value_exposed"
require_false_field "${secret_body}" "secret boundary" "key_prefix_returned"
require_false_field "${secret_body}" "secret boundary" "key_suffix_returned"
require_false_field "${secret_body}" "secret boundary" "masked_key_returned"
require_false_field "${secret_body}" "secret boundary" "token_value_returned"
require_false_field "${secret_body}" "secret boundary" "secret_value_stored"

for category in ai ocr document legal enterprise; do
  body="$(check_endpoint_200 "/personal-provider-readiness/categories/${category}/providers")"
  assert_provider_readiness_safe "${body}" "/personal-provider-readiness/categories/${category}/providers"
done

gate_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"provider_id\":\"${provider_id}\",
      \"explicit_live_confirmation\":false,
      \"owner_authorized\":false,
      \"external_transfer_acknowledged\":false,
      \"no_training_use_acknowledged\":true,
      \"audit_acknowledged\":true
    }" \
    "${API_BASE}/personal-provider-readiness/live-gates/mock"
)"
assert_provider_readiness_safe "${gate_body}" "live-gates/mock"
require_false_field "${gate_body}" "live-gates/mock" "global_live_enabled"
require_false_field "${gate_body}" "live-gates/mock" "provider_live_enabled"
require_false_field "${gate_body}" "live-gates/mock" "live_call_allowed"
require_false_field "${gate_body}" "live-gates/mock" "live_call_executed"

health_body="$(check_endpoint_200 "/personal-provider-readiness/providers/${provider_id}/health/dry-run")"
assert_provider_readiness_safe "${health_body}" "health dry-run"
require_false_field "${health_body}" "health dry-run" "network_call_executed"

pass "personal provider live readiness APIs v7.26"

