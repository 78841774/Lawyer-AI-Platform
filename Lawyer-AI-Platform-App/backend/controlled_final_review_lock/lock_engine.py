import re
from typing import Any
from uuid import uuid4

from controlled_final_review_lock.audit import append_controlled_final_review_lock_audit_log
from controlled_final_review_lock.guards import run_all_controlled_final_review_lock_guards
from controlled_final_review_lock.runtime_storage import (
    load_controlled_final_review_lock_record,
    store_controlled_final_review_lock,
)
from controlled_final_review_lock.schemas import (
    ControlledFinalReviewChecklistItem,
    ControlledFinalReviewLockRecord,
    ControlledFinalReviewLockRequest,
    ControlledFinalReviewLockResult,
    ControlledFinalReviewLockStatus,
    ControlledFinalReviewSourceRef,
    utc_now,
)


def get_controlled_final_review_lock_status() -> dict[str, Any]:
    return ControlledFinalReviewLockStatus(
        warnings=[
            "v4.9 is local-only controlled final review lock workflow.",
            "Mock final review lock is enabled by default.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No final legal opinion is generated.",
            "Manual lawyer final review and explicit final lock confirmation are required.",
        ]
    ).model_dump()


def create_mock_final_review_lock(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    created_at = utc_now()
    final_lock_id = f"controlled_final_lock_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_final_lock_audit_{uuid4().hex[:12]}"
    guard_results = run_all_controlled_final_review_lock_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.9 controlled final review lock workflow.")

    if not allowed_to_continue:
        append_controlled_final_review_lock_audit_log(_audit_event(audit_log_id, request, final_lock_id, "blocked_by_controlled_final_review_lock_guard", warnings, created_at))
        return ControlledFinalReviewLockResult(
            final_lock_id=final_lock_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            draft_id=request.draft_id,
            review_id=request.review_id,
            revision_id=request.revision_id,
            status="blocked",
            lock_mode=request.lock_mode,
            mock_final_lock_created=False,
            immutable_snapshot_created=False,
            final_legal_opinion_generated=False,
            llm_called=False,
            deepseek_live_called=False,
            real_ocr_called=False,
            real_legal_database_called=False,
            raw_material_text_included=False,
            raw_ocr_text_included=False,
            raw_legal_search_results_included=False,
            mock_final_review_snapshot={},
            final_review_checklist=[],
            source_refs=[],
            guard_results=guard_results,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            warnings=list(dict.fromkeys(warnings)),
            created_at=created_at,
        ).model_dump()

    final_review_checklist = _build_final_review_checklist()
    source_refs = _build_source_refs(final_lock_id, request)
    mock_final_review_snapshot = _build_mock_final_review_snapshot(request, final_review_checklist, source_refs)
    storage = store_controlled_final_review_lock(
        final_lock_id,
        {
            "case_id": request.case_id,
            "workspace_id": request.workspace_id,
            "draft_id": request.draft_id,
            "review_id": request.review_id,
            "revision_id": request.revision_id,
            "lock_mode": request.lock_mode,
            "mock_final_review_snapshot": mock_final_review_snapshot,
            "final_review_checklist": final_review_checklist,
            "source_refs": source_refs,
            "created_at": created_at,
        },
    )
    warnings.extend(storage.get("warnings", []))
    append_controlled_final_review_lock_audit_log(_audit_event(audit_log_id, request, final_lock_id, "mock_final_review_locked", warnings, created_at))
    return ControlledFinalReviewLockResult(
        final_lock_id=final_lock_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        draft_id=request.draft_id,
        review_id=request.review_id,
        revision_id=request.revision_id,
        status="mock_final_review_locked",
        lock_mode=request.lock_mode,
        mock_final_lock_created=True,
        immutable_snapshot_created=True,
        final_legal_opinion_generated=False,
        llm_called=False,
        deepseek_live_called=False,
        real_ocr_called=False,
        real_legal_database_called=False,
        raw_material_text_included=False,
        raw_ocr_text_included=False,
        raw_legal_search_results_included=False,
        final_lock_storage_path=storage["storage_path"],
        mock_final_review_snapshot=mock_final_review_snapshot,
        final_review_checklist=final_review_checklist,
        source_refs=source_refs,
        guard_results=guard_results,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        warnings=list(dict.fromkeys(warnings)),
        created_at=created_at,
    ).model_dump()


def load_controlled_final_review_lock(final_lock_id: str) -> dict[str, Any]:
    loaded = load_controlled_final_review_lock_record(final_lock_id)
    return ControlledFinalReviewLockRecord(
        final_lock_id=str(loaded.get("final_lock_id", final_lock_id)),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        draft_id=str(loaded.get("draft_id", "")),
        review_id=str(loaded.get("review_id", "")),
        revision_id=str(loaded.get("revision_id", "")),
        lock_mode=str(loaded.get("lock_mode", "")),
        mock_final_review_snapshot=dict(loaded.get("mock_final_review_snapshot", {})),
        final_review_checklist=list(loaded.get("final_review_checklist", [])),
        source_refs=list(loaded.get("source_refs", [])),
        warnings=list(loaded.get("warnings", [])),
        created_at=str(loaded.get("created_at", utc_now())),
        immutable_snapshot=bool(loaded.get("immutable_snapshot", True)),
    ).model_dump()


def _build_mock_final_review_snapshot(request: ControlledFinalReviewLockRequest, checklist: list[dict[str, Any]], source_refs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "title": "Mock Controlled Final Review Lock Snapshot",
        "status": "mock_final_review_locked",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "draft_id": request.draft_id,
        "review_id": request.review_id,
        "revision_id": request.revision_id,
        "lock_mode": request.lock_mode,
        "final_review_notes_redacted": _redact_free_text(request.final_review_notes),
        "sections": {
            "final_review_scope": {
                "lock_mode": request.lock_mode,
                "scope": "Mock final review candidate lock only. No raw draft, material, OCR, or legal search text included.",
            },
            "controlled_draft_snapshot": {
                "draft_id": request.draft_id,
                "snapshot_type": "mock_reference_only",
            },
            "controlled_revision_snapshot": {
                "revision_id": request.revision_id,
                "review_id": request.review_id,
                "snapshot_type": "mock_reference_only",
            },
            "source_trace_snapshot": {
                "source_ref_count": len(source_refs),
                "source_refs": source_refs,
            },
            "final_lawyer_checklist": checklist,
            "lock_limitations": [
                "This is only a mock final review lock candidate.",
                "No final legal opinion is generated.",
                "No real provider was called.",
                "Manual lawyer final review remains required.",
            ],
        },
        "legal_opinion_finalized": False,
        "final_legal_opinion_generated": False,
        "requires_human_review": True,
        "mock_only": True,
        "immutable_mock_snapshot": True,
        "warnings": [
            "No real LLM call.",
            "No raw material text included.",
            "No raw OCR text included.",
            "No real legal search result included.",
            "Not a final legal opinion.",
            "Manual lawyer final review required.",
            "This is only a mock final review lock candidate.",
        ],
    }


def _build_final_review_checklist() -> list[dict[str, Any]]:
    return [
        ControlledFinalReviewChecklistItem(item_id="check_draft_id_present", label="Confirm draft ID is present.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_review_id_present", label="Confirm review ID is present.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_revision_id_present", label="Confirm revision ID is present.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_final_checklist_confirmed", label="Confirm final checklist was reviewed by a lawyer.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_no_final_legal_opinion", label="Confirm no final legal opinion is generated.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_no_raw_content", label="Confirm no raw material, OCR, or legal search text is included.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_source_trace_snapshot", label="Confirm source trace snapshot is mock or redacted only.").model_dump(),
        ControlledFinalReviewChecklistItem(
            item_id="check_A10_not_modified",
            label="Confirm A10 remains 争议焦点法律深化分析.",
            notes="保持 A10 的既定分析标题，不得改为其他 A 系列分类。",
        ).model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_manual_final_review_required", label="Confirm manual lawyer final review is required.").model_dump(),
        ControlledFinalReviewChecklistItem(item_id="check_mock_only_lock", label="Confirm this lock is mock-only and not production.").model_dump(),
    ]


def _build_source_refs(final_lock_id: str, request: ControlledFinalReviewLockRequest) -> list[dict[str, Any]]:
    return [
        ControlledFinalReviewSourceRef(
            source_ref_id="source_ref_controlled_final_lock_001",
            final_lock_id=final_lock_id,
            linked_draft_id=request.draft_id,
            linked_review_id=request.review_id,
            linked_revision_id=request.revision_id,
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
    for pattern, replacement in replacements:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text[:800]


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.9 controlled final review lock workflow only.",
        "Mock final review lock by default.",
        "No real LLM, DeepSeek live, OCR, or legal database provider was called.",
        "Raw material text, raw OCR text, and raw legal search results are not returned, logged, or stored in Git.",
        "No final legal opinion was generated.",
        "Manual lawyer final review required.",
        "This is only a mock final review lock candidate.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _audit_event(audit_log_id: str, request: ControlledFinalReviewLockRequest, final_lock_id: str, result: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return {
        "audit_log_id": audit_log_id,
        "event_type": "controlled_final_review_lock",
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "draft_id": request.draft_id,
        "review_id": request.review_id,
        "revision_id": request.revision_id,
        "final_lock_id": final_lock_id,
        "result": result,
        "warnings": list(dict.fromkeys(warnings)),
        "created_at": created_at,
    }
