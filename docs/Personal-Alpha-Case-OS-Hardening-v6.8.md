# Personal Alpha Case OS Hardening v6.8

## Objective

v6.8 hardens the Personal Alpha Case OS safety surface. It unifies safe responses, no raw content guards, runtime storage guards, response consistency checks, and hardening API visibility without adding a new business workflow.

v6.8 remains local-only, mock-first, controlled-first, metadata-only, redacted-only, preview-only, and advisory-only.

## Relationship to v6.7

v6.7 added a local regression suite for Case OS. v6.8 builds on that suite by adding hardening APIs and a new regression script that checks safe response flags, hardening safety checks, response consistency, and runtime storage guard behavior.

## Safe Response Utilities

`personal_alpha_case_os/safety_response.py` provides common builders and flags:

- safe safety flags
- safe warnings
- safe not_found response
- blocked response
- redacted response
- metadata response normalization helper

These helpers avoid exposing unsafe case ids, local paths, runtime storage paths, or raw content.

## Safe Not Found Response

The safe not_found builder returns a blocked metadata response with:

- `status=not_found`
- `reason=safe_not_found`
- `blocked=true`
- safe or redacted `case_id`
- `raw_content_included=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`

## Blocked and Redacted Responses

Blocked and redacted responses use common safety flags and warnings. Unsafe values are not echoed back to clients. Unsafe case ids become empty safe metadata tokens.

## No Raw Content Guard

`personal_alpha_case_os/safety_guard.py` provides:

- `contains_unsafe_value`
- `redact_unsafe_value`
- `assert_safe_metadata_value`
- `scan_response_for_unsafe_values`
- `scan_scoped_payloads`

The guard detects API keys, personal identifiers, local paths, raw material markers, raw OCR markers, raw legal search markers, real case directories, and unsafe file extensions. It keeps known metadata values such as `json`, `markdown`, and app routes from being misclassified.

## Runtime Storage Guard

`personal_alpha_case_os/runtime_guard.py` centralizes runtime root handling:

- runtime root is `Lawyer-AI-Platform-App/backend/storage/runtime`
- `ensure_runtime_path` blocks paths outside runtime storage
- `is_path_under_runtime` checks path containment
- `redacted_runtime_path` avoids returning absolute paths

Case OS export package storage uses this guard for runtime path construction.

## Response Consistency Checks

`personal_alpha_case_os/response_consistency.py` checks and normalizes:

- `mock_or_redacted_only`
- `raw_content_included`
- `final_legal_opinion_generated`
- `final_report_generated`
- `warnings`

The hardening response consistency API verifies selected Case OS responses after safe normalization.

## Hardening APIs

New endpoints:

- `GET /case-os/hardening/status`
- `GET /case-os/{case_id}/hardening/safety-check`
- `GET /case-os/{case_id}/hardening/response-consistency`
- `GET /case-os/{case_id}/hardening/runtime-storage-check`

All hardening APIs are metadata-only and do not execute workflow actions.

## Frontend Updates

The Case OS detail page now includes:

- Hardening Safety Check
- Response Consistency
- Runtime Storage Check
- JSON panels for each hardening response

## Regression Updates

The regression suite adds:

- `scripts/regression/check_case_os_hardening_apis.sh`

The full suite now runs hardening checks after quality API checks.

## Metadata-Only Rule

Hardening APIs scan metadata responses only. They do not read raw material text, raw OCR text, raw legal search text, package file content, or real case files.

## No Final Legal Opinion

v6.8 does not generate a formal legal opinion and verifies generated flags remain false.

## No Final Report Generated

v6.8 does not generate final report bodies, PDF, or DOCX output and verifies generated flags remain false.

## v6.9 Readiness

v6.9 can become a Personal Alpha Case OS release candidate: summarize v6.0-v6.8 capabilities, run full regression, verify tags/docs/changelogs, and perform final hardening audit without adding major new workflow behavior.
