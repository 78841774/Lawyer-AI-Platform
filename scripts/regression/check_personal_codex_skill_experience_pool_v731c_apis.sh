#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Codex Skill Experience Pool v7.31c"
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

extract_id() {
  local body="$1"
  local field="$2"
  printf '%s' "${body}" | sed -n "s/.*\"${field}\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p" | head -n 1
}

assert_v731c_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|secret|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
  assert_absent "${body}" "${label}" 'Bearer[[:space:]]+[A-Za-z0-9._-]+|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "local_private_processing_only"
  require_true_field "${body}" "${label}" "redacted_output_only"
  require_true_field "${body}" "${label}" "approved_experience_only"
  require_true_field "${body}" "${label}" "manual_review_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "provider_call_executed"
  require_false_field "${body}" "${label}" "credential_value_returned"
  require_false_field "${body}" "${label}" "unreviewed_experience_imported"
  require_false_field "${body}" "${label}" "unsafe_experience_imported"
  require_false_field "${body}" "${label}" "missing_source_trace_imported"
  require_false_field "${body}" "${label}" "formal_training_set_generated"
  require_false_field "${body}" "${label}" "real_codex_training_triggered"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "skill_publishable"
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

ocr_body="$(post_json "/personal-skill-studio/training-artifacts/ocr-jobs" '{
  "material_label":"authorized_lawyer_work_product_metadata_001",
  "owner_user_id":"owner_local_demo",
  "document_type":"case_work_product",
  "page_count":8,
  "explicit_authorized_case_confirmation":true,
  "explicit_internal_processing_confirmation":true,
  "explicit_no_provider_confirmation":true,
  "explicit_no_raw_return_confirmation":true
}')"
ocr_job_id="$(extract_id "${ocr_body}" "job_id")"
if [ -z "${ocr_job_id}" ]; then
  fail "setup ocr job missing job_id"
fi

retrieval_body="$(post_json "/personal-skill-studio/training-artifacts/legal-retrieval-jobs" "{
  \"source_ocr_job_id\":\"${ocr_job_id}\",
  \"query_label\":\"contract_dispute_experience_basis\",
  \"owner_user_id\":\"owner_local_demo\",
  \"explicit_no_provider_confirmation\":true,
  \"explicit_no_key_value_confirmation\":true,
  \"explicit_demo_safe_confirmation\":true
}")"
retrieval_job_id="$(extract_id "${retrieval_body}" "retrieval_job_id")"
if [ -z "${retrieval_job_id}" ]; then
  fail "setup legal retrieval missing retrieval_job_id"
fi

candidates_body="$(post_json "/personal-skill-studio/training-artifacts/experience-candidates/build" "{
  \"source_ocr_job_id\":\"${ocr_job_id}\",
  \"source_legal_retrieval_job_id\":\"${retrieval_job_id}\",
  \"owner_user_id\":\"owner_local_demo\",
  \"explicit_redaction_required_confirmation\":true,
  \"explicit_manual_review_required_confirmation\":true,
  \"explicit_no_skill_publish_confirmation\":true
}")"
candidate_id="$(extract_id "${candidates_body}" "candidate_id")"
if [ -z "${candidate_id}" ]; then
  fail "setup experience candidates missing candidate_id"
fi

rejected_import_body="$(post_json "/personal-skill-studio/training-artifacts/skill-experience-pool/import-approved" "{\"source_candidate_ids\":[\"${candidate_id}\"],\"owner_user_id\":\"owner_local_demo\",\"explicit_approved_experience_only_confirmation\":true,\"explicit_redacted_output_only_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
assert_v731c_safe "${rejected_import_body}" "import-approved before review"
require_contains "${rejected_import_body}" "import-approved before review" '"imported_count"[[:space:]]*:[[:space:]]*0'
require_contains "${rejected_import_body}" "import-approved before review" '"rejected_count"[[:space:]]*:[[:space:]]*1'

post_json "/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/redact" '{}' >/dev/null
post_json "/personal-skill-studio/training-artifacts/experience-candidates/${candidate_id}/review" '{
  "action":"approve",
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"experience candidate metadata review only",
  "explicit_manual_review_confirmation":true,
  "explicit_no_raw_return_confirmation":true,
  "explicit_no_skill_publish_confirmation":true
}' >/dev/null

