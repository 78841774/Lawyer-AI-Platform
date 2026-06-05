#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Metadata-only Responses"
endpoints=(
  "/case-os/${CASE_ID}/quality/summary"
  "/case-os/${CASE_ID}/quality/report-preview"
  "/case-os/${CASE_ID}/metadata-closure/export-preview"
  "/case-os/${CASE_ID}/export-packages/status"
  "/case-os/${CASE_ID}/audit-timeline/redaction-check"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_metadata_safe "${body}" "${endpoint}"
  assert_absent "${body}" "${endpoint}" 'raw material'
  assert_absent "${body}" "${endpoint}" 'raw OCR'
  assert_absent "${body}" "${endpoint}" 'raw legal search'
  assert_absent "${body}" "${endpoint}" '\.docx'
  assert_absent "${body}" "${endpoint}" '\.xlsx'
done

pass "metadata-only response checks"
