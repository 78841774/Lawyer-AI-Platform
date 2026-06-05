# Personal Alpha Case OS Final Lock Consolidation v6.4

## Objective

v6.4 adds a controlled Case OS metadata closure view that consolidates final lock metadata, review state metadata, closure checklist metadata, closure blockers, and an export preview.

This stage does not create a final legal opinion, does not generate a final report, and does not execute workflow actions.

## Relationship to v5.9 and v6.3

- v5.9 provides controlled final lock metadata.
- v6.3 provides the derived review state machine.
- v6.4 combines those records with the unified audit timeline into a metadata-only closure view.

## APIs

- `GET /case-os/{case_id}/final-lock-consolidation`
- `GET /case-os/{case_id}/metadata-closure`
- `GET /case-os/{case_id}/metadata-closure/checklist`
- `GET /case-os/{case_id}/metadata-closure/blockers`
- `GET /case-os/{case_id}/metadata-closure/export-preview`

## Final Lock Consolidation

The consolidation response reports whether a final lock exists, which packet and lawyer review action are linked, the derived review state, and whether the case has reached `completed_metadata_review`.

If no final lock exists, the response remains metadata-only and returns `final_lock_pending`. It does not create a lock.

## Metadata Closure

Metadata closure is ready only when required upstream metadata exists, the lawyer review is approved, final lock metadata exists, audit metadata is available, and the redaction check passes.

The response remains advisory and includes the next metadata action when closure is pending or blocked.

## Checklist and Blockers

The closure checklist includes workspace, source review, source decision, readiness, gate, packet, lawyer review, final lock, audit, redaction, and safety checks.

Closure blockers are generated from failed required checklist items. The `final_lock_missing` blocker points to `/personal-alpha-final-lock` with `create_final_lock`, but v6.4 does not execute that action.

## Export Preview

The export preview is metadata-only:

- `would_create_file=false`
- `would_include_raw_content=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`

It previews sections only and writes no files.

## Frontend Updates

The Case OS detail page now shows:

- Final Lock Consolidation
- Metadata Closure Summary
- Metadata Closure Checklist
- Closure Blockers
- Export Preview
- JSON panels for the v6.4 payloads

## Safety Rules

- Local-only.
- Mock-first and controlled-first.
- Metadata-only and redacted-only.
- Preview-only and advisory-only.
- Manual review and lawyer review required.
- No raw material text.
- No raw OCR text.
- No raw legal search result text.
- No final legal opinion.
- No final report generated.
- No automatic workflow execution.
- No automatic Skill publish.
- No automatic Workspace Runtime enablement.

## v6.5 Readiness

v6.5 can build on the v6.4 export preview to create a metadata-only export package in ignored runtime storage while preserving the same no-raw-content boundaries.
