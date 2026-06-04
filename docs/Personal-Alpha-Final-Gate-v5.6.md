# Personal Alpha Controlled Final Review Gate v5.6

## Objective

v5.6 adds a Personal Alpha Controlled Final Review Gate. It checks whether a `workspace_run_id` may enter a controlled final review step based on v5.5 Final Review Readiness metadata and a manual gate decision.

v5.6 does not generate a final report and does not generate a formal legal opinion.

## Relationship to v5.5

v5.5 produces a metadata-only final review readiness checklist. v5.6 consumes that checklist and requires a manual gate decision before allowing the run to proceed to the controlled final review step.

The gate is advisory metadata only. It does not approve legal content.

## Backend API

Base path: `/personal-alpha-final-gate`

### GET `/status`

Returns local-only final gate status and provider safety flags.

### GET `/run/{workspace_run_id}`

Returns:

- final readiness metadata
- gate open status
- controlled final review proceed status
- gate requirements
- safety checklist
- gate summary

### GET `/run/{workspace_run_id}/summary`

Returns gate summary metadata:

- `gate_open`
- `final_review_ready`
- `requires_additional_review`
- `latest_gate_decision`
- `gate_decision_count`
- `can_proceed_to_controlled_final_review`

### GET `/run/{workspace_run_id}/decisions`

Returns metadata-only gate decision history from ignored runtime storage.

### POST `/run/{workspace_run_id}/decisions`

Records a valid manual gate decision when all confirmation gates pass.

Allowed decisions:

- `approve_gate`
- `block_gate`
- `request_more_review`

Required confirmations:

- `manual_review_confirmed=true`
- `metadata_only_confirmation=true`
- `no_final_legal_opinion_confirmation=true`

## Gate Decision Logic

`can_proceed_to_controlled_final_review=true` only when:

- v5.5 `final_review_ready=true`
- `gate_open=true`
- latest gate decision is `approve_gate`
- latest gate decision is not `block_gate` or `request_more_review`

This only allows the controlled final review step. It does not mean a final legal opinion is approved.

If readiness has not passed, `approve_gate` is blocked and not written as a formal gate decision record.

## No Raw Content Guard

The final gate checks:

- `workspace_run_id`
- `decision`
- `reviewer_id`
- `reason`

It blocks path-like or raw-content-like values including API keys, phone numbers, ID numbers, emails, case numbers, local paths, filenames, `.env`, `local.db`, `storage/runtime`, `real_cases`, and `sandbox_cases`.

## Frontend Page

The `/personal-alpha-final-gate` page includes:

- Safety Boundary
- Workspace Run Input
- Gate Summary
- Gate Requirements
- Gate Decision Form
- Gate Decision History
- JSON Panels for run detail, summary, and decisions

The Final Readiness page links to the Final Gate page with `workspace_run_id`.

## Safety Boundary

v5.6 remains:

- local-only
- mock-first
- controlled-first
- metadata-only
- redacted-only
- preview-only
- advisory-only
- manual-review-required

v5.6 does not:

- call real LLM providers
- call DeepSeek live
- call real OCR
- call real legal databases
- read or return raw material text
- return raw OCR text
- return raw legal search results
- write raw quote into gate decisions
- generate a final legal opinion
- generate final report body
- publish a Skill
- enable Workspace Runtime automatically

## Runtime Storage

Gate records are written only to ignored runtime storage:

`storage/runtime/personal_alpha_final_gate/decisions`

Runtime files must not enter Git.

## v5.7 Readiness

v5.6 prepares a safe gate for a future v5.7 controlled final review packet. A future packet should remain metadata-only and include only run summary, stage readiness, source review decisions, gate decisions, and safety checklist.
