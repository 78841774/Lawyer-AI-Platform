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
    curl -sS -o /tmp/personal_delivery_packet_regression_error.json -w "%{http_code}" \
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

assert_delivery_packet_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_absent "${body}" "${label}" '自动胜诉'
  assert_absent "${body}" "${label}" '替代律师'
  assert_absent "${body}" "${label}" '保证准确'
  assert_absent "${body}" "${label}" '一键交付'
  assert_absent "${body}" "${label}" '自动完成客户交付'
  assert_absent "${body}" "${label}" '自动发送客户'
  assert_absent "${body}" "${label}" '最终法律意见正文'
  assert_absent "${body}" "${label}" '最终报告正文'
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "raw_case_content_read"
  assert_field_false_if_present "${body}" "${label}" "raw_content_returned"
  assert_field_false_if_present "${body}" "${label}" "live_provider_call_executed"
  assert_field_false_if_present "${body}" "${label}" "live_provider_called"
  assert_field_false_if_present "${body}" "${label}" "api_key_accessed"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_triggered"
  assert_field_false_if_present "${body}" "${label}" "external_delivery_ready"
  assert_field_false_if_present "${body}" "${label}" "email_sent"
  assert_field_false_if_present "${body}" "${label}" "final_file_generated"
  assert_field_false_if_present "${body}" "${label}" "auto_delivery_enabled"
}

section "Personal Delivery Packet APIs"

rm -rf "${REPO_ROOT}/Lawyer-AI-Platform-App/backend/storage/runtime/personal_delivery_packet"

endpoints=(
  "/personal-delivery-packet/status"
  "/personal-delivery-packet/runtimes"
  "/personal-delivery-packet/runtimes/delivery_packet_runtime"
  "/personal-delivery-packet/runtimes/packet_item_runtime"
  "/personal-delivery-packet/runtimes/source_bundle_runtime"
  "/personal-delivery-packet/runtimes/export_readiness_engine"
  "/personal-delivery-packet/runtimes/final_lock_engine"
  "/personal-delivery-packet/packets"
  "/personal-delivery-packet/packet-items"
  "/personal-delivery-packet/source-bundles"
  "/personal-delivery-packet/export-readiness"
  "/personal-delivery-packet/final-locks"
  "/personal-delivery-packet/review-summaries"
  "/personal-delivery-packet/audit"
  "/personal-delivery-packet/safety"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_delivery_packet_safe "${body}" "${endpoint}"
done

packet_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "production_case_id":"case_v55_approve_all",
      "workflow_run_id":"workflow_run_demo",
      "packet_title":"个人生产交付包草案",
      "packet_scope":"律师复核前 metadata 汇总",
      "client_alias":"client_demo",
      "delivery_purpose":"受控导出准备度检查",
      "explicit_mock_confirmation":true,
      "explicit_lawyer_review_confirmation":true,
      "explicit_no_raw_content_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-delivery-packet/packets/mock"
)"
assert_delivery_packet_safe "${packet_body}" "packets/mock"
assert_field_false_required "${packet_body}" "packets/mock" "raw_content_included"
assert_field_false_required "${packet_body}" "packets/mock" "raw_case_content_read"
assert_field_false_required "${packet_body}" "packets/mock" "final_legal_opinion_generated"
assert_field_false_required "${packet_body}" "packets/mock" "final_report_generated"
assert_field_false_required "${packet_body}" "packets/mock" "external_delivery_triggered"
assert_field_false_required "${packet_body}" "packets/mock" "email_sent"
assert_field_false_required "${packet_body}" "packets/mock" "final_file_generated"
require_true_field "${packet_body}" "packets/mock" "requires_lawyer_review"
require_true_field "${packet_body}" "packets/mock" "final_lock_required"
require_true_field "${packet_body}" "packets/mock" "source_trace_required"

delivery_packet_id="$(printf '%s' "${packet_body}" | sed -n 's/.*"delivery_packet_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${delivery_packet_id}" ]; then
  fail "packets/mock did not return delivery_packet_id"
fi

packet_detail="$(check_endpoint_200 "/personal-delivery-packet/packets/${delivery_packet_id}")"
assert_delivery_packet_safe "${packet_detail}" "packet detail"

expect_request_failure "packet missing confirmation" "/personal-delivery-packet/packets/mock" '{
  "production_case_id":"case_v55_approve_all",
  "packet_title":"个人生产交付包草案",
  "packet_scope":"律师复核前 metadata 汇总",
  "client_alias":"client_demo",
  "delivery_purpose":"受控导出准备度检查"
}'

