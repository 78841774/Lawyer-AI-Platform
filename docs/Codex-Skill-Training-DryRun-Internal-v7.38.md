# Codex Skill Training Dry Run / Internal Training v7.38

v7.38 connects the safe Training Skill Spec to a dry-run / internal training simulation record.

## Scope

- Starts a `codex-skill-training-run` from a ready Training Skill Spec.
- Records logs, metrics, gate report, training artifact metadata, audit, source trace, and provider adapter checks.
- Carries forward the generated differentiated fact extraction experience package.
- Validates facts output difference, procedure / stage difference, substantive/procedural split, procedural exact-match boundary, substantive impact presence, legal summary presence, audit, source trace, and readiness metadata.
- Keeps the artifact not publishable and not runtime loadable.
- Requires later Practice Load Review before any practical loading path.

## Output Artifact

The internal training artifact includes:

- `generated_experience_package`: redacted / abstracted package metadata
- `fact_output_diff_summary`: common framework count, case-cause count, point counts, diff check, and readiness
- `substantive_experience_profiles`: substantive references with source-stage and cross-procedure usage boundary
- `procedural_experience_profiles`: exact procedure/stage profiles with cross-stage use disabled
- `profile_loading_contract`: profile selection by case cause, procedure type, and procedure stage
- `legal_summary_validated=true`
- `case_cause_differentiation_validated=true`
- `procedural_stage_differentiation_validated=true`
- `substantive_procedural_split_validated=true`
- `procedural_exact_match_boundary_validated=true`
- `substantive_cross_procedure_boundary_validated=true`
- `substantive_impact_validated=true`
- `not_publishable=true`
- `not_runtime_loadable=true`
- `requires_practice_load_review=true`

## Safety

- No live provider call is executed.
- No credential value is read or returned to the Skill, frontend, logs, docs, or regression output.
- No runtime package is replaced.
- No Skill is published.
- No final legal opinion, formal report, public link, email, or external delivery is generated.

## APIs

Prefix: `/personal-skill-studio/training-artifacts`

- `POST /codex-skill-training-runs/start`
- `GET /codex-skill-training-runs`
- `GET /codex-skill-training-runs/{training_run_id}`
- `GET /codex-skill-training-runs/{training_run_id}/logs`
- `GET /codex-skill-training-runs/{training_run_id}/metrics`
- `GET /codex-skill-training-runs/{training_run_id}/gate-report`
- `GET /codex-skill-training-runs/{training_run_id}/artifact`
- `GET /codex-skill-training-runs/{training_run_id}/audit`
- `GET /codex-skill-training-runs/{training_run_id}/source-trace`
- `GET /v7-38/status`

## Regression

- `scripts/regression/check_personal_codex_skill_training_run_v738_apis.sh`
