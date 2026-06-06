#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Training Dataset Alias v7.36"

bash "${SCRIPT_DIR}/check_personal_training_dataset_v735_apis.sh" >/dev/null

post_json() {
  local endpoint="$1"
  local payload="${2:-{}}"
  local response body code
  response="$(curl -sS -H "X-Dev-Token: ${LOCAL_DEV_TOKEN}" -w '\n%{http_code}' --json "${payload}" "${API_BASE}${endpoint}")"
  code="${response##*$'\n'}"
  body="${response%$'\n'*}"
  if [[ ! "${code}" =~ ^2 ]]; then
    printf '%s\n' "${body}" >&2
    fail "POST ${endpoint} returned HTTP ${code}"
  fi
  printf '%s' "${body}"
}

assert_dataset_safe() {
  local body="$1"
  local label="$2"
  assert_metadata_safe "${body}" "${label}"
  assert_no_stack_trace "${body}" "${label}"
  assert_absent "${body}" "${label}" 'raw_text|ocr_text|original_text|full_document_text|raw_material|raw_case_material|local_path|file_path|absolute_path|api_key|private_key|access_token|refresh_token|provider_response|provider_raw_response|unredacted'
}

dataset="$(post_json "/personal-skill-studio/training-artifacts/training-datasets/build" '{"explicit_metadata_only_confirmation":true,"explicit_ready_candidate_only_confirmation":true,"explicit_no_training_confirmation":true,"explicit_no_package_mutation_confirmation":true,"explicit_no_skill_publish_confirmation":true}')"
assert_dataset_safe "${dataset}" "training dataset alias build"
dataset_id="$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("dataset_id",""))' <<<"${dataset}")"
[ -n "${dataset_id}" ] || fail "missing dataset id"

for endpoint in \
  "/personal-skill-studio/training-artifacts/training-datasets" \
  "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}" \
  "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}/examples" \
  "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}/task-plan" \
  "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}/gate-report" \
  "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}/audit" \
  "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}/source-trace" \
  "/personal-skill-studio/training-artifacts/v7-36/status"; do
  body="$(check_endpoint_200 "${endpoint}")"
  assert_dataset_safe "${body}" "${endpoint}"
done

gate="$(post_json "/personal-skill-studio/training-artifacts/training-datasets/${dataset_id}/gate/run" '{}')"
assert_dataset_safe "${gate}" "training dataset gate alias"

pass "personal training dataset alias v7.36"
