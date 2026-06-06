#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Production Pilot APIs v7.17"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_production_pilot"

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

assert_pilot_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" '身份证号|银行卡号|手机号|合同全文|聊天记录'
  assert_absent "${body}" "${label}" '一键发送客户|一键外部交付|自动提交法院|自动生成公开链接|自动上传网盘'
  assert_field_false_if_present "${body}" "${label}" "public_link_created"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "third_party_share_enabled"
  assert_field_false_if_present "${body}" "${label}" "client_auto_delivery"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_auto_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_auto_generated"
  assert_field_false_if_present "${body}" "${label}" "training_data_generated"
  assert_field_false_if_present "${body}" "${label}" "writes_to_training_set"
  assert_field_false_if_present "${body}" "${label}" "skill_updated"
  assert_field_false_if_present "${body}" "${label}" "skill_published"
  assert_field_false_if_present "${body}" "${label}" "api_key_exposed"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_git"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_docs"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_diagnostics"
  assert_field_false_if_present "${body}" "${label}" "raw_content_written_to_regression_output"
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "downloadable_by_owner_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "provider_gated"
}

for endpoint in \
  "/personal-production-pilot/status" \
  "/personal-production-pilot/readiness" \
  "/personal-production-pilot/workflow" \
  "/personal-production-pilot/runtimes" \
  "/personal-production-pilot/provider-gates" \
  "/personal-production-pilot/safety" \
  "/personal-production-pilot/runs" \
  "/personal-production-pilot/case-analysis-summary" \
  "/personal-production-pilot/skill-final-drafts" \
  "/personal-production-pilot/outputs" \
  "/personal-production-pilot/owner-downloads" \
  "/personal-production-pilot/review-queue" \
  "/personal-production-pilot/source-traces" \
  "/personal-production-pilot/audit" \
  "/personal-production-pilot/export-boundary"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_pilot_safe "${body}" "${endpoint}"
done

run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"open_case_pilot_mock_001",
      "case_alias":"未结案件实战 Pilot 样本",
      "workflow_scope":"personal_production_pilot",
      "selected_runtime_ids":[],
      "explicit_owner_confirmation":true,
      "explicit_provider_gated_confirmation":true,
      "explicit_no_external_delivery_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-production-pilot/runs/mock"
)"
assert_pilot_safe "${run_body}" "runs/mock"

run_id="$(printf '%s' "${run_body}" | sed -n 's/.*"run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
output_id="$(printf '%s' "${run_body}" | sed -n 's/.*"output_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
download_id="$(printf '%s' "${run_body}" | sed -n 's/.*"download_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${run_id}" ] || [ -z "${output_id}" ] || [ -z "${download_id}" ]; then
  fail "runs/mock did not return expected ids"
fi

for endpoint in \
  "/personal-production-pilot/runs/${run_id}" \
  "/personal-production-pilot/outputs/${output_id}" \
  "/personal-production-pilot/owner-downloads/${download_id}"; do
  detail_body="$(check_endpoint_200 "${endpoint}")"
  assert_pilot_safe "${detail_body}" "${endpoint}"
done

draft_list="$(check_endpoint_200 "/personal-production-pilot/skill-final-drafts")"
assert_pilot_safe "${draft_list}" "skill-final-drafts"
draft_id="$(printf '%s' "${draft_list}" | sed -n 's/.*"draft_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${draft_id}" ]; then
  fail "skill-final-drafts did not return draft_id"
fi
draft_detail="$(check_endpoint_200 "/personal-production-pilot/skill-final-drafts/${draft_id}")"
assert_pilot_safe "${draft_detail}" "skill final draft detail"

output_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "run_id":null,
      "output_type":"case_analysis_draft",
      "title":"案件分析草稿",
      "format":"Markdown",
      "explicit_owner_confirmation":true,
      "explicit_no_external_delivery_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-production-pilot/outputs/mock"
)"
assert_pilot_safe "${output_body}" "outputs/mock"
second_output_id="$(printf '%s' "${output_body}" | sed -n 's/.*"output_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${second_output_id}" ]; then
  fail "outputs/mock did not return output_id"
fi

download_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "requested_format":"Markdown",
      "explicit_owner_confirmation":true,
      "explicit_no_public_link_confirmation":true,
      "explicit_no_email_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-production-pilot/outputs/${second_output_id}/owner-downloads/mock"
)"
assert_pilot_safe "${download_body}" "owner-downloads/mock"

review_queue_body="$(check_endpoint_200 "/personal-production-pilot/review-queue")"
assert_pilot_safe "${review_queue_body}" "review queue"
review_item_id="$(printf '%s' "${review_queue_body}" | sed -n 's/.*"review_item_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${review_item_id}" ]; then
  fail "review queue did not return review_item_id"
fi

review_action_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"request_revision",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"仅更新 owner-download review metadata",
      "explicit_lawyer_confirmation":true,
      "explicit_no_external_delivery_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-production-pilot/review-queue/${review_item_id}/actions"
)"
assert_pilot_safe "${review_action_body}" "review action"

for endpoint in \
  "/personal-production-pilot/outputs" \
  "/personal-production-pilot/owner-downloads" \
  "/personal-production-pilot/review-queue" \
  "/personal-production-pilot/source-traces" \
  "/personal-production-pilot/audit" \
  "/personal-production-pilot/export-boundary" \
  "/personal-production-pilot/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_pilot_safe "${body}" "${endpoint} after actions"
done

pass "personal production pilot APIs v7.17"
