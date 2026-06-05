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
    curl -sS -o /tmp/personal_showcase_pack_regression_error.json -w "%{http_code}" \
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

assert_showcase_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" '自动胜诉'
  assert_absent "${body}" "${label}" '替代律师'
  assert_absent "${body}" "${label}" '保证准确'
  assert_absent "${body}" "${label}" '自动出具最终法律意见'
  assert_absent "${body}" "${label}" '自动完成客户交付'
  assert_absent "${body}" "${label}" '一键交付'
  assert_absent "${body}" "${label}" '全自动办案'
  assert_absent "${body}" "${label}" '自动发送客户'
  assert_absent "${body}" "${label}" '智能判案'
  assert_absent "${body}" "${label}" '包赢'
  assert_absent "${body}" "${label}" '无需律师'
  assert_absent "${body}" "${label}" '真实客户姓名'
  assert_absent "${body}" "${label}" '真实案件名称'
  assert_absent "${body}" "${label}" '真实判决原文'
  assert_field_false_if_present "${body}" "${label}" "real_provider_called"
  assert_field_false_if_present "${body}" "${label}" "api_key_accessed"
  assert_field_false_if_present "${body}" "${label}" "real_case_data_included"
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "final_file_generated"
  assert_field_false_if_present "${body}" "${label}" "auto_delivery_enabled"
}

section "Personal Showcase Pack APIs"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_showcase_pack"

endpoints=(
  "/personal-showcase-pack/status"
  "/personal-showcase-pack/runtimes"
  "/personal-showcase-pack/runtimes/showcase_pack_runtime"
  "/personal-showcase-pack/runtimes/pilot_sample_runtime"
  "/personal-showcase-pack/runtimes/story_flow_runtime"
  "/personal-showcase-pack/runtimes/showcase_metrics_runtime"
  "/personal-showcase-pack/runtimes/trust_panel_runtime"
  "/personal-showcase-pack/safety"
  "/personal-showcase-pack/trust-panel"
  "/personal-showcase-pack/metrics"
  "/personal-showcase-pack/pilot-samples"
  "/personal-showcase-pack/story-flows"
  "/personal-showcase-pack/audit"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_showcase_safe "${body}" "${endpoint}"
done

sample_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "sample_title":"合同纠纷试点样本",
      "sample_type":"contract_dispute_demo",
      "legal_area":"民商事",
      "case_cause":"合同纠纷",
      "risk_level":"controlled_demo",
      "demo_persona":"试点演示律师",
      "linked_runtime_ids":["personal_intelligence_gateway","personal_skill_studio","personal_case_production","personal_delivery_packet"],
      "explicit_mock_confirmation":true,
      "explicit_no_real_case_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-showcase-pack/pilot-samples/mock"
)"
assert_showcase_safe "${sample_body}" "pilot-samples/mock"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "real_case_data_included"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "raw_content_included"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "final_legal_opinion_generated"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "final_report_generated"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "external_delivery_triggered"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "email_sent"
assert_field_false_required "${sample_body}" "pilot-samples/mock" "final_file_generated"
require_true_field "${sample_body}" "pilot-samples/mock" "requires_lawyer_review"
require_true_field "${sample_body}" "pilot-samples/mock" "final_lock_required"
require_true_field "${sample_body}" "pilot-samples/mock" "source_trace_required"
require_true_field "${sample_body}" "pilot-samples/mock" "synthetic_demo_only"

pilot_sample_id="$(printf '%s' "${sample_body}" | sed -n 's/.*"pilot_sample_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${pilot_sample_id}" ]; then
  fail "pilot-samples/mock did not return pilot_sample_id"
fi

sample_detail="$(check_endpoint_200 "/personal-showcase-pack/pilot-samples/${pilot_sample_id}")"
assert_showcase_safe "${sample_detail}" "pilot sample detail"

expect_request_failure "pilot sample missing confirmation" "/personal-showcase-pack/pilot-samples/mock" '{
  "sample_title":"合同纠纷试点样本",
  "sample_type":"contract_dispute_demo",
  "legal_area":"民商事",
  "case_cause":"合同纠纷",
  "risk_level":"controlled_demo",
  "demo_persona":"试点演示律师"
}'

expect_request_failure "pilot sample invalid type" "/personal-showcase-pack/pilot-samples/mock" '{
  "sample_title":"非法试点样本",
  "sample_type":"real_client_case",
  "legal_area":"民商事",
  "case_cause":"合同纠纷",
  "risk_level":"controlled_demo",
  "demo_persona":"试点演示律师",
  "explicit_mock_confirmation":true,
  "explicit_no_real_case_confirmation":true,
  "explicit_no_raw_content_confirmation":true,
  "explicit_no_final_opinion_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}'

