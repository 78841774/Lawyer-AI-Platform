#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Case OS Release Candidate APIs"
endpoints=(
  "/case-os/release-candidate/status"
  "/case-os/release-candidate/summary"
  "/case-os/release-candidate/checklist"
  "/case-os/release-candidate/readiness"
  "/case-os/release-candidate/audit"
  "/case-os/release-candidate/release-notes-preview"
  "/case-os/${CASE_ID}/release-candidate/case-readiness"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_field_false_required "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_required "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_required "${body}" "${endpoint}" "final_report_generated"
  assert_metadata_safe "${body}" "${endpoint}"
  if [ "${endpoint}" = "/case-os/release-candidate/release-notes-preview" ]; then
    assert_field_false_required "${body}" "${endpoint}" "would_create_file"
    assert_field_false_required "${body}" "${endpoint}" "would_generate_final_report"
    assert_field_false_required "${body}" "${endpoint}" "would_generate_legal_opinion"
    assert_field_false_required "${body}" "${endpoint}" "would_include_raw_content"
  fi
  if printf '%s' "${endpoint}" | grep -Eq '/case-os/release-candidate/(status|summary|readiness|release-notes-preview)$'; then
    if ! printf '%s' "${body}" | grep -Eq '"next_major_version"[[:space:]]*:[[:space:]]*"[^"]*Personal Production Workspace Foundation'; then
      fail "${endpoint} expected next_major_version to include Personal Production Workspace Foundation"
    fi
  fi
done

pass "case os release candidate APIs"
