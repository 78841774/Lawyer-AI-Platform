import json
from pathlib import Path
from typing import Any

from personal_alpha_dashboard.schemas import (
    PersonalAlphaDashboardAuditTimeline,
    PersonalAlphaDashboardSourceTraceSummary,
    PersonalAlphaDashboardStageHealth,
    PersonalAlphaDashboardStatus,
    PersonalAlphaWorkspaceSummary,
)
from personal_alpha_workspace.audit import list_personal_alpha_workspace_audit_logs

REPO_ROOT = Path("/Users/wazhen/Lawyer-AI-Platform")
WORKSPACE_RUNTIME_DIR = REPO_ROOT / "storage/runtime/personal_alpha_workspace"

DEFAULT_STAGES = [
    ("controlled_material_preview", "Material Preview"),
    ("controlled_ocr_preview", "OCR Preview"),
    ("controlled_legal_search_preview", "Legal Search Preview"),
    ("controlled_report_draft", "Report Draft"),
    ("controlled_lawyer_review", "Lawyer Review"),
    ("controlled_revision", "Revision"),
    ("controlled_final_review_lock", "Final Review Lock"),
]


def get_personal_alpha_dashboard_status() -> dict[str, Any]:
    return PersonalAlphaDashboardStatus(
        warnings=[
            "v5.1 dashboard is local-only and metadata-only.",
            "Dashboard aggregates mock or redacted v5.0 personal alpha workspace metadata.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No raw material text, raw OCR text, or raw legal search results are returned.",
            "No final legal opinion is generated.",
        ]
    ).model_dump()


def get_personal_alpha_dashboard_summary() -> dict[str, Any]:
    records = _load_workspace_records()
    stage_health = _stage_health_from_records(records)
    audit_events = _dashboard_audit_timeline(records)
    source_refs = _dashboard_source_refs(records)
    return PersonalAlphaWorkspaceSummary(
        total_workspace_runs=len(records),
        ready_stage_count=sum(1 for stage in stage_health if _is_ready(stage.get("status", ""))),
        pending_stage_count=sum(1 for stage in stage_health if _is_pending(stage.get("status", ""))),
        blocked_stage_count=sum(1 for stage in stage_health if _is_blocked(stage.get("status", ""))),
        audit_event_count=len(audit_events),
        source_trace_count=len(source_refs),
        mock_or_redacted_only=True,
        warnings=[
            "Summary is derived from local mock personal alpha workspace metadata only.",
            "Raw material text, OCR text, and legal search result text are not read.",
        ],
    ).model_dump()


def get_personal_alpha_dashboard_stage_health() -> dict[str, Any]:
    records = _load_workspace_records()
    return {
        "stage_health": [PersonalAlphaDashboardStageHealth(**stage).model_dump() for stage in _stage_health_from_records(records)],
        "mock_or_redacted_only": True,
        "warnings": ["Stage health is aggregated from mock or redacted controlled workflow metadata only."],
    }


def get_personal_alpha_dashboard_audit_timeline() -> dict[str, Any]:
    records = _load_workspace_records()
    return PersonalAlphaDashboardAuditTimeline(
        timeline=_dashboard_audit_timeline(records),
        mock_or_redacted_only=True,
        warnings=["Audit timeline contains sanitized mock or redacted events only."],
    ).model_dump()


def get_personal_alpha_dashboard_source_trace_summary() -> dict[str, Any]:
    records = _load_workspace_records()
    source_refs = _dashboard_source_refs(records)
    return PersonalAlphaDashboardSourceTraceSummary(
        source_refs=source_refs,
        source_trace_count=len(source_refs),
        mock_or_redacted_only=True,
        warnings=["Source trace summary contains metadata placeholders only. No raw source content is returned."],
    ).model_dump()


