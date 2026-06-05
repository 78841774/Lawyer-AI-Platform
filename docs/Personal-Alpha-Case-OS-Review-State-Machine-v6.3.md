# Personal Alpha Case OS Review State Machine v6.3

## Objective

v6.3 adds a metadata-only Review State Machine to the Personal Alpha Case OS.

It unifies current stage, next action, transition preview, blockers, and audit metadata into a defined review state model. It validates transitions and derives state history without executing workflow actions.

## Relationship to v6.0, v6.1, and v6.2

v6.0 introduced the Case OS foundation.

v6.1 added stage orchestration, action eligibility, blockers, and route mapping.

v6.2 added the unified audit timeline, filters, summary statistics, and redaction checks.

v6.3 builds on those layers and adds formal review state definitions, transition rules, transition validation, state history, and review state summaries.

## Review States

- `draft`
- `intake_ready`
- `workspace_run_ready`
- `source_review_pending`
- `source_reviewed`
- `source_decision_pending`
- `source_decision_completed`
- `final_readiness_pending`
- `final_readiness_ready`
- `final_gate_pending`
- `final_gate_approved`
- `final_packet_pending`
- `final_packet_created`
- `lawyer_final_review_pending`
- `lawyer_review_approved`
- `lawyer_review_revision_requested`
- `lawyer_review_rejected`
- `final_lock_pending`
- `final_lock_created`
- `completed_metadata_review`
- `blocked`

All states are metadata states. They do not represent a formal legal opinion or a final legal conclusion.

## Allowed Transitions

The state rules define a linear metadata review path from draft intake through final lock, with branches for lawyer final review approval, revision request, and rejection.

The transition validator returns `allowed` and `valid_transition` only. It never executes the target action.

## Blocked Transitions

Unsafe input or blocked metadata returns `blocked` or a blocked validation response. Unsafe values are not echoed back to the caller.

v6.3 does not implement reset from `blocked` to `draft`; reset is reserved for a later controlled feature.

## Terminal States

Terminal states are:

- `completed_metadata_review`
- `blocked`

`completed_metadata_review` means the metadata workflow has reached final lock metadata. It does not mean a formal legal review or legal opinion has been completed.

## State History Metadata

State history is derived from unified audit timeline metadata and stage metadata. It includes only metadata ids, modules, stages, transition names, and timestamps.

It does not include raw material text, raw OCR text, legal search result text, quotes, evidence text, local paths, or real filenames.

## Transition Validation API

Added:

- `GET /case-os/{case_id}/review-state`
- `GET /case-os/{case_id}/review-state/history`
- `GET /case-os/{case_id}/review-state/transitions`
- `GET /case-os/{case_id}/review-state/validate-transition`
- `GET /case-os/{case_id}/review-state/summary`

Validation supports:

- `from_state`
- `to_state`

The response always includes `would_execute_action=false`.

## Frontend Updates

The Case OS detail page now includes:

- Review State Machine
- Review State Summary
- Review State History
- Available Transitions
- Transition Validation Panel
- JSON panels for review state payloads

Existing Case OS detail sections remain available, including stage orchestration and unified audit timeline panels.

## Metadata-Only Rule

All v6.3 APIs are metadata-only, redacted-only, preview-only, and advisory-only.

## No Raw Content Rule

v6.3 does not return:

- raw material text
- raw OCR text
- raw legal search result text
- raw quotes
- evidence text
- local filesystem paths
- real filenames

## No Final Legal Opinion

v6.3 does not generate a formal legal opinion and reports `final_legal_opinion_generated=false`.

## No Final Report Generated

v6.3 does not generate final report bodies and reports `final_report_generated=false`.

## v6.4 Readiness

v6.3 prepares for Controlled Final Lock Consolidation by giving Case OS a stable `completed_metadata_review` state, transition validation, and metadata-only state history.
