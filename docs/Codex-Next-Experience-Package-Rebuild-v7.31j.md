# Codex Next Experience Package Rebuild v7.31j

v7.31j converts a ready v7.31i feedback candidate pack into a next experience package draft.

## Scope

- Reads `ready_for_next_experience_build` candidate pack metadata.
- Applies candidate diff metadata into a next package draft view.
- Generates lawyer review view, draft manifest, validation result, audit events, and source trace.
- Supports marking the draft as `pending_practice_load_review`.
- Supports archival of draft metadata.

## API

- `GET /personal-skill-studio/training-artifacts/next-experience-packages/status`
- `POST /personal-skill-studio/training-artifacts/next-experience-packages/rebuild`
- `GET /personal-skill-studio/training-artifacts/next-experience-packages`
- `GET /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}`
- `GET /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}/lawyer-review-view`
- `GET /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}/manifest`
- `GET /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}/audit`
- `GET /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}/source-trace`
- `POST /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}/mark-pending-load-review`
- `POST /personal-skill-studio/training-artifacts/next-experience-packages/{next_package_id}/archive`
- `GET /personal-skill-studio/training-artifacts/v7-31j/status`

## Safety Boundary

The next experience package is draft metadata only. It does not replace current runtime packages, does not mutate lawyer-approved packages, does not change runtime policy, and does not load into practice runtime.

`pending_practice_load_review` is a review preparation state only. A later lawyer load review boundary is still required before future runtime loading.

Provider calls, key value reads, source content exposure, final legal opinions, final reports, public links, email, and external delivery remain disabled.

## Validation

The lightweight API regression is:

`scripts/regression/check_personal_next_experience_package_v731j_apis.sh`

The script prepares v7.31h feedback metadata, builds and marks a v7.31i candidate pack ready, rebuilds a v7.31j next package draft, and verifies review view, manifest, audit, source trace, pending-review, archive, and safety boundaries.
