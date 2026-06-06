#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

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

assert_skill_final_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'OPENAI_API_KEY|DEEPSEEK|API_KEY[[:space:]]*[:=]'
  assert_absent "${body}" "${label}" 'SECRET[[:space:]]*[:=]|TOKEN[[:space:]]*[:=]|PASSWORD[[:space:]]*[:=]|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '/Users/'
  assert_absent "${body}" "${label}" 'storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR 原文|真实案件原文|真实案件材料'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "downloadable_by_owner_only"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "quality_reference_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "blocks_next_stage"
  require_false_field "${body}" "${label}" "final_skill_published"
  require_false_field "${body}" "${label}" "skill_auto_published"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "open_case_data_used"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "api_key_exposed"
}

section "Personal Skill Final Draft APIs v7.22"

list_body="$(check_endpoint_200 "/personal-skill-studio/final-drafts")"
assert_skill_final_safe "${list_body}" "/personal-skill-studio/final-drafts"
assert_absent "${list_body}" "final-drafts list" '已自动发布|发布成功|无需律师|自动胜诉|保证准确'

for skill_id in case_fact_extraction_skill case_legal_analysis_skill; do
  for endpoint in \
    "/personal-skill-studio/final-drafts/${skill_id}" \
    "/personal-skill-studio/final-drafts/${skill_id}/lineage" \
    "/personal-skill-studio/final-drafts/${skill_id}/baseline" \
    "/personal-skill-studio/final-drafts/${skill_id}/quality" \
    "/personal-skill-studio/final-drafts/${skill_id}/gate" \
    "/personal-skill-studio/final-drafts/${skill_id}/optimization" \
    "/personal-skill-studio/final-drafts/${skill_id}/source-traces" \
    "/personal-skill-studio/final-drafts/${skill_id}/audit"; do
    body="$(check_endpoint_200 "${endpoint}")"
    assert_skill_final_safe "${body}" "${endpoint}"
  done

  download_body="$(
    curl -fsS \
      -H "Content-Type: application/json" \
      -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
      -d '{
        "requested_format":"Markdown",
        "explicit_owner_confirmation":true,
        "explicit_no_public_link_confirmation":true,
        "explicit_no_email_confirmation":true,
        "explicit_no_external_delivery_confirmation":true,
        "explicit_no_auto_publish_confirmation":true
      }' \
      "${API_BASE}/personal-skill-studio/final-drafts/${skill_id}/owner-downloads/mock"
  )"
  assert_skill_final_safe "${download_body}" "${skill_id} owner-downloads/mock"
  require_false_field "${download_body}" "${skill_id} owner-downloads/mock" "file_generated"
  require_false_field "${download_body}" "${skill_id} owner-downloads/mock" "file_path_visible"
done

downloads_body="$(check_endpoint_200 "/personal-skill-studio/final-draft-downloads")"
assert_skill_final_safe "${downloads_body}" "/personal-skill-studio/final-draft-downloads"

download_id="$(printf '%s' "${downloads_body}" | sed -n 's/.*"download_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -n "${download_id}" ]; then
  download_detail="$(check_endpoint_200 "/personal-skill-studio/final-draft-downloads/${download_id}")"
  assert_skill_final_safe "${download_detail}" "final-draft-download detail"
fi

safety_body="$(check_endpoint_200 "/personal-skill-studio/final-drafts-safety")"
assert_skill_final_safe "${safety_body}" "/personal-skill-studio/final-drafts-safety"

pass "personal skill final draft APIs v7.22"
