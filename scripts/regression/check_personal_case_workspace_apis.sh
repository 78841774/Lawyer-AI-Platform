#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Case Workspace APIs v7.18"
cd "${REPO_ROOT}"

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

assert_case_workspace_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" 'local\.db|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" '身份证号|银行卡号|手机号|客户姓名|真实判决|真实企业信息'
  assert_field_false_if_present "${body}" "${label}" "public_link_created"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "third_party_share_enabled"
  assert_field_false_if_present "${body}" "${label}" "client_auto_delivery"
  assert_field_false_if_present "${body}" "${label}" "training_data_generated"
  assert_field_false_if_present "${body}" "${label}" "writes_to_training_set"
  assert_field_false_if_present "${body}" "${label}" "skill_updated"
  assert_field_false_if_present "${body}" "${label}" "skill_published"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_git"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_docs"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_diagnostics"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_regression_output"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "local_path_visible"
  assert_field_false_if_present "${body}" "${label}" "api_key_exposed"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "real_pdf_docx_generated"
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "owner_access_required"
  require_true_field "${body}" "${label}" "downloadable_by_owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
}

for endpoint in \
  "/personal-case-workspace/status" \
  "/personal-case-workspace/cases" \
  "/personal-case-workspace/source-traces" \
  "/personal-case-workspace/audit" \
  "/personal-case-workspace/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_case_workspace_safe "${body}" "${endpoint}"
done

case_body="$(check_endpoint_200 "/personal-case-workspace/cases")"
case_id="$(printf '%s' "${case_body}" | sed -n 's/.*"case_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${case_id}" ]; then
  fail "cases did not return case_id"
fi

for endpoint in \
  "/personal-case-workspace/cases/${case_id}" \
  "/personal-case-workspace/cases/${case_id}/materials"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_case_workspace_safe "${body}" "${endpoint}"
done

materials_body="$(check_endpoint_200 "/personal-case-workspace/cases/${case_id}/materials")"
material_id="$(printf '%s' "${materials_body}" | sed -n 's/.*"material_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${material_id}" ]; then
  fail "materials did not return material_id"
fi

for endpoint in \
  "/personal-case-workspace/materials/${material_id}" \
  "/personal-case-workspace/materials/${material_id}/ocr-status" \
  "/personal-case-workspace/materials/${material_id}/source-traces" \
  "/personal-case-workspace/materials/${material_id}/fact-input"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_case_workspace_safe "${body}" "${endpoint}"
done

owner_raw_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "explicit_owner_confirmation":true,
      "explicit_no_external_delivery_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_ai_prompt_confirmation":true
    }' \
    "${API_BASE}/personal-case-workspace/materials/${material_id}/owner-raw-view"
)"
assert_case_workspace_safe "${owner_raw_body}" "owner-raw-view"
assert_field_false_if_present "${owner_raw_body}" "owner-raw-view" "raw_content_loaded"
assert_field_false_if_present "${owner_raw_body}" "owner-raw-view" "raw_content_included_in_prompt"

correction_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "correction_note":"仅更新事实输入纠正 metadata",
      "explicit_owner_confirmation":true,
      "explicit_lawyer_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-case-workspace/materials/${material_id}/fact-input/corrections/mock"
)"
assert_case_workspace_safe "${correction_body}" "fact correction"

pass "personal case workspace APIs v7.18"
