# Experience Package Skill Studio v7.4

## Objective

v7.4 adds a controlled Experience Package Skill Studio foundation for personal production validation. It turns reviewed workflow metadata into experience package drafts, skill candidate drafts, test case drafts, and mock evaluation metadata without publishing Skills automatically.

## Relationship to v7.3

v7.3 prepares source-trace-ready legal and enterprise intelligence metadata. v7.4 can reference reviewed metadata ids, but it does not read raw case materials or external provider content.

## Studio Runtimes

v7.4 registers:

- `experience_package_runtime`
- `skill_candidate_runtime`
- `test_case_runtime`
- `evaluation_runtime`
- `promotion_gate`

All runtimes are mock-first, manual-review-required, lawyer-review-required, source-trace-required, and not live.

## Experience Package Drafts

`POST /personal-skill-studio/experience-packages/mock` creates an experience package draft only when explicit confirmations are present.

The workflow:

- Does not read real case materials.
- Does not expose raw content.
- Creates source trace metadata.
- Creates draft section placeholders.
- Requires lawyer review.
- Does not generate a final legal opinion or final report.
- Does not publish a Skill.

## Skill Candidate Drafts

`POST /personal-skill-studio/skill-candidates/mock` creates a skill candidate draft linked to an experience package draft.

The workflow:

- Requires an existing experience package id.
- Creates prompt template, reasoning pattern, input schema, and output schema draft metadata.
- Requires lawyer review and evaluation.
- Keeps `auto_publish_enabled=false`.
- Keeps `published_to_registry=false`.

## Test Case Drafts

`POST /personal-skill-studio/test-cases/mock` creates mock test case metadata linked to a skill candidate draft.

The workflow does not include raw case content and only returns mock input and expected behavior metadata.

## Mock Evaluations

`POST /personal-skill-studio/evaluations/mock` creates mock evaluation metadata linked to a skill candidate draft and optional test case ids.

Evaluations include:

- score summary metadata
- checklist metadata
- risk flags
- recommendation metadata
- manual review required
- lawyer review required
- no automatic publish

## Promotion Gate

`GET /personal-skill-studio/promotion-queue` lists draft skill candidates that still need manual promotion review.

`POST /personal-skill-studio/promotion-queue/{skill_candidate_id}/actions` records controlled actions:

- `approve_for_future_review`
- `request_revision`
- `reject`
- `mark_low_confidence`
- `mark_not_ready`

Promotion actions only update metadata. They do not publish a Skill, update the formal Skill Registry, or generate final legal output.

## Source Trace

Source trace metadata records package, candidate, test case, and evaluation links. It does not include raw content, real case materials, provider responses, local paths, or final-output material.

## Audit Metadata

Audit metadata is written under ignored runtime storage:

`Lawyer-AI-Platform-App/backend/storage/runtime/personal_skill_studio/audit/`

Audit APIs return metadata only.

## Frontend Page

The page at `/personal-skill-studio` includes:

- runtime cards
- experience package draft form
- skill candidate draft form
- test case draft form
- mock evaluation form
- promotion gate action form
- source trace, safety, and diagnostics panels

The UI does not show API keys, raw content, local paths, final legal output, or published Skill artifacts.

## Personal Production Integration

The Personal Production Console registers Skill Studio runtimes with `target_route=/personal-skill-studio`.

## Regression Updates

The regression suite adds `scripts/regression/check_personal_skill_studio_apis.sh` and includes it after v7.3 checks.

The script checks status, runtimes, experience package drafts, skill candidate drafts, test case drafts, evaluations, promotion gate, source traces, audit, safety, required confirmation blocking, and sensitive-string absence.

## No Automatic Skill Publish

v7.4 does not publish Skills automatically and does not write approved candidates into the formal Skill Registry.

## No Final Legal Opinion

v7.4 does not generate final legal opinions.

## No Final Report

v7.4 does not generate final reports and does not enable external delivery.

## Release Status

v7.4 is implemented in the current worktree for validation and release preparation. It is not committed, tagged, or released in this worktree.

## v7.5 Readiness

The next stage is Real Case Production Workflow:

- controlled case production metadata
- workflow stage orchestration
- readiness checks
- lawyer review gate
- no automatic final legal opinion
- no automatic final report
- no automatic external delivery
