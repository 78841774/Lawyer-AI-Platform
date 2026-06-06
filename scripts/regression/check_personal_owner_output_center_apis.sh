#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Owner-only Output Center APIs v7.23"
cd "${REPO_ROOT}"

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

assert_owner_output_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" 'API key|OPENAI_API_KEY|DEEPSEEK|API_KEY[[:space:]]*[:=]|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR 原文|真实案件原文|真实案件材料|身份证号|银行卡号|手机号|客户姓名'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "owner_access_required"
  require_true_field "${body}" "${label}" "downloadable_by_owner_only"
  require_true_field "${body}" "${label}" "draft_or_metadata"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "quality_reference_only"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "audit_required"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "third_party_share_enabled"
  require_false_field "${body}" "${label}" "client_auto_delivery"
  require_false_field "${body}" "${label}" "final_legal_opinion_auto_generated"
  require_false_field "${body}" "${label}" "final_report_auto_generated"
  require_false_field "${body}" "${label}" "final_skill_published"
  require_false_field "${body}" "${label}" "skill_auto_published"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "blocks_next_stage"
  require_false_field "${body}" "${label}" "api_key_exposed"
}

for endpoint in \
  "/personal-owner-output-center/status" \
  "/personal-owner-output-center/outputs" \
  "/personal-owner-output-center/downloads" \
  "/personal-owner-output-center/audit" \
  "/personal-owner-output-center/safety"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_owner_output_safe "${body}" "${endpoint}"
done

outputs_body="$(check_endpoint_200 "/personal-owner-output-center/outputs")"
output_id="$(printf '%s' "${outputs_body}" | sed -n 's/.*"output_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${output_id}" ]; then
  fail "owner output center did not return output_id"
fi

for endpoint in \
  "/personal-owner-output-center/outputs/${output_id}" \
  "/personal-owner-output-center/outputs/${output_id}/quality" \
  "/personal-owner-output-center/outputs/${output_id}/gate" \
  "/personal-owner-output-center/outputs/${output_id}/optimization" \
  "/personal-owner-output-center/outputs/${output_id}/source-traces"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_owner_output_safe "${body}" "${endpoint}"
done

download_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "owner_user_id":"local_owner",
      "requested_format":"markdown",
      "explicit_owner_confirmation":true,
      "explicit_no_public_link_confirmation":true,
      "explicit_no_email_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-owner-output-center/outputs/${output_id}/downloads/mock"
)"
assert_owner_output_safe "${download_body}" "owner output download mock"
require_false_field "${download_body}" "owner output download mock" "file_generated"
require_false_field "${download_body}" "owner output download mock" "file_path_visible"

download_id="$(printf '%s' "${download_body}" | sed -n 's/.*"download_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${download_id}" ]; then
  fail "owner output download did not return download_id"
fi

downloads_body="$(check_endpoint_200 "/personal-owner-output-center/downloads")"
assert_owner_output_safe "${downloads_body}" "/personal-owner-output-center/downloads"

download_detail_body="$(check_endpoint_200 "/personal-owner-output-center/downloads/${download_id}")"
assert_owner_output_safe "${download_detail_body}" "/personal-owner-output-center/downloads/${download_id}"

pass "personal owner-only output center APIs v7.23"
