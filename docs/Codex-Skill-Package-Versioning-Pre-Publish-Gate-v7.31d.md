# Codex Skill Package Versioning & Pre-Publish Gate v7.31d

v7.31d adds the Skill Package versioning layer for confirmed v7.31c Codex Skill Draft metadata.

## Scope

- Backend module: `personal_skill_studio.training_artifacts.skill_package_*`.
- API prefix: `/personal-skill-studio/training-artifacts/skill-packages`.
- Frontend page: `/personal-skill-studio/training-artifacts`.
- Regression script: `scripts/regression/check_personal_codex_skill_package_v731d_apis.sh`.

## Package Metadata

Skill Packages include package id, name, version, source draft id, experience ids, manifest id, source trace bundle id, audit bundle id, pre-publish gate status, final review status, rollback metadata, timestamps, manifest, source trace bundle, audit events, validation result, and safety flags.

## System Validation Gate

The gate checks approved/redacted experiences, source trace presence, audit presence, confirmed draft structure, manifest generation, sensitive metadata scan, and valid package state.

## Boundaries

- Only approved and redacted experience metadata may be packaged.
- v7.31d does not perform manual review of training output.
- Practice load review is deferred to v7.31f.
- No provider call, API key read, real training, Skill publish, final legal opinion, final report, public link, email, or external delivery is triggered.
