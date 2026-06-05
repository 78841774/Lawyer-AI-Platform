#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Case OS Status APIs"
endpoints=(
  "/health"
  "/personal-alpha-workspace/status"
  "/personal-alpha-dashboard/status"
  "/personal-alpha-source-review/status"
  "/personal-alpha-final-readiness/status"
  "/personal-alpha-final-gate/status"
  "/personal-alpha-final-packet/status"
  "/personal-alpha-lawyer-final-review/status"
  "/personal-alpha-final-lock/status"
  "/case-os/status"
  "/case-os"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_field_false_if_present "${body}" "${endpoint}" "production_enabled"
  assert_field_false_if_present "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_if_present "${body}" "${endpoint}" "final_legal_opinion_enabled"
  assert_field_false_if_present "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${endpoint}" "final_report_generation_enabled"
  assert_field_false_if_present "${body}" "${endpoint}" "final_report_generated"
done

pass "case os status APIs"
