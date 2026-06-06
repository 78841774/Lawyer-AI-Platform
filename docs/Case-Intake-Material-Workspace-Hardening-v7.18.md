# Case Intake & Material Workspace Hardening v7.18

v7.18 adds a personal case and material workspace for the continuous Personal Live Intelligence & Controlled Case Analysis large stage.

## Positioning

- Personal case and material workspace.
- Owner-only.
- Metadata-only.
- Draft-only.
- Source trace required.
- Audit required.
- Lawyer review required.
- No real provider calls.
- No API key exposure.
- No real case material reading.
- No raw content in diagnostics, docs, Git, or regression output.

## API Surface

- `GET /personal-case-workspace/status`
- `GET /personal-case-workspace/cases`
- `GET /personal-case-workspace/cases/{case_id}`
- `GET /personal-case-workspace/cases/{case_id}/materials`
- `GET /personal-case-workspace/materials/{material_id}`
- `POST /personal-case-workspace/materials/{material_id}/owner-raw-view`
- `GET /personal-case-workspace/materials/{material_id}/ocr-status`
- `GET /personal-case-workspace/materials/{material_id}/source-traces`
- `GET /personal-case-workspace/materials/{material_id}/fact-input`
- `POST /personal-case-workspace/materials/{material_id}/fact-input/corrections/mock`
- `GET /personal-case-workspace/source-traces`
- `GET /personal-case-workspace/audit`
- `GET /personal-case-workspace/safety`

## Frontend

The `/personal-case-workspace` page shows:

- Workspace status cards.
- Case and material metadata selection.
- Owner raw view gate.
- OCR status metadata.
- Fact input and correction metadata.
- Source trace summary.
- Audit summary.
- Trust / Safety panel.
- Developer Diagnostics folded by default.

All display copy is Chinese by default. API fields and diagnostics JSON remain English.

## Safety

Every major response keeps owner-only, metadata-only, draft-only, source-trace-required, audit-required, and lawyer-review-required posture.

The runtime does not:

- call real providers
- read API keys
- read real case materials
- return raw content
- display local paths
- generate final legal opinions
- generate final reports
- create real PDF/DOCX files
- send email
- trigger external delivery
- generate training data
- write open-case material to training sets
- update or publish Skills

## Regression

`scripts/regression/check_personal_case_workspace_apis.sh` checks the v7.18 API surface, owner raw view gate, fact correction metadata, safety fields, and forbidden sensitive patterns.

The script is included in `run_personal_alpha_regression.sh`, but the large stage still uses lightweight sub-stage checks until final unified validation and comprehensive security audit.
