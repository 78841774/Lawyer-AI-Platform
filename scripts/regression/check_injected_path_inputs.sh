#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Injected Path-like Inputs"
INJECTED_CASE_ID="%2FUsers%2Ftest%2Freal_cases%2Fclient.pdf"
endpoints=(
  "/case-os/${INJECTED_CASE_ID}/quality/summary"
  "/case-os/${INJECTED_CASE_ID}/hardening/safety-check"
  "/case-os/${INJECTED_CASE_ID}/metadata-closure"
  "/case-os/${INJECTED_CASE_ID}/export-packages/status"
  "/case-os/${INJECTED_CASE_ID}/audit-timeline/unified"
  "/case-os/${INJECTED_CASE_ID}/review-state"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_metadata_safe "${body}" "${endpoint}"
done

pass "injected/path-like input checks"
