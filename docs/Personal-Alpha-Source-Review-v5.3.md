# Personal Alpha Source Review v5.3

## Objective

v5.3 adds a Personal Alpha Evidence / Source Trace Review view for workspace-run source refs and evidence-chain metadata.

The module focuses on manual review of metadata-level source traces. It does not add real provider integrations and does not read or return raw content.

## API

- `GET /personal-alpha-source-review/status`
- `GET /personal-alpha-source-review/run/{workspace_run_id}`
- `GET /personal-alpha-source-review/run/{workspace_run_id}/source-traces`
- `GET /personal-alpha-source-review/run/{workspace_run_id}/evidence-summary`

Each endpoint reads existing Personal Alpha Workspace mock metadata and returns metadata-only, mock or redacted payloads.

If a workspace run is not available, the API returns a safe `not_found` response without local paths, file paths, or raw text.

## Frontend

The frontend page is:

`/personal-alpha-source-review`

The Run Detail page links to Source Review with `workspace_run_id`, and the Source Review page also supports manual input.

The page displays:

- run summary
- safety checklist
- source trace metadata
- evidence summary
- audit timeline

## Safety Boundary

- Local-only.
- Mock-first / controlled-first.
- Metadata-only.
- Redacted-only.
- Preview-only.
- Manual review required.
- No real LLM call.
- No DeepSeek live call.
- No real OCR call.
- No real legal database call.
- No raw material text returned.
- No raw OCR text returned.
- No raw legal search result text returned.
- No final legal opinion generated.
- No automatic Skill publish.
- No automatic Workspace Runtime enablement.

## Metadata-Only Rule

Source Review may display source ref IDs, stage IDs, mock provider metadata, evidence status, audit event metadata, and safety booleans.

Source Review must not display raw material content, OCR text, legal search result text, API keys, local paths, real client identifiers, or final legal opinion content.
