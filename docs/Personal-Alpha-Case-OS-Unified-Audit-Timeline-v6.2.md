# Personal Alpha Case OS Unified Audit Timeline v6.2

## Objective

v6.2 adds a unified metadata audit timeline for the Personal Alpha Case OS.

The goal is to normalize audit metadata from v5.0-v5.9 controlled workflow modules and v6.0-v6.1 Case OS modules into a single Case OS audit view with filters, summary statistics, and redaction checks.

## Relationship to v6.0 and v6.1

v6.0 introduced the Case OS foundation, including the initial audit timeline endpoint.

v6.1 added the stage orchestration layer, including stage routes, action eligibility, blockers, and transition preview.

v6.2 keeps those endpoints intact and strengthens audit visibility by adding a unified timeline engine around metadata-only workflow events.

## Unified Audit Timeline API

Added:

- `GET /case-os/{case_id}/audit-timeline/unified`
- `GET /case-os/{case_id}/audit-timeline/summary`
- `GET /case-os/{case_id}/audit-timeline/redaction-check`
- `GET /case-os/{case_id}/audit-timeline/filters`

The legacy endpoint remains available:

- `GET /case-os/{case_id}/audit-timeline`

The legacy endpoint remains compatible while using the unified audit event source internally.

## Audit Filters

The unified timeline supports:

- `stage_id`
- `event_type`
- `result`
- `safety_status`
- `limit`
- `offset`

Filtering is metadata-only and does not read raw case material, OCR output, legal search result text, or local case directories.

## Audit Summary

The summary endpoint reports:

- total events
- stage count
- blocked event count
- warning event count
- redacted event count
- unsafe event count
- raw content event count
- latest event timestamp
- modules
- per-stage event summaries

## Redaction Check

The redaction check scans public audit event fields for unsafe values and reports only safe summaries:

- event id
- field name
- reason

It never echoes the unsafe original value.

## Event Normalization

Unified audit events use a stable schema:

- `timeline_event_id`
- `case_id`
- `workspace_run_id`
- `packet_id`
- `lock_id`
- `stage_id`
- `module`
- `event_type`
- `result`
- `safety_status`
- `actor_id`
- `action`
- `target_id`
- `message`
- `mock_or_redacted_only`
- `raw_content_included`
- `redacted`
- `warnings`
- `created_at`

## Frontend Updates

The Case OS detail page now includes:

- Unified Audit Timeline
- Audit Filters
- Audit Summary
- Redaction Check
- JSON panels for unified timeline, summary, redaction check, and available filters

The page keeps the existing Case Profile, Next Action, Stage Summary, Stage Orchestration, Stage Progress, Action Eligibility, Blockers, Stage Transitions, and Safety Checklist sections.

## Metadata-Only Rule

All v6.2 audit APIs are metadata-only. Public responses include `mock_or_redacted_only=true` and `raw_content_included=false`.

## No Raw Content Rule

v6.2 does not return:

- raw material text
- raw OCR text
- raw legal search result text
- raw quotes
- original evidence text
- local filesystem paths
- real filenames

Unsafe audit fields are redacted at the event level without failing the whole timeline response.

## No Final Legal Opinion

v6.2 does not generate formal legal opinions and reports `final_legal_opinion_generated=false` where applicable.

## No Final Report Generated

v6.2 does not generate final report bodies and reports `final_report_generated=false` where applicable.

## v6.3 Readiness

v6.2 prepares for a Case OS Review State Machine by providing normalized stage metadata, event types, safety status, summary statistics, and redaction checks that future state transitions can reference.
