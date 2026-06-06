#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Practice Runtime Feedback v7.31h"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_practice_runtime_loading_v731g_apis.sh" >/dev/null

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

require_contains() {
  local body="$1"
  local label="$2"
  local pattern="$3"
  if ! printf '%s' "${body}" | grep -Eq "${pattern}"; then
    fail "${label} expected pattern: ${pattern}"
  fi
}

extract_id() {
  local body="$1"
  local field="$2"
  printf '%s' "${body}" | sed -n "s/.*\"${field}\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p" | head -n 1
}

extract_allowed_usage_id() {
  python3 -c 'import json,sys
data=json.load(sys.stdin)
for item in data.get("usage_events", []):
    if item.get("allowed") is True:
        print(item.get("usage_event_id", ""))
        break
'
}

assert_v731h_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "lawyer_approved_package_only"
  require_true_field "${body}" "${label}" "redacted_abstracted_experience_only"
  require_true_field "${body}" "${label}" "output_observation_metadata_only"
  require_true_field "${body}" "${label}" "lawyer_feedback_metadata_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_result_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "source_material_returned"
  require_false_field "${body}" "${label}" "full_output_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
  require_false_field "${body}" "${label}" "feedback_auto_mutates_loaded_package"
  require_false_field "${body}" "${label}" "candidate_pack_auto_mutates_loaded_package"
  require_false_field "${body}" "${label}" "package_auto_disabled_by_feedback"
  require_false_field "${body}" "${label}" "package_auto_rolled_back_by_feedback"
  require_false_field "${body}" "${label}" "practice_runtime_package_auto_replaced"
  require_false_field "${body}" "${label}" "automatic_training_triggered"
  require_false_field "${body}" "${label}" "formal_training_set_written"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

post_json() {
  local endpoint="$1"
  local payload="$2"
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "${payload}" \
    "${API_BASE}${endpoint}"
}

usage_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-runtime-usage")"
usage_event_id="$(printf '%s' "${usage_body}" | extract_allowed_usage_id)"
if [ -z "${usage_event_id}" ]; then
  fail "missing allowed practice runtime usage event for v7.31h"
fi

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-31h/status")"
assert_v731h_safe "${status_body}" "v7-31h/status"
require_contains "${status_body}" "v7-31h/status" '"observation_registry_ready"[[:space:]]*:[[:space:]]*true'

observation_body="$(post_json "/personal-skill-studio/training-artifacts/practice-output-observations" "{
  \"usage_event_id\":\"${usage_event_id}\",
  \"output_category\":\"risk_warning\",
  \"output_summary_redacted\":\"脱敏输出观察：系统给出了风险提示方向，仍需律师结合个案复核。\",
  \"observed_issue_summary\":\"提示边界需要更明确，不能表达为最终法律意见。\",
  \"observed_by\":\"local_demo_lawyer\",
  \"safety_flags\":[\"metadata_only\",\"source_trace_required\",\"lawyer_review_required\"],
  \"explicit_no_raw_output_confirmation\":true,
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_package_mutation_confirmation\":true
}")"
assert_v731h_safe "${observation_body}" "practice-output-observations create"
require_contains "${observation_body}" "practice-output-observations create" '"output_category"[[:space:]]*:[[:space:]]*"risk_warning"'
observation_id="$(extract_id "${observation_body}" "observation_id")"
if [ -z "${observation_id}" ]; then
  fail "missing observation_id"
fi

