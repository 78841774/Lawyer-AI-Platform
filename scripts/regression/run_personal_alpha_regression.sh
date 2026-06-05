#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Alpha Regression Suite"
printf 'API_BASE=%s\n' "${API_BASE}"
printf 'FRONTEND_BASE=%s\n' "${FRONTEND_BASE}"
printf 'CASE_ID=%s\n' "${CASE_ID}"

checks=(
  "check_backend_compile.sh"
  "check_frontend_build.sh"
  "check_case_os_status_apis.sh"
  "check_case_os_core_apis.sh"
  "check_case_os_quality_apis.sh"
  "check_case_os_hardening_apis.sh"
  "check_case_os_release_candidate_apis.sh"
  "check_personal_production_apis.sh"
  "check_personal_ai_gateway_apis.sh"
  "check_personal_material_runtime_apis.sh"
  "check_metadata_only_responses.sh"
  "check_safe_not_found.sh"
  "check_injected_path_inputs.sh"
  "check_git_safety.sh"
  "check_runtime_ignored.sh"
  "check_docs_not_empty.sh"
  "check_no_sensitive_files.sh"
)

for check in "${checks[@]}"; do
  section "${check}"
  bash "${SCRIPT_DIR}/${check}"
done

printf '\nPersonal Alpha regression suite passed.\n'
