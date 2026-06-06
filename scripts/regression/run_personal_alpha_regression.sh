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
  "check_personal_intelligence_apis.sh"
  "check_personal_skill_studio_apis.sh"
  "check_personal_case_production_apis.sh"
  "check_personal_delivery_packet_apis.sh"
  "check_personal_showcase_pack_apis.sh"
  "check_personal_ui_polish.sh"
  "check_personal_demo_pack_docs.sh"
  "check_personal_public_demo_readiness.sh"
  "check_personal_local_pilot_stability.sh"
  "check_personal_ai_live_gateway_apis.sh"
  "check_personal_material_live_gateway_apis.sh"
  "check_personal_intelligence_live_gateway_apis.sh"
  "check_personal_case_analysis_apis.sh"
  "check_personal_production_pilot_apis.sh"
  "check_personal_case_workspace_apis.sh"
  "check_personal_production_pilot_dashboard_apis.sh"
  "check_personal_fact_correction_apis.sh"
  "check_personal_legal_draft_apis.sh"
  "check_personal_skill_final_drafts_apis.sh"
  "check_personal_owner_output_center_apis.sh"
  "check_personal_trial_readiness_apis.sh"
  "check_personal_provider_readiness_apis.sh"
  "check_personal_live_connection_apis.sh"
  "check_personal_legal_enterprise_apis.sh"
  "check_personal_training_artifact_loader_apis.sh"
  "check_personal_codex_training_runs_apis.sh"
  "check_personal_real_closed_case_training_intake_apis.sh"
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
