# Personal Alpha Controlled Lawyer Final Review v5.8

## Objective

v5.8 adds controlled lawyer final review actions for metadata-only final review packets created in v5.7. It allows a local reviewer or lawyer to approve, request revision, or reject a final review packet before any later controlled lock workflow.

This stage does not generate a final legal opinion or final report body.

## Relationship to v5.7

v5.8 requires an existing v5.7 final review packet. The workflow reads packet metadata and records lawyer review action metadata in ignored runtime storage.

## Backend API

- `GET /personal-alpha-lawyer-final-review/status`
- `GET /personal-alpha-lawyer-final-review/packets/{packet_id}`
- `GET /personal-alpha-lawyer-final-review/packets/{packet_id}/summary`
- `GET /personal-alpha-lawyer-final-review/packets/{packet_id}/actions`
- `POST /personal-alpha-lawyer-final-review/packets/{packet_id}/actions`
- `GET /personal-alpha-lawyer-final-review/actions/{action_id}`

## Action Types

Allowed actions:

- `approve_packet`
- `request_packet_revision`
- `reject_packet`

Any other action is blocked and is not written to action storage.

## Summary Logic

- Latest `approve_packet`: ready for controlled final lock.
- Latest `request_packet_revision`: packet revision required.
- Latest `reject_packet`: additional lawyer review required.
- No actions: pending lawyer review.

## Frontend Page

The `/personal-alpha-lawyer-final-review` page provides:

- safety boundary card
- packet input
- packet review summary
- packet metadata panel
- lawyer final review action form
- review action history
- action detail panel

The Final Packet page links to this page only for created packet records.

## Safety Boundary

- local-only
- mock-first
- controlled-first
- metadata-only
- redacted-only
- preview-only
- advisory-only
- manual review required
- lawyer review required
- final packet required
- no raw content
- no raw quote
- no real LLM
- no DeepSeek live
- no real OCR
- no real legal database
- no final legal opinion
- no final report generated
- no automatic Skill publish
- no automatic Workspace Runtime enablement

## Runtime Storage

Lawyer final review action records are written only to ignored runtime storage:

`storage/runtime/personal_alpha_lawyer_final_review/actions`

Action records do not include raw material text, raw OCR text, raw legal search result text, local absolute paths, real filenames, or final legal analysis content.

## v5.9 Readiness

v5.8 exposes lawyer action detail and summary APIs that can be consumed by a later controlled final lock workflow.
