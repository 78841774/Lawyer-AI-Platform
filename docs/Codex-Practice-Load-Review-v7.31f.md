# Codex Practice Load Review Gate v7.31f

v7.31f adds the lawyer review gate before any experience package can be loaded into a practice runtime.

## Scope

- Backend modules: `practice_load_review_gate.py` and `lawyer_experience_editor.py`.
- API prefix: `/personal-skill-studio/training-artifacts/practice-load-review`.
- Frontend page: `/personal-skill-studio/training-artifacts`.
- Regression script: `scripts/regression/check_personal_practice_load_review_v731f_apis.sh`.

## Review Flow

- Start from v7.31e experience packages with `pending_practice_load_review`.
- Preserve `generated_experience_package` as read-only metadata.
- Create lawyer-editable experience cards for generated experience text, lawyer experience text, applicable scenarios, non-applicable scenarios, risk warnings, usage boundaries, and gray-load setting.
- Save edits as a `lawyer_approved_experience_package` candidate.
- Run system revalidation for metadata safety, source trace, audit, sensitive-field scan, and generated-package preservation.
- Approve or reject the package for future practice runtime loading.

## Statuses

- `pending_practice_load_review`
- `review_editing`
- `review_changes_saved`
- `system_revalidation_required`
- `system_revalidated`
- `approved_for_practice_load`
- `rejected_for_practice_load`
- `changes_requested`

## Boundaries

- v7.31f is the lawyer review point before practice runtime loading.
- v7.31f does not execute practice runtime loading; controlled loading and monitoring are deferred to v7.31g.
- No provider call, API key read, real training, formal training set write, Skill publish, final legal opinion, final report, public link, email, or external delivery is triggered.
