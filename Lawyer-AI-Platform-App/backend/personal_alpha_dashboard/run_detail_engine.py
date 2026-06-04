from typing import Any

from personal_alpha_dashboard.schemas import (
    PersonalAlphaRunDetail,
    PersonalAlphaRunGuardSummary,
    PersonalAlphaRunSafetyChecklist,
    PersonalAlphaRunStageDetail,
)
from personal_alpha_workspace.audit import list_personal_alpha_workspace_audit_logs
from personal_alpha_workspace.workspace_engine import load_personal_alpha_workspace_run


def get_personal_alpha_run_detail(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run(workspace_run_id)
    if _is_not_found(loaded):
        return PersonalAlphaRunDetail(
            workspace_run_id=workspace_run_id,
            status="not_found",
            mock_or_redacted_only=True,
            raw_content_included=False,
            final_legal_opinion_generated=False,
            llm_called=False,
            deepseek_live_called=False,
            real_ocr_called=False,
            real_legal_database_called=False,
            guard_summary=PersonalAlphaRunGuardSummary().model_dump(),
            safety_checklist=PersonalAlphaRunSafetyChecklist().model_dump(),
            warnings=["Workspace run not found or not available in runtime storage."],
            created_at="",
        ).model_dump()

    stage_details = _stage_details(loaded)
    audit_timeline = _audit_timeline_for_run(loaded)
    source_refs = _source_refs_for_run(loaded)
    warnings = [
        "Personal alpha run detail is metadata-only.",
        "No raw material text, raw OCR text, or raw legal search result text is returned.",
        *[str(item) for item in loaded.get("warnings", [])],
    ]
    return PersonalAlphaRunDetail(
        workspace_run_id=str(loaded.get("workspace_run_id", workspace_run_id)),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        workflow_mode=str(loaded.get("workflow_mode", "")),
        status="mock_run_detail_ready",
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        llm_called=False,
        deepseek_live_called=False,
        real_ocr_called=False,
        real_legal_database_called=False,
        stage_details=stage_details,
        audit_timeline=audit_timeline,
        source_refs=source_refs,
        guard_summary=_guard_summary(loaded),
        safety_checklist=PersonalAlphaRunSafetyChecklist().model_dump(),
        warnings=list(dict.fromkeys(warnings)),
        created_at=str(loaded.get("created_at", "")),
    ).model_dump()


def _is_not_found(loaded: dict[str, Any]) -> bool:
    warnings = " ".join(str(item).lower() for item in loaded.get("warnings", []))
    return "not found" in warnings and not loaded.get("stage_statuses")


def _stage_details(loaded: dict[str, Any]) -> list[dict[str, Any]]:
    details = []
    for stage in _safe_list(loaded.get("stage_statuses", [])):
        if not isinstance(stage, dict):
            continue
        details.append(
            PersonalAlphaRunStageDetail(
                stage_id=str(stage.get("stage_id", "")),
                label=str(stage.get("label", "")),
                status=str(stage.get("status", "mock_pending_reference")),
                required=bool(stage.get("required", True)),
                mock_only=True,
                source_ref_id=str(stage.get("source_ref_id", "")),
                notes="Metadata-only stage detail. No raw content included.",
            ).model_dump()
        )
    return details


def _audit_timeline_for_run(loaded: dict[str, Any]) -> list[dict[str, Any]]:
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


def _source_refs_for_run(loaded: dict[str, Any]) -> list[dict[str, Any]]:
    workspace_run_id = str(loaded.get("workspace_run_id", ""))
    source_refs = []
    for source_ref in _safe_list(loaded.get("source_refs", [])):
        if not isinstance(source_ref, dict):
            continue
        if str(source_ref.get("workspace_run_id", workspace_run_id)) != workspace_run_id:
            continue
        source_refs.append(
            {
                "source_ref_id": str(source_ref.get("source_ref_id", "")),
                "source_type": str(source_ref.get("source_type", "personal_alpha_workspace_stage")),
                "workspace_run_id": workspace_run_id,
                "case_id": str(source_ref.get("case_id", loaded.get("case_id", ""))),
                "workspace_id": str(source_ref.get("workspace_id", loaded.get("workspace_id", ""))),
                "stage_id": str(source_ref.get("stage_id", "")),
                "quote": "Mock personal alpha workspace source trace placeholder. No raw content included.",
                "provider": str(source_ref.get("provider", "personal_alpha_workspace")),
                "provider_mode": "mock",
                "mock_or_redacted_only": True,
            }
        )
    return source_refs


def _guard_summary(loaded: dict[str, Any]) -> dict[str, Any]:
    guard_results = _safe_list(loaded.get("guard_results", []))
    blocked_count = sum(1 for item in guard_results if isinstance(item, dict) and not bool(item.get("allowed", False)))
    passed_count = sum(1 for item in guard_results if isinstance(item, dict) and bool(item.get("allowed", False)))
    warnings = []
    for item in guard_results:
        if isinstance(item, dict):
            warnings.extend(str(warning) for warning in _safe_list(item.get("warnings", [])))
    return PersonalAlphaRunGuardSummary(
        guard_count=len(guard_results),
        blocked_count=blocked_count,
        passed_count=passed_count,
        warnings=list(dict.fromkeys(warnings)),
    ).model_dump()


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
