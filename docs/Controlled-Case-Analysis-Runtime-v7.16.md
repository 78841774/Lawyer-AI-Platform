# Controlled Case Analysis Runtime v7.16

v7.16 adds the controlled open-case analysis runtime for AIHome.law Personal Production. It is an execution-stage runtime for unfinished cases, not a training-stage runtime.

## Positioning

- Open-case runtime.
- Draft-only case analysis.
- Metadata-only.
- Lawyer review required.
- Source trace required.
- Evaluation and gate are reference-only.
- No training data generation.
- No Skill update.
- No Skill publishing.
- No final legal opinion.
- No final report.
- No email, real PDF/DOCX, or external delivery.

## Training vs Execution Separation

v7.15 Skill Training Runtime is the closed-case training stage. It may create desensitized training sample metadata, Skill Candidate drafts, Test Case drafts, Evaluation metadata, Promotion Gate metadata, and Experience Package drafts.

v7.16 Controlled Case Analysis Runtime is the open-case execution stage. It only references existing Skill metadata:

- `case_fact_extraction_skill`
- `case_legal_analysis_skill`

If the existing v7.15 baseline is incomplete, v7.16 reports a missing baseline and uses placeholder lineage metadata. It does not create training data or pretend that a complete Skill exists.

## API Surface

- `GET /personal-case-analysis/status`
- `GET /personal-case-analysis/runtimes`
- `GET /personal-case-analysis/runtimes/{runtime_id}`
- `GET /personal-case-analysis/skill-baselines`
- `POST /personal-case-analysis/runs/mock`
- `POST /personal-case-analysis/runs`
- `GET /personal-case-analysis/runs`
- `GET /personal-case-analysis/runs/{run_id}`
- `POST /personal-case-analysis/fact-drafts/mock`
- `GET /personal-case-analysis/fact-drafts`
- `GET /personal-case-analysis/fact-drafts/{draft_id}`
- `POST /personal-case-analysis/legal-drafts/mock`
- `GET /personal-case-analysis/legal-drafts`
- `GET /personal-case-analysis/legal-drafts/{draft_id}`
- `GET /personal-case-analysis/review-queue`
- `POST /personal-case-analysis/review-queue/{review_item_id}/actions`
- `GET /personal-case-analysis/evaluations`
- `GET /personal-case-analysis/evaluations/{evaluation_id}`
- `GET /personal-case-analysis/gates`
- `GET /personal-case-analysis/gates/{gate_id}`
- `GET /personal-case-analysis/source-traces`
- `GET /personal-case-analysis/source-traces/{source_trace_id}`
- `GET /personal-case-analysis/audit`
- `GET /personal-case-analysis/safety`

## Stages

### Fact Analysis Stage

Inputs are case metadata, material metadata, OCR / document parse metadata, source trace metadata, optional redacted preview metadata, and the case fact extraction Skill baseline metadata.

Outputs are:

- fact summary draft
- evidence mapping draft
- timeline draft
- disputed facts draft
- missing facts draft
- confidence metadata
- source trace ids
- review required metadata

The stage does not read raw full content, does not inject OCR raw text into an AI prompt, does not generate a final fact finding, and does not generate training data.

### Legal Analysis Stage

Inputs are fact analysis draft metadata, lawyer review status, legal search metadata, enterprise info metadata, source trace metadata, and the case legal analysis Skill baseline metadata.

Outputs are:

- legal relationship draft
- issue spotting draft
- claim basis draft
- defense path draft
- burden of proof draft
- legal search questions draft
- risk flags draft
- next action checklist draft

The stage does not read raw material, does not generate a final legal opinion, and does not generate a final report.

### Review & Readiness Stage

Outputs are:

- lawyer review queue
- low confidence flags
- missing information checklist
- source trace completeness
- analysis readiness
- delivery packet readiness metadata

Readiness is status metadata only. It does not trigger a delivery packet, PDF/DOCX generation, email sending, or external delivery.

## Evaluation / Gate

The v7.16 evaluation and gate are runtime quality metadata for the current open case only:

- `gate_reference_only=true`
- `blocks_next_stage=false`
- `training_data_generated=false`
- `writes_to_training_set=false`

They are not v7.15 training-stage evaluation or promotion gates.

## Frontend

The `/personal-case-analysis` page shows:

- Hero and status cards.
- Three-stage Stepper.
- Skill baseline panel.
- Fact Analysis Stage panel.
- Legal Analysis Stage panel.
- Evaluation / Gate panel.
- Review Queue.
- Source Trace panel.
- Trust / Safety panel.
- Developer Diagnostics folded by default.

All display copy is Chinese by default. API fields and diagnostics JSON remain English.

## Regression

`scripts/regression/check_personal_case_analysis_apis.sh` checks v7.16 endpoints and core safety fields:

- `training_data_generated=false`
- `writes_to_training_set=false`
- `skill_updated=false`
- `skill_published=false`
- `gate_reference_only=true`
- `blocks_next_stage=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `external_delivery_triggered=false`
- `source_trace_required=true`
- `lawyer_review_required=true`

The script is included in `run_personal_alpha_regression.sh`, but the v7.10-v7.17 large stage does not require full regression after each sub-stage.
