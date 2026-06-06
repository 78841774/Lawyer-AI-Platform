#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Case Analysis Improvement v7.34"
cd "${REPO_ROOT}"

bash "${SCRIPT_DIR}/check_personal_case_analysis_workbench_v733_apis.sh" >/dev/null

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

assert_v734_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "improvement_candidate_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "training_gate_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "key_value_read"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "provider_payload_returned"
  require_false_field "${body}" "${label}" "source_content_returned"
  require_false_field "${body}" "${label}" "case_material_returned"
  require_false_field "${body}" "${label}" "loaded_package_mutated"
  require_false_field "${body}" "${label}" "loaded_package_auto_mutated"
  require_false_field "${body}" "${label}" "lawyer_approved_package_auto_mutated"
  require_false_field "${body}" "${label}" "output_schema_auto_mutated"
  require_false_field "${body}" "${label}" "runtime_package_auto_replaced"
  require_false_field "${body}" "${label}" "training_triggered"
  require_false_field "${body}" "${label}" "training_dataset_auto_built"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "package_disable_auto_executed"
  require_false_field "${body}" "${label}" "package_rollback_auto_executed"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/v7-34/status")"
assert_v734_safe "${status_body}" "v7-34/status"
require_contains "${status_body}" "v7-34/status" '"feedback_to_improvement_mapper_ready"[[:space:]]*:[[:space:]]*true'

build_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/build" '{"explicit_metadata_only_confirmation":true,"explicit_no_package_mutation_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_schema_mutation_confirmation":true}')"
assert_v734_safe "${build_body}" "candidate build"
require_contains "${build_body}" "candidate build" '"candidate_count"[[:space:]]*:[[:space:]]*[1-9]'
candidate_id="$(extract_first_field "${build_body}" "candidates" "candidate_id")"
if [ -z "${candidate_id}" ]; then
  fail "missing candidate_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/case-analysis-improvement/status" \
  "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates" \
  "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}" \
  "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}/readiness" \
  "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}/audit" \
  "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}/source-trace"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v734_safe "${body}" "${endpoint}"
done

ready_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}/mark-ready" '{"explicit_metadata_only_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_package_mutation_confirmation":true}')"
assert_v734_safe "${ready_body}" "mark ready"
require_contains "${ready_body}" "mark ready" '"readiness_status"[[:space:]]*:[[:space:]]*"ready_for_training_dataset_build"'

traces_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-improvement/output-traces")"
assert_v734_safe "${traces_body}" "output traces"
require_contains "${traces_body}" "output traces" '"trace_count"[[:space:]]*:[[:space:]]*[1-9]'
trace_id="$(extract_first_field "${traces_body}" "output_traces" "trace_id")"
if [ -z "${trace_id}" ]; then
  fail "missing trace_id"
fi
trace_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-improvement/output-traces/${trace_id}")"
assert_v734_safe "${trace_body}" "trace detail"

diff_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-improvement/diff/build" '{}')"
assert_v734_safe "${diff_body}" "diff build"
require_contains "${diff_body}" "diff build" '"diff_summary"[[:space:]]*:'
diff_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin)["diff_id"])' <<<"${diff_body}")"

diffs_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-improvement/diffs")"
assert_v734_safe "${diffs_body}" "diff list"
require_contains "${diffs_body}" "diff list" '"diff_count"[[:space:]]*:[[:space:]]*[1-9]'
diff_detail_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-analysis-improvement/diffs/${diff_id}")"
assert_v734_safe "${diff_detail_body}" "diff detail"

archive_body="$(post_json "/personal-skill-studio/training-artifacts/case-analysis-improvement/candidates/${candidate_id}/archive" '{"explicit_metadata_only_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_package_mutation_confirmation":true}')"
assert_v734_safe "${archive_body}" "archive candidate"
require_contains "${archive_body}" "archive candidate" '"candidate_status"[[:space:]]*:[[:space:]]*"archived"'

pass "personal case analysis improvement v7.34"
