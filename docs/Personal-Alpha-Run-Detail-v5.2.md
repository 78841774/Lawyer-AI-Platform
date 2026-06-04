# Personal Alpha Run Detail v5.2

## Objective

v5.2 adds a workspace-run detail API and frontend detail page for a single Personal Alpha Workspace run.

The detail view is scoped by `workspace_run_id` and shows metadata-only run summary, stage details, filtered audit timeline, source refs, guard summary, safety checklist, and warnings.

## Relationship To v5.0 And v5.1

v5.0 creates local mock Personal Alpha Workspace runs.

v5.1 provides the Personal Alpha Case Dashboard summary view.

v5.2 adds the run-level drilldown from the Dashboard. It does not add real AI capabilities and does not change the controlled workflow.

## API

`GET /personal-alpha-dashboard/runs/{workspace_run_id}`

The API loads existing Personal Alpha Workspace runtime metadata and returns a safe detail payload. If the run is unavailable, it returns a safe `not_found` structure without local paths or raw content.

## Frontend Route

`/personal-alpha-dashboard/runs/{workspaceRunId}`

The Dashboard also provides a `workspace_run_id` input and a View Run Detail link when a workspace run ID is available in the audit timeline.

## Safety Boundary

- Local-only.
- Mock-first / controlled-first.
- Metadata-only.
- Redacted-only.
- Preview-only.
- Manual review required.
- No production provider.
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

The run detail view may display IDs, stage status, timestamps, mock source refs, mock audit events, and explicit safety booleans. It must not display raw material text, OCR text, legal search result text, API keys, local file paths, real client identifiers, or case numbers.

## v5.3 Readiness

v5.3 can build a Personal Alpha Evidence / Source Trace Review view that improves manual review of source ref metadata while keeping the no-raw-content boundary.
