# Personal Production Pilot with Real AI Gated Mode v7.17

v7.17 closes the v7.10-v7.17 Personal Live Intelligence & Controlled Case Analysis large stage. It connects the personal production console, gated AI / OCR / document / legal / enterprise provider foundations, Skill Training metadata, Controlled Case Analysis metadata, Personal Delivery Packet metadata, and owner-only download metadata into one controlled pilot route.

## Positioning

- Personal production pilot.
- Real AI gated mode foundation.
- Live providers disabled by default.
- Explicit confirmation required for live-provider eligibility.
- Owner-only view and owner-only download metadata.
- Draft-only case assistance.
- Source trace required.
- Lawyer review required.
- Final lock required.
- No automatic final legal opinion.
- No automatic final report.
- No email, public link, third-party upload, or external delivery.
- No open-case training data generation.
- No automatic Skill update or Skill publish.

## Pilot Flow

The pilot flow connects these controlled modules:

1. Personal Production Console.
2. AI Provider Live Gateway.
3. OCR / Document Provider Live Gateway.
4. Legal / Enterprise API Live Gateway.
5. Skill Training Runtime metadata.
6. Controlled Case Analysis Runtime metadata.
7. Personal Delivery Packet metadata.
8. Final Lock / Owner Download metadata.

If a provider adapter is incomplete or disabled, v7.17 returns gated / adapter-unavailable metadata. It does not pretend a live call succeeded.

## Training vs Open-case Execution

Closed-case training remains separated from open-case execution:

- Closed-case training uses desensitized, manually confirmed samples.
- Training may produce Skill Candidate, Evaluation, Promotion Gate, Experience Package, and Skill final draft metadata.
- v7.17 exposes two owner-only Skill final draft records:
  - `case_fact_extraction_skill`
  - `case_legal_analysis_skill`
- Open-case pilot runs do not create training data.
- Open-case pilot runs do not write to a training set.
- Open-case pilot runs do not update or publish Skills.

## Fact and Legal Analysis Boundary

Fact outputs remain draft metadata for owner review:

- fact summary draft
- evidence mapping draft
- timeline draft
- disputed facts draft
- missing facts draft
- confidence metadata
- source trace ids

Legal outputs remain draft metadata for owner review:

- legal relationship draft
- issue spotting draft
- claim basis draft
- defense path draft
- burden of proof draft
- legal search questions draft
- risk flags draft
- next action checklist draft

These outputs may be prepared for owner-only download or Delivery Packet draft metadata. They are not final fact findings, final legal opinions, formal lawyer reports, or external delivery artifacts.

## Owner-only Download Boundary

v7.17 supports owner-only download metadata for:

- Skill final draft Markdown / JSON / PDF draft / DOCX draft records.
- OCR / material organization draft metadata.
- fact preview and correction draft metadata.
- legal analysis draft metadata.
- case analysis draft metadata.
- source trace summary metadata.
- review summary metadata.
- delivery packet draft metadata.

Every output and download response keeps:

- `owner_only=true`
- `downloadable_by_owner_only=true`
- `public_link_created=false`
- `email_sent=false`
- `external_delivery_triggered=false`
- `third_party_share_enabled=false`
- `client_auto_delivery=false`
- `final_legal_opinion_auto_generated=false`
- `final_report_auto_generated=false`

The runtime does not create public links, send email, upload to third-party systems, send files to clients, or label generated drafts as final legal opinions or formal reports.

## Raw Content Boundary

Raw case material and OCR text must not be written to:

- Git.
- `docs/*.md`.
- `09-Change-Logs/*.md`.
- `00-Project-Context/*.md`.
- `README.md`.
- `AGENTS.md`.
- Developer Diagnostics.
- regression stdout.
- error stacks.
- public showcase pages.

Raw content is not automatically inserted into AI prompts, not automatically sent to external providers, and not written to training sets.

## API Surface

- `GET /personal-production-pilot/status`
- `GET /personal-production-pilot/readiness`
- `GET /personal-production-pilot/workflow`
- `GET /personal-production-pilot/runtimes`
- `GET /personal-production-pilot/provider-gates`
- `GET /personal-production-pilot/safety`
- `POST /personal-production-pilot/runs/mock`
- `POST /personal-production-pilot/runs`
- `GET /personal-production-pilot/runs`
- `GET /personal-production-pilot/runs/{run_id}`
- `GET /personal-production-pilot/case-analysis-summary`
- `GET /personal-production-pilot/skill-final-drafts`
- `GET /personal-production-pilot/skill-final-drafts/{draft_id}`
- `POST /personal-production-pilot/outputs/mock`
- `GET /personal-production-pilot/outputs`
- `GET /personal-production-pilot/outputs/{output_id}`
- `POST /personal-production-pilot/outputs/{output_id}/owner-downloads/mock`
- `GET /personal-production-pilot/owner-downloads`
- `GET /personal-production-pilot/owner-downloads/{download_id}`
- `GET /personal-production-pilot/review-queue`
- `POST /personal-production-pilot/review-queue/{review_item_id}/actions`
- `GET /personal-production-pilot/source-traces`
- `GET /personal-production-pilot/audit`
- `GET /personal-production-pilot/export-boundary`

## Frontend

The `/personal-production-pilot` page shows:

- Hero and pilot status cards.
- Workflow Stepper.
- Pilot run creation area.
- Provider Gate Summary.
- Skill Final Draft panel.
- Case Analysis Output panel.
- Owner Download Boundary.
- Runtime Readiness.
- Review Queue.
- Source Trace Summary.
- Export Boundary.
- Trust / Safety panel.
- Developer Diagnostics folded by default.

Display copy is Chinese by default. API fields and diagnostics JSON remain English.

## Regression

`scripts/regression/check_personal_production_pilot_apis.sh` checks the v7.17 API surface, creation flows, owner-download boundaries, review action metadata, source trace metadata, audit metadata, and safety fields.

The script is included in `run_personal_alpha_regression.sh`, but the v7.10-v7.17 large stage does not require full regression after each sub-stage. Full regression and a comprehensive security audit should run after v7.17 baseline validation before the combined release.
