#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Experience Lifecycle v7.32"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_next_experience_package_v731j_apis.sh" >/dev/null

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
  local payload="${2:-{}}"
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "${payload}" \
    "${API_BASE}${endpoint}"
}

assert_v732_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "lifecycle_view_only"
  require_true_field "${body}" "${label}" "redacted_abstracted_experience_only"
  require_true_field "${body}" "${label}" "lawyer_approval_required_for_runtime_load"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "feedback_does_not_mutate_loaded_package"
  require_true_field "${body}" "${label}" "candidate_pack_does_not_mutate_loaded_package"
  require_true_field "${body}" "${label}" "next_package_requires_load_review"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_result_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "source_material_returned"
  require_false_field "${body}" "${label}" "full_output_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
  require_false_field "${body}" "${label}" "loaded_package_mutated"
  require_false_field "${body}" "${label}" "next_package_draft_auto_loaded"
  require_false_field "${body}" "${label}" "automatic_training_triggered"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-32/status")"
assert_v732_safe "${status_body}" "v7-32/status"
require_contains "${status_body}" "v7-32/status" '"lifecycle_registry_ready"[[:space:]]*:[[:space:]]*true'
require_contains "${status_body}" "v7-32/status" '"stage_event_count"[[:space:]]*:[[:space:]]*[1-9]'

list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/experience-lifecycles")"
assert_v732_safe "${list_body}" "experience-lifecycles"
lifecycle_id="$(extract_id "${list_body}" "lifecycle_id")"
if [ -z "${lifecycle_id}" ]; then
  fail "missing lifecycle_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}" \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/state" \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/graph" \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/audit-timeline" \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/source-trace-view" \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/integrity-check" \
  "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/safety-summary"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v732_safe "${body}" "${endpoint}"
done

detail_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}")"
require_contains "${detail_body}" "experience lifecycle detail" '"current_stage"[[:space:]]*:'
require_contains "${detail_body}" "experience lifecycle detail" '"stage_events"[[:space:]]*:[[:space:]]*\['
require_contains "${detail_body}" "experience lifecycle detail" '"next_allowed_actions"[[:space:]]*:[[:space:]]*\['

graph_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/graph")"
require_contains "${graph_body}" "experience lifecycle graph" '"nodes"[[:space:]]*:[[:space:]]*\['
require_contains "${graph_body}" "experience lifecycle graph" '"edges"[[:space:]]*:[[:space:]]*\['
require_contains "${graph_body}" "experience lifecycle graph" '"lineage"[[:space:]]*:[[:space:]]*\['

integrity_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/integrity-check")"
require_contains "${integrity_body}" "experience lifecycle integrity" '"passed_checks"[[:space:]]*:[[:space:]]*\['
require_contains "${integrity_body}" "experience lifecycle integrity" '"recommended_actions"[[:space:]]*:[[:space:]]*\['

safety_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/safety-summary")"
require_contains "${safety_body}" "experience lifecycle safety" '"raw_content_absent"[[:space:]]*:[[:space:]]*true'
require_contains "${safety_body}" "experience lifecycle safety" '"ocr_payload_absent"[[:space:]]*:[[:space:]]*true'
require_contains "${safety_body}" "experience lifecycle safety" '"filesystem_location_absent"[[:space:]]*:[[:space:]]*true'
require_contains "${safety_body}" "experience lifecycle safety" '"credential_value_absent"[[:space:]]*:[[:space:]]*true'
require_contains "${safety_body}" "experience lifecycle safety" '"provider_payload_absent"[[:space:]]*:[[:space:]]*true'

recompute_body="$(post_json "/personal-skill-studio/training-artifacts/experience-lifecycles/${lifecycle_id}/recompute" '{}')"
assert_v732_safe "${recompute_body}" "experience lifecycle recompute"
require_contains "${recompute_body}" "experience lifecycle recompute" '"lifecycle_id"[[:space:]]*:[[:space:]]*"'"${lifecycle_id}"'"'

pass "personal experience lifecycle v7.32"
