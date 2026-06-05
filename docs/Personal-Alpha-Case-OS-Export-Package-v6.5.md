# Personal Alpha Case OS Export Package v6.5

## Objective

v6.5 adds metadata-only export package creation on top of the v6.4 metadata closure export preview.

The package is a Personal Alpha local artifact. It is not production archive, not a formal legal opinion, and not a final case report.

## Relationship to v6.4

v6.4 introduced metadata closure and export preview with `would_create_file=false`. v6.5 keeps the same safety rules but allows a confirmed metadata-only package to be written to ignored runtime storage.

## APIs

- `GET /case-os/{case_id}/export-packages/status`
- `POST /case-os/{case_id}/export-packages/create`
- `GET /case-os/{case_id}/export-packages`
- `GET /case-os/{case_id}/export-packages/{package_id}`
- `GET /case-os/{case_id}/export-packages/{package_id}/content`
- `GET /case-os/{case_id}/export-packages/{package_id}/safety-check`
- `GET /case-os/{case_id}/export-packages/summary`

## JSON Package Structure

The JSON package contains metadata-only sections:

- package_header
- case_profile_metadata
- stage_summary
- review_state_summary
- final_lock_consolidation
- metadata_closure_summary
- metadata_closure_checklist
- audit_summary
- redaction_check_summary
- safety_checklist
- version_trace

It sets `metadata_only=true`, `raw_content_included=false`, `final_legal_opinion_generated=false`, and `final_report_generated=false`.

## Markdown Package Structure

The Markdown package contains the same metadata sections rendered as a human-readable summary:

- Safety Notice
- Case Profile Metadata
- Stage Summary
- Review State Summary
- Final Lock Consolidation
- Metadata Closure Checklist
- Audit Summary
- Safety Checklist
- Version Trace

It does not contain source text, OCR text, legal search text, formal legal analysis, final report body, local paths, real filenames, API keys, or personal identifiers.

## Storage

Export packages are written only under ignored runtime storage:

`Lawyer-AI-Platform-App/backend/storage/runtime/personal_alpha_case_os/export_packages`

The APIs redact file paths and expose only safe metadata names.

## Safety Check

The safety check scans package metadata and content for path-like values, API-key-like values, and personal-identifier-like values. Unsafe results return only field names and reasons, never the original values.

## Safety Rules

- Local-only.
- Mock-first and controlled-first.
- Metadata-only and redacted-only.
- Advisory-only.
- Manual review and lawyer review required.
- No automatic workflow execution.
- No raw material text exported.
- No raw OCR text exported.
- No raw legal search result text exported.
- No final legal opinion generated.
- No final report generated.
- No PDF or DOCX generated in v6.5.
- No external upload or transmission.
- No automatic Skill publish.
- No automatic Workspace Runtime enablement.

## Frontend Updates

The Case OS detail page now includes export package status, create form, summary, list, detail, content, safety check, and JSON panels.

## v6.6 Readiness

v6.6 can add a quality checklist over workspace, source review, final lock, metadata closure, and export package completeness while keeping the same no-raw-content boundary.
