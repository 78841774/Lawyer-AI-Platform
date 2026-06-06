#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training Artifact Loader v7.30"
cd "${REPO_ROOT}"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/training_artifacts"

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

assert_training_artifact_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR|real case content|raw provider response|customer name|ID number|phone number|客户姓名|身份证号|手机号'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "training_artifact_only"
  require_true_field "${body}" "${label}" "codex_training_scheme"
  require_true_field "${body}" "${label}" "closed_case_only"
  require_true_field "${body}" "${label}" "case_cause_taxonomy_required"
  require_true_field "${body}" "${label}" "multi_level_case_cause_enabled"
  require_true_field "${body}" "${label}" "case_cause_match_required"
  require_true_field "${body}" "${label}" "fallback_supported"
  require_true_field "${body}" "${label}" "load_dry_run"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "fine_tune_model_training"
  require_false_field "${body}" "${label}" "open_case_data_used"
  require_false_field "${body}" "${label}" "raw_content_included"
  require_false_field "${body}" "${label}" "raw_ocr_content_included"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "secret_value_returned"
  require_false_field "${body}" "${label}" "local_path_exposed"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "skill_auto_published"
  require_false_field "${body}" "${label}" "load_executed"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "blocks_next_stage"
}

for endpoint in \
  "/personal-skill-studio/training-artifacts/status" \
  "/personal-skill-studio/training-artifacts/scheme" \
  "/personal-skill-studio/training-artifacts/case-cause-taxonomy" \
  "/personal-skill-studio/training-artifacts/packages" \
  "/personal-skill-studio/training-artifacts/skills" \
  "/personal-skill-studio/training-artifacts/evaluations" \
  "/personal-skill-studio/training-artifacts/gates" \
  "/personal-skill-studio/training-artifacts/test-cases" \
  "/personal-skill-studio/training-artifacts/loading-manifests" \
  "/personal-skill-studio/training-artifacts/load-dry-runs" \
  "/personal-skill-studio/training-artifacts/skill-contexts" \
  "/personal-skill-studio/training-artifacts/audit" \
  "/personal-skill-studio/training-artifacts/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_training_artifact_safe "${body}" "${endpoint}"
done

taxonomy_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-cause-taxonomy")"
case_cause_id="$(printf '%s' "${taxonomy_body}" | sed -n 's/.*"case_cause_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${case_cause_id}" ]; then
  fail "taxonomy did not return case_cause_id"
fi
node_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/case-cause-taxonomy/${case_cause_id}")"
assert_training_artifact_safe "${node_body}" "case-cause-taxonomy/${case_cause_id}"

packages_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/packages")"
package_id="$(printf '%s' "${packages_body}" | sed -n 's/.*"package_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${package_id}" ]; then
  fail "packages did not return package_id"
fi
package_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/packages/${package_id}")"
assert_training_artifact_safe "${package_body}" "packages/${package_id}"

skills_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/skills")"
skill_id="$(printf '%s' "${skills_body}" | sed -n 's/.*"skill_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${skill_id}" ]; then
  fail "skills did not return skill_id"
fi
skill_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/skills/${skill_id}")"
assert_training_artifact_safe "${skill_body}" "skills/${skill_id}"

match_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_domain":"civil",
      "case_cause_level_1":"contract_dispute",
      "case_cause_level_2":"sales_contract_dispute",
      "case_cause_level_3":"",
      "case_cause_name":"买卖合同纠纷",
      "case_cause_code":"civil.contract.sales",
      "case_cause_path":["civil","contract_dispute","sales_contract_dispute"],
      "evidence_types":["contract","invoice","delivery_record"]
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/case-cause-match/mock"
)"
assert_training_artifact_safe "${match_body}" "case-cause-match/mock"
require_true_field "${match_body}" "case-cause-match/mock" "fallback_supported"

dry_run_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_domain":"civil",
      "case_cause_level_1":"contract_dispute",
      "case_cause_level_2":"sales_contract_dispute",
      "case_cause_level_3":"",
      "case_cause_name":"买卖合同纠纷",
      "case_cause_code":"civil.contract.sales",
      "case_cause_path":["civil","contract_dispute","sales_contract_dispute"],
      "evidence_types":["contract","invoice","delivery_record"],
      "target_skill_ids":["case_fact_extraction_skill","case_legal_analysis_skill"],
      "explicit_dry_run_confirmation":true,
      "explicit_no_training_confirmation":true,
      "explicit_no_open_case_training_confirmation":true,
      "explicit_no_auto_publish_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/load-dry-run/mock"
)"
assert_training_artifact_safe "${dry_run_body}" "load-dry-run/mock"
run_id="$(printf '%s' "${dry_run_body}" | sed -n 's/.*"run_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
skill_context_id="$(printf '%s' "${dry_run_body}" | sed -n 's/.*"skill_context_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${run_id}" ] || [ -z "${skill_context_id}" ]; then
  fail "load dry-run did not return run_id and skill_context_id"
fi

run_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/load-dry-runs/${run_id}")"
assert_training_artifact_safe "${run_body}" "load-dry-runs/${run_id}"
context_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/skill-contexts/${skill_context_id}")"
assert_training_artifact_safe "${context_body}" "skill-contexts/${skill_context_id}"

pass "personal training artifact loader v7.30"

