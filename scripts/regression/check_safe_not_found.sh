#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Safe Not Found"
endpoints=(
  "/case-os/not_exist_case"
  "/case-os/not_exist_case/quality/status"
  "/case-os/not_exist_case/quality/summary"
  "/case-os/not_exist_case/hardening/safety-check"
  "/case-os/not_exist_case/metadata-closure"
  "/case-os/not_exist_case/export-packages/status"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_metadata_safe "${body}" "${endpoint}"
  assert_no_stack_trace "${body}" "${endpoint}"
done

pass "safe not_found checks"
