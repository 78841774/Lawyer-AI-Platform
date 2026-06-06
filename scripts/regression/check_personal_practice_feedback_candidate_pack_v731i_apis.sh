#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Practice Feedback Candidate Pack v7.31i"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_practice_feedback_v731h_apis.sh" >/dev/null

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

post_json() {
  local endpoint="$1"
  local payload="$2"
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "${payload}" \
    "${API_BASE}${endpoint}"
}

assert_v731i_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "feedback_candidate_pack_only"
  require_true_field "${body}" "${label}" "next_iteration_candidate_only"
  require_true_field "${body}" "${label}" "redacted_abstracted_experience_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "feedback_auto_mutates_loaded_package"
  require_false_field "${body}" "${label}" "candidate_pack_auto_mutates_loaded_package"
  require_false_field "${body}" "${label}" "loaded_package_mutated"
  require_false_field "${body}" "${label}" "lawyer_approved_package_mutated"
  require_false_field "${body}" "${label}" "runtime_policy_changed"
  require_false_field "${body}" "${label}" "package_auto_disabled"
  require_false_field "${body}" "${label}" "package_auto_rolled_back"
  require_false_field "${body}" "${label}" "next_package_draft_auto_loaded"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_result_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "source_material_returned"
  require_false_field "${body}" "${label}" "full_output_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
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

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-31i/status")"
assert_v731i_safe "${status_body}" "v7-31i/status"
require_contains "${status_body}" "v7-31i/status" '"candidate_pack_registry_ready"[[:space:]]*:[[:space:]]*true'
require_contains "${status_body}" "v7-31i/status" '"triaged_feedback_count"[[:space:]]*:[[:space:]]*[1-9]'

build_body="$(post_json "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/build" '{
  "proposed_next_package_name":"v7.31i metadata-only next iteration candidate",
  "proposed_next_package_version":"v7.31i-candidate.1",
  "build_requested_by":"local_demo_lawyer",
  "explicit_triaged_feedback_only_confirmation":true,
  "explicit_no_loaded_package_mutation_confirmation":true,
  "explicit_no_lawyer_approved_package_mutation_confirmation":true,
  "explicit_no_runtime_policy_change_confirmation":true,
  "explicit_no_auto_disable_confirmation":true,
  "explicit_no_auto_rollback_confirmation":true,
  "explicit_no_training_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}')"
assert_v731i_safe "${build_body}" "practice-feedback-candidate-packs build"
require_contains "${build_body}" "practice-feedback-candidate-packs build" '"candidate_status"[[:space:]]*:[[:space:]]*"draft_candidate_pack"'
require_contains "${build_body}" "practice-feedback-candidate-packs build" '"proposed_changes_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${build_body}" "practice-feedback-candidate-packs build" '"added_risk_warnings"[[:space:]]*:[[:space:]]*\['
candidate_pack_id="$(extract_id "${build_body}" "candidate_pack_id")"
if [ -z "${candidate_pack_id}" ]; then
  fail "missing candidate_pack_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/status" \
  "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs" \
  "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}" \
  "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}/diff" \
  "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}/audit" \
  "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}/source-trace" \
  "/personal-skill-studio/training-artifacts/v7-31i/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731i_safe "${body}" "${endpoint}"
done

diff_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}/diff")"
require_contains "${diff_body}" "candidate pack diff" '"proposed_changes_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${diff_body}" "candidate pack diff" '"added_risk_warnings"[[:space:]]*:[[:space:]]*\['
require_contains "${diff_body}" "candidate pack diff" '"candidate_pack_auto_mutates_loaded_package"[[:space:]]*:[[:space:]]*false'
require_contains "${diff_body}" "candidate pack diff" '"loaded_package_mutated"[[:space:]]*:[[:space:]]*false'
require_contains "${diff_body}" "candidate pack diff" '"next_package_draft_auto_loaded"[[:space:]]*:[[:space:]]*false'

ready_body="$(post_json "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}/mark-ready" '{
  "actor_id":"local_demo_lawyer",
  "actor_note":"标记为可进入 v7.31j rebuild 准备，不自动加载。",
  "explicit_no_loaded_package_mutation_confirmation":true,
  "explicit_no_lawyer_approved_package_mutation_confirmation":true,
  "explicit_no_runtime_policy_change_confirmation":true,
  "explicit_no_training_confirmation":true
}')"
assert_v731i_safe "${ready_body}" "candidate pack mark-ready"
require_contains "${ready_body}" "candidate pack mark-ready" '"candidate_status"[[:space:]]*:[[:space:]]*"ready_for_next_experience_build"'

archive_body="$(post_json "/personal-skill-studio/training-artifacts/practice-feedback-candidate-packs/${candidate_pack_id}/archive" '{
  "actor_id":"local_demo_lawyer",
  "actor_note":"回归测试归档候选包 metadata。",
  "explicit_no_loaded_package_mutation_confirmation":true,
  "explicit_no_lawyer_approved_package_mutation_confirmation":true,
  "explicit_no_runtime_policy_change_confirmation":true,
  "explicit_no_training_confirmation":true
}')"
assert_v731i_safe "${archive_body}" "candidate pack archive"
require_contains "${archive_body}" "candidate pack archive" '"candidate_status"[[:space:]]*:[[:space:]]*"archived"'

pass "personal practice feedback candidate pack v7.31i"
