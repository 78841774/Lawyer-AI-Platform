#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Codex Training Dry Run v7.36"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_training_dataset_v735_apis.sh" >/dev/null

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

assert_v736_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "codex_skill_dry_run"
  require_true_field "${body}" "${label}" "internal_training_simulation_only"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "sensitive_metadata_scan_passed"
  require_false_field "${body}" "${label}" "provider_access_attempted"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
  require_false_field "${body}" "${label}" "loaded_package_mutated"
  require_false_field "${body}" "${label}" "loaded_package_auto_mutated"
  require_false_field "${body}" "${label}" "lawyer_approved_package_auto_mutated"
  require_false_field "${body}" "${label}" "runtime_package_written"
  require_false_field "${body}" "${label}" "runtime_package_replaced"
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

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-dryrun/status")"
assert_v736_safe "${status_body}" "training dryrun status"
require_contains "${status_body}" "training dryrun status" '"dryrun_engine_ready"[[:space:]]*:[[:space:]]*true'

run_body="$(post_json "/personal-skill-studio/training-artifacts/training-dryrun/run" '{"explicit_internal_dry_run_confirmation":true,"explicit_no_provider_confirmation":true,"explicit_no_key_read_confirmation":true,"explicit_no_runtime_package_write_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_skill_publish_confirmation":true}')"
assert_v736_safe "${run_body}" "training dryrun run"
require_contains "${run_body}" "training dryrun run" '"run_status"[[:space:]]*:[[:space:]]*"dryrun_completed_reference_only"'
require_contains "${run_body}" "training dryrun run" '"training_gate_status"[[:space:]]*:[[:space:]]*"passed_reference_only"'
require_contains "${run_body}" "training dryrun run" '"loaded_metadata_refs"[[:space:]]*:'
require_contains "${run_body}" "training dryrun run" '"audit_id"[[:space:]]*:'
require_contains "${run_body}" "training dryrun run" '"source_trace_id"[[:space:]]*:'

logs_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-dryrun/logs")"
assert_v736_safe "${logs_body}" "training dryrun logs"
require_contains "${logs_body}" "training dryrun logs" '"log_count"[[:space:]]*:[[:space:]]*[1-9]'
require_contains "${logs_body}" "training dryrun logs" '"step_name"[[:space:]]*:'
require_contains "${logs_body}" "training dryrun logs" '"step_status"[[:space:]]*:'

gate_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/training-dryrun/gate-report")"
assert_v736_safe "${gate_body}" "training dryrun gate report"
require_contains "${gate_body}" "training dryrun gate report" '"gate_status"[[:space:]]*:[[:space:]]*"passed_reference_only"'
require_contains "${gate_body}" "training dryrun gate report" '"provider_boundary_safe"[[:space:]]*:[[:space:]]*true'
require_contains "${gate_body}" "training dryrun gate report" '"key_boundary_safe"[[:space:]]*:[[:space:]]*true'
require_contains "${gate_body}" "training dryrun gate report" '"runtime_package_boundary_safe"[[:space:]]*:[[:space:]]*true'
require_contains "${gate_body}" "training dryrun gate report" '"training_boundary_safe"[[:space:]]*:[[:space:]]*true'

pass "personal codex training dryrun v7.36"
