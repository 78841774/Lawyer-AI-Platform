# Personal Alpha Dashboard v5.1

## Overview

v5.1 adds an independent Personal Alpha Case Dashboard on top of the v5.0 Personal Alpha End-to-End Local Case Workspace.

The dashboard provides a metadata-only control surface for reviewing local controlled workflow state:

- workspace summary
- stage health
- audit timeline
- source trace summary
- safety boundary status

The module aggregates v5.0 mock or redacted workspace metadata only. It does not read raw case materials, does not call live providers, and does not generate a final legal opinion or final report body.

## Baseline

- Baseline version: `v5.0-personal-alpha-workspace`
- v5.1 commit: `7ed843e`
- Commit message: `feat: add personal alpha case dashboard v5.1`

v5.1 files added or modified:

- `Lawyer-AI-Platform-App/backend/personal_alpha_dashboard/`
- `Lawyer-AI-Platform-App/backend/app/main.py`
- `Lawyer-AI-Platform-App/frontend/app/personal-alpha-dashboard/page.tsx`
- `Lawyer-AI-Platform-App/frontend/components/AppShell.tsx`
- `Lawyer-AI-Platform-App/frontend/services/api.ts`
- `Lawyer-AI-Platform-App/frontend/types/index.ts`

## Backend Module

Module path:

- `Lawyer-AI-Platform-App/backend/personal_alpha_dashboard/`

Files:

- `__init__.py`
- `dashboard_engine.py`
- `router.py`
- `schemas.py`

The module is registered in `app/main.py` and exposes routes under:

- `/personal-alpha-dashboard`

## API List

### GET /personal-alpha-dashboard/status

Returns the local dashboard status and hard safety flags.

Example response:

```json
{
  "enabled": true,
  "mode": "local_only_personal_alpha_dashboard",
  "production_enabled": false,
  "mock_first_enabled": true,
  "controlled_first_enabled": true,
  "metadata_only": true,
  "redacted_only": true,
  "requires_manual_review": true,
  "llm_live_enabled": false,
  "deepseek_live_enabled": false,
  "ocr_live_enabled": false,
  "legal_search_live_enabled": false,
  "final_legal_opinion_enabled": false,
  "auto_skill_publish_enabled": false,
  "auto_workspace_runtime_enabled": false,
  "source_runtime_path": "storage/runtime/personal_alpha_workspace",
  "warnings": [
    "v5.1 dashboard is local-only and metadata-only.",
    "Dashboard aggregates mock or redacted v5.0 personal alpha workspace metadata."
  ]
}
```

### GET /personal-alpha-dashboard/summary

Returns workspace-level aggregate counts.

Example response:

```json
{
  "total_workspace_runs": 0,
  "ready_stage_count": 0,
  "pending_stage_count": 7,
  "blocked_stage_count": 0,
  "audit_event_count": 0,
  "source_trace_count": 0,
  "mock_or_redacted_only": true,
  "warnings": [
    "Summary is derived from local mock personal alpha workspace metadata only.",
    "Raw material text, OCR text, and legal search result text are not read."
  ]
}
```

### GET /personal-alpha-dashboard/stage-health

Returns the seven controlled v5.0 stage cards:

- Material Preview
- OCR Preview
- Legal Search Preview
- Report Draft
- Lawyer Review
- Revision
- Final Review Lock

Example response:

```json
{
  "stage_health": [
    {
      "stage_id": "controlled_material_preview",
      "label": "Material Preview",
      "status": "mock_pending_reference",
      "required": true,
      "mock_only": true,
      "source_ref_id": "source_ref_controlled_material_preview",
      "notes": "Material Preview dashboard health is metadata-only."
    }
  ],
  "mock_or_redacted_only": true,
  "warnings": [
    "Stage health is aggregated from mock or redacted controlled workflow metadata only."
  ]
}
```

### GET /personal-alpha-dashboard/audit-timeline

Returns sanitized dashboard audit events from v5.0 workspace metadata.

Example response:

```json
{
  "timeline": [
    {
      "timeline_event_id": "timeline_controlled_material_preview",
      "workspace_run_id": "personal_alpha_workspace_run_demo",
      "case_id": "case_v50_demo_001",
      "workspace_id": "workspace_demo_001",
      "stage_id": "controlled_material_preview",
      "event_type": "mock_stage_status",
      "result": "mock_ready",
      "mock_or_redacted_only": true,
      "created_at": "2026-06-04T00:00:00Z"
    }
  ],
  "mock_or_redacted_only": true,
  "warnings": [
    "Audit timeline contains sanitized mock or redacted events only."
  ]
}
```

### GET /personal-alpha-dashboard/source-trace-summary

Returns source reference metadata placeholders only. It does not include raw quote text, raw OCR text, raw legal search results, or real material paths.

Example response:

```json
{
  "source_refs": [
    {
      "source_ref_id": "source_ref_controlled_material_preview",
      "source_type": "personal_alpha_workspace_stage",
      "workspace_run_id": "personal_alpha_workspace_run_demo",
      "case_id": "case_v50_demo_001",
      "workspace_id": "workspace_demo_001",
      "stage_id": "controlled_material_preview",
      "provider": "personal_alpha_workspace",
      "provider_mode": "mock",
      "mock_or_redacted_only": true
    }
  ],
  "source_trace_count": 1,
  "mock_or_redacted_only": true,
  "warnings": [
    "Source trace summary contains metadata placeholders only. No raw source content is returned."
  ]
}
```

## Frontend Page

Page path:

- `/personal-alpha-dashboard`

The page displays:

- Safety Boundary card
- Workspace Summary cards
- Stage Health cards
- Audit Timeline JSON panel
- Source Trace Summary JSON panel

AppShell navigation includes:

- `Personal Alpha Dashboard`

The frontend uses API helpers in `frontend/services/api.ts` and dashboard-related types in `frontend/types/index.ts`.

## Safety Boundary

v5.1 must remain:

- local-only
- mock-first
- controlled-first
- metadata-only
- redacted-only
- advisory-only
- manual-review-required

v5.1 must not:

- call a real LLM
- call DeepSeek live
- call real OCR
- call a real legal database
- read raw material text
- return raw OCR text
- return raw legal search results
- return raw source quote text
- generate a final legal opinion
- generate a final report body
- publish a Skill
- enable Workspace Runtime automatically
- write raw content into Git-tracked paths

## Runtime and Storage

The dashboard reads local v5.0 workspace runtime metadata from:

- `storage/runtime/personal_alpha_workspace`

The runtime storage path must remain ignored by Git. Dashboard responses are derived from sanitized metadata and must not expose real local paths or raw case content.

## Validation

v5.1 acceptance checks:

```bash
python -m compileall app personal_alpha_workspace personal_alpha_dashboard
npm run build
curl http://127.0.0.1:8001/personal-alpha-dashboard/status
curl http://127.0.0.1:8001/personal-alpha-dashboard/summary
curl http://127.0.0.1:8001/personal-alpha-dashboard/stage-health
curl http://127.0.0.1:8001/personal-alpha-dashboard/audit-timeline
curl http://127.0.0.1:8001/personal-alpha-dashboard/source-trace-summary
```

Expected results:

- backend compile succeeds
- frontend build succeeds
- all dashboard APIs return HTTP 200 in local mode
- all live provider flags are `false`
- `mock_or_redacted_only=true` where applicable
- no raw material, OCR text, legal-search result text, raw quote, final legal opinion, or final report body is returned
- runtime storage remains ignored by Git

## Release Notes

v5.1 is a controlled dashboard layer only. It does not change the v5.0 workflow execution model and does not introduce production provider behavior.
