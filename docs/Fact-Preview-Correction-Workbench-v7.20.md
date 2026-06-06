# Fact Preview & Correction Workbench v7.20

v7.20 adds the owner-only fact preview and correction layer for the Personal Live Intelligence & Controlled Case Analysis large stage.

## Positioning

- Chinese page title: 事实预览与输入纠正工作台.
- Route: `/personal-case-workspace`.
- Scope: fact layer only.
- Metadata-only.
- Draft-only.
- Owner-only.
- Source trace required.
- Audit required.
- Lawyer review required.
- Quality gate is reference-only.
- Legal analysis input readiness does not auto-trigger legal analysis.

## API Surface

- `GET /personal-case-workspace/fact-previews`
- `POST /personal-case-workspace/fact-previews/mock`
- `GET /personal-case-workspace/fact-previews/{fact_preview_id}`
- `POST /personal-case-workspace/fact-previews/{fact_preview_id}/corrections/mock`
- `GET /personal-case-workspace/fact-previews/{fact_preview_id}/corrections`
- `GET /personal-case-workspace/fact-corrections/{correction_id}`
- `GET /personal-case-workspace/fact-previews/{fact_preview_id}/versions`
- `POST /personal-case-workspace/fact-previews/{fact_preview_id}/versions/mock`
- `GET /personal-case-workspace/fact-previews/{fact_preview_id}/quality`
- `GET /personal-case-workspace/fact-previews/{fact_preview_id}/gate`
- `GET /personal-case-workspace/fact-previews/{fact_preview_id}/source-traces`
- `POST /personal-case-workspace/fact-previews/{fact_preview_id}/confirm-for-legal-analysis/mock`
- `GET /personal-case-workspace/fact-input-readiness`
- `GET /personal-case-workspace/fact-audit`
- `GET /personal-case-workspace/fact-safety`

## Frontend

`/personal-case-workspace` now shows:

- Fact Preview hero and safety badges.
- Fact draft cards for summary, evidence mapping, timeline, disputed facts, and missing facts.
- Correction panel for owner correction metadata.
- Version timeline for AI draft, owner correction, and owner confirmation metadata.
- Quality / Gate panel with reference-only score and suggestions.
- Legal Analysis Input Readiness panel.
- Source Trace panel.
- Owner Download Boundary panel.
- Trust / Safety panel.
- Developer Diagnostics folded by default.

`/personal-case-analysis` receives read-only fact input readiness metadata so users can see that fact input readiness is separate from legal analysis creation.

`/personal-production-pilot` receives fact preview quality and readiness summary cards.

`/personal-production` receives v7.20 readiness and capability summary cards.

## Safety

v7.20 does not:

- call real providers
- read API keys
- read real case materials
- return raw content
- expose local paths
- inject raw OCR text into AI prompts
- auto-trigger legal analysis
- generate training data
- write to training sets
- update Skills
- publish Skills
- generate final fact findings
- generate final legal opinions
- generate final reports
- create real PDF/DOCX files
- send email
- create public links
- trigger external delivery

Fact quality and gate status are advisory mock metadata only. They do not represent final fact findings, legal correctness, lawyer conclusions, or delivery readiness.

## Regression

`scripts/regression/check_personal_fact_correction_apis.sh` checks fact preview, correction, version, quality, gate, source trace, audit, safety, and legal-analysis-input readiness APIs. It verifies metadata-only / draft-only / owner-only fields and forbidden sensitive patterns.

The script is included in `run_personal_alpha_regression.sh`, but full Personal Alpha regression remains reserved for the final large-stage validation pass.
