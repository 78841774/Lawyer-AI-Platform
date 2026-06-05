#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Case OS Hardening APIs"
endpoints=(
  "/case-os/hardening/status"
  "/case-os/${CASE_ID}/hardening/safety-check"
  "/case-os/${CASE_ID}/hardening/response-consistency"
  "/case-os/${CASE_ID}/hardening/runtime-storage-check"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_field_false_required "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_required "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_required "${body}" "${endpoint}" "final_report_generated"
  assert_metadata_safe "${body}" "${endpoint}"
  if [ "${endpoint}" = "/case-os/hardening/status" ]; then
    if ! printf '%s' "${body}" | grep -Eq '"safe_response_enabled"[[:space:]]*:[[:space:]]*true'; then
      fail "${endpoint} expected safe_response_enabled=true"
    fi
  fi
  if [ "${endpoint}" = "/case-os/${CASE_ID}/hardening/runtime-storage-check" ]; then
    assert_field_false_required "${body}" "${endpoint}" "absolute_path_returned"
    assert_field_false_required "${body}" "${endpoint}" "tracked_path_write_enabled"
  fi
done

pass "case os hardening APIs"
