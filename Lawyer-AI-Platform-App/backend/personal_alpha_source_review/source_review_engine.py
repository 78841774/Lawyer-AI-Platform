from typing import Any

from personal_alpha_source_review.schemas import (
    PersonalAlphaEvidenceSummary,
    PersonalAlphaSourceReviewRunDetail,
    PersonalAlphaSourceReviewSafetyChecklist,
    PersonalAlphaSourceReviewStatus,
    PersonalAlphaSourceTrace,
)
from personal_alpha_workspace.audit import list_personal_alpha_workspace_audit_logs
from personal_alpha_workspace.workspace_engine import load_personal_alpha_workspace_run


def get_personal_alpha_source_review_status() -> dict[str, Any]:
    return PersonalAlphaSourceReviewStatus(
        warnings=[
            "v5.3 source review is local-only and metadata-only.",
            "Only mock or redacted source refs and evidence metadata are returned.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No raw material text, raw OCR text, or raw legal search result text is returned.",
            "No final legal opinion is generated.",
        ]
    ).model_dump()


def get_personal_alpha_source_review_run(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_not_found(loaded):
        return _not_found(workspace_run_id)
    source_traces = _source_traces(loaded)
    return PersonalAlphaSourceReviewRunDetail(
        workspace_run_id=str(loaded.get("workspace_run_id", workspace_run_id)),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        workflow_mode=str(loaded.get("workflow_mode", "")),
        status="mock_source_review_ready",
        mock_or_redacted_only=True,
        raw_content_included=False,
        source_traces=source_traces,
        evidence_summary=_evidence_summary(source_traces).model_dump(),
        audit_timeline=_audit_timeline(loaded),
        safety_checklist=PersonalAlphaSourceReviewSafetyChecklist().model_dump(),
        warnings=[
            "Personal alpha source review is metadata-only.",
            "No raw material text, raw OCR text, or raw legal search result text is returned.",
            *[str(item) for item in loaded.get("warnings", [])],
        ],
        created_at=str(loaded.get("created_at", "")),
    ).model_dump()


def get_personal_alpha_source_traces(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_not_found(loaded):
        return {
            "workspace_run_id": workspace_run_id,
            "source_traces": [],
            "mock_or_redacted_only": True,
            "raw_content_included": False,
            "warnings": ["Workspace run not found or not available in runtime storage."],
        }
    return {
        "workspace_run_id": str(loaded.get("workspace_run_id", workspace_run_id)),
        "source_traces": _source_traces(loaded),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
        "warnings": ["Source traces are metadata-only. No raw content included."],
    }


def get_personal_alpha_evidence_summary(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_not_found(loaded):
        return {
            "workspace_run_id": workspace_run_id,
            "evidence_summary": PersonalAlphaEvidenceSummary(
                warnings=["Workspace run not found or not available in runtime storage."]
            ).model_dump(),
            "mock_or_redacted_only": True,
            "raw_content_included": False,
        }
    source_traces = _source_traces(loaded)
    return {
        "workspace_run_id": str(loaded.get("workspace_run_id", workspace_run_id)),
        "evidence_summary": _evidence_summary(source_traces).model_dump(),
        "mock_or_redacted_only": True,
        "raw_content_included": False,
    }


def _not_found(workspace_run_id: str) -> dict[str, Any]:
    return PersonalAlphaSourceReviewRunDetail(
        workspace_run_id=workspace_run_id,
        status="not_found",
        mock_or_redacted_only=True,
        raw_content_included=False,
        source_traces=[],
        evidence_summary=PersonalAlphaEvidenceSummary(
            warnings=["Workspace run not found or not available in runtime storage."]
        ).model_dump(),
        audit_timeline=[],
        safety_checklist=PersonalAlphaSourceReviewSafetyChecklist().model_dump(),
        warnings=["Workspace run not found or not available in runtime storage."],
        created_at="",
    ).model_dump()


def _is_not_found(loaded: dict[str, Any]) -> bool:
    warnings = " ".join(str(item).lower() for item in loaded.get("warnings", []))
    return "not found" in warnings and not loaded.get("source_refs") and not loaded.get("stage_statuses")


def _source_traces(loaded: dict[str, Any]) -> list[dict[str, Any]]:
    workspace_run_id = str(loaded.get("workspace_run_id", ""))
    stage_status_by_id = {
        str(stage.get("stage_id", "")): str(stage.get("status", "mock_pending_reference"))
        for stage in _safe_list(loaded.get("stage_statuses", []))
        if isinstance(stage, dict)
    }
    traces = []
    for source_ref in _safe_list(loaded.get("source_refs", [])):
        if not isinstance(source_ref, dict):
            continue
        if str(source_ref.get("workspace_run_id", workspace_run_id)) != workspace_run_id:
            continue
        stage_id = str(source_ref.get("stage_id", ""))
        status = stage_status_by_id.get(stage_id, "mock_pending_reference")
        traces.append(
            PersonalAlphaSourceTrace(
                source_ref_id=str(source_ref.get("source_ref_id", "")),
                source_type=str(source_ref.get("source_type", "personal_alpha_workspace_stage")),
                workspace_run_id=workspace_run_id,
                case_id=str(source_ref.get("case_id", loaded.get("case_id", ""))),
                workspace_id=str(source_ref.get("workspace_id", loaded.get("workspace_id", ""))),
                stage_id=stage_id,
                evidence_item_id=f"evidence_{stage_id or 'unknown'}",
                evidence_status=status,
                provider=str(source_ref.get("provider", "personal_alpha_workspace")),
                provider_mode="mock",
                mock_or_redacted_only=True,
                raw_content_included=False,
                notes="Metadata-only source trace. No raw content included.",
            ).model_dump()
        )
    return traces


def _evidence_summary(source_traces: list[dict[str, Any]]) -> PersonalAlphaEvidenceSummary:
    blocked = sum(1 for trace in source_traces if "blocked" in str(trace.get("evidence_status", "")).lower())
    ready = sum(1 for trace in source_traces if "ready" in str(trace.get("evidence_status", "")).lower())
    pending = sum(1 for trace in source_traces if "pending" in str(trace.get("evidence_status", "")).lower())
    return PersonalAlphaEvidenceSummary(
        total_sources=len(source_traces),
        total_evidence_items=len(source_traces),
        blocked_sources=blocked,
        ready_sources=ready,
        pending_sources=pending,
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Evidence summary is derived from mock or redacted source trace metadata only."],
    )


def _audit_timeline(loaded: dict[str, Any]) -> list[dict[str, Any]]:
    workspace_run_id = str(loaded.get("workspace_run_id", ""))
    timeline = []
    for event in _safe_list(loaded.get("unified_audit_timeline", [])):
        if not isinstance(event, dict):
            continue
        if str(event.get("workspace_run_id", workspace_run_id)) != workspace_run_id:
            continue
        timeline.append(
            {
                "timeline_event_id": str(event.get("timeline_event_id", "")),
                "workspace_run_id": workspace_run_id,
                "case_id": str(event.get("case_id", loaded.get("case_id", ""))),
                "workspace_id": str(event.get("workspace_id", loaded.get("workspace_id", ""))),
                "stage_id": str(event.get("stage_id", "")),
                "event_type": str(event.get("event_type", "mock_stage_status")),
                "result": str(event.get("result", "")),
                "mock_or_redacted_only": True,
                "created_at": str(event.get("created_at", loaded.get("created_at", ""))),
            }
        )
    for event in list_personal_alpha_workspace_audit_logs():
        if not isinstance(event, dict) or str(event.get("workspace_run_id", "")) != workspace_run_id:
            continue
        timeline.append(
            {
                "timeline_event_id": str(event.get("audit_log_id", "")),
                "workspace_run_id": workspace_run_id,
                "case_id": str(event.get("case_id", loaded.get("case_id", ""))),
                "workspace_id": str(event.get("workspace_id", loaded.get("workspace_id", ""))),
                "stage_id": "personal_alpha_workspace",
                "event_type": str(event.get("event_type", "personal_alpha_workspace")),
                "result": str(event.get("result", "")),
                "mock_or_redacted_only": True,
                "created_at": str(event.get("created_at", "")),
            }
        )
    return timeline


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
