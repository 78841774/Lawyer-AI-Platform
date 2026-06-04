from typing import Any
from uuid import uuid4

from controlled_revision_workflow.audit import append_controlled_revision_audit_log
from controlled_revision_workflow.guards import run_all_controlled_revision_guards
from controlled_revision_workflow.runtime_storage import load_controlled_revision_record, store_controlled_revision
from controlled_revision_workflow.schemas import (
    ControlledRevisionChecklistItem,
    ControlledRevisionRecord,
    ControlledRevisionRequest,
    ControlledRevisionResult,
    ControlledRevisionSourceRef,
    ControlledRevisionStatus,
    utc_now,
)


def get_controlled_revision_status() -> dict[str, Any]:
    return ControlledRevisionStatus(
        warnings=[
            "v4.8 is local-only controlled revision request workflow.",
            "Mock revision is enabled by default.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No final legal opinion is generated.",
            "Manual lawyer re-review and explicit revision confirmation are required.",
        ]
    ).model_dump()


def create_mock_revision_request(request: ControlledRevisionRequest) -> dict[str, Any]:
    created_at = utc_now()
    revision_id = f"controlled_revision_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_revision_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_revision_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.8 controlled revision workflow.")

    if not allowed_to_continue:
        append_controlled_revision_audit_log(_audit_event(audit_log_id, request, revision_id, "blocked_by_controlled_revision_guard", warnings, created_at))
        return ControlledRevisionResult(
            revision_id=revision_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            review_id=request.review_id,
            draft_id=request.draft_id,
            status="blocked",
            requested_action=request.requested_action,
            mock_revision_created=False,
            final_legal_opinion_generated=False,
            llm_called=False,
            deepseek_live_called=False,
            real_ocr_called=False,
            real_legal_database_called=False,
            raw_material_text_included=False,
            raw_ocr_text_included=False,
            raw_legal_search_results_included=False,
            mock_revision_plan={},
            revision_checklist=[],
            source_refs=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    revision_checklist = _build_revision_checklist()
    source_refs = _build_source_refs(revision_id, request)
    mock_revision_plan = _build_mock_revision_plan(request, revision_checklist)
    storage = store_controlled_revision(
        revision_id,
        {
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "review_id": request.review_id,
            "draft_id": request.draft_id,
            "requested_action": request.requested_action,
            "mock_revision_plan": mock_revision_plan,
            "revision_checklist": revision_checklist,
            "source_refs": source_refs,
            "created_at": created_at,
        },
    )
    warnings.extend(storage.get("warnings", []))
    append_controlled_revision_audit_log(_audit_event(audit_log_id, request, revision_id, "mock_revision_requested", warnings, created_at))
    return ControlledRevisionResult(
        revision_id=revision_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        review_id=request.review_id,
        draft_id=request.draft_id,
        status="mock_revision_requested",
        requested_action=request.requested_action,
        mock_revision_created=True,
        final_legal_opinion_generated=False,
        llm_called=False,
        deepseek_live_called=False,
        real_ocr_called=False,
        real_legal_database_called=False,
        raw_material_text_included=False,
        raw_ocr_text_included=False,
        raw_legal_search_results_included=False,
        revision_storage_path=storage["storage_path"],
        mock_revision_plan=mock_revision_plan,
        revision_checklist=revision_checklist,
        source_refs=source_refs,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def load_controlled_revision(revision_id: str) -> dict[str, Any]:
    loaded = load_controlled_revision_record(revision_id)
    return ControlledRevisionRecord(
        revision_id=str(loaded.get("revision_id", revision_id)),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        review_id=str(loaded.get("review_id", "")),
        draft_id=str(loaded.get("draft_id", "")),
        requested_action=str(loaded.get("requested_action", "")),
        mock_revision_plan=dict(loaded.get("mock_revision_plan", {})),
        revision_checklist=list(loaded.get("revision_checklist", [])),
        source_refs=list(loaded.get("source_refs", [])),
        warnings=list(loaded.get("warnings", [])),
        created_at=str(loaded.get("created_at", utc_now())),
    ).model_dump()


def _build_mock_revision_plan(request: ControlledRevisionRequest, revision_checklist: list[dict[str, Any]]) -> dict[str, Any]:
    reason_redacted = _redact_free_text(request.revision_reason)
    instructions_redacted = _redact_free_text(request.revision_instructions)
    return {
        "title": "Mock Controlled Revision Plan",
        "status": "mock_revision_requested",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "review_id": request.review_id,
        "draft_id": request.draft_id,
        "requested_action": request.requested_action,
        "revision_reason_redacted": reason_redacted,
        "revision_instructions_redacted": instructions_redacted,
        "sections": {
            "revision_scope": {
                "requested_action": request.requested_action,
                "scope": "Mock revision scope only. No raw draft or material text included.",
            },
            "affected_report_sections": [
                "controlled_material_summary",
                "controlled_ocr_summary",
                "controlled_legal_search_summary",
                "source_trace_summary",
                "lawyer_review_checklist",
            ],
            "citation_review_notes": "Citation notes remain mock or manually verified only. No real legal database was called.",
            "risk_warning_review_notes": "Risk warning changes require lawyer re-review and must not become a final legal opinion.",
            "lawyer_re_review_checklist": revision_checklist,
        },
        "legal_opinion_finalized": False,
        "requires_human_review": True,
        "mock_only": True,
        "warnings": [
            "No real LLM call.",
            "No raw material text included.",
            "No raw OCR text included.",
            "No real legal search result included.",
            "Not a final legal opinion.",
            "Manual lawyer re-review required.",
        ],
    }


def _build_revision_checklist() -> list[dict[str, Any]]:
    return [
        ControlledRevisionChecklistItem(
            item_id="check_revision_scope",
            label="Confirm revision scope is limited to the requested mock change.",
            notes="律师需确认修改范围不扩大为正式法律意见。",
        ).model_dump(),
        ControlledRevisionChecklistItem(
            item_id="check_facts_not_overwritten",
            label="Confirm facts are not overwritten without controlled material support.",
            notes="不得用 revision request 覆盖事实来源。",
        ).model_dump(),
        ControlledRevisionChecklistItem(
            item_id="check_citations_remain_mock_or_verified",
            label="Confirm citations remain mock placeholders or manually verified.",
            notes="不得把 mock citation 当作真实法律检索结果。",
        ).model_dump(),
        ControlledRevisionChecklistItem(
            item_id="check_no_final_legal_opinion",
            label="Confirm no final legal opinion is generated.",
            notes="v4.8 不生成正式法律意见。",
        ).model_dump(),
        ControlledRevisionChecklistItem(
            item_id="check_lawyer_re_review_required",
            label="Confirm lawyer re-review is required before any next step.",
            notes="revision 后必须再次人工复核。",
        ).model_dump(),
        ControlledRevisionChecklistItem(
            item_id="check_A10_not_modified",
            label="Confirm A10 remains 争议焦点法律深化分析.",
            notes="保持 A10 的既定分析标题，不得改为其他 A 系列分类。",
        ).model_dump(),
    ]


def _build_source_refs(revision_id: str, request: ControlledRevisionRequest) -> list[dict[str, Any]]:
    return [
        ControlledRevisionSourceRef(
            source_ref_id="source_ref_controlled_revision_001",
            revision_id=revision_id,
            linked_review_id=request.review_id,
            linked_draft_id=request.draft_id,
        ).model_dump()
    ]


def _redact_free_text(value: str) -> str:
    text = (value or "").strip()
    replacements = [
        (r"(?<!\d)1[3-9]\d{9}(?!\d)", "<PHONE_REDACTED>"),
        (r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)", "<ID_NUMBER_REDACTED>"),
        (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<EMAIL_REDACTED>"),
        (r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号", "<CASE_NUMBER_REDACTED>"),
        (r"sk-[A-Za-z0-9_-]{12,}", "<API_KEY_REDACTED>"),
    ]
    import re

    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text[:800]


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.8 controlled revision request workflow only.",
        "Mock revision by default.",
        "No real LLM, DeepSeek live, OCR, or legal database provider was called.",
        "Raw material text, raw OCR text, and raw legal search results are not returned, logged, or stored in Git.",
        "No final legal opinion was generated.",
        "Manual lawyer re-review required.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _audit_event(audit_log_id: str, request: ControlledRevisionRequest, revision_id: str, result: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return {
        "audit_log_id": audit_log_id,
        "event_type": "controlled_revision_request",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "review_id": request.review_id,
        "draft_id": request.draft_id,
        "revision_id": revision_id,
        "result": result,
        "warnings": list(dict.fromkeys(warnings)),
        "created_at": created_at,
    }
