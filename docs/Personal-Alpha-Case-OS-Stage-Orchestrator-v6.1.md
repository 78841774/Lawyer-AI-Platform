# Personal Alpha Case OS Stage Orchestrator v6.1

## Objective

v6.1 adds a metadata-only stage orchestration layer on top of the v6.0 Personal Alpha Case OS foundation.

The goal is to make `current_stage`, `next_action`, `blocked_reasons`, `target_route`, and `action_eligibility` more stable and easier to inspect from both API and frontend views.

## Relationship to v6.0

v6.0 introduced the Case OS foundation:

- Case OS status, list, detail, audit timeline, next action, and safety checklist endpoints.
- Metadata aggregation for the controlled Personal Alpha workflow.
- Redacted-only and mock-first safety defaults.

v6.1 keeps those endpoints intact and adds a stage orchestration layer without reading raw case content or producing legal outputs.

## New API Surface

The following endpoints are available under `/case-os`:

- `GET /case-os/{case_id}/stage-orchestration`
- `GET /case-os/{case_id}/stage-transitions`
- `GET /case-os/{case_id}/action-eligibility`
- `GET /case-os/{case_id}/blockers`

All responses include:

- `mock_or_redacted_only=true`
- `raw_content_included=false`
- no final legal opinion
- no final report body

## Stage Orchestration

The stage orchestrator builds a stable ordered view of the Personal Alpha workflow:

1. `workspace_run`
2. `source_review`
3. `source_review_decision`
4. `final_readiness`
5. `final_gate`
6. `final_packet`
7. `lawyer_final_review`
8. `final_lock`

Each stage reports:

- readiness
- blocked state
- required state
- next action when applicable
- frontend target route
- metadata-only and raw-content flags

## Transition Preview

Stage transitions are advisory previews. They report whether a transition is completed, available, pending, or blocked. They do not execute workflow actions and do not enable automatic runtime behavior.

## Action Eligibility

Action eligibility is calculated from metadata-only workflow state:

- available action must match the Case OS `next_action`
- required metadata must exist
- manual confirmation is still required
- lawyer review confirmation is required for final review and final lock steps
- final lock requires latest lawyer final review action to be `approve_packet`

## Blocker Summary

The blocker endpoint aggregates stage-level blockers and top-level blocked reasons. It uses controlled fixed reason strings and does not include raw source text, raw OCR text, local file paths, filenames, or legal search result text.

## Route Mapping

Stage routes are centralized in `stage_routes.py`. Routes only return frontend paths and may use metadata identifiers such as `case_id` or `workspace_run_id`. They do not include local filesystem paths or raw filenames.

## Frontend Updates

The Case OS list page now shows:

- current stage
- next action
- blocked state
- blocked reasons
- View Case OS action
- View Next Action action

The Case OS detail page now shows:

- Stage Orchestration
- Stage Progress
- Action Eligibility
- Blockers
- Stage Transitions
- JSON panels for the new orchestration responses

It continues to show:

- Case Profile
- Next Action
- Stage Summary
- Audit Timeline
- Safety Checklist

## Safety Boundary

v6.1 remains:

- local-only
- mock-first
- controlled-first
- metadata-only
- redacted-only
- preview-only
- advisory-only
- manual-review-required
- lawyer-review-required

v6.1 does not:

- call a real LLM
- call DeepSeek live
- call real OCR
- call a real legal database
- read raw material text
- return raw OCR text
- include raw legal search result text
- write evidence source text into Case OS
- generate a formal legal opinion
- generate a final report body
- publish a Skill automatically
- enable Workspace Runtime automatically

## v6.2 Readiness

The stage orchestrator prepares Case OS for v6.2 Unified Audit Timeline work by providing stable stage ids, stage routes, action ids, eligibility checks, and blocker summaries that can be attached to future metadata audit events.
