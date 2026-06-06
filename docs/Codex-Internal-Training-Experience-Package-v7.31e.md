# Codex Internal Training / Experience Package Builder v7.31e

v7.31e adds the internal training task and experience package builder for system-validated v7.31d Skill Package metadata.

## Scope

- Backend modules: `internal_training_task_builder.py`, `experience_package_builder.py`, and `training_package_registry.py`.
- API prefix: `/personal-skill-studio/training-artifacts`.
- Frontend page: `/personal-skill-studio/training-artifacts`.
- Regression script: `scripts/regression/check_personal_internal_training_v731e_apis.sh`.

## Training Task Metadata

Training tasks are built only from v7.31d Skill Packages with `pre_publish_gate_status=system_validated`, `package_status=ready_for_training_package_build`, and a passing system validation result.

Each task keeps source package, source draft, source experience, source trace, audit, prompt template, and input-output pair metadata. It does not trigger provider calls or real model training.

## Experience Package Metadata

Experience packages aggregate training task samples into structured internal package metadata and retain source trace and audit bundles.

The package status is `pending_practice_load_review`. Training-output manual review is `not_applicable` in v7.31e. Practice runtime loading requires v7.31f review before use.

## Boundaries

- Only system-validated Skill Package metadata may enter v7.31e.
- Outputs are redacted, metadata-safe, source-traced, and audited.
- v7.31e does not call providers, read API keys, trigger real training, write formal training sets, publish Skills, generate final legal opinions, generate final reports, create public links, send email, or trigger external delivery.
