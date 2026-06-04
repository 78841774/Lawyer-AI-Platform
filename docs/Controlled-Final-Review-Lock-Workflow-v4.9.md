# Controlled Final Review Lock Workflow v4.9

## Objective

v4.9 adds a local-only Controlled Final Review Lock workflow for locking a mock final review candidate after the v4.6 draft, v4.7 lawyer review, and v4.8 revision workflow.

This workflow is a dry controlled lock step. It does not produce a formal legal opinion, does not publish a Skill, and does not enable production runtime.

## Scope

- Default mode: mock final review lock.
- Runtime route group: `/controlled-final-review`.
- Runtime storage: `storage/runtime/controlled_final_review_locks`.
- Storage target is ignored local runtime only.
- The lock snapshot is immutable mock metadata and redacted notes only.
- Draft, review, and revision IDs are required.
- Explicit final lock confirmation is required.
- Manual final lawyer review confirmation is required.
- Final checklist confirmation is required.

## API

- `GET /controlled-final-review/status`
- `POST /controlled-final-review/lock`
- `GET /controlled-final-review/{final_lock_id}`
- `GET /controlled-final-review/audit-logs`

## Safety Boundary

v4.9 is intentionally local-only and mock-only.

- v4.9 does not call a real LLM.
- v4.9 does not call DeepSeek live.
- v4.9 does not call real OCR.
- v4.9 does not call a real legal database.
- v4.9 does not submit raw material text.
- v4.9 does not submit raw OCR text.
- v4.9 does not submit raw legal search results.
- v4.9 mock final lock snapshot is stored only in ignored runtime storage.
- v4.9 does not generate a formal legal opinion.
- v4.9 is only a final review candidate lock.

The provider guard blocks live, production, remote, external, deepseek, and deepseek_live modes.

## Lock Gates

The lock request must pass all of these gates:

- `draft_id` is present.
- `review_id` is present.
- `revision_id` is present.
- `final_checklist_confirmed` is true.
- `explicit_final_lock_confirmation` is true.
- `manual_final_review_confirmed` is true.
- `preview_only` remains true.
- Provider mode remains controlled local or mock.
- No raw content keys are accepted.
- Runtime storage is enabled and Git storage remains disabled.

## Audit

Every lock attempt writes a sanitized audit event with:

- case ID
- workspace ID
- draft ID
- review ID
- revision ID
- final lock ID
- result
- warnings
- timestamp

Audit logs do not include raw material text, raw OCR text, raw legal search results, or final legal opinion content.

## Snapshot

The mock final review snapshot contains:

- linked draft ID
- linked review ID
- linked revision ID
- redacted final review notes
- final lawyer checklist
- mock source trace snapshot
- explicit limitations

The snapshot is not a production artifact and is not a formal legal opinion.

## A1-A13

v4.9 does not alter the A1-A13 analysis chain.

A10 remains: 争议焦点法律深化分析。

## v5.0 Readiness

v4.9 prepares a safe lock boundary for a later v5.0 acceptance workflow. Any v5.0 path must separately decide whether to enable production, external providers, formal opinion generation, and non-runtime storage.