expect_request_failure "pilot sample sensitive metadata blocked" "/personal-showcase-pack/pilot-samples/mock" '{
  "sample_title":"/Users/test/real_cases/client.pdf",
  "sample_type":"contract_dispute_demo",
  "legal_area":"民商事",
  "case_cause":"合同纠纷",
  "risk_level":"controlled_demo",
  "demo_persona":"试点演示律师",
  "explicit_mock_confirmation":true,
  "explicit_no_real_case_confirmation":true,
  "explicit_no_raw_content_confirmation":true,
  "explicit_no_final_opinion_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}'

story_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"pilot_sample_id\":\"${pilot_sample_id}\",
      \"story_title\":\"受控生产到展示包流程\",
      \"story_scope\":\"v7.3-v7.6 能力串联的 mock metadata 演示\",
      \"selected_stage_ids\":[\"case_intake\",\"material_processing\",\"ai_draft\",\"legal_enterprise_check\",\"skill_studio\",\"delivery_packet\",\"final_lock\"],
      \"explicit_mock_confirmation\":true,
      \"explicit_no_real_case_confirmation\":true,
      \"explicit_no_final_opinion_confirmation\":true,
      \"explicit_no_external_delivery_confirmation\":true
    }" \
    "${API_BASE}/personal-showcase-pack/story-flows/mock"
)"
assert_showcase_safe "${story_body}" "story-flows/mock"
assert_field_false_required "${story_body}" "story-flows/mock" "real_case_data_included"
assert_field_false_required "${story_body}" "story-flows/mock" "raw_content_included"
assert_field_false_required "${story_body}" "story-flows/mock" "final_legal_opinion_generated"
assert_field_false_required "${story_body}" "story-flows/mock" "final_report_generated"
assert_field_false_required "${story_body}" "story-flows/mock" "external_delivery_triggered"
require_true_field "${story_body}" "story-flows/mock" "requires_lawyer_review"
require_true_field "${story_body}" "story-flows/mock" "final_lock_required"
require_true_field "${story_body}" "story-flows/mock" "source_trace_required"
require_true_field "${story_body}" "story-flows/mock" "synthetic_demo_only"

story_flow_id="$(printf '%s' "${story_body}" | sed -n 's/.*"story_flow_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${story_flow_id}" ]; then
  fail "story-flows/mock did not return story_flow_id"
fi

story_detail="$(check_endpoint_200 "/personal-showcase-pack/story-flows/${story_flow_id}")"
assert_showcase_safe "${story_detail}" "story flow detail"

expect_request_failure "story flow missing confirmation" "/personal-showcase-pack/story-flows/mock" "{
  \"pilot_sample_id\":\"${pilot_sample_id}\",
  \"story_title\":\"受控生产到展示包流程\",
  \"story_scope\":\"v7.3-v7.6 能力串联的 mock metadata 演示\",
  \"selected_stage_ids\":[\"case_intake\"]
}"

expect_request_failure "story flow invalid stage" "/personal-showcase-pack/story-flows/mock" "{
  \"pilot_sample_id\":\"${pilot_sample_id}\",
  \"story_title\":\"非法阶段流程\",
  \"story_scope\":\"mock metadata\",
  \"selected_stage_ids\":[\"real_provider_call\"],
  \"explicit_mock_confirmation\":true,
  \"explicit_no_real_case_confirmation\":true,
  \"explicit_no_final_opinion_confirmation\":true,
  \"explicit_no_external_delivery_confirmation\":true
}"

expect_request_failure "story flow sensitive metadata blocked" "/personal-showcase-pack/story-flows/mock" "{
  \"pilot_sample_id\":\"${pilot_sample_id}\",
  \"story_title\":\"受控生产到展示包流程\",
  \"story_scope\":\"storage/runtime/raw-content\",
  \"selected_stage_ids\":[\"case_intake\"],
  \"explicit_mock_confirmation\":true,
  \"explicit_no_real_case_confirmation\":true,
  \"explicit_no_final_opinion_confirmation\":true,
  \"explicit_no_external_delivery_confirmation\":true
}"

samples_body="$(check_endpoint_200 "/personal-showcase-pack/pilot-samples")"
flows_body="$(check_endpoint_200 "/personal-showcase-pack/story-flows")"
metrics_body="$(check_endpoint_200 "/personal-showcase-pack/metrics")"
trust_body="$(check_endpoint_200 "/personal-showcase-pack/trust-panel")"
audit_body="$(check_endpoint_200 "/personal-showcase-pack/audit")"
safety_body="$(check_endpoint_200 "/personal-showcase-pack/safety")"
assert_showcase_safe "${samples_body}" "pilot samples list"
assert_showcase_safe "${flows_body}" "story flows list"
assert_showcase_safe "${metrics_body}" "metrics"
assert_showcase_safe "${trust_body}" "trust-panel"
assert_showcase_safe "${audit_body}" "audit"
assert_showcase_safe "${safety_body}" "safety"
require_true_field "${metrics_body}" "metrics" "synthetic_demo_only"
assert_field_false_required "${metrics_body}" "metrics" "real_provider_called"
assert_field_false_required "${metrics_body}" "metrics" "external_delivery_triggered"

pass "personal showcase pack APIs"