status_body="$(check_endpoint_200 "/personal-skill-studio/training-artifacts/skill-experience-pool/status")"
assert_v731c_safe "${status_body}" "skill-experience-pool/status"

import_body="$(post_json "/personal-skill-studio/training-artifacts/skill-experience-pool/import-approved" "{\"source_candidate_ids\":[\"${candidate_id}\"],\"owner_user_id\":\"owner_local_demo\",\"explicit_approved_experience_only_confirmation\":true,\"explicit_redacted_output_only_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
assert_v731c_safe "${import_body}" "skill-experience-pool/import-approved"
require_contains "${import_body}" "skill-experience-pool/import-approved" '"imported_count"[[:space:]]*:[[:space:]]*1'
experience_id="$(extract_id "${import_body}" "experience_id")"
if [ -z "${experience_id}" ]; then
  fail "skill-experience-pool/import-approved did not return experience_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/skill-experience-pool" \
  "/personal-skill-studio/training-artifacts/skill-experience-pool/${experience_id}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731c_safe "${body}" "${endpoint}"
done

binding_body="$(post_json "/personal-skill-studio/training-artifacts/skill-experience-bindings" "{\"experience_ids\":[\"${experience_id}\"],\"skill_domain\":\"case_analysis\",\"skill_name_candidate\":\"案件经验提炼 Skill 草案\",\"case_cause_scope\":\"demo_safe_case_cause_scope\",\"experience_types\":[],\"draft_target_id\":\"codex_skill_draft_target_v731c\"}")"
assert_v731c_safe "${binding_body}" "skill-experience-bindings create"
binding_id="$(extract_id "${binding_body}" "binding_id")"
if [ -z "${binding_id}" ]; then
  fail "skill-experience-bindings create did not return binding_id"
fi

for endpoint in \
  "/personal-skill-studio/training-artifacts/skill-experience-bindings" \
  "/personal-skill-studio/training-artifacts/skill-experience-bindings/${binding_id}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731c_safe "${body}" "${endpoint}"
done

draft_body="$(post_json "/personal-skill-studio/training-artifacts/codex-skill-drafts/build" "{\"experience_ids\":[\"${experience_id}\"],\"binding_id\":\"${binding_id}\",\"draft_name\":\"Codex Skill 草案 v7.31c\",\"draft_target_id\":\"codex_skill_draft_target_v731c\",\"explicit_approved_experience_only_confirmation\":true,\"explicit_no_provider_confirmation\":true,\"explicit_no_real_training_confirmation\":true,\"explicit_no_skill_publish_confirmation\":true}")"
assert_v731c_safe "${draft_body}" "codex-skill-drafts/build"
draft_id="$(extract_id "${draft_body}" "draft_id")"
if [ -z "${draft_id}" ]; then
  fail "codex-skill-drafts/build did not return draft_id"
fi
require_contains "${draft_body}" "codex-skill-drafts/build" '"publish_status"[[:space:]]*:[[:space:]]*"not_publishable"'
require_contains "${draft_body}" "codex-skill-drafts/build" '"training_status"[[:space:]]*:[[:space:]]*"not_training_ready"'

for endpoint in \
  "/personal-skill-studio/training-artifacts/codex-skill-drafts" \
  "/personal-skill-studio/training-artifacts/codex-skill-drafts/${draft_id}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731c_safe "${body}" "${endpoint}"
done

review_body="$(post_json "/personal-skill-studio/training-artifacts/codex-skill-drafts/${draft_id}/review" '{
  "action":"approve_draft_structure",
  "reviewer_id":"local_demo_lawyer",
  "reviewer_note":"draft structure review only",
  "explicit_manual_confirmation":true,
  "explicit_no_skill_publish_confirmation":true,
  "explicit_no_real_training_confirmation":true
}')"
assert_v731c_safe "${review_body}" "codex-skill-draft review"
require_contains "${review_body}" "codex-skill-draft review" '"confirmation_status"[[:space:]]*:[[:space:]]*"structure_approved_requires_pre_publish_gate"'
require_false_field "${review_body}" "codex-skill-draft review" "skill_published"
require_false_field "${review_body}" "codex-skill-draft review" "real_training_triggered"

for endpoint in \
  "/personal-skill-studio/training-artifacts/codex-skill-drafts/${draft_id}/audit" \
  "/personal-skill-studio/training-artifacts/v7-31c/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_v731c_safe "${body}" "${endpoint}"
done

pass "personal codex skill experience pool v7.31c"
