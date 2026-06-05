#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Production APIs"
endpoints=(
  "/personal-production/status"
  "/personal-production/mode"
  "/personal-production/showcase"
  "/personal-production/runtime-registry"
  "/personal-production/provider-capabilities"
  "/personal-production/readiness"
  "/personal-production/safety"
  "/personal-production/console-summary"
)

for endpoint in "${endpoints[@]}"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_field_false_required "${body}" "${endpoint}" "raw_content_included"
  assert_field_false_required "${body}" "${endpoint}" "final_legal_opinion_generated"
  assert_field_false_required "${body}" "${endpoint}" "final_report_generated"
  assert_metadata_safe "${body}" "${endpoint}"
  assert_field_false_if_present "${body}" "${endpoint}" "real_provider_call_enabled"
  assert_field_false_if_present "${body}" "${endpoint}" "external_client_delivery_ready"
  assert_field_false_if_present "${body}" "${endpoint}" "external_delivery_enabled"
  assert_field_false_if_present "${body}" "${endpoint}" "team_workspace_enabled"
  if [ "${endpoint}" = "/personal-production/status" ] || [ "${endpoint}" = "/personal-production/readiness" ] || [ "${endpoint}" = "/personal-production/console-summary" ]; then
    if ! printf '%s' "${body}" | grep -Eq '"showcase_ready"[[:space:]]*:[[:space:]]*true'; then
      fail "${endpoint} expected showcase_ready=true"
    fi
  fi
  if [ "${endpoint}" = "/personal-production/runtime-registry" ]; then
    if ! printf '%s' "${body}" | grep -Eq '"live_runtime_count"[[:space:]]*:[[:space:]]*0'; then
      fail "${endpoint} expected live_runtime_count=0"
    fi
    if printf '%s' "${body}" | grep -Eq '"live_enabled"[[:space:]]*:[[:space:]]*true'; then
      fail "${endpoint} expected all live_enabled=false"
    fi
  fi
  if [ "${endpoint}" = "/personal-production/console-summary" ]; then
    if ! printf '%s' "${body}" | grep -Eq '"live_runtime_count"[[:space:]]*:[[:space:]]*0'; then
      fail "${endpoint} expected live_runtime_count=0"
    fi
  fi
done

pass "personal production APIs"
