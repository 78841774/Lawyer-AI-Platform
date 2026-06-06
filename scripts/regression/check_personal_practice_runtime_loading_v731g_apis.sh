#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Practice Runtime Controlled Loading v7.31g"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_practice_load_review_v731f_apis.sh" >/dev/null

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

extract_approved_package_id() {
  python3 -c 'import json,sys
data=json.load(sys.stdin)
for item in data.get("packages", []):
    if item.get("review_status") == "approved_for_practice_load":
        print(item.get("package_id", ""))
        break
'
}

assert_v731g_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted_payload|unredacted_material'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "lawyer_approved_package_only"
  require_true_field "${body}" "${label}" "metadata_safe"
  require_true_field "${body}" "${label}" "redacted_abstracted_experience_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "runtime_monitoring_required"
  require_true_field "${body}" "${label}" "rollback_available"
  require_true_field "${body}" "${label}" "controlled_runtime_loading_only"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_result_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "source_material_returned"
  require_false_field "${body}" "${label}" "unreviewed_package_loaded"
  require_false_field "${body}" "${label}" "system_revalidation_failed_package_loaded"
  require_false_field "${body}" "${label}" "generated_only_package_loaded"
  require_false_field "${body}" "${label}" "unredacted_content_loaded"
  require_false_field "${body}" "${label}" "automatic_training_triggered"
  require_false_field "${body}" "${label}" "formal_training_set_written"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "feedback_auto_mutates_loaded_package"
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

review_list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-load-review/packages")"
approved_package_id="$(printf '%s' "${review_list_body}" | extract_approved_package_id)"
if [ -z "${approved_package_id}" ]; then
  fail "missing approved_for_practice_load package for v7.31g"
fi

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-31g/status")"
assert_v731g_safe "${status_body}" "v7-31g/status"
require_contains "${status_body}" "v7-31g/status" '"loader_ready"[[:space:]]*:[[:space:]]*true'

load_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-loads/load" "{
  \"experience_package_id\":\"${approved_package_id}\",
  \"loaded_by\":\"local_demo_lawyer\",
  \"rollout_mode\":\"disabled\",
  \"rollout_percentage\":0,
  \"allowed_case_causes\":[\"买卖合同纠纷\"],
  \"allowed_workspaces\":[\"owner_workspace\"],
  \"allowed_runtime_modes\":[\"assistive_draft\"],
  \"allowed_task_types\":[\"legal_analysis_draft\"],
  \"usage_limit_per_day\":3,
  \"emergency_disable_enabled\":true,
  \"explicit_lawyer_approved_package_confirmation\":true,
  \"explicit_system_revalidated_confirmation\":true,
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_source_content_confirmation\":true,
  \"explicit_no_final_opinion_confirmation\":true
}")"
assert_v731g_safe "${load_body}" "practice-runtime-loads/load"
require_contains "${load_body}" "practice-runtime-loads/load" '"load_status"[[:space:]]*:[[:space:]]*"loaded_disabled"'
runtime_load_id="$(extract_id "${load_body}" "runtime_load_id")"
if [ -z "${runtime_load_id}" ]; then
  fail "practice runtime load missing runtime_load_id"
fi

blocked_policy_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-policy/evaluate" '{
  "case_cause":"买卖合同纠纷",
  "workspace_id":"owner_workspace",
  "user_id":"local_demo_lawyer",
  "runtime_mode":"assistive_draft",
  "requested_task_type":"legal_analysis_draft",
  "request_context_metadata":{"metadata_only":true}
}')"
assert_v731g_safe "${blocked_policy_body}" "practice-runtime-policy blocked"
require_contains "${blocked_policy_body}" "practice-runtime-policy blocked" '"allowed"[[:space:]]*:[[:space:]]*false'

gray_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}/enable-gray" '{
  "operator_id":"local_demo_lawyer",
  "operator_note":"enable gray rollout for regression",
  "rollout_percentage":100,
  "usage_limit_per_day":3,
  "explicit_manual_control_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}')"
assert_v731g_safe "${gray_body}" "practice-runtime-load enable-gray"
require_contains "${gray_body}" "practice-runtime-load enable-gray" '"load_status"[[:space:]]*:[[:space:]]*"loaded_gray"'
require_contains "${gray_body}" "practice-runtime-load enable-gray" '"rollout_percentage"[[:space:]]*:[[:space:]]*100'

allowed_policy_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-policy/evaluate" '{
  "case_cause":"买卖合同纠纷",
  "workspace_id":"owner_workspace",
  "user_id":"local_demo_lawyer",
  "runtime_mode":"assistive_draft",
  "requested_task_type":"legal_analysis_draft",
  "request_context_metadata":{"metadata_only":true}
}')"
assert_v731g_safe "${allowed_policy_body}" "practice-runtime-policy allowed"
require_contains "${allowed_policy_body}" "practice-runtime-policy allowed" '"allowed"[[:space:]]*:[[:space:]]*true'
require_contains "${allowed_policy_body}" "practice-runtime-policy allowed" "${approved_package_id}"

