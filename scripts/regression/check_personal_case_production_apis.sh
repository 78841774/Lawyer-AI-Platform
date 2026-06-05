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
    curl -sS -o /tmp/personal_case_production_regression_error.json -w "%{http_code}" \
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

assert_case_production_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" '自动胜诉'
  assert_absent "${body}" "${label}" '替代律师'
  assert_absent "${body}" "${label}" '保证准确'
  assert_absent "${body}" "${label}" '最终法律意见正文'
  assert_absent "${body}" "${label}" '最终报告正文'
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "live_provider_call_executed"
  assert_field_false_if_present "${body}" "${label}" "live_provider_called"
  assert_field_false_if_present "${body}" "${label}" "api_key_accessed"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "auto_delivery_enabled"
  assert_field_false_if_present "${body}" "${label}" "delivery_ready"
}

section "Personal Case Production APIs"

endpoints=(
  "/personal-case-production/status"
  "/personal-case-production/workflow-stages"
  "/personal-case-production/workflow-stages/case_intake_stage"
  "/personal-case-production/workflow-stages/material_processing_stage"
  "/personal-case-production/workflow-stages/ai_draft_stage"
  "/personal-case-production/workflow-stages/intelligence_check_stage"
  "/personal-case-production/workflow-stages/skill_studio_stage"
  "/personal-case-production/workflow-stages/lawyer_review_stage"
  "/personal-case-production/workflow-stages/final_readiness_stage"
  "/personal-case-production/cases"
  "/personal-case-production/workflow-runs"
  "/personal-case-production/stage-runs"
  "/personal-case-production/readiness"
  "/personal-case-production/review-gates"
  "/personal-case-production/source-traces"
  "/personal-case-production/audit"
  "/personal-case-production/safety"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_case_production_safe "${body}" "${endpoint}"
done

case_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_v55_approve_all",
      "production_title":"真实案件生产记录草案",
      "case_type":"civil",
      "client_alias":"client_demo",
      "jurisdiction":"中国大陆",
      "legal_area":"合同纠纷",
      "desensitization_status":"metadata_only",
      "explicit_mock_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-case-production/cases/mock"
)"
assert_case_production_safe "${case_body}" "cases/mock"
assert_field_false_required "${case_body}" "cases/mock" "raw_content_included"
assert_field_false_required "${case_body}" "cases/mock" "final_legal_opinion_generated"
assert_field_false_required "${case_body}" "cases/mock" "final_report_generated"
assert_field_false_required "${case_body}" "cases/mock" "external_delivery_triggered"
require_true_field "${case_body}" "cases/mock" "requires_lawyer_review"
require_true_field "${case_body}" "cases/mock" "final_gate_required"
require_true_field "${case_body}" "cases/mock" "source_trace_required"

production_case_id="$(printf '%s' "${case_body}" | sed -n 's/.*"production_case_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${production_case_id}" ]; then
  fail "cases/mock did not return production_case_id"
fi

case_detail="$(check_endpoint_200 "/personal-case-production/cases/${production_case_id}")"
assert_case_production_safe "${case_detail}" "production case detail"

expect_request_failure "case missing confirmation" "/personal-case-production/cases/mock" '{
  "case_id":"case_v55_approve_all",
  "production_title":"真实案件生产记录草案",
  "case_type":"civil",
  "client_alias":"client_demo",
  "jurisdiction":"中国大陆",
  "legal_area":"合同纠纷",
  "desensitization_status":"metadata_only"
}'

workflow_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"production_case_id\":\"${production_case_id}\",
      \"workflow_scope\":\"full_controlled_mock_workflow\",
      \"selected_stage_ids\":[
        \"case_intake_stage\",
        \"material_processing_stage\",
        \"ai_draft_stage\",
        \"intelligence_check_stage\",
        \"skill_studio_stage\",
        \"lawyer_review_stage\",
        \"final_readiness_stage\"
      ],
      \"explicit_mock_confirmation\":true,
      \"explicit_lawyer_review_confirmation\":true,
      \"explicit_no_final_opinion_confirmation\":true,
      \"explicit_no_external_delivery_confirmation\":true
    }" \
    "${API_BASE}/personal-case-production/workflow-runs/mock"
)"
assert_case_production_safe "${workflow_body}" "workflow-runs/mock"
assert_field_false_required "${workflow_body}" "workflow-runs/mock" "final_legal_opinion_generated"
assert_field_false_required "${workflow_body}" "workflow-runs/mock" "final_report_generated"
assert_field_false_required "${workflow_body}" "workflow-runs/mock" "external_delivery_triggered"
require_true_field "${workflow_body}" "workflow-runs/mock" "requires_lawyer_review"
require_true_field "${workflow_body}" "workflow-runs/mock" "final_gate_required"

