# Personal Alpha Source Review Decision v5.4

## Goal

v5.4 adds a local-only decision layer to Personal Alpha Source Review. It lets a reviewer record advisory metadata decisions for source refs and evidence-chain entries after v5.3 review.

The workflow remains:

- local-only
- mock-first
- controlled-first
- metadata-only
- redacted-only
- preview-only
- manual-review-required

It does not generate a formal legal opinion and does not call any live provider.

## API

Base path: `/personal-alpha-source-review`

### GET `/run/{workspace_run_id}/decisions`

Returns decision history for the workspace run from ignored runtime storage.

### POST `/run/{workspace_run_id}/decisions`

Records one advisory source-review decision.

Allowed decisions:

- `approve`
- `reject`
- `request_revision`
- `mark_unclear`

Required gates:

- `manual_review_confirmed=true`
- `metadata_only_confirmation=true`

Request fields:

- `source_ref_id`
- `decision`
- `reviewer_id`
- `reason`
- `manual_review_confirmed`
- `metadata_only_confirmation`

Invalid decisions return a safe blocked-style result with `status=invalid_decision`.
Unsafe raw-content-like payloads return a safe blocked result and are not written to runtime storage.

### GET `/run/{workspace_run_id}/decision-summary`

Returns count-based decision metadata:

- total decisions
- approved count
- rejected count
- revision requested count
- unclear count
- latest decision time
- ready for next stage
- requires additional review

If the run does not exist, the response remains safe and does not expose local paths or raw content.

## Runtime Storage

Decision records are stored under ignored runtime storage:

`storage/runtime/personal_alpha_source_review/decisions`

Records are sanitized before writing. They do not include raw material text, raw OCR text, raw legal search result text, local material paths, API keys, or final legal opinion content.

## Frontend

The `/personal-alpha-source-review` page now includes:

- Safety Boundary
- Run Summary
- Source Review Decision form
- Decision Summary
- Decision History
- Safety Checklist
- Source Trace Metadata
- Audit Timeline

The decision form supports `approve`, `reject`, `request_revision`, and `mark_unclear`, with manual review and metadata-only confirmation gates.

## Safety Boundary

v5.4 explicitly keeps these capabilities disabled:

- real LLM calls
- DeepSeek live calls
- real OCR calls
- real legal database calls
- raw material text reading or return
- raw OCR text return
- raw legal search result return
- formal legal opinion generation
- Skill publication
- Workspace Runtime auto-enablement

The decision layer is advisory metadata only.
