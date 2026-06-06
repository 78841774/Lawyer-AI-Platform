#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Practice Runtime Load Review v7.31f"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_internal_training_v731e_apis.sh" >/dev/null

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

assert_v731f_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted_payload|unredacted_material'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "generated_package_read_only"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "practice_load_review_required"
  require_true_field "${body}" "${label}" "approved_for_practice_load_required"
  require_true_field "${body}" "${label}" "redacted_output_only"
  require_true_field "${body}" "${label}" "abstracted_experience_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "sensitive_field_scan_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_result_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "source_material_returned"
  require_false_field "${body}" "${label}" "unreviewed_package_loaded"
  require_false_field "${body}" "${label}" "unredacted_content_loaded"
  require_false_field "${body}" "${label}" "non_pending_review_package_loaded"
  require_false_field "${body}" "${label}" "missing_source_trace_loaded"
  require_false_field "${body}" "${label}" "real_codex_training_triggered"
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

post_status() {
  local endpoint="$1"
  local payload="$2"
  curl -sS \
    -o /tmp/v731f_response_body.json \
    -w "%{http_code}" \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "${payload}" \
    "${API_BASE}${endpoint}"
}

packages_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-packages")"
training_package_id="$(extract_id "${packages_body}" "package_id")"
if [ -z "${training_package_id}" ]; then
  fail "v7.31e setup did not leave training package"
fi

review_list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-load-review/packages")"
assert_v731f_safe "${review_list_body}" "practice-load-review/packages"
require_contains "${review_list_body}" "practice-load-review/packages" '"review_status"[[:space:]]*:[[:space:]]*"pending_practice_load_review"'

review_detail_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}")"
assert_v731f_safe "${review_detail_body}" "practice-load-review detail"
require_contains "${review_detail_body}" "practice-load-review detail" '"generated_experience_package"'
require_contains "${review_detail_body}" "practice-load-review detail" '"generated_experience_text"'
require_contains "${review_detail_body}" "practice-load-review detail" '"lawyer_experience_text"'
card_id="$(extract_id "${review_detail_body}" "card_id")"
if [ -z "${card_id}" ]; then
  fail "practice-load-review detail missing card_id"
fi

early_approve_status="$(post_status "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/approve" '{
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"early approve should be rejected",
  "gray_load_enabled":true,
  "explicit_lawyer_review_confirmation":true,
  "explicit_system_revalidated_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_real_training_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}')"
if [ "${early_approve_status}" -lt 400 ]; then
  fail "approve before revalidation should be rejected"
fi
assert_no_stack_trace "$(cat /tmp/v731f_response_body.json)" "early approve"

edit_body="$(post_json "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/edit" '{
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"practice load editing started",
  "explicit_lawyer_review_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_raw_content_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}')"
assert_v731f_safe "${edit_body}" "practice-load-review edit"
require_contains "${edit_body}" "practice-load-review edit" '"review_status"[[:space:]]*:[[:space:]]*"review_editing"'

save_body="$(post_json "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/save" "{
  \"reviewer_id\":\"local_demo_lawyer\",
  \"reviewer_note\":\"lawyer edited experience metadata\",
  \"edited_cards\":[{
    \"card_id\":\"${card_id}\",
    \"title\":\"律师确认后的脱敏经验卡片\",
    \"lawyer_experience_text\":\"律师确认后的脱敏经验：适用于同类案由的事实组织、证据核验和风险提示，不替代律师判断。\",
    \"applicable_scenarios\":[\"同类案由的实战辅助提示\",\"律师复核后的灰度加载候选\"],
    \"not_applicable_scenarios\":[\"未脱敏材料\",\"自动最终法律意见\",\"未授权案件\"],
    \"risk_warnings\":[\"需结合个案事实和现行法律重新判断。\"],
    \"usage_boundaries\":[\"仅作实战加载前经验提示\",\"不得自动对外交付\"],
    \"gray_load_enabled\":true
  }],
  \"gray_load_enabled\":true,
  \"explicit_lawyer_review_confirmation\":true,
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_raw_content_confirmation\":true,
  \"explicit_no_skill_publish_confirmation\":true
}")"
assert_v731f_safe "${save_body}" "practice-load-review save"
require_contains "${save_body}" "practice-load-review save" '"review_status"[[:space:]]*:[[:space:]]*"review_changes_saved"'
require_contains "${save_body}" "practice-load-review save" '"validation_status"[[:space:]]*:[[:space:]]*"system_revalidation_required"'
require_contains "${save_body}" "practice-load-review save" '"lawyer_approved_experience_package"'

