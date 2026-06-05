# Legal & Enterprise Intelligence Gateway v7.3

## Objective

v7.3 adds a controlled Legal & Enterprise Intelligence Gateway foundation for personal production validation. It prepares legal search and enterprise intelligence metadata workflows without calling real providers, reading provider secrets, or returning raw external content.

## Relationship to v7.2

v7.2 introduced controlled material parsing and PaddleOCR runtime metadata. v7.3 does not consume raw OCR or parsing output. It only creates source-trace-ready metadata that can be reviewed by a lawyer before any later controlled use.

## Provider Placeholders

v7.3 registers metadata for:

- `kuaicha365_lawskills_provider`
- `tianyancha_ai_provider`
- `qichacha_provider_placeholder`
- `pkulaw_provider_placeholder`
- `national_law_database_provider_placeholder`

All providers remain provider-gated, metadata-only, not configured for live calls, and do not expose provider secrets.

## Legal Search Runtime

`POST /personal-intelligence/legal-search/mock` creates mock legal search metadata only when explicit confirmations are present.

The workflow:

- Does not call 快查 365 LawSkills API.
- Does not return law, judgment, article, or case full text.
- Does not use results in an AI prompt.
- Creates citation candidate metadata.
- Creates source trace metadata.
- Requires lawyer confirmation.
- Does not generate a final legal opinion or final report.

## Enterprise Intelligence Runtime

`POST /personal-intelligence/enterprise-query/mock` creates mock enterprise query metadata only when explicit confirmations are present.

The workflow:

- Does not call 天眼查 AI or other enterprise providers.
- Does not return raw enterprise records.
- Does not use results in an AI prompt.
- Creates source trace metadata.
- Requires lawyer confirmation.
- Does not generate a final legal opinion or final report.

## Confirmation Queue

`GET /personal-intelligence/confirmation-queue` lists source trace metadata pending lawyer confirmation.

`POST /personal-intelligence/confirmation-queue/{source_trace_id}/actions` records controlled confirmation actions:

- `confirm`
- `reject`
- `request_verification`
- `mark_low_confidence`
- `mark_not_relevant`

Confirmation actions only update metadata. They do not fetch raw provider content, call live services, or generate legal conclusions.

## Source Trace

Source trace metadata records:

- provider id
- source type
- source category
- query id
- citation status
- lawyer confirmation state
- mock-only flags

Source traces do not include raw external content, provider responses, API keys, local paths, or final-output material.

## Audit Metadata

Audit metadata is written under ignored runtime storage:

`Lawyer-AI-Platform-App/backend/storage/runtime/personal_intelligence_gateway/audit/`

Audit APIs return metadata only and do not expose provider secrets, external raw content, local paths, or final legal output.

## Safety Checklist

`GET /personal-intelligence/safety` confirms:

- mock-first enabled
- live provider calls disabled
- provider secret hidden
- manual and lawyer confirmation required
- source trace required
- no raw external content returned
- no AI prompt usage
- no final legal opinion
- no final report
- no external delivery

## Frontend Page

The page at `/personal-intelligence` includes:

- provider cards
- mock legal search form
- mock enterprise query form
- source trace panel
- lawyer confirmation queue
- audit and safety metadata

The UI does not show API keys, raw external content, local paths, or final legal output.

## Personal Production Integration

The Personal Production Console now registers legal search and enterprise intelligence runtimes with `target_route=/personal-intelligence`. Provider capability metadata points legal and enterprise providers to the same controlled gateway.

## Regression Updates

The regression suite adds `scripts/regression/check_personal_intelligence_apis.sh` and includes it after the v7.2 material runtime checks.

The script checks status, providers, mock legal search, mock enterprise query, source traces, confirmation queue, audit, safety, required confirmation blocking, and sensitive-string absence.

## No Live Provider Call

v7.3 does not call 快查 365 LawSkills API, 天眼查 AI, 企查查, 北大法宝, or the National Law Database.

## No Final Legal Opinion

v7.3 does not generate final legal opinions.

## No Final Report

v7.3 does not generate final reports and does not enable external delivery.

## Release Status

v7.3 is implemented in the current worktree for validation and release preparation. It is not committed, tagged, or released in this worktree.

## v7.4 Readiness

The next stage is Experience Package Skill Studio:

- experience package draft metadata
- skill candidate draft metadata
- mock test cases
- mock evaluations
- source trace metadata
- manual promotion gate
- no automatic Skill publish
