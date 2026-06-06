#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training Dataset v7.35"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_case_analysis_workbench_v733_apis.sh" >/dev/null

post_json() {
  local endpoint="$1"
  local payload="${2:-{}}"
  local response
  response="$(curl -sS \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -w '\n%{http_code}' \
    --json "${payload}" \
    "${API_BASE}${endpoint}")"
  local code="${response##*$'\n'}"
  local body="${response%$'\n'*}"
  if [[ ! "${code}" =~ ^2 ]]; then
    printf '%s\n' "${body}" >&2
    fail "POST ${endpoint} returned HTTP ${code}"
  fi
  printf '%s' "${body}"
}

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

extract_first_field() {
  local body="$1"
  local collection="$2"
  local field="$3"
  python3 -c 'import json,sys; data=json.load(sys.stdin); items=data.get(sys.argv[1], []); print(items[0].get(sys.argv[2], "")) if items else None' "${collection}" "${field}" <<<"${body}"
}

assert_v735_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "training_dataset_manifest_generated"
  require_true_field "${body}" "${label}" "training_examples_generated"
  require_true_field "${body}" "${label}" "training_task_plan_generated"
  require_true_field "${body}" "${label}" "training_gate_report_generated"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "source_trace_checked"
  require_true_field "${body}" "${label}" "candidate_audit_checked"
  require_true_field "${body}" "${label}" "sensitive_metadata_scan_passed"
  require_false_field "${body}" "${label}" "blocks_next_stage"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
  require_false_field "${body}" "${label}" "loaded_package_mutated"
  require_false_field "${body}" "${label}" "loaded_package_auto_mutated"
  require_false_field "${body}" "${label}" "lawyer_approved_package_auto_mutated"
  require_false_field "${body}" "${label}" "runtime_package_auto_replaced"
  require_false_field "${body}" "${label}" "training_triggered"
  require_false_field "${body}" "${label}" "formal_training_set_written"
  require_false_field "${body}" "${label}" "real_training_triggered"
  require_false_field "${body}" "${label}" "real_training_output_generated"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

candidate_build_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/build" '{"explicit_metadata_only_confirmation":true,"explicit_no_package_mutation_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_schema_mutation_confirmation":true}')"
candidate_id="$(extract_first_field "${candidate_build_body}" "candidates" "candidate_id")"
if [ -z "${candidate_id}" ]; then
  fail "missing candidate_id for v7.35"
fi
post_json "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}/mark-ready" '{"explicit_metadata_only_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_package_mutation_confirmation":true}' >/dev/null

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-dataset/status")"
assert_v735_safe "${status_body}" "training dataset status"
require_contains "${status_body}" "training dataset status" '"dataset_builder_ready"[[:space:]]*:[[:space:]]*true'

build_body="$(post_json "/personal-skill-studio/training-artifacts/training-dataset/build" '{"explicit_metadata_only_confirmation":true,"explicit_ready_candidate_only_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_package_mutation_confirmation":true,"explicit_no_skill_publish_confirmation":true}')"
assert_v735_safe "${build_body}" "training dataset build"
require_contains "${build_body}" "training dataset build" '"dataset_status"[[:space:]]*:[[:space:]]*"dataset_manifest_ready"'
require_contains "${build_body}" "training dataset build" '"example_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${build_body}" "training dataset build" '"candidate_id"[[:space:]]*:'
require_contains "${build_body}" "training dataset build" '"audit_id"[[:space:]]*:'
require_contains "${build_body}" "training dataset build" '"source_trace_id"[[:space:]]*:'

examples_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-dataset/examples")"
assert_v735_safe "${examples_body}" "training dataset examples"
require_contains "${examples_body}" "training dataset examples" '"example_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${examples_body}" "training dataset examples" '"training_input_summary"[[:space:]]*:'
require_contains "${examples_body}" "training dataset examples" '"training_target_summary"[[:space:]]*:'

gate_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-dataset/gate-report")"
assert_v735_safe "${gate_body}" "training dataset gate report"
require_contains "${gate_body}" "training dataset gate report" '"gate_status"[[:space:]]*:[[:space:]]*"passed_reference_only"'
require_contains "${gate_body}" "training dataset gate report" '"gate_summary"[[:space:]]*:'
require_contains "${gate_body}" "training dataset gate report" '"candidate_metadata_safe"[[:space:]]*:[[:space:]]*true'
require_contains "${gate_body}" "training dataset gate report" '"audit_source_trace_safe"[[:space:]]*:[[:space:]]*true'

pass "personal training dataset v7.35"
