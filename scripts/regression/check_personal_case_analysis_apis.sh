#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Case Analysis APIs v7.16"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_case_analysis"

require_true_field() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*true"; then
    fail "${label} expected ${field}=true"
  fi
}

assert_case_analysis_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" 'raw_material'
  assert_absent "${body}" "${label}" 'raw_ocr_text[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" '最终法律意见已生成'
  assert_absent "${body}" "${label}" '最终报告已生成'
  assert_absent "${body}" "${label}" '已自动发布 Skill|Skill 发布成功'
  assert_field_false_if_present "${body}" "${label}" "closed_case_training"
  assert_field_false_if_present "${body}" "${label}" "training_data_generated"
  assert_field_false_if_present "${body}" "${label}" "writes_to_training_set"
  assert_field_false_if_present "${body}" "${label}" "skill_updated"
  assert_field_false_if_present "${body}" "${label}" "skill_published"
  assert_field_false_if_present "${body}" "${label}" "future_training_candidate"
  assert_field_false_if_present "${body}" "${label}" "blocks_next_stage"
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "raw_ocr_text_included"
  assert_field_false_if_present "${body}" "${label}" "ai_prompt_injected"
  assert_field_false_if_present "${body}" "${label}" "live_call_executed"
  assert_field_false_if_present "${body}" "${label}" "api_key_accessed"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "real_pdf_docx_generated"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "open_case_runtime"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "gate_reference_only"
}

for endpoint in \
  "/personal-case-analysis/status" \
  "/personal-case-analysis/runtimes" \
  "/personal-case-analysis/runtimes/controlled_case_analysis_runtime" \
  "/personal-case-analysis/skill-baselines" \
  "/personal-case-analysis/runs" \
  "/personal-case-analysis/fact-drafts" \
  "/personal-case-analysis/legal-drafts" \
  "/personal-case-analysis/review-queue" \
  "/personal-case-analysis/evaluations" \
  "/personal-case-analysis/gates" \
  "/personal-case-analysis/source-traces" \
  "/personal-case-analysis/audit" \
  "/personal-case-analysis/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_case_analysis_safe "${body}" "${endpoint}"
done

run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"open_case_mock_001",
      "case_alias":"未结案件本地试点样本",
      "analysis_scope":"fact_and_legal_analysis",
      "material_metadata_ids":["material_metadata_mock_001"],
      "source_trace_ids":[],
      "selected_skill_ids":["case_fact_extraction_skill","case_legal_analysis_skill"],
      "explicit_mock_confirmation":true,
      "explicit_open_case_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_lawyer_review_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-case-analysis/runs/mock"
)"
assert_case_analysis_safe "${run_body}" "runs/mock"
assert_field_false_required "${run_body}" "runs/mock" "training_data_generated"
assert_field_false_required "${run_body}" "runs/mock" "writes_to_training_set"
assert_field_false_required "${run_body}" "runs/mock" "skill_updated"
assert_field_false_required "${run_body}" "runs/mock" "skill_published"
assert_field_false_required "${run_body}" "runs/mock" "final_legal_opinion_generated"
assert_field_false_required "${run_body}" "runs/mock" "final_report_generated"
assert_field_false_required "${run_body}" "runs/mock" "external_delivery_triggered"
require_true_field "${run_body}" "runs/mock" "gate_reference_only"

run_id="$(printf '%s' "${run_body}" | sed -n 's/.*"run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
fact_draft_id="$(printf '%s' "${run_body}" | sed -n 's/.*"fact_draft_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
legal_draft_id="$(printf '%s' "${run_body}" | sed -n 's/.*"legal_draft_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
evaluation_id="$(printf '%s' "${run_body}" | sed -n 's/.*"evaluation_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
gate_id="$(printf '%s' "${run_body}" | sed -n 's/.*"gate_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${run_id}" ] || [ -z "${fact_draft_id}" ] || [ -z "${legal_draft_id}" ] || [ -z "${evaluation_id}" ] || [ -z "${gate_id}" ]; then
  fail "runs/mock did not return expected ids"
fi

for endpoint in \
  "/personal-case-analysis/runs/${run_id}" \
  "/personal-case-analysis/fact-drafts/${fact_draft_id}" \
  "/personal-case-analysis/legal-drafts/${legal_draft_id}" \
  "/personal-case-analysis/evaluations/${evaluation_id}" \
  "/personal-case-analysis/gates/${gate_id}"; do
  detail_body="$(check_endpoint_200 "${endpoint}")"
  assert_case_analysis_safe "${detail_body}" "${endpoint}"
done

fact_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"open_case_mock_002",
      "run_id":null,
      "source_trace_ids":[],
      "material_metadata_ids":["material_metadata_mock_002"],
      "case_fact_extraction_skill_id":"case_fact_extraction_skill",
      "explicit_mock_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_lawyer_review_confirmation":true
    }' \
    "${API_BASE}/personal-case-analysis/fact-drafts/mock"
)"
assert_case_analysis_safe "${fact_body}" "fact-drafts/mock"

legal_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"case_id\":\"open_case_mock_002\",
      \"fact_draft_id\":\"${fact_draft_id}\",
      \"source_trace_ids\":[],
      \"legal_search_metadata_ids\":[\"legal_search_metadata_mock_001\"],
      \"enterprise_metadata_ids\":[\"enterprise_metadata_mock_001\"],
      \"case_legal_analysis_skill_id\":\"case_legal_analysis_skill\",
      \"explicit_mock_confirmation\":true,
      \"explicit_no_training_data_confirmation\":true,
      \"explicit_no_raw_content_confirmation\":true,
      \"explicit_lawyer_review_confirmation\":true,
      \"explicit_no_final_opinion_confirmation\":true
    }" \
    "${API_BASE}/personal-case-analysis/legal-drafts/mock"
)"
assert_case_analysis_safe "${legal_body}" "legal-drafts/mock"

review_queue_body="$(check_endpoint_200 "/personal-case-analysis/review-queue")"
assert_case_analysis_safe "${review_queue_body}" "review queue after drafts"
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
      "reviewer_note":"仅更新 review metadata",
      "explicit_lawyer_confirmation":true,
      "explicit_no_training_data_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-case-analysis/review-queue/${review_item_id}/actions"
)"
assert_case_analysis_safe "${review_action_body}" "review action"

for endpoint in \
  "/personal-case-analysis/runs" \
  "/personal-case-analysis/fact-drafts" \
  "/personal-case-analysis/legal-drafts" \
  "/personal-case-analysis/review-queue" \
  "/personal-case-analysis/evaluations" \
  "/personal-case-analysis/gates" \
  "/personal-case-analysis/source-traces" \
  "/personal-case-analysis/audit" \
  "/personal-case-analysis/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_case_analysis_safe "${body}" "${endpoint} after actions"
done

pass "personal case analysis APIs v7.16"
