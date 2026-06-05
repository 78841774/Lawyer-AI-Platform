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

expect_request_failure() {
  local label="$1"
  local endpoint="$2"
  local payload="$3"
  local status
  status="$(
    curl -sS -o /tmp/personal_skill_studio_regression_error.json -w "%{http_code}" \
      -H "Content-Type: application/json" \
      -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
      -d "${payload}" \
      "${API_BASE}${endpoint}"
  )"
  if [ "${status}" -lt 400 ]; then
    fail "${label} expected failure status, got ${status}"
  fi
  pass "${label} returned ${status}"
}

assert_skill_studio_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" '已自动发布'
  assert_absent "${body}" "${label}" '发布成功'
  assert_absent "${body}" "${label}" '替代律师'
  assert_absent "${body}" "${label}" '保证准确'
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "live_ai_call_executed"
  assert_field_false_if_present "${body}" "${label}" "auto_publish_enabled"
  assert_field_false_if_present "${body}" "${label}" "published_to_registry"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
}

section "Personal Skill Studio APIs"

endpoints=(
  "/personal-skill-studio/status"
  "/personal-skill-studio/runtimes"
  "/personal-skill-studio/runtimes/experience_package_studio_runtime"
  "/personal-skill-studio/runtimes/skill_candidate_studio_runtime"
  "/personal-skill-studio/runtimes/skill_test_case_runtime"
  "/personal-skill-studio/runtimes/skill_evaluation_runtime"
  "/personal-skill-studio/runtimes/controlled_promotion_gate"
  "/personal-skill-studio/experience-packages"
  "/personal-skill-studio/skill-candidates"
  "/personal-skill-studio/test-cases"
  "/personal-skill-studio/evaluations"
  "/personal-skill-studio/promotion-queue"
  "/personal-skill-studio/source-traces"
  "/personal-skill-studio/audit"
  "/personal-skill-studio/safety"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_skill_studio_safe "${body}" "${endpoint}"
done

package_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "case_id":"case_v55_approve_all",
      "source_trace_ids":[],
      "review_result_ids":[],
      "package_title":"合同纠纷经验包草案",
      "legal_area":"合同纠纷",
      "case_cause":"买卖合同纠纷",
      "jurisdiction":"中国大陆",
      "explicit_mock_confirmation":true,
      "explicit_source_trace_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_auto_publish_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/experience-packages/mock"
)"
assert_skill_studio_safe "${package_body}" "experience-packages/mock"
assert_field_false_required "${package_body}" "experience-packages/mock" "raw_content_included"
assert_field_false_required "${package_body}" "experience-packages/mock" "auto_publish_enabled"
assert_field_false_required "${package_body}" "experience-packages/mock" "final_legal_opinion_generated"
assert_field_false_required "${package_body}" "experience-packages/mock" "final_report_generated"
require_true_field "${package_body}" "experience-packages/mock" "requires_lawyer_review"
require_true_field "${package_body}" "experience-packages/mock" "source_trace_required"

experience_package_id="$(printf '%s' "${package_body}" | sed -n 's/.*"experience_package_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${experience_package_id}" ]; then
  fail "experience-packages/mock did not return experience_package_id"
fi

package_detail="$(check_endpoint_200 "/personal-skill-studio/experience-packages/${experience_package_id}")"
assert_skill_studio_safe "${package_detail}" "experience package detail"

expect_request_failure "experience-package missing confirmation" "/personal-skill-studio/experience-packages/mock" '{
  "case_id":"case_v55_approve_all",
  "source_trace_ids":[],
  "review_result_ids":[],
  "package_title":"合同纠纷经验包草案",
  "legal_area":"合同纠纷",
  "case_cause":"买卖合同纠纷",
  "jurisdiction":"中国大陆"
}'

candidate_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"experience_package_id\":\"${experience_package_id}\",
      \"skill_title\":\"合同纠纷技能候选草案\",
      \"skill_type\":\"draft_skill_candidate\",
      \"target_legal_area\":\"合同纠纷\",
      \"target_case_cause\":\"买卖合同纠纷\",
      \"explicit_mock_confirmation\":true,
      \"explicit_lawyer_review_confirmation\":true,
      \"explicit_no_auto_publish_confirmation\":true
    }" \
    "${API_BASE}/personal-skill-studio/skill-candidates/mock"
)"
assert_skill_studio_safe "${candidate_body}" "skill-candidates/mock"
assert_field_false_required "${candidate_body}" "skill-candidates/mock" "auto_publish_enabled"
assert_field_false_required "${candidate_body}" "skill-candidates/mock" "published_to_registry"
require_true_field "${candidate_body}" "skill-candidates/mock" "requires_lawyer_review"

