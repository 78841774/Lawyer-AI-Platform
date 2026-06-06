#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Fact Preview & Correction APIs v7.20"
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

assert_fact_correction_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'OPENAI_API_KEY|DEEPSEEK|API_KEY[[:space:]]*[:=]|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" 'local\.db|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" '真实客户|真实案件|真实判决|真实企业信息|身份证号|银行卡号|手机号|客户姓名'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "owner_access_required"
  require_true_field "${body}" "${label}" "downloadable_by_owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "correction_allowed"
  require_true_field "${body}" "${label}" "owner_correction_allowed"
  require_true_field "${body}" "${label}" "legal_analysis_input_allowed"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_false_field "${body}" "${label}" "legal_analysis_auto_triggered"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "blocks_next_stage"
  require_false_field "${body}" "${label}" "final_fact_finding"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "real_pdf_docx_generated"
  require_false_field "${body}" "${label}" "raw_content_returned"
  require_false_field "${body}" "${label}" "local_path_visible"
  require_false_field "${body}" "${label}" "api_key_exposed"
}

for endpoint in \
  "/personal-case-workspace/fact-previews" \
  "/personal-case-workspace/fact-input-readiness" \
  "/personal-case-workspace/fact-audit" \
  "/personal-case-workspace/fact-safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_fact_correction_safe "${body}" "${endpoint}"
done

preview_list_body="$(check_endpoint_200 "/personal-case-workspace/fact-previews")"
fact_preview_id="$(printf '%s' "${preview_list_body}" | sed -n 's/.*"fact_preview_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${fact_preview_id}" ]; then
  fail "fact-previews did not return fact_preview_id"
fi

for endpoint in \
  "/personal-case-workspace/fact-previews/${fact_preview_id}" \
  "/personal-case-workspace/fact-previews/${fact_preview_id}/corrections" \
  "/personal-case-workspace/fact-previews/${fact_preview_id}/versions" \
  "/personal-case-workspace/fact-previews/${fact_preview_id}/quality" \
  "/personal-case-workspace/fact-previews/${fact_preview_id}/gate" \
  "/personal-case-workspace/fact-previews/${fact_preview_id}/source-traces"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_fact_correction_safe "${body}" "${endpoint}"
done

created_preview_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_workspace_mock_001",
      "material_ids":["material_contract_metadata_001"],
      "explicit_owner_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_auto_legal_analysis_confirmation":true
    }' \
    "${API_BASE}/personal-case-workspace/fact-previews/mock"
)"
assert_fact_correction_safe "${created_preview_body}" "create fact preview"
created_preview_id="$(printf '%s' "${created_preview_body}" | sed -n 's/.*"fact_preview_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${created_preview_id}" ]; then
  fail "created fact preview did not return fact_preview_id"
fi

correction_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "corrected_sections":["fact_summary_draft","timeline_draft"],
      "correction_reason":"用户本人纠正事实输入 metadata",
      "correction_type":"owner_fact_correction",
      "explicit_owner_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_skill_update_confirmation":true,
      "explicit_no_auto_legal_analysis_confirmation":true
    }' \
    "${API_BASE}/personal-case-workspace/fact-previews/${created_preview_id}/corrections/mock"
)"
assert_fact_correction_safe "${correction_body}" "create fact correction"
correction_id="$(printf '%s' "${correction_body}" | sed -n 's/.*"correction_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${correction_id}" ]; then
  fail "created correction did not return correction_id"
fi

correction_detail_body="$(check_endpoint_200 "/personal-case-workspace/fact-corrections/${correction_id}")"
assert_fact_correction_safe "${correction_detail_body}" "fact correction detail"

version_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "created_from":"owner_correction",
      "change_summary":"基于用户纠正生成事实版本 metadata",
      "explicit_owner_confirmation":true,
      "explicit_no_training_data_confirmation":true
    }' \
    "${API_BASE}/personal-case-workspace/fact-previews/${created_preview_id}/versions/mock"
)"
assert_fact_correction_safe "${version_body}" "create fact version"

confirm_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "explicit_owner_confirmation":true,
      "explicit_source_trace_confirmation":true,
      "explicit_no_auto_legal_analysis_confirmation":true,
      "explicit_no_training_data_confirmation":true
    }' \
    "${API_BASE}/personal-case-workspace/fact-previews/${created_preview_id}/confirm-for-legal-analysis/mock"
)"
assert_fact_correction_safe "${confirm_body}" "confirm for legal analysis"
require_true_field "${confirm_body}" "confirm for legal analysis" "legal_analysis_input_ready"
require_false_field "${confirm_body}" "confirm for legal analysis" "legal_analysis_auto_triggered"

pass "personal fact preview and correction APIs v7.20"