item_types=(
  "case_metadata_summary"
  "material_processing_summary"
  "ai_draft_summary"
  "intelligence_summary"
  "skill_studio_summary"
  "lawyer_review_summary"
  "source_trace_summary"
  "export_placeholder"
)

last_item_id=""
for item_type in "${item_types[@]}"; do
  item_body="$(
    curl -fsS \
      -H "Content-Type: application/json" \
      -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
      -d "{
        \"delivery_packet_id\":\"${delivery_packet_id}\",
        \"item_title\":\"${item_type} 草案\",
        \"item_type\":\"${item_type}\",
        \"linked_object_type\":\"mock_metadata\",
        \"linked_object_id\":\"${item_type}_demo\",
        \"source_trace_ids\":[\"trace_${item_type}\"],
        \"explicit_mock_confirmation\":true,
        \"explicit_no_raw_content_confirmation\":true,
        \"explicit_no_final_opinion_confirmation\":true
      }" \
      "${API_BASE}/personal-delivery-packet/packet-items/mock"
  )"
  assert_delivery_packet_safe "${item_body}" "packet-items/mock ${item_type}"
  assert_field_false_required "${item_body}" "packet-items/mock ${item_type}" "raw_content_included"
  require_true_field "${item_body}" "packet-items/mock ${item_type}" "requires_lawyer_review"
  require_true_field "${item_body}" "packet-items/mock ${item_type}" "source_trace_required"
  last_item_id="$(printf '%s' "${item_body}" | sed -n 's/.*"packet_item_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
done

if [ -z "${last_item_id}" ]; then
  fail "packet-items/mock did not return packet_item_id"
fi

item_detail="$(check_endpoint_200 "/personal-delivery-packet/packet-items/${last_item_id}")"
assert_delivery_packet_safe "${item_detail}" "packet item detail"

expect_request_failure "packet item invalid type" "/personal-delivery-packet/packet-items/mock" "{
  \"delivery_packet_id\":\"${delivery_packet_id}\",
  \"item_title\":\"非法交付项\",
  \"item_type\":\"final_opinion_body\",
  \"linked_object_type\":\"mock_metadata\",
  \"linked_object_id\":\"invalid_demo\",
  \"source_trace_ids\":[],
  \"explicit_mock_confirmation\":true,
  \"explicit_no_raw_content_confirmation\":true,
  \"explicit_no_final_opinion_confirmation\":true
}"

bundle_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d "{
      \"delivery_packet_id\":\"${delivery_packet_id}\",
      \"source_trace_ids\":[\"trace_case_demo\",\"trace_material_demo\",\"trace_review_demo\"],
      \"bundle_scope\":\"交付包来源追踪 metadata\",
      \"explicit_mock_confirmation\":true,
      \"explicit_source_trace_confirmation\":true,
      \"explicit_no_raw_content_confirmation\":true
    }" \
    "${API_BASE}/personal-delivery-packet/source-bundles/mock"
)"
assert_delivery_packet_safe "${bundle_body}" "source-bundles/mock"
assert_field_false_required "${bundle_body}" "source-bundles/mock" "raw_content_included"
assert_field_false_required "${bundle_body}" "source-bundles/mock" "raw_content_returned"
require_true_field "${bundle_body}" "source-bundles/mock" "source_trace_required"

source_bundle_id="$(printf '%s' "${bundle_body}" | sed -n 's/.*"source_bundle_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
if [ -z "${source_bundle_id}" ]; then
  fail "source-bundles/mock did not return source_bundle_id"
fi

bundle_detail="$(check_endpoint_200 "/personal-delivery-packet/source-bundles/${source_bundle_id}")"
assert_delivery_packet_safe "${bundle_detail}" "source bundle detail"

expect_request_failure "source bundle missing confirmation" "/personal-delivery-packet/source-bundles/mock" "{
  \"delivery_packet_id\":\"${delivery_packet_id}\",
  \"source_trace_ids\":[\"trace_case_demo\"],
  \"bundle_scope\":\"交付包来源追踪 metadata\"
}"

readiness_body="$(check_endpoint_200 "/personal-delivery-packet/export-readiness/${delivery_packet_id}")"
assert_delivery_packet_safe "${readiness_body}" "export readiness detail"
require_true_field "${readiness_body}" "export readiness detail" "source_trace_complete"
require_true_field "${readiness_body}" "export readiness detail" "final_lock_ready"
assert_field_false_required "${readiness_body}" "export readiness detail" "export_ready"
assert_field_false_required "${readiness_body}" "export readiness detail" "external_delivery_ready"

