# Personal Alpha Case OS v6.0

## Objective

v6.0 adds a local-only Personal Alpha Case OS foundation on top of the controlled v5.0-v5.9 workflow. It aggregates mock and redacted metadata for each Personal Alpha case so a reviewer can inspect workflow status, stage health, next action, audit timeline, and safety boundaries from a single place.

This module is advisory-only. It does not generate a final legal opinion, final report body, production output, or Skill publication.

## Backend Module

Module path:

- `Lawyer-AI-Platform-App/backend/personal_alpha_case_os/`

Files:

- `__init__.py`
- `router.py`
- `schemas.py`
- `case_os_engine.py`
- `audit_engine.py`
- `state_machine.py`
- `next_action_engine.py`

Registered in `app/main.py` with the `/case-os` prefix.

## APIs

- `GET /case-os/status`
- `GET /case-os`
- `GET /case-os/{case_id}`
- `GET /case-os/{case_id}/audit-timeline`
- `GET /case-os/{case_id}/next-action`
- `GET /case-os/{case_id}/safety-checklist`

All responses are metadata-only and mock/redacted. Missing or unsafe case ids return safe blocked or not-found responses without local paths, raw material text, OCR text, legal-search result text, raw quotes, final reports, or final legal opinions.

## Aggregated Workflow

Case OS reads controlled metadata from:

- Personal Alpha Workspace
- Source Review
- Source Review Decision
- Final Readiness
- Final Gate
- Final Packet
- Lawyer Final Review
- Final Lock

The state machine derives the current stage and next recommended action from the latest metadata. It does not perform live execution and does not automatically advance workflow stages.

## Frontend

Pages:

- `/case-os`
- `/case-os/[caseId]`

The list page shows the Case OS safety boundary, case list, high-level state, and status JSON. The detail page shows run summary, stage cards, next action, audit timeline, safety checklist, and metadata JSON.

The AppShell navigation includes `Personal Alpha Case OS`.

## Safety Boundary

Required:

- local-only
- mock-first
- controlled-first
- metadata-only
- redacted-only
- preview-only
- advisory-only
- manual-review-required
- lawyer-review-required

Forbidden:

- real LLM calls
- DeepSeek live calls
- real OCR calls
- real legal database calls
- raw material text
- raw OCR text
- raw legal search results
- raw quotes
- final legal opinion generation
- final report body generation
- automatic Skill publishing
- automatic Workspace Runtime enabling

## Runtime and Git

Case OS aggregates existing ignored runtime metadata. It does not write raw content into Git-tracked paths and does not require storing production output.

Ignored paths remain required:

- `.env`
- `local.db`
- `storage/runtime`
- `node_modules`
- `__pycache__`
- `.DS_Store`

## v6.1 Readiness

v6.0 establishes the safe case-level orchestration surface. Future versions may add richer reviewer dashboards or workflow planning, but must preserve metadata-only, redacted-only, advisory-only behavior unless an explicit production safety design is introduced.