feedback_body="$(post_json "/personal-skill-studio/training-artifacts/practice-lawyer-feedback" "{
  \"observation_id\":\"${observation_id}\",
  \"feedback_type\":\"missing_risk_warning\",
  \"feedback_summary\":\"律师反馈：建议增加更醒目的风险提示 metadata。\",
  \"suggested_change\":\"下一轮候选中增加风险提示，不修改当前已加载 package。\",
  \"severity\":\"medium\",
  \"applies_to_experience_card_id\":null,
  \"applies_to_usage_boundary\":\"不得作为最终法律意见\",
  \"created_by\":\"local_demo_lawyer\",
  \"explicit_no_auto_disable_confirmation\":true,
  \"explicit_no_auto_rollback_confirmation\":true,
  \"explicit_no_package_mutation_confirmation\":true,
  \"explicit_no_training_confirmation\":true
}")"
assert_v731h_safe "${feedback_body}" "practice-lawyer-feedback create"
require_contains "${feedback_body}" "practice-lawyer-feedback create" '"feedback_status"[[:space:]]*:[[:space:]]*"submitted"'
require_contains "${feedback_body}" "practice-lawyer-feedback create" '"create_iteration_candidate_recommended"[[:space:]]*:[[:space:]]*true'
feedback_id="$(extract_id "${feedback_body}" "feedback_id")"
if [ -z "${feedback_id}" ]; then
  fail "missing feedback_id"
fi

triage_body="$(post_json "/personal-skill-studio/training-artifacts/practice-lawyer-feedback/${feedback_id}/triage" '{
  "triaged_by":"local_demo_lawyer",
  "feedback_status":"triaged",
  "triage_note":"接受为后续 v7.31i 候选输入，不自动改包。",
  "explicit_no_auto_disable_confirmation":true,
  "explicit_no_auto_rollback_confirmation":true,
  "explicit_no_package_mutation_confirmation":true,
  "explicit_no_training_confirmation":true
}')"
assert_v731h_safe "${triage_body}" "practice-lawyer-feedback triage"
require_contains "${triage_body}" "practice-lawyer-feedback triage" '"feedback_status"[[:space:]]*:[[:space:]]*"triaged"'

risk_body="$(post_json "/personal-skill-studio/training-artifacts/practice-risk-events" "{
  \"observation_id\":\"${observation_id}\",
  \"severity\":\"high\",
  \"risk_type\":\"missing_disclaimer\",
  \"risk_summary\":\"输出提示中免责声明不够醒目，需后续迭代补强。\",
  \"immediate_action_required\":true,
  \"suggested_action\":\"进入律师反馈复核队列，不自动禁用或回滚。\",
  \"created_by\":\"local_demo_lawyer\",
  \"explicit_no_auto_disable_confirmation\":true,
  \"explicit_no_auto_rollback_confirmation\":true,
  \"explicit_no_package_mutation_confirmation\":true
}")"
assert_v731h_safe "${risk_body}" "practice-risk-events create"
require_contains "${risk_body}" "practice-risk-events create" '"risk_type"[[:space:]]*:[[:space:]]*"missing_disclaimer"'
risk_event_id="$(extract_id "${risk_body}" "risk_event_id")"
if [ -z "${risk_event_id}" ]; then
  fail "missing risk_event_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/practice-output-observations/status" \
  "/personal-skill-studio/training-artifacts/practice-output-observations" \
  "/personal-skill-studio/training-artifacts/practice-output-observations/${observation_id}" \
  "/personal-skill-studio/training-artifacts/practice-lawyer-feedback" \
  "/personal-skill-studio/training-artifacts/practice-lawyer-feedback/${feedback_id}" \
  "/personal-skill-studio/training-artifacts/practice-risk-events" \
  "/personal-skill-studio/training-artifacts/practice-risk-events/${risk_event_id}" \
  "/personal-skill-studio/training-artifacts/practice-feedback-summary" \
  "/personal-skill-studio/training-artifacts/v7-31h/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731h_safe "${body}" "${endpoint}"
done

summary_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-feedback-summary")"
require_contains "${summary_body}" "practice-feedback-summary" '"observation_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${summary_body}" "practice-feedback-summary" '"feedback_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${summary_body}" "practice-feedback-summary" '"risk_event_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${summary_body}" "practice-feedback-summary" '"iteration_candidate_recommended_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${summary_body}" "practice-feedback-summary" '"package_auto_disabled_by_feedback"[[:space:]]*:[[:space:]]*false'
require_contains "${summary_body}" "practice-feedback-summary" '"package_auto_rolled_back_by_feedback"[[:space:]]*:[[:space:]]*false'

pass "personal practice runtime feedback v7.31h"
