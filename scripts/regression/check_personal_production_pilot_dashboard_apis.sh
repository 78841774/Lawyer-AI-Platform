#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Production Pilot Dashboard APIs v7.19"
cd "${REPO_ROOT}"

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

assert_pilot_dashboard_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" 'local\.db|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" '自动胜诉|替代律师|保证准确|自动出具最终法律意见|自动完成客户交付|一键交付|全自动办案|自动发送客户|智能判案|包赢|无需律师'
  assert_field_false_if_present "${body}" "${label}" "public_link_created"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "third_party_share_enabled"
  assert_field_false_if_present "${body}" "${label}" "client_auto_delivery"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_auto_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_auto_generated"
  assert_field_false_if_present "${body}" "${label}" "real_pdf_docx_generated"
  assert_field_false_if_present "${body}" "${label}" "training_data_generated"
  assert_field_false_if_present "${body}" "${label}" "writes_to_training_set"
  assert_field_false_if_present "${body}" "${label}" "skill_updated"
  assert_field_false_if_present "${body}" "${label}" "skill_published"
  assert_field_false_if_present "${body}" "${label}" "api_key_exposed"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_git"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_docs"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_diagnostics"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_regression_output"
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "owner_access_required"
  require_true_field "${body}" "${label}" "downloadable_by_owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "audit_required"
}

for endpoint in \
  "/personal-production-pilot/dashboard/status" \
  "/personal-production-pilot/dashboard/metrics" \
  "/personal-production-pilot/dashboard/quality" \
  "/personal-production-pilot/dashboard/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_pilot_dashboard_safe "${body}" "${endpoint}"
done

quality_body="$(check_endpoint_200 "/personal-production-pilot/dashboard/quality")"
assert_absent "${quality_body}" "dashboard quality" '"quality_score"[[:space:]]*:[[:space:]]*0'
if ! printf '%s' "${quality_body}" | grep -Eq '"optimization_suggestions"[[:space:]]*:'; then
  fail "dashboard quality missing optimization_suggestions"
fi
if ! printf '%s' "${quality_body}" | grep -Eq '"gate_reference_only"[[:space:]]*:[[:space:]]*true'; then
  fail "dashboard quality expected gate_reference_only=true"
fi

safety_body="$(check_endpoint_200 "/personal-production-pilot/dashboard/safety")"
if ! printf '%s' "${safety_body}" | grep -Eq '"safety_item_count"[[:space:]]*:[[:space:]]*12'; then
  fail "dashboard safety expected 12 safety items"
fi

pass "personal production pilot dashboard APIs v7.19"
