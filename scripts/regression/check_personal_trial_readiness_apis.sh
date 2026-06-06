#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Practical Case Trial Readiness APIs v7.25"
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

assert_trial_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'OPENAI_API_KEY|DEEPSEEK|API_KEY[[:space:]]*[:=]|SECRET|TOKEN|PASSWORD|BEGIN PRIVATE KEY|sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" '\.env|local\.db|/Users/|storage/runtime|node_modules|__pycache__|\.DS_Store'
  assert_absent "${body}" "${label}" 'raw OCR 原文|真实案件原文|真实案件材料|客户姓名|身份证号|手机号|银行卡号'
  require_true_field "${body}" "${label}" "owner_only"
  require_true_field "${body}" "${label}" "trial_metadata_only"
  require_true_field "${body}" "${label}" "metadata_only"
  require_true_field "${body}" "${label}" "draft_only"
  require_true_field "${body}" "${label}" "gate_reference_only"
  require_true_field "${body}" "${label}" "audit_required"
  require_true_field "${body}" "${label}" "source_trace_required"
  require_true_field "${body}" "${label}" "lawyer_review_required"
  require_false_field "${body}" "${label}" "raw_case_content_included"
  require_false_field "${body}" "${label}" "raw_ocr_content_included"
  require_false_field "${body}" "${label}" "api_key_exposed"
  require_false_field "${body}" "${label}" "provider_live_call_triggered"
  require_false_field "${body}" "${label}" "public_link_created"
  require_false_field "${body}" "${label}" "email_sent"
  require_false_field "${body}" "${label}" "external_delivery_triggered"
  require_false_field "${body}" "${label}" "final_legal_opinion_generated"
  require_false_field "${body}" "${label}" "final_report_generated"
  require_false_field "${body}" "${label}" "training_data_generated"
  require_false_field "${body}" "${label}" "writes_to_training_set"
  require_false_field "${body}" "${label}" "skill_updated"
  require_false_field "${body}" "${label}" "skill_published"
  require_false_field "${body}" "${label}" "blocks_next_stage"
}

for endpoint in \
  "/personal-trial-readiness/status" \
  "/personal-trial-readiness/checklist" \
  "/personal-trial-readiness/safety" \
  "/personal-trial-readiness/trials" \
  "/personal-trial-readiness/issues" \
  "/personal-trial-readiness/optimization-backlog" \
  "/personal-trial-readiness/audit"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_trial_safe "${body}" "${endpoint}"
done

trial_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "trial_name":"个人版实战试运行样本",
      "case_mode":"synthetic_case",
      "owner_user_id":"local_owner",
      "case_reference_label":"合成试运行样本",
      "explicit_owner_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_provider_confirmation":true,
      "explicit_no_training_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-trial-readiness/trials/mock"
)"
assert_trial_safe "${trial_body}" "trials/mock"
trial_id="$(printf '%s' "${trial_body}" | sed -n 's/.*"trial_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${trial_id}" ]; then
  fail "trials/mock did not return trial_id"
fi

for endpoint in \
  "/personal-trial-readiness/trials/${trial_id}" \
  "/personal-trial-readiness/trials/${trial_id}/checklist" \
  "/personal-trial-readiness/trials/${trial_id}/observations" \
  "/personal-trial-readiness/trials/${trial_id}/issues" \
  "/personal-trial-readiness/trials/${trial_id}/quality" \
  "/personal-trial-readiness/trials/${trial_id}/safety-confirmation"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_trial_safe "${body}" "${endpoint}"
done

checklist_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-trial-readiness/trials/${trial_id}/checklist/mock"
)"
assert_trial_safe "${checklist_body}" "checklist/mock"

observation_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{"stage_id":"legal_analysis_draft","notes":"仅记录试运行观察 metadata","issue_count":1}' \
    "${API_BASE}/personal-trial-readiness/trials/${trial_id}/observations/mock"
)"
assert_trial_safe "${observation_body}" "observations/mock"

issue_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "stage_id":"owner_output_center",
      "issue_type":"workflow",
      "severity":"low",
      "title":"本人下载边界提示可继续强化",
      "description":"问题记录只用于优化，不阻断下一步。",
      "suggested_fix":"在 v7.26 优化按钮旁提示。"
    }' \
    "${API_BASE}/personal-trial-readiness/trials/${trial_id}/issues/mock"
)"
assert_trial_safe "${issue_body}" "issues/mock"
require_false_field "${issue_body}" "issues/mock" "blocks_trial"
issue_id="$(printf '%s' "${issue_body}" | sed -n 's/.*"issue_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)"
if [ -z "${issue_id}" ]; then
  fail "issues/mock did not return issue_id"
fi

issue_detail="$(check_endpoint_200 "/personal-trial-readiness/issues/${issue_id}")"
assert_trial_safe "${issue_detail}" "/personal-trial-readiness/issues/${issue_id}"

quality_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-trial-readiness/trials/${trial_id}/quality/mock"
)"
assert_trial_safe "${quality_body}" "quality/mock"

safety_confirmation_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{}' \
    "${API_BASE}/personal-trial-readiness/trials/${trial_id}/safety-confirmation/mock"
)"
assert_trial_safe "${safety_confirmation_body}" "safety-confirmation/mock"
require_true_field "${safety_confirmation_body}" "safety-confirmation/mock" "no_open_case_training_confirmed"
require_true_field "${safety_confirmation_body}" "safety-confirmation/mock" "no_skill_auto_publish_confirmed"

backlog_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"source_trial_id\":\"${trial_id}\",
      \"source_issue_ids\":[\"${issue_id}\"],
      \"priority\":\"medium\",
      \"target_area\":\"trial_readiness\",
      \"title\":\"v7.26 试运行反馈优化\",
      \"description\":\"汇总试运行问题记录，用于下一轮优化。\",
      \"recommended_version\":\"v7.26\"
    }" \
    "${API_BASE}/personal-trial-readiness/optimization-backlog/mock"
)"
assert_trial_safe "${backlog_body}" "optimization-backlog/mock"

for endpoint in \
  "/personal-trial-readiness/trials/${trial_id}/observations" \
  "/personal-trial-readiness/trials/${trial_id}/issues" \
  "/personal-trial-readiness/issues" \
  "/personal-trial-readiness/optimization-backlog"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_trial_safe "${body}" "${endpoint} after actions"
done

pass "personal practical case trial readiness APIs v7.25"