def _load_workspace_records() -> list[dict[str, Any]]:
    if not WORKSPACE_RUNTIME_DIR.exists():
        return []
    records: list[dict[str, Any]] = []
    for file_path in sorted(WORKSPACE_RUNTIME_DIR.glob("*.json")):
        try:
            parsed = json.loads(file_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(parsed, dict):
            records.append(_sanitize_workspace_record(parsed))
    return records


def _sanitize_workspace_record(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "workspace_run_id": str(record.get("workspace_run_id", "")),
        "case_id": str(record.get("case_id", "")),
        "workspace_id": str(record.get("workspace_id", "")),
        "workflow_mode": str(record.get("workflow_mode", "")),
        "stage_statuses": _safe_list(record.get("stage_statuses", [])),
        "unified_audit_timeline": _safe_list(record.get("unified_audit_timeline", [])),
        "source_refs": _safe_list(record.get("source_refs", [])),
        "created_at": str(record.get("created_at", "")),
        "mock_or_redacted_only": True,
    }


def _stage_health_from_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest_record = records[-1] if records else {}
    stage_map = {
        str(stage.get("stage_id", "")): stage
        for stage in _safe_list(latest_record.get("stage_statuses", []))
        if isinstance(stage, dict)
    }
    stage_health: list[dict[str, Any]] = []
    for stage_id, label in DEFAULT_STAGES:
        existing = stage_map.get(stage_id, {})
        stage_health.append(
            {
                "stage_id": stage_id,
                "label": str(existing.get("label", label)),
                "status": str(existing.get("status", "mock_pending_reference")),
                "required": bool(existing.get("required", True)),
                "mock_only": True,
                "source_ref_id": str(existing.get("source_ref_id", f"source_ref_{stage_id}")),
                "notes": str(existing.get("notes", f"{label} dashboard health is metadata-only.")),
            }
        )
    return stage_health


def _dashboard_audit_timeline(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    timeline: list[dict[str, Any]] = []
    for record in records:
        for event in _safe_list(record.get("unified_audit_timeline", [])):
            if not isinstance(event, dict):
                continue
            timeline.append(
                {
                    "timeline_event_id": str(event.get("timeline_event_id", "")),
                    "workspace_run_id": str(event.get("workspace_run_id", record.get("workspace_run_id", ""))),
                    "case_id": str(event.get("case_id", record.get("case_id", ""))),
                    "workspace_id": str(event.get("workspace_id", record.get("workspace_id", ""))),
                    "stage_id": str(event.get("stage_id", "")),
                    "event_type": str(event.get("event_type", "mock_stage_status")),
                    "result": str(event.get("result", "")),
                    "mock_or_redacted_only": True,
                    "created_at": str(event.get("created_at", record.get("created_at", ""))),
                }
            )
    for event in list_personal_alpha_workspace_audit_logs():
        if not isinstance(event, dict):
            continue
        timeline.append(
            {
                "timeline_event_id": str(event.get("audit_log_id", "")),
                "workspace_run_id": str(event.get("workspace_run_id", "")),
                "case_id": str(event.get("case_id", "")),
                "workspace_id": str(event.get("workspace_id", "")),
                "stage_id": "personal_alpha_workspace",
                "event_type": str(event.get("event_type", "personal_alpha_workspace")),
                "result": str(event.get("result", "")),
                "mock_or_redacted_only": True,
                "created_at": str(event.get("created_at", "")),
            }
        )
    return timeline


def _dashboard_source_refs(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_refs: list[dict[str, Any]] = []
    for record in records:
        for source_ref in _safe_list(record.get("source_refs", [])):
            if not isinstance(source_ref, dict):
                continue
            source_refs.append(
                {
                    "source_ref_id": str(source_ref.get("source_ref_id", "")),
                    "source_type": str(source_ref.get("source_type", "personal_alpha_workspace_stage")),
                    "workspace_run_id": str(source_ref.get("workspace_run_id", record.get("workspace_run_id", ""))),
                    "case_id": str(source_ref.get("case_id", record.get("case_id", ""))),
                    "workspace_id": str(source_ref.get("workspace_id", record.get("workspace_id", ""))),
                    "stage_id": str(source_ref.get("stage_id", "")),
                    "provider": str(source_ref.get("provider", "personal_alpha_workspace")),
                    "provider_mode": "mock",
                    "mock_or_redacted_only": True,
                }
            )
    return source_refs


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _is_ready(status: str) -> bool:
    return "ready" in status.lower()


def _is_pending(status: str) -> bool:
    return "pending" in status.lower()


def _is_blocked(status: str) -> bool:
    return "blocked" in status.lower()
