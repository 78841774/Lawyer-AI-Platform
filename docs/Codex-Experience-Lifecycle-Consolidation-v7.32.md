# Codex Experience Lifecycle Consolidation v7.32

v7.32 consolidates the v7.31b-v7.31j experience pipeline into one metadata-only lifecycle view.

## Scope

- Registers experience lifecycle metadata from controlled work-product processing, Skill experience pool import, Skill package versioning, internal training package building, practice load review, controlled runtime loading, output observation, feedback candidate packs, and next package rebuilds.
- Builds lifecycle state, lineage graph, audit timeline, source trace view, integrity checks, and safety summary.
- Adds frontend lifecycle overview inside `/personal-skill-studio/training-artifacts`.
- Recomputes lifecycle views without mutating source packages, loaded packages, lawyer-approved packages, Skills, or runtime policy.

## API

- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/status`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/state`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/graph`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/audit-timeline`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/source-trace-view`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/integrity-check`
- `GET /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/safety-summary`
- `POST /personal-skill-studio/training-artifacts/experience-lifecycles/{lifecycle_id}/recompute`
- `GET /personal-skill-studio/training-artifacts/v7-32/status`

## Safety Boundary

v7.32 is a lifecycle operating-system view for metadata only. It does not read raw case materials, OCR text, local paths, provider responses, or key values.

Recompute is view-level only. It does not replace runtime packages, auto-load next packages, update Skills, trigger training, publish Skills, generate final legal opinions, generate final reports, create public links, send email, or trigger external delivery.

## Validation

The lightweight API regression is:

`scripts/regression/check_personal_experience_lifecycle_v732_apis.sh`

The script verifies status, list, detail, state, graph, audit timeline, source trace, integrity, safety summary, recompute, and sensitive-response boundaries.