skill_candidate_id="$(printf '%s' "${candidate_body}" | sed -n 's/.*"skill_candidate_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${skill_candidate_id}" ]; then
  fail "skill-candidates/mock did not return skill_candidate_id"
fi

candidate_detail="$(check_endpoint_200 "/personal-skill-studio/skill-candidates/${skill_candidate_id}")"
assert_skill_studio_safe "${candidate_detail}" "skill candidate detail"

expect_request_failure "skill-candidate missing confirmation" "/personal-skill-studio/skill-candidates/mock" "{
  \"experience_package_id\":\"${experience_package_id}\",
  \"skill_title\":\"合同纠纷技能候选草案\",
  \"skill_type\":\"draft_skill_candidate\",
  \"target_legal_area\":\"合同纠纷\",
  \"target_case_cause\":\"买卖合同纠纷\"
}"

test_case_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"skill_candidate_id\":\"${skill_candidate_id}\",
      \"test_case_title\":\"合同纠纷测试用例草案\",
      \"scenario_type\":\"metadata_only_scenario\",
      \"explicit_mock_confirmation\":true,
      \"explicit_no_raw_content_confirmation\":true
    }" \
    "${API_BASE}/personal-skill-studio/test-cases/mock"
)"
assert_skill_studio_safe "${test_case_body}" "test-cases/mock"
assert_field_false_required "${test_case_body}" "test-cases/mock" "raw_content_included"

test_case_id="$(printf '%s' "${test_case_body}" | sed -n 's/.*"test_case_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${test_case_id}" ]; then
  fail "test-cases/mock did not return test_case_id"
fi

test_case_detail="$(check_endpoint_200 "/personal-skill-studio/test-cases/${test_case_id}")"
assert_skill_studio_safe "${test_case_detail}" "test case detail"

evaluation_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"skill_candidate_id\":\"${skill_candidate_id}\",
      \"test_case_ids\":[\"${test_case_id}\"],
      \"evaluation_scope\":\"mock_safety_and_quality_check\",
      \"explicit_mock_confirmation\":true,
      \"explicit_manual_review_confirmation\":true,
      \"explicit_no_auto_publish_confirmation\":true
    }" \
    "${API_BASE}/personal-skill-studio/evaluations/mock"
)"
assert_skill_studio_safe "${evaluation_body}" "evaluations/mock"
assert_field_false_required "${evaluation_body}" "evaluations/mock" "auto_publish_enabled"
assert_field_false_required "${evaluation_body}" "evaluations/mock" "published_to_registry"
require_true_field "${evaluation_body}" "evaluations/mock" "requires_manual_review"
require_true_field "${evaluation_body}" "evaluations/mock" "requires_lawyer_review"

evaluation_id="$(printf '%s' "${evaluation_body}" | sed -n 's/.*"evaluation_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${evaluation_id}" ]; then
  fail "evaluations/mock did not return evaluation_id"
fi

evaluation_detail="$(check_endpoint_200 "/personal-skill-studio/evaluations/${evaluation_id}")"
assert_skill_studio_safe "${evaluation_detail}" "evaluation detail"

promotion_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"approve_for_future_review",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"metadata only",
      "explicit_manual_confirmation":true,
      "explicit_no_auto_publish_confirmation":true,
      "explicit_no_final_opinion_confirmation":true
    }' \
    "${API_BASE}/personal-skill-studio/promotion-queue/${skill_candidate_id}/actions"
)"
assert_skill_studio_safe "${promotion_body}" "promotion action"
assert_field_false_required "${promotion_body}" "promotion action" "auto_publish_enabled"
assert_field_false_required "${promotion_body}" "promotion action" "published_to_registry"
assert_field_false_required "${promotion_body}" "promotion action" "final_legal_opinion_generated"
assert_field_false_required "${promotion_body}" "promotion action" "final_report_generated"

expect_request_failure "promotion invalid action" "/personal-skill-studio/promotion-queue/${skill_candidate_id}/actions" '{
  "action":"invalid_action",
  "reviewer_id":"local_demo_lawyer",
  "explicit_manual_confirmation":true,
  "explicit_no_auto_publish_confirmation":true,
  "explicit_no_final_opinion_confirmation":true
}'

queue_body="$(check_endpoint_200 "/personal-skill-studio/promotion-queue")"
traces_body="$(check_endpoint_200 "/personal-skill-studio/source-traces")"
audit_body="$(check_endpoint_200 "/personal-skill-studio/audit")"
assert_skill_studio_safe "${queue_body}" "promotion queue"
assert_skill_studio_safe "${traces_body}" "source traces"
assert_skill_studio_safe "${audit_body}" "audit"

pass "personal skill studio APIs"
