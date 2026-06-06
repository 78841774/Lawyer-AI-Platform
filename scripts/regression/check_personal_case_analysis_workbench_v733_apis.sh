#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Case Analysis Workbench v7.33"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_experience_lifecycle_v732_apis.sh" >/dev/null

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

extract_first_output_id() {
  python3 -c 'import json,sys; data=json.load(sys.stdin); print(data["outputs"][0]["output_id"])'
}

post_json() {
  local endpoint="$1"
  local payload="${2:-{}}"
  local attempt
  for attempt in 1 2 3; do
    local response
    response="$(curl -sS \
      -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
      -w '\n%{http_code}' \
      --json "${payload}" \
      "${API_BASE}${endpoint}")"
    local code="${response##*$'\n'}"
    local body="${response%$'\n'*}"
    if [[ "${code}" =~ ^2 ]]; then
      printf '%s' "${body}"
      return 0
    fi
    if [ "${attempt}" -lt 3 ]; then
      sleep 1
      continue
    fi
    printf '%s\n' "${body}" >&2
    fail "POST ${endpoint} returned HTTP ${code}"
  done
}

assert_v733_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "schema_driven_output_only"
  require_true_field "${body}" "${label}" "redacted_abstracted_output_only"
  require_true_field "${body}" "${label}" "frontend_output_definition_forbidden"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
  require_false_field "${body}" "${label}" "loaded_package_mutated"
  require_false_field "${body}" "${label}" "next_package_auto_generated"
  require_false_field "${body}" "${label}" "training_triggered"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-33/status")"
assert_v733_safe "${status_body}" "v7-33/status"
require_contains "${status_body}" "v7-33/status" '"skill_output_schema_ready"[[:space:]]*:[[:space:]]*true'
require_contains "${status_body}" "v7-33/status" '"output_count"[[:space:]]*:[[:space:]]*18'
require_contains "${status_body}" "v7-33/status" '"fact_group_count"[[:space:]]*:[[:space:]]*1'
require_contains "${status_body}" "v7-33/status" '"legal_analysis_group_count"[[:space:]]*:[[:space:]]*1'

list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-workbench/views")"
assert_v733_safe "${list_body}" "workbench views"
view_id="$(extract_id "${list_body}" "view_id")"
if [ -z "${view_id}" ]; then
  fail "missing workbench view_id"
fi

view_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-workbench/views/${view_id}")"
assert_v733_safe "${view_body}" "workbench view detail"
require_contains "${view_body}" "workbench view detail" '"summary_metrics"[[:space:]]*:'

schema_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-workbench/views/${view_id}/schema")"
assert_v733_safe "${schema_body}" "workbench schema"
require_contains "${schema_body}" "workbench schema" '"group_type"[[:space:]]*:[[:space:]]*"fact_extraction"'
require_contains "${schema_body}" "workbench schema" '"group_type"[[:space:]]*:[[:space:]]*"legal_analysis"'
require_contains "${schema_body}" "workbench schema" '"expected_count"[[:space:]]*:[[:space:]]*2'
require_contains "${schema_body}" "workbench schema" '"expected_count"[[:space:]]*:[[:space:]]*16'

outputs_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-workbench/views/${view_id}/outputs")"
assert_v733_safe "${outputs_body}" "workbench outputs"
require_contains "${outputs_body}" "workbench outputs" '"output_count"[[:space:]]*:[[:space:]]*18'
output_id="$(extract_id "${outputs_body}" "output_id")"
output_id="$(printf '%s' "${outputs_body}" | extract_first_output_id)"
if [ -z "${output_id}" ]; then
  fail "missing output_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}" \
  "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/feedback" \
  "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/risk-events" \
  "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/audit" \
  "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/source-trace"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v733_safe "${body}" "${endpoint}"
done

feedback_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/feedback" '{"reviewer_id":"owner_lawyer","feedback_type":"schema_output_feedback","feedback_summary":"metadata feedback for schema output","severity":"low","explicit_metadata_only_confirmation":true,"explicit_no_training_confirmation":true}')"
assert_v733_safe "${feedback_body}" "submit feedback"
require_contains "${feedback_body}" "submit feedback" '"feedback_status"[[:space:]]*:[[:space:]]*"submitted"'

risk_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/risk-event" '{"reporter_id":"owner_lawyer","risk_level":"medium","risk_summary":"metadata risk for lawyer review","mitigation_note":"assistive only","explicit_metadata_only_confirmation":true,"explicit_no_external_delivery_confirmation":true}')"
assert_v733_safe "${risk_body}" "submit risk event"
require_contains "${risk_body}" "submit risk event" '"risk_status"[[:space:]]*:[[:space:]]*"logged_for_lawyer_review"'

reviewed_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/mark-reviewed" '{}')"
assert_v733_safe "${reviewed_body}" "mark-reviewed"
require_contains "${reviewed_body}" "mark-reviewed" '"output_status"[[:space:]]*:[[:space:]]*"reviewed"'

feedback_list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/feedback")"
assert_v733_safe "${feedback_list_body}" "feedback list"
require_contains "${feedback_list_body}" "feedback list" '"feedback_count"[[:space:]]*:[[:space:]]*[1-9]'

risk_list_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/${output_id}/risk-events")"
assert_v733_safe "${risk_list_body}" "risk event list"
require_contains "${risk_list_body}" "risk event list" '"risk_event_count"[[:space:]]*:[[:space:]]*[1-9]'

pass "personal case analysis workbench v7.33"