active_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}/enable-active" '{
  "operator_id":"local_demo_lawyer",
  "operator_note":"enable active rollout for regression",
  "rollout_percentage":100,
  "usage_limit_per_day":3,
  "explicit_manual_control_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}')"
assert_v731g_safe "${active_body}" "practice-runtime-load enable-active"
require_contains "${active_body}" "practice-runtime-load enable-active" '"load_status"[[:space:]]*:[[:space:]]*"loaded_active"'

for endpoint in \
  "/personal-skill-studio/training-artifacts/practice-runtime-loads" \
  "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}" \
  "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}/audit" \
  "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}/source-trace" \
  "/personal-skill-studio/training-artifacts/practice-runtime-usage" \
  "/personal-skill-studio/training-artifacts/practice-runtime-loads/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731g_safe "${body}" "${endpoint}"
done

task_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-tasks")"
training_task_id="$(extract_id "${task_body}" "training_task_id")"
if [ -z "${training_task_id}" ]; then
  fail "missing training_task_id for v7.31g blocked setup"
fi
pending_package_body="$(post_json "/personal-skill-studio/training-artifacts/training-packages/build" "{
  \"source_training_task_id\":\"${training_task_id}\",
  \"source_skill_package_id\":null,
  \"package_name\":\"内部训练经验包 v7.31g blocked setup\",
  \"package_version\":\"v7.31g-blocked.0\",
  \"explicit_pending_practice_load_review_confirmation\":true,
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_real_training_confirmation\":true,
  \"explicit_no_skill_publish_confirmation\":true
}")"
pending_package_id="$(extract_id "${pending_package_body}" "package_id")"
if [ -z "${pending_package_id}" ]; then
  fail "blocked setup did not create pending package"
fi
check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-load-review/packages/${pending_package_id}" >/dev/null
blocked_load_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-loads/load" "{
  \"experience_package_id\":\"${pending_package_id}\",
  \"loaded_by\":\"local_demo_lawyer\",
  \"rollout_mode\":\"active\",
  \"rollout_percentage\":100,
  \"allowed_case_causes\":[\"买卖合同纠纷\"],
  \"allowed_workspaces\":[\"owner_workspace\"],
  \"allowed_runtime_modes\":[\"assistive_draft\"],
  \"allowed_task_types\":[\"legal_analysis_draft\"],
  \"usage_limit_per_day\":3,
  \"emergency_disable_enabled\":true,
  \"explicit_lawyer_approved_package_confirmation\":true,
  \"explicit_system_revalidated_confirmation\":true,
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_source_content_confirmation\":true,
  \"explicit_no_final_opinion_confirmation\":true
}")"
assert_v731g_safe "${blocked_load_body}" "practice-runtime blocked load"
require_contains "${blocked_load_body}" "practice-runtime blocked load" '"load_status"[[:space:]]*:[[:space:]]*"blocked"'
require_contains "${blocked_load_body}" "practice-runtime blocked load" 'package_not_approved_for_practice_load'

disable_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}/disable" '{
  "operator_id":"local_demo_lawyer",
  "operator_note":"disable runtime load for regression",
  "mark_blocked":false,
  "explicit_manual_control_confirmation":true,
  "explicit_no_package_delete_confirmation":true
}')"
assert_v731g_safe "${disable_body}" "practice-runtime-load disable"
require_contains "${disable_body}" "practice-runtime-load disable" '"load_status"[[:space:]]*:[[:space:]]*"disabled"'

rollback_body="$(post_json "/personal-skill-studio/training-artifacts/practice-runtime-loads/${runtime_load_id}/rollback" '{
  "operator_id":"local_demo_lawyer",
  "operator_note":"rollback runtime load for regression",
  "rollback_to_load_id":null,
  "explicit_manual_rollback_confirmation":true,
  "explicit_no_package_delete_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}')"
assert_v731g_safe "${rollback_body}" "practice-runtime-load rollback"
require_contains "${rollback_body}" "practice-runtime-load rollback" '"load_status"[[:space:]]*:[[:space:]]*"rolled_back"'

final_status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-31g/status")"
assert_v731g_safe "${final_status_body}" "v7-31g/status final"
require_contains "${final_status_body}" "v7-31g/status final" '"blocked_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${final_status_body}" "v7-31g/status final" '"usage_event_count"[[:space:]]*:[[:space:]]*[1-9]'

pass "personal practice runtime controlled loading v7.31g"