workflow_run_id="$(printf '%s' "${workflow_body}" | sed -n 's/.*"workflow_run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${workflow_run_id}" ]; then
  fail "workflow-runs/mock did not return workflow_run_id"
fi

workflow_detail="$(check_endpoint_200 "/personal-case-production/workflow-runs/${workflow_run_id}")"
assert_case_production_safe "${workflow_detail}" "workflow run detail"

expect_request_failure "workflow missing confirmation" "/personal-case-production/workflow-runs/mock" "{
  \"production_case_id\":\"${production_case_id}\",
  \"workflow_scope\":\"full_controlled_mock_workflow\",
  \"selected_stage_ids\":[\"case_intake_stage\"]
}"

stage_ids=(
  "case_intake_stage"
  "material_processing_stage"
  "ai_draft_stage"
  "intelligence_check_stage"
  "skill_studio_stage"
  "lawyer_review_stage"
  "final_readiness_stage"
)

last_stage_run_id=""
for stage_id in "${stage_ids[@]}"; do
  stage_body="$(
    curl -fsS \
      -H "Content-Type: application/json" \
      -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
      -d "{
        \"workflow_run_id\":\"${workflow_run_id}\",
        \"stage_id\":\"${stage_id}\",
        \"linked_runtime_object_ids\":[],
        \"stage_note\":\"模拟阶段运行 metadata\",
        \"explicit_mock_confirmation\":true,
        \"explicit_no_live_provider_confirmation\":true,
        \"explicit_no_final_opinion_confirmation\":true
      }" \
      "${API_BASE}/personal-case-production/stage-runs/mock"
  )"
  assert_case_production_safe "${stage_body}" "stage-runs/mock ${stage_id}"
  assert_field_false_required "${stage_body}" "stage-runs/mock ${stage_id}" "live_provider_called"
  assert_field_false_required "${stage_body}" "stage-runs/mock ${stage_id}" "raw_content_included"
  last_stage_run_id="$(printf '%s' "${stage_body}" | sed -n 's/.*"stage_run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
done

if [ -z "${last_stage_run_id}" ]; then
  fail "stage-runs/mock did not return stage_run_id"
fi

stage_detail="$(check_endpoint_200 "/personal-case-production/stage-runs/${last_stage_run_id}")"
assert_case_production_safe "${stage_detail}" "stage run detail"

expect_request_failure "stage missing confirmation" "/personal-case-production/stage-runs/mock" "{
  \"workflow_run_id\":\"${workflow_run_id}\",
  \"stage_id\":\"case_intake_stage\",
  \"linked_runtime_object_ids\":[]
}"

readiness_body="$(check_endpoint_200 "/personal-case-production/readiness/${production_case_id}")"
assert_case_production_safe "${readiness_body}" "readiness detail"
require_true_field "${readiness_body}" "readiness detail" "final_gate_ready"
assert_field_false_required "${readiness_body}" "readiness detail" "delivery_ready"
assert_field_false_required "${readiness_body}" "readiness detail" "external_delivery_triggered"

review_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"approve_for_final_gate",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"metadata only",
      "explicit_lawyer_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-case-production/review-gates/${production_case_id}/actions"
)"
assert_case_production_safe "${review_body}" "review gate action"
assert_field_false_required "${review_body}" "review gate action" "final_legal_opinion_generated"
assert_field_false_required "${review_body}" "review gate action" "final_report_generated"
assert_field_false_required "${review_body}" "review gate action" "external_delivery_triggered"

expect_request_failure "review gate invalid action" "/personal-case-production/review-gates/${production_case_id}/actions" '{
  "action":"invalid_action",
  "reviewer_id":"local_demo_lawyer",
  "explicit_lawyer_confirmation":true,
  "explicit_no_final_opinion_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}'

cases_body="$(check_endpoint_200 "/personal-case-production/cases")"
readiness_list_body="$(check_endpoint_200 "/personal-case-production/readiness")"
traces_body="$(check_endpoint_200 "/personal-case-production/source-traces")"
audit_body="$(check_endpoint_200 "/personal-case-production/audit")"
assert_case_production_safe "${cases_body}" "cases list"
assert_case_production_safe "${readiness_list_body}" "readiness list"
assert_case_production_safe "${traces_body}" "source traces"
assert_case_production_safe "${audit_body}" "audit"

pass "personal case production APIs"
