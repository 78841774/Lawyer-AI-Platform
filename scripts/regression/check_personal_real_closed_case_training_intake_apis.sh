#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Real Closed Case Training Intake v7.31a"
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

require_contains() {
  local body="$1"
  local label="$2"
  local pattern="$3"
  if ! printf '%s' "${body}" | grep -Eq "${pattern}"; then
    fail "${label} expected pattern: ${pattern}"
  fi
}

assert_real_closed_case_intake_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|pycache|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR content|raw case content|raw provider response|customer name|ID number|phone number|客户姓名|身份证号|手机号'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "closed_case_only"
  require_true_field "${body}" "${label}" "real_closed_case_intake"
  require_true_field "${body}" "${label}" "redaction_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "manual_review_required"
  require_false_field "${body}" "${label}" "open_case_data_used"
  require_false_field "${body}" "${label}" "raw_content_included"
  require_false_field "${body}" "${label}" "raw_ocr_content_included"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "secret_value_returned"
  require_false_field "${body}" "${label}" "local_path_exposed"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
}

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/real-closed-case-intake/status")"
assert_real_closed_case_intake_safe "${status_body}" "real-closed-case-intake/status"

create_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_reference_label":"authorized_closed_case_training_metadata_001",
      "owner_user_id":"owner_local_demo",
      "authorization_confirmed":true,
      "case_closed_confirmed":true,
      "target_case_cause_path":["civil","contract_dispute","sales_contract_dispute"],
      "target_skill_ids":["case_fact_extraction_skill","case_legal_analysis_skill"],
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_open_case_confirmation":true,
      "explicit_no_provider_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/real-closed-case-intake/mock"
)"
assert_real_closed_case_intake_safe "${create_body}" "real-closed-case-intake/mock"
require_contains "${create_body}" "real-closed-case-intake/mock" '"source_case_mode"[[:space:]]*:[[:space:]]*"real_closed_case"'
require_contains "${create_body}" "real-closed-case-intake/mock" '"authorization_confirmed"[[:space:]]*:[[:space:]]*true'
require_contains "${create_body}" "real-closed-case-intake/mock" '"case_closed_confirmed"[[:space:]]*:[[:space:]]*true'

intake_id="$(printf '%s' "${create_body}" | sed -n 's/.*"intake_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${intake_id}" ]; then
  fail "real-closed-case-intake/mock did not return intake_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/redaction-report" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/case-cause-classification" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/segments" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/review-queue" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/source-traces" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/audit" \
  "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_real_closed_case_intake_safe "${body}" "${endpoint}"
done

redaction_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/redaction/mock"
)"
assert_real_closed_case_intake_safe "${redaction_body}" "redaction/mock"
require_true_field "${redaction_body}" "redaction/mock" "redaction_completed"
require_true_field "${redaction_body}" "redaction/mock" "personal_identifiers_removed"
require_true_field "${redaction_body}" "redaction/mock" "legal_relevance_preserved"

classification_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/case-cause-classification/mock"
)"
assert_real_closed_case_intake_safe "${classification_body}" "case-cause-classification/mock"
require_contains "${classification_body}" "case-cause-classification/mock" '"case_cause_path"'
require_contains "${classification_body}" "case-cause-classification/mock" '"manual_review_required"[[:space:]]*:[[:space:]]*true'

segments_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/segments/mock"
)"
assert_real_closed_case_intake_safe "${segments_body}" "segments/mock"
require_contains "${segments_body}" "segments/mock" '"fact_summary"'
require_contains "${segments_body}" "segments/mock" '"legal_issues"'
require_contains "${segments_body}" "segments/mock" '"case_fact_extraction_skill"'
require_contains "${segments_body}" "segments/mock" '"case_legal_analysis_skill"'

review_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/review-queue")"
review_item_id="$(printf '%s' "${review_body}" | sed -n 's/.*"review_item_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${review_item_id}" ]; then
  fail "review-queue did not return review_item_id"
fi
review_action_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"approve_metadata_only",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"metadata review only",
      "explicit_manual_review_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_training_set_write_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/training-artifacts/real-closed-case-intakes/${intake_id}/review-queue/${review_item_id}/actions/mock"
)"
assert_real_closed_case_intake_safe "${review_action_body}" "review action"
require_contains "${review_action_body}" "review action" '"approved_metadata_only"'

pass "personal real closed case training intake v7.31a"
