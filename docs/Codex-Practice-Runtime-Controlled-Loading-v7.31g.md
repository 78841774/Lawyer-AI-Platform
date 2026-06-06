# Codex Practice Runtime Controlled Loading v7.31g

v7.31g adds controlled practice runtime loading and monitoring after the v7.31f lawyer load review gate.

## Scope

- Backend modules: `practice_runtime_loader.py`, `practice_runtime_registry.py`, `practice_runtime_policy_engine.py`, `practice_runtime_monitor.py`, `practice_runtime_rollback_engine.py`, `practice_runtime_usage_audit.py`, `practice_runtime_safety_engine.py`, and `practice_runtime_source_trace_engine.py`.
- API prefix: `/personal-skill-studio/training-artifacts/practice-runtime-*`.
- Regression script: `scripts/regression/check_personal_practice_runtime_loading_v731g_apis.sh`.

## Runtime Flow

- Start from v7.31f packages with `review_status=approved_for_practice_load`.
- Validate lawyer-approved package metadata, system revalidation, source trace, audit, sensitive scan, and generated-package preservation.
- Create a Practice Runtime Loading Registry record with disabled, gray, active, disabled, blocked, or rolled-back status.
- Evaluate runtime policy by case cause, workspace, runtime mode, task type, gray rollout percentage, and usage limit.
- Record usage events, blocked reasons, risk events, audit metadata, and source trace metadata.
- Disable and rollback change load state only; packages, audit, and source trace records are preserved.

## Boundaries

- Only lawyer-approved package metadata can be loaded.
- Runtime records do not read source materials or return source content.
- Feedback or output observation does not automatically mutate loaded packages in v7.31g.
- No provider call, API key read, real training, formal training set write, Skill publish, final legal opinion, final report, public link, email, or external delivery is triggered.