revalidate_body="$(post_json "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/revalidate" '{}')"
assert_v731f_safe "${revalidate_body}" "practice-load-review revalidate"
require_contains "${revalidate_body}" "practice-load-review revalidate" '"review_status"[[:space:]]*:[[:space:]]*"system_revalidated"'
require_contains "${revalidate_body}" "practice-load-review revalidate" '"validation_status"[[:space:]]*:[[:space:]]*"system_revalidated"'
require_true_field "${revalidate_body}" "practice-load-review revalidate" "revalidation_passed"
require_true_field "${revalidate_body}" "practice-load-review revalidate" "source_trace_complete"
require_true_field "${revalidate_body}" "practice-load-review revalidate" "audit_complete"
require_true_field "${revalidate_body}" "practice-load-review revalidate" "sensitive_field_scan_passed"

approve_body="$(post_json "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/approve" '{
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"approved for later controlled practice load",
  "gray_load_enabled":true,
  "explicit_lawyer_review_confirmation":true,
  "explicit_system_revalidated_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_real_training_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}')"
assert_v731f_safe "${approve_body}" "practice-load-review approve"
require_contains "${approve_body}" "practice-load-review approve" '"review_status"[[:space:]]*:[[:space:]]*"approved_for_practice_load"'
require_contains "${approve_body}" "practice-load-review approve" '"load_gate_status"[[:space:]]*:[[:space:]]*"approved_for_practice_load"'
require_true_field "${approve_body}" "practice-load-review approve" "can_load_to_practice_runtime"
require_true_field "${approve_body}" "practice-load-review approve" "gray_load_enabled"

task_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-tasks")"
training_task_id="$(extract_id "${task_body}" "training_task_id")"
if [ -z "${training_task_id}" ]; then
  fail "missing training_task_id for reject setup"
fi
reject_setup_body="$(post_json "/personal-skill-studio/training-artifacts/training-packages/build" "{
  \"source_training_task_id\":\"${training_task_id}\",
  \"source_skill_package_id\":null,
  \"package_name\":\"内部训练经验包 v7.31f reject setup\",
  \"package_version\":\"v7.31f-reject.0\",
  \"explicit_pending_practice_load_review_confirmation\":true,
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_real_training_confirmation\":true,
  \"explicit_no_skill_publish_confirmation\":true
}")"
reject_package_id="$(extract_id "${reject_setup_body}" "package_id")"
if [ -z "${reject_package_id}" ]; then
  fail "reject setup did not create package"
fi
check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-load-review/packages/${reject_package_id}" >/dev/null
reject_body="$(post_json "/personal-skill-studio/training-artifacts/practice-load-review/packages/${reject_package_id}/reject" '{
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"rejected for practice load metadata",
  "gray_load_enabled":false,
  "explicit_lawyer_review_confirmation":true,
  "explicit_system_revalidated_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_real_training_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}')"
assert_v731f_safe "${reject_body}" "practice-load-review reject"
require_contains "${reject_body}" "practice-load-review reject" '"review_status"[[:space:]]*:[[:space:]]*"rejected_for_practice_load"'
require_false_field "${reject_body}" "practice-load-review reject" "can_load_to_practice_runtime"

for endpoint in \
  "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/audit" \
  "/personal-skill-studio/training-artifacts/practice-load-review/packages/${training_package_id}/source-trace" \
  "/personal-skill-studio/training-artifacts/v7-31f/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731f_safe "${body}" "${endpoint}"
done

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-31f/status")"
require_contains "${status_body}" "v7-31f/status" '"approved_for_practice_load_count"[[:space:]]*:[[:space:]]*[1-9][0-9]*'
require_contains "${status_body}" "v7-31f/status" '"rejected_for_practice_load_count"[[:space:]]*:[[:space:]]*[1-9][0-9]*'

pass "personal practice runtime load review v7.31f"
