from typing import Any
from uuid import uuid4

from personal_alpha_workspace.audit import (
    append_personal_alpha_workspace_audit_log,
    list_personal_alpha_workspace_audit_logs as read_personal_alpha_workspace_audit_logs,
)
from personal_alpha_workspace.guards import run_all_personal_alpha_workspace_guards
from personal_alpha_workspace.runtime_storage import (
    load_personal_alpha_workspace_run_record,
    store_personal_alpha_workspace_run,
)
from personal_alpha_workspace.schemas import (
    PersonalAlphaWorkspaceRequest,
    PersonalAlphaWorkspaceRunResult,
    PersonalAlphaWorkspaceSnapshot,
    PersonalAlphaWorkspaceStageStatus,
    PersonalAlphaWorkspaceStatus,
    utc_now,
)


def get_personal_alpha_workspace_status() -> dict[str, Any]:
    return PersonalAlphaWorkspaceStatus(
        warnings=[
            "v5.0 is a local-only personal alpha workspace.",
            "Mock-first and controlled-first workflow is enabled by default.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No final legal opinion is generated.",
            "Manual review and explicit workspace confirmation are required for end-to-end runs.",
        ]
    ).model_dump()


def run_personal_alpha_workspace(request: PersonalAlphaWorkspaceRequest) -> dict[str, Any]:
    created_at = utc_now()
    workspace_run_id = f"personal_alpha_workspace_run_{uuid4().hex[:12]}"
    audit_log_id = f"personal_alpha_workspace_audit_{uuid4().hex[:12]}"
    guard_results = run_all_personal_alpha_workspace_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v5.0 personal alpha workspace.")

    if not allowed_to_continue:
        append_personal_alpha_workspace_audit_log(_audit_event(audit_log_id, request, workspace_run_id, "blocked_by_personal_alpha_workspace_guard", warnings, created_at))
        return PersonalAlphaWorkspaceRunResult(
            workspace_run_id=workspace_run_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            workflow_mode=request.workflow_mode,
            status="blocked",
            end_to_end_mock_run_created=False,
            final_legal_opinion_generated=False,
            llm_called=False,
            deepseek_live_called=False,
            real_ocr_called=False,
            real_legal_database_called=False,
            raw_material_text_included=False,
            raw_ocr_text_included=False,
            raw_legal_search_results_included=False,
            stage_statuses=[],
            workspace_snapshot={},
            unified_audit_timeline=[],
            source_refs=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    stage_statuses = _build_stage_statuses(request)
    source_refs = _build_source_refs(workspace_run_id, request, stage_statuses)
    unified_audit_timeline = _build_unified_audit_timeline(workspace_run_id, request, stage_statuses, created_at)
    workspace_snapshot = _build_workspace_snapshot(request, stage_statuses, source_refs, unified_audit_timeline)
    storage = store_personal_alpha_workspace_run(
        workspace_run_id,
        {
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "workflow_mode": request.workflow_mode,
            "stage_statuses": stage_statuses,
            "workspace_snapshot": workspace_snapshot,
            "unified_audit_timeline": unified_audit_timeline,
            "source_refs": source_refs,
            "created_at": created_at,
        },
    )
    warnings.extend(storage.get("warnings", []))
    append_personal_alpha_workspace_audit_log(_audit_event(audit_log_id, request, workspace_run_id, "mock_personal_alpha_workspace_ready", warnings, created_at))
    return PersonalAlphaWorkspaceRunResult(
        workspace_run_id=workspace_run_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        workflow_mode=request.workflow_mode,
        status="mock_workspace_ready",
        end_to_end_mock_run_created=True,
        final_legal_opinion_generated=False,
        llm_called=False,
        deepseek_live_called=False,
        real_ocr_called=False,
        real_legal_database_called=False,
        raw_material_text_included=False,
        raw_ocr_text_included=False,
        raw_legal_search_results_included=False,
        stage_statuses=stage_statuses,
        workspace_snapshot=workspace_snapshot,
        unified_audit_timeline=unified_audit_timeline,
        source_refs=source_refs,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def load_personal_alpha_workspace_run(workspace_run_id: str) -> dict[str, Any]:
    loaded = load_personal_alpha_workspace_run_record(workspace_run_id)
    return {
        "workspace_run_id": str(loaded.get("workspace_run_id", workspace_run_id)),
        "case_id": str(loaded.get("case_id", "")),
        "workspace_id": str(loaded.get("workspace_id", "")),
        "workflow_mode": str(loaded.get("workflow_mode", "")),
        "stage_statuses": list(loaded.get("stage_statuses", [])),
        "workspace_snapshot": dict(loaded.get("workspace_snapshot", {})),
        "unified_audit_timeline": list(loaded.get("unified_audit_timeline", [])),
        "source_refs": list(loaded.get("source_refs", [])),
        "warnings": list(loaded.get("warnings", [])),
        "created_at": str(loaded.get("created_at", utc_now())),
    }


def list_personal_alpha_workspace_audit_logs() -> dict[str, Any]:
    return {"audit_logs": read_personal_alpha_workspace_audit_logs()}


def _build_stage_statuses(request: PersonalAlphaWorkspaceRequest) -> list[dict[str, Any]]:
    stage_inputs = [
        ("controlled_material_preview", "Material Preview", request.material_preview_id),
        ("controlled_ocr_preview", "OCR Preview", request.ocr_preview_id),
        ("controlled_legal_search_preview", "Legal Search Preview", request.legal_search_preview_id),
        ("controlled_report_draft", "Report Draft", request.draft_id),
        ("controlled_lawyer_review", "Lawyer Review", request.review_id),
        ("controlled_revision", "Revision", request.revision_id),
        ("controlled_final_review_lock", "Final Review Lock", request.final_lock_id),
    ]
    statuses = []
    for stage_id, label, linked_id in stage_inputs:
        statuses.append(
            PersonalAlphaWorkspaceStageStatus(
                stage_id=stage_id,
                label=label,
                status="mock_ready" if linked_id else "mock_pending_reference",
                required=True,
                mock_only=True,
                source_ref_id=f"source_ref_{stage_id}",
                notes=f"{label} is represented by mock or redacted metadata only.",
            ).model_dump()
        )
    return statuses


def _build_source_refs(workspace_run_id: str, request: PersonalAlphaWorkspaceRequest, stage_statuses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source_ref_id": str(stage["source_ref_id"]),
            "source_type": "personal_alpha_workspace_stage",
            "workspace_run_id": workspace_run_id,
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "stage_id": stage["stage_id"],
            "quote": "Mock personal alpha workspace source trace placeholder. No raw content included.",
            "provider": "personal_alpha_workspace",
            "provider_mode": "mock",
            "mock_or_redacted_only": True,
        }
        for stage in stage_statuses
    ]


def _build_unified_audit_timeline(workspace_run_id: str, request: PersonalAlphaWorkspaceRequest, stage_statuses: list[dict[str, Any]], created_at: str) -> list[dict[str, Any]]:
    return [
        {
            "timeline_event_id": f"timeline_{stage['stage_id']}",
            "workspace_run_id": workspace_run_id,
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "stage_id": stage["stage_id"],
            "event_type": "mock_stage_status",
            "result": stage["status"],
            "mock_or_redacted_only": True,
            "created_at": created_at,
        }
        for stage in stage_statuses
    ]


def _build_workspace_snapshot(
    request: PersonalAlphaWorkspaceRequest,
    stage_statuses: list[dict[str, Any]],
    source_refs: list[dict[str, Any]],
    unified_audit_timeline: list[dict[str, Any]],
) -> dict[str, Any]:
    return PersonalAlphaWorkspaceSnapshot(
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        workflow_mode=request.workflow_mode,
        stages=stage_statuses,
        source_trace_summary={
            "source_ref_count": len(source_refs),
            "mock_or_redacted_only": True,
            "source_refs": source_refs,
        },
        audit_timeline_summary={
            "timeline_event_count": len(unified_audit_timeline),
            "mock_or_redacted_only": True,
        },
        safety_boundaries=[
            "local-only",
            "mock-first",
            "controlled-first",
            "no real LLM",
            "no DeepSeek live",
            "no real OCR",
            "no real legal database",
            "no final legal opinion",
            "no automatic Skill publish",
            "no automatic Workspace Runtime enablement",
        ],
        final_legal_opinion_generated=False,
        requires_human_review=True,
        mock_only=True,
        warnings=[
            "No real LLM call.",
            "No DeepSeek live call.",
            "No real OCR call.",
            "No real legal database call.",
            "No raw material text included.",
            "No final legal opinion generated.",
            "Manual lawyer review required.",
        ],
    ).model_dump()


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v5.0 personal alpha workspace workflow only.",
        "Mock-first and controlled-first by default.",
        "No real LLM, DeepSeek live, OCR, or legal database provider was called.",
        "Raw material text, raw OCR text, and raw legal search results are not returned, logged, or stored in Git.",
        "No final legal opinion was generated.",
        "No Skill was published and no Workspace Runtime was enabled.",
        "Manual lawyer review required.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _audit_event(audit_log_id: str, request: PersonalAlphaWorkspaceRequest, workspace_run_id: str, result: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return {
        "audit_log_id": audit_log_id,
        "event_type": "personal_alpha_workspace",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "workspace_run_id": workspace_run_id,
        "workflow_mode": request.workflow_mode,
        "result": result,
        "warnings": list(dict.fromkeys(warnings)),
        "created_at": created_at,
    }
