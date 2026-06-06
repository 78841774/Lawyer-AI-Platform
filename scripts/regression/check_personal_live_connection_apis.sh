#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Live Connection APIs v7.28"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_live_connection"

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

assert_live_connection_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR 原文|真实案件原文|raw provider response|客户姓名|身份证号|手机号'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "dry_run"
  require_true_field "${body}" "${label}" "provider_gated"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "live_default_enabled"
  require_false_field "${body}" "${label}" "live_call_executed"
  require_false_field "${body}" "${label}" "network_call_executed"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "secret_value_returned"
  require_false_field "${body}" "${label}" "secret_logged"
  require_false_field "${body}" "${label}" "frontend_key_input_enabled"
  require_false_field "${body}" "${label}" "raw_content_exposed"
  require_false_field "${body}" "${label}" "raw_provider_response_exposed"
  require_false_field "${body}" "${label}" "local_path_exposed"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "real_pdf_generated"
  require_false_field "${body}" "${label}" "real_docx_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

for endpoint in \
  "/personal-live-connection/status" \
  "/personal-live-connection/runtimes" \
  "/personal-live-connection/providers" \
  "/personal-live-connection/runs" \
  "/personal-live-connection/audit" \
  "/personal-live-connection/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_live_connection_safe "${body}" "${endpoint}"
done

providers_body="$(check_endpoint_200 "/personal-live-connection/providers")"
provider_id="$(printf '%s' "${providers_body}" | sed -n 's/.*"provider_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${provider_id}" ]; then
  fail "providers did not return provider_id"
fi

for endpoint in \
  "/personal-live-connection/providers/${provider_id}" \
  "/personal-live-connection/providers/${provider_id}/secret-boundary" \
  "/personal-live-connection/providers/${provider_id}/live-gate" \
  "/personal-live-connection/providers/${provider_id}/usage-policy" \
  "/personal-live-connection/providers/${provider_id}/health/dry-run"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_live_connection_safe "${body}" "${endpoint}"
done

dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"provider_id\":\"${provider_id}\",
      \"run_type\":\"controlled_provider_readiness\",
      \"case_id\":\"case_v55_approve_all\",
      \"material_id\":\"material_demo_001\",
      \"query_purpose\":\"regression_dry_run\",
      \"dry_run\":true,
      \"manual_confirmation\":false,
      \"owner_confirmation\":false,
      \"lawyer_gate_acknowledged\":false,
      \"source_trace_acknowledged\":true,
      \"raw_content_boundary_acknowledged\":true,
      \"draft_only_acknowledged\":true
    }" \
    "${API_BASE}/personal-live-connection/runs/dry-run"
)"
assert_live_connection_safe "${dry_run_body}" "runs/dry-run"
require_true_field "${dry_run_body}" "runs/dry-run" "quality_reference_only"

run_id="$(printf '%s' "${dry_run_body}" | sed -n 's/.*"run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${run_id}" ]; then
  fail "runs/dry-run did not return run_id"
fi

detail_body="$(check_endpoint_200 "/personal-live-connection/runs/${run_id}")"
assert_live_connection_safe "${detail_body}" "run detail"

blocked_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"provider_id\":\"${provider_id}\",
      \"run_type\":\"controlled_provider_readiness\",
      \"case_id\":\"case_v55_approve_all\",
      \"query_purpose\":\"regression_blocked_live\",
      \"dry_run\":false,
      \"manual_confirmation\":false,
      \"owner_confirmation\":false,
      \"lawyer_gate_acknowledged\":false,
      \"source_trace_acknowledged\":false,
      \"raw_content_boundary_acknowledged\":false,
      \"draft_only_acknowledged\":false
    }" \
    "${API_BASE}/personal-live-connection/runs"
)"
assert_live_connection_safe "${blocked_body}" "runs live blocked"
if ! printf '%s' "${blocked_body}" | grep -Eq '"status"[[:space:]]*:[[:space:]]*"live_call_blocked"'; then
  fail "runs live blocked expected live_call_blocked"
fi

pass "personal live connection APIs v7.28"

