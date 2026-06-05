#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Case OS Quality APIs"
endpoints=(
  "/case-os/${CASE_ID}/quality/status"
  "/case-os/${CASE_ID}/quality/checklist"
  "/case-os/${CASE_ID}/quality/score"
  "/case-os/${CASE_ID}/quality/findings"
  "/case-os/${CASE_ID}/quality/recommendations"
  "/case-os/${CASE_ID}/quality/report-preview"
  "/case-os/${CASE_ID}/quality/summary"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_field_false_required "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_if_present "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${endpoint}" "final_report_generated"
  assert_metadata_safe "${body}" "${endpoint}"
  if [ "${endpoint}" = "/case-os/${CASE_ID}/quality/recommendations" ]; then
    assert_field_false_if_present "${body}" "${endpoint}" "would_execute_action"
  fi
  if [ "${endpoint}" = "/case-os/${CASE_ID}/quality/report-preview" ]; then
    assert_field_false_required "${body}" "${endpoint}" "would_create_file"
    assert_field_false_required "${body}" "${endpoint}" "would_generate_final_report"
    assert_field_false_required "${body}" "${endpoint}" "would_generate_legal_opinion"
    assert_field_false_required "${body}" "${endpoint}" "would_include_raw_content"
  fi
done

pass "case os quality APIs"
