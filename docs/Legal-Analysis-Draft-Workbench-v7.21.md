# Legal Analysis Draft Workbench v7.21

v7.21 adds the legal analysis draft workbench for the Personal Live Intelligence & Controlled Case Analysis large stage.

## Positioning

- Chinese page title: 法律分析草稿工作台.
- Route: `/personal-case-analysis/legal-drafts`.
- Scope: legal analysis draft layer only.
- Metadata-only.
- Draft-only.
- Owner-only.
- Source trace required.
- Audit required.
- Lawyer review required.
- Gate and quality scores are reference-only.
- No final legal opinion.
- No final report.
- No automatic delivery.

## API Surface

- `GET /personal-case-analysis/legal-drafts`
- `GET /personal-case-analysis/legal-drafts/{draft_id}`
- `POST /personal-case-analysis/legal-drafts/mock`
- `GET /personal-case-analysis/legal-drafts/{draft_id}/versions`
- `POST /personal-case-analysis/legal-drafts/{draft_id}/versions/mock`
- `GET /personal-case-analysis/legal-drafts/{draft_id}/quality`
- `GET /personal-case-analysis/legal-drafts/{draft_id}/gate`
- `POST /personal-case-analysis/legal-drafts/{draft_id}/confirm-for-review/mock`

Existing `/personal-case-analysis/review-queue`, `/source-traces`, `/audit`, and `/safety` APIs remain available.

## Frontend

`/personal-case-analysis/legal-drafts` shows:

- Legal draft hero and safety badges.
- Legal analysis summary draft.
- Dispute focus draft.
- Claim basis draft.
- Defense path draft.
- Risk notes draft.
- Next step checklist draft.
- Version history.
- Quality / Gate panel.
- Review queue panel.
- Source Trace panel.
- Owner Download Boundary.
- Trust / Safety panel.
- Developer Diagnostics folded by default.

`/personal-production` and `/personal-production-pilot` show v7.21 readiness and draft boundary metadata.

## Safety

v7.21 does not:

- call real providers
- read API keys
- read real case materials
- return raw content
- expose local paths
- write raw content into Git, docs, diagnostics, or regression output
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

Legal draft quality and gate status are advisory mock metadata only. They do not represent final legal conclusions, legal correctness guarantees, lawyer work product, final opinions, final reports, or delivery readiness.

## Regression

`scripts/regression/check_personal_legal_draft_apis.sh` checks legal draft, version, quality, gate, review confirmation, source trace, audit, and safety APIs. It verifies metadata-only / draft-only / owner-only fields and forbidden sensitive patterns.

The script is included in `run_personal_alpha_regression.sh`, but full Personal Alpha regression remains reserved for the final large-stage validation pass.
