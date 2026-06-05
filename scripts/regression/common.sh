#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

: "${API_BASE:=http://127.0.0.1:8001}"
: "${FRONTEND_BASE:=http://127.0.0.1:3001}"
: "${CASE_ID:=case_v55_approve_all}"
: "${LOCAL_DEV_TOKEN:=dev-local-token}"

PASS_PREFIX="PASS"
FAIL_PREFIX="FAIL"

section() {
  printf '\n== %s ==\n' "$1"
}

pass() {
  printf '%s %s\n' "${PASS_PREFIX}" "$1" >&2
}

fail() {
  printf '%s %s\n' "${FAIL_PREFIX}" "$1" >&2
  exit 1
}

repo_root() {
  cd "${REPO_ROOT}"
}

api_get() {
  local endpoint="$1"
  curl -fsS -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" "${API_BASE}${endpoint}"
}

check_endpoint_200() {
  local endpoint="$1"
  local body
  if ! body="$(api_get "${endpoint}")"; then
    fail "${endpoint} request failed"
  fi
  printf '%s' "${body}"
  pass "${endpoint}"
}

assert_absent() {
  local body="$1"
  local label="$2"
  local pattern="$3"
  if printf '%s' "${body}" | grep -Eiq "${pattern}"; then
    fail "${label} contains forbidden pattern: ${pattern}"
  fi
}

assert_field_false_if_present() {
  local body="$1"
  local label="$2"
  local field="$3"
  if printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:"; then
    if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*false"; then
      fail "${label} expected ${field}=false"
    fi
  fi
}

assert_field_false_required() {
  local body="$1"
  local label="$2"
  local field="$3"
  if ! printf '%s' "${body}" | grep -Eq "\"${field}\"[[:space:]]*:[[:space:]]*false"; then
    fail "${label} expected required ${field}=false"
  fi
}

assert_metadata_safe() {
  local body="$1"
  local label="$2"
  assert_absent "${body}" "${label}" '/Users'
  assert_absent "${body}" "${label}" '/Volumes'
  assert_absent "${body}" "${label}" 'C:\\\\'
  assert_absent "${body}" "${label}" 'real_cases'
  assert_absent "${body}" "${label}" 'sandbox_cases'
  assert_absent "${body}" "${label}" 'storage/runtime'
  assert_absent "${body}" "${label}" 'local\.db'
  assert_absent "${body}" "${label}" '\.env'
  assert_absent "${body}" "${label}" 'sk-[A-Za-z0-9_-]+'
  assert_absent "${body}" "${label}" 'client\.pdf'
  assert_field_false_if_present "${body}" "${label}" "raw_content_included"
  assert_field_false_if_present "${body}" "${label}" "final_legal_opinion_generated"
  assert_field_false_if_present "${body}" "${label}" "final_report_generated"
}

assert_no_stack_trace() {
  local body="$1"
  local label="$2"
  assert_absent "${body}" "${label}" 'Traceback'
  assert_absent "${body}" "${label}" 'File "[^"]+", line [0-9]+'
}
