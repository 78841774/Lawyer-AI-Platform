# Real Case Production Workflow v7.5

## Objective

v7.5 adds a controlled Real Case Production Workflow foundation for personal production validation. It links the personal production modules into a metadata-only workflow for real-case-style production rehearsal without reading raw case materials, calling real providers, generating final legal output, or triggering external delivery.

## Relationship to v7.4

v7.4 prepares experience package and skill candidate metadata. v7.5 can reference Skill Studio metadata as part of a controlled workflow stage, but it does not publish Skills or rely on unreviewed AI output.

## Workflow Stage Registry

`GET /personal-case-production/workflow-stages` exposes controlled stages:

- `case_intake_stage`
- `material_processing_stage`
- `ai_draft_stage`
- `intelligence_check_stage`
- `skill_studio_stage`
- `lawyer_review_stage`
- `final_readiness_stage`

Each stage requires manual review, lawyer review, source trace, and final gate checks. Auto delivery is disabled.

## Production Case Runtime

`POST /personal-case-production/cases/mock` creates a production case record only when explicit confirmations are present.

The workflow:

- Does not read real case materials.
- Stores metadata only.
- Requires desensitization status metadata.
- Requires lawyer review.
- Requires final gate.
- Does not generate final legal opinions or reports.
- Does not trigger external delivery.

## Workflow Runs

`POST /personal-case-production/workflow-runs/mock` creates a mock workflow run linked to a production case.

The workflow:

- Validates selected stage ids.
- Creates workflow source trace metadata.
- Records selected stage count and readiness metadata.
- Does not call live providers.
- Does not generate final output.

## Stage Runs

`POST /personal-case-production/stage-runs/mock` records stage run metadata.

Stage runs can link controlled runtime object ids from earlier modules, but they do not fetch raw content, call providers, or generate final legal conclusions.

## Readiness Engine

`GET /personal-case-production/readiness` and `GET /personal-case-production/readiness/{production_case_id}` return production readiness metadata:

- completed stage count
- missing stage ids
- lawyer review status
- source trace status
- final gate readiness
- delivery readiness
- risk flags
- checklist metadata

Even when all workflow stages are recorded, `delivery_ready=false` because external delivery is outside v7.5 scope.

## Lawyer Review Gate

`GET /personal-case-production/review-gates` lists production cases requiring controlled review.

`POST /personal-case-production/review-gates/{production_case_id}/actions` records controlled actions:

- `approve_for_final_gate`
- `request_revision`
- `reject`
- `mark_not_ready`
- `mark_low_confidence`

Review gate actions only update metadata. They do not generate final legal opinions, final reports, or external delivery packets.

## Source Trace

Source trace metadata records production case, workflow run, stage run, and review gate links. It does not include raw content, real case materials, provider responses, local paths, or final-output material.

## Audit Metadata

Audit metadata is written under ignored runtime storage:

`Lawyer-AI-Platform-App/backend/storage/runtime/personal_case_production/audit/`

Audit APIs return metadata only.

## Frontend Page

The page at `/personal-case-production` includes:

- workflow stage cards
- production case form
- mock workflow form
- stage run form
- readiness panel
- review gate action form
- source trace, safety, and diagnostics panels

The UI does not show API keys, raw content, local paths, final legal output, final report text, or delivery artifacts.

## Personal Production Integration

The Personal Production Console registers case production runtimes with `target_route=/personal-case-production`:

- Case Production Runtime
- Workflow Stage Orchestrator
- Production Readiness Engine
- Lawyer Review Gate

## Regression Updates

The regression suite adds `scripts/regression/check_personal_case_production_apis.sh` and includes it after v7.4 checks.

The script checks status, stage registry, production case records, workflow runs, stage runs, readiness, review gates, source traces, audit, safety, required confirmation blocking, and sensitive-string absence.

## No Live Provider Call

v7.5 does not call real AI, OCR, legal search, enterprise, parsing, or delivery providers.

## No Final Legal Opinion

v7.5 does not generate final legal opinions.

## No Final Report

v7.5 does not generate final reports.

## No External Delivery

v7.5 does not create a delivery packet and does not trigger external delivery.

## Release Status

v7.5 is implemented in the current worktree for validation and release preparation. It is not committed, tagged, or released in this worktree.

## v7.6 Readiness

Only after v7.3-v7.5 validation passes and the user explicitly starts the next version should the project proceed to Personal Delivery Packet work.
