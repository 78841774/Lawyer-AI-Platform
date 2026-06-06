#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Legal Analysis Draft APIs v7.21"
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

assert_legal_draft_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'OPENAI_API_KEY|DEEPSEEK|API_KEY[[:space:]]*[:=]|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" 'local\.db|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" '真实客户|真实案件|真实判决|真实企业信息|身份证号|银行卡号|手机号|客户姓名|raw OCR 原文|真实案件原文'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "legal_analysis_draft_only"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_false_field "${body}" "${label}" "blocks_next_stage"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_skill_published"
  require_false_field "${body}" "${label}" "raw_content_included"
  require_false_field "${body}" "${label}" "raw_ocr_text_included"
  require_false_field "${body}" "${label}" "raw_content_written_to_git"
  require_false_field "${body}" "${label}" "raw_content_written_to_docs"
  require_false_field "${body}" "${label}" "raw_content_written_to_diagnostics"
  require_false_field "${body}" "${label}" "raw_content_written_to_regression_output"
  require_false_field "${body}" "${label}" "api_key_accessed"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "final_fact_finding"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "real_pdf_docx_generated"
}

for endpoint in \
  "/personal-case-analysis/status" \
  "/personal-case-analysis/legal-drafts" \
  "/personal-case-analysis/review-queue" \
  "/personal-case-analysis/source-traces" \
  "/personal-case-analysis/audit" \
  "/personal-case-analysis/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_legal_draft_safe "${body}" "${endpoint}"
done

created_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"open_case_mock_001",
      "fact_draft_id":null,
      "source_trace_ids":[],
      "legal_search_metadata_ids":["legal_search_metadata_mock_001"],
      "enterprise_metadata_ids":["enterprise_metadata_mock_001"],
      "case_legal_analysis_skill_id":"case_legal_analysis_skill",
      "explicit_mock_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_lawyer_review_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-case-analysis/legal-drafts/mock"
)"
assert_legal_draft_safe "${created_body}" "create legal draft"
legal_draft_id="$(printf '%s' "${created_body}" | sed -n 's/.*"legal_draft_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${legal_draft_id}" ]; then
  fail "created legal draft did not return legal_draft_id"
fi

for endpoint in \
  "/personal-case-analysis/legal-drafts/${legal_draft_id}" \
  "/personal-case-analysis/legal-drafts/${legal_draft_id}/versions" \
  "/personal-case-analysis/legal-drafts/${legal_draft_id}/quality" \
  "/personal-case-analysis/legal-drafts/${legal_draft_id}/gate"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_legal_draft_safe "${body}" "${endpoint}"
done

version_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "created_from":"owner_correction",
      "change_summary":"用户本人修订法律分析草稿 metadata",
      "explicit_owner_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_training_data_confirmation":true
    }' \
    "${API_BASE}/personal-case-analysis/legal-drafts/${legal_draft_id}/versions/mock"
)"
assert_legal_draft_safe "${version_body}" "create legal draft version"

confirm_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"仅确认进入律师复核队列 metadata",
      "explicit_owner_confirmation":true,
      "explicit_lawyer_review_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_final_report_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-case-analysis/legal-drafts/${legal_draft_id}/confirm-for-review/mock"
)"
assert_legal_draft_safe "${confirm_body}" "confirm legal draft for review"
require_true_field "${confirm_body}" "confirm legal draft for review" "review_ready"

pass "personal legal analysis draft APIs v7.21"
