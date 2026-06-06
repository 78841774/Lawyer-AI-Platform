# v7.31c Codex Skill Experience Pool & Draft Builder

## 中文定位

复核通过的训练经验进入 Codex Skill 经验池，并生成待人工确认的 Codex Skill 草案。

## Scope

v7.31c imports only v7.31b candidates with `review_status=approved_for_skill_experience`, `redaction_status=passed`, source trace metadata, and audit metadata. It creates Skill Experience Pool entries, binds them to draft targets, builds Codex Skill draft metadata, and records manual confirmation and audit metadata.

## Pipeline

- Import approved v7.31b experience candidates into the Skill Experience Pool.
- Reject pending, rejected, changes-requested, missing-source-trace, or not-redacted candidates.
- Bind pool entries to a draft target.
- Build non-publishable Codex Skill draft metadata.
- Review draft structure with manual confirmation metadata.
- Keep audit and source trace references on pool entries, bindings, and drafts.

## API

Prefix: `/personal-skill-studio/training-artifacts`

- `GET /skill-experience-pool/status`
- `POST /skill-experience-pool/import-approved`
- `GET /skill-experience-pool`
- `GET /skill-experience-pool/{experience_id}`
- `POST /skill-experience-bindings`
- `GET /skill-experience-bindings`
- `GET /skill-experience-bindings/{binding_id}`
- `POST /codex-skill-drafts/build`
- `GET /codex-skill-drafts`
- `GET /codex-skill-drafts/{draft_id}`
- `POST /codex-skill-drafts/{draft_id}/review`
- `GET /codex-skill-drafts/{draft_id}/audit`
- `GET /v7-31c/status`

## Safety Boundary

- `owner_only=true`
- `local_private_processing_only=true`
- `approved_experience_only=true`
- `redacted_output_only=true`
- `abstracted_experience_only=true`
- `manual_review_required=true`
- `source_trace_required=true`
- `audit_required=true`
- `unreviewed_experience_imported=false`
- `unsafe_experience_imported=false`
- `missing_source_trace_imported=false`
- `formal_training_set_generated=false`
- `real_codex_training_triggered=false`
- `skill_published=false`
- `skill_publishable=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `public_link_created=false`
- `email_sent=false`
- `external_delivery_triggered=false`

## Regression

- `scripts/regression/check_personal_codex_skill_experience_pool_v731c_apis.sh`
- Included in `scripts/regression/run_personal_alpha_regression.sh`

## Next

Next planned sub-stage: v7.31d Skill Package Versioning & Pre-Publish Gate.