review_body="$(check_endpoint_200 "/personal-delivery-packet/review-summaries/${delivery_packet_id}")"
assert_delivery_packet_safe "${review_body}" "review summary detail"
assert_field_false_required "${review_body}" "review summary detail" "raw_content_included"

lock_body="$(
  curl -fsS \
    -H "Content-Type: application/json" \
    -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" \
    -d '{
      "action":"lock_for_controlled_export",
      "reviewer_id":"local_demo_lawyer",
      "reviewer_note":"metadata only",
      "explicit_lawyer_confirmation":true,
      "explicit_final_lock_confirmation":true,
      "explicit_no_real_export_confirmation":true,
      "explicit_no_email_confirmation":true,
      "explicit_no_final_opinion_confirmation":true,
      "explicit_no_final_report_confirmation":true,
      "explicit_no_external_delivery_confirmation":true
    }' \
    "${API_BASE}/personal-delivery-packet/final-locks/${delivery_packet_id}/actions"
)"
assert_delivery_packet_safe "${lock_body}" "final lock action"
assert_field_false_required "${lock_body}" "final lock action" "export_ready"
assert_field_false_required "${lock_body}" "final lock action" "external_delivery_ready"
assert_field_false_required "${lock_body}" "final lock action" "final_legal_opinion_generated"
assert_field_false_required "${lock_body}" "final lock action" "final_report_generated"
assert_field_false_required "${lock_body}" "final lock action" "external_delivery_triggered"
assert_field_false_required "${lock_body}" "final lock action" "email_sent"
assert_field_false_required "${lock_body}" "final lock action" "final_file_generated"
require_true_field "${lock_body}" "final lock action" "final_locked"

locked_packet="$(check_endpoint_200 "/personal-delivery-packet/packets/${delivery_packet_id}")"
assert_delivery_packet_safe "${locked_packet}" "locked packet detail"
require_true_field "${locked_packet}" "locked packet detail" "final_locked"
assert_field_false_required "${locked_packet}" "locked packet detail" "external_delivery_triggered"

expect_request_failure "locked packet item mutation blocked" "/personal-delivery-packet/packet-items/mock" "{
  \"delivery_packet_id\":\"${delivery_packet_id}\",
  \"item_title\":\"锁定后修改尝试\",
  \"item_type\":\"case_metadata_summary\",
  \"linked_object_type\":\"mock_metadata\",
  \"linked_object_id\":\"blocked_after_lock\",
  \"source_trace_ids\":[],
  \"explicit_mock_confirmation\":true,
  \"explicit_no_raw_content_confirmation\":true,
  \"explicit_no_final_opinion_confirmation\":true
}"

expect_request_failure "final lock invalid action" "/personal-delivery-packet/final-locks/${delivery_packet_id}/actions" '{
  "action":"send_email_to_client",
  "reviewer_id":"local_demo_lawyer",
  "explicit_lawyer_confirmation":true,
  "explicit_final_lock_confirmation":true,
  "explicit_no_real_export_confirmation":true,
  "explicit_no_email_confirmation":true,
  "explicit_no_final_opinion_confirmation":true,
  "explicit_no_final_report_confirmation":true,
  "explicit_no_external_delivery_confirmation":true
}'

packets_body="$(check_endpoint_200 "/personal-delivery-packet/packets")"
items_body="$(check_endpoint_200 "/personal-delivery-packet/packet-items")"
bundles_body="$(check_endpoint_200 "/personal-delivery-packet/source-bundles")"
readiness_list_body="$(check_endpoint_200 "/personal-delivery-packet/export-readiness")"
locks_body="$(check_endpoint_200 "/personal-delivery-packet/final-locks")"
reviews_body="$(check_endpoint_200 "/personal-delivery-packet/review-summaries")"
audit_body="$(check_endpoint_200 "/personal-delivery-packet/audit")"
safety_body="$(check_endpoint_200 "/personal-delivery-packet/safety")"
assert_delivery_packet_safe "${packets_body}" "packets list"
assert_delivery_packet_safe "${items_body}" "packet items list"
assert_delivery_packet_safe "${bundles_body}" "source bundles list"
assert_delivery_packet_safe "${readiness_list_body}" "readiness list"
assert_delivery_packet_safe "${locks_body}" "final locks list"
assert_delivery_packet_safe "${reviews_body}" "review summaries list"
assert_delivery_packet_safe "${audit_body}" "audit"
assert_delivery_packet_safe "${safety_body}" "safety"

pass "personal delivery packet APIs"
