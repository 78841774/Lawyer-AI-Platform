#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Case OS Core APIs"
endpoints=(
  "/case-os/${CASE_ID}"
  "/case-os/${CASE_ID}/audit-timeline"
  "/case-os/${CASE_ID}/next-action"
  "/case-os/${CASE_ID}/safety-checklist"
  "/case-os/${CASE_ID}/stage-orchestration"
  "/case-os/${CASE_ID}/stage-transitions"
  "/case-os/${CASE_ID}/action-eligibility"
  "/case-os/${CASE_ID}/blockers"
  "/case-os/${CASE_ID}/audit-timeline/unified"
  "/case-os/${CASE_ID}/audit-timeline/summary"
  "/case-os/${CASE_ID}/audit-timeline/redaction-check"
  "/case-os/${CASE_ID}/audit-timeline/filters"
  "/case-os/${CASE_ID}/review-state"
  "/case-os/${CASE_ID}/review-state/history"
  "/case-os/${CASE_ID}/review-state/transitions"
  "/case-os/${CASE_ID}/review-state/summary"
  "/case-os/${CASE_ID}/metadata-closure"
  "/case-os/${CASE_ID}/metadata-closure/checklist"
  "/case-os/${CASE_ID}/metadata-closure/blockers"
  "/case-os/${CASE_ID}/metadata-closure/export-preview"
  "/case-os/${CASE_ID}/export-packages/status"
  "/case-os/${CASE_ID}/export-packages/summary"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_metadata_safe "${body}" "${endpoint}"
done

pass "case os core APIs"
