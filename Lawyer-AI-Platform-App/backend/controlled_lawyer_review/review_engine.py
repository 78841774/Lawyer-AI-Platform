import json
import re
from pathlib import Path
from typing import Any
from uuid import uuid4

from controlled_lawyer_review.audit import append_controlled_lawyer_review_audit_log
from controlled_lawyer_review.guards import run_action_guards, run_submit_guards
from controlled_lawyer_review.schemas import (
    ControlledLawyerReviewActionRequest,
    ControlledLawyerReviewRecord,
    ControlledLawyerReviewResult,
    ControlledLawyerReviewStatus,
    ControlledLawyerReviewSubmitRequest,
    utc_now,
)

RUNTIME_REVIEW_STORAGE_RELATIVE_PATH = "storage/runtime/controlled_lawyer_reviews"


def get_controlled_lawyer_review_status() -> dict[str, Any]:
    return ControlledLawyerReviewStatus(
        warnings=[
            "v4.7 is local-only controlled lawyer review for v4.6 mock report drafts.",
            "No final legal opinion is generated.",
            "No real LLM, DeepSeek live, real OCR, or real legal database provider is called.",
            "No Skill is published and production remains disabled.",
            "Manual review and explicit review confirmation are required.",
        ]
    ).model_dump()


def submit_controlled_lawyer_review(request: ControlledLawyerReviewSubmitRequest) -> dict[str, Any]:
    created_at = utc_now()
    review_id = f"controlled_lawyer_review_{uuid4().hex[:12]}"
    audit_log_id = f"controlled_lawyer_review_audit_{uuid4().hex[:12]}"
    guard_results = run_submit_guards(request)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results)
    warnings = _collect_warnings(guard_results)

    if not request.preview_only:
        allowed_to_continue = False
        warnings.append("preview_only must remain true for v4.7 controlled lawyer review.")

    if not allowed_to_continue:
        append_controlled_lawyer_review_audit_log(_audit_event(audit_log_id, review_id, request.draft_id, request.case_id, request.workspace_id, "submit", "blocked_by_controlled_lawyer_review_guard", warnings, created_at))
        return _result(
            review_id=review_id,
            draft_id=request.draft_id,
            case_id=request.case_id,
            workspace_id=request.workspace_id,
            status="blocked",
            action="submit",
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            submitted=False,
            guard_results=guard_results,
            warnings=warnings,
            created_at=created_at,
        )

    history = [_history_event("submit", request.submitted_by, "submitted_for_controlled_review", created_at)]
    record = {
        "review_id": review_id,
        "draft_id": request.draft_id,
        "case_id": request.case_id,
        "workspace_id": request.workspace_id,
        "status": "submitted",
        "submitted_by": request.submitted_by,
        "reviewer_id": "",
        "review_notes": "",
        "final_legal_opinion_generated": False,
        "history": history,
        "created_at": created_at,
        "updated_at": created_at,
        "mock_or_redacted_only": True,
    }
    storage_path = _store_review_record(review_id, record)
    warnings.append("Controlled lawyer review record stored in ignored runtime storage.")
    append_controlled_lawyer_review_audit_log(_audit_event(audit_log_id, review_id, request.draft_id, request.case_id, request.workspace_id, "submit", "submitted_for_controlled_review", warnings, created_at))
    return _result(
        review_id=review_id,
        draft_id=request.draft_id,
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        status="submitted",
        action="submit",
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        submitted=True,
        review_record_storage_path=storage_path,
        review_record=record,
        history=history,
        guard_results=guard_results,
        warnings=warnings,
        created_at=created_at,
    )


def get_controlled_lawyer_review(review_id: str) -> dict[str, Any]:
    loaded = _load_review_record(review_id)
    return ControlledLawyerReviewRecord(
        review_id=str(loaded.get("review_id", _safe_review_id(review_id))),
        draft_id=str(loaded.get("draft_id", "")),
        case_id=str(loaded.get("case_id", "")),
        workspace_id=str(loaded.get("workspace_id", "")),
        status=str(loaded.get("status", "not_found")),
        submitted_by=str(loaded.get("submitted_by", "")),
        reviewer_id=str(loaded.get("reviewer_id", "")),
        review_notes=str(loaded.get("review_notes", "")),
        final_legal_opinion_generated=False,
        history=list(loaded.get("history", [])),
        warnings=list(loaded.get("warnings", [])),
        created_at=str(loaded.get("created_at", utc_now())),
        updated_at=str(loaded.get("updated_at", utc_now())),
    ).model_dump()


def approve_controlled_lawyer_review(review_id: str, request: ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return _apply_review_action(review_id, request, "approve", "approved")


def reject_controlled_lawyer_review(review_id: str, request: ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return _apply_review_action(review_id, request, "reject", "rejected")


def request_revision_controlled_lawyer_review(review_id: str, request: ControlledLawyerReviewActionRequest) -> dict[str, Any]:
    return _apply_review_action(review_id, request, "request_revision", "revision_requested")


def _apply_review_action(review_id: str, request: ControlledLawyerReviewActionRequest, action: str, next_status: str) -> dict[str, Any]:
    created_at = utc_now()
    safe_review_id = _safe_review_id(review_id)
    audit_log_id = f"controlled_lawyer_review_audit_{uuid4().hex[:12]}"
    record = _load_review_record(safe_review_id)
    guard_results = run_action_guards(request, safe_review_id)
    allowed_to_continue = all(bool(result.get("allowed")) for result in guard_results) and record.get("status") not in {"not_found", "blocked"}
    warnings = _collect_warnings(guard_results)
    if record.get("status") in {"not_found", "blocked"}:
        warnings.append("Controlled lawyer review record must exist and must not be blocked before review action.")

    if not allowed_to_continue:
        append_controlled_lawyer_review_audit_log(_audit_event(audit_log_id, safe_review_id, str(record.get("draft_id", "")), str(record.get("case_id", "")), str(record.get("workspace_id", "")), action, "blocked_by_controlled_lawyer_review_guard", warnings, created_at))
        return _result(
            review_id=safe_review_id,
            draft_id=str(record.get("draft_id", "")),
            case_id=str(record.get("case_id", "")),
            workspace_id=str(record.get("workspace_id", "")),
            status="blocked",
            action=action,
            audit_log_id=audit_log_id,
            allowed_to_continue=False,
            guard_results=guard_results,
            warnings=warnings,
            created_at=created_at,
        )

    history = list(record.get("history", []))
    history.append(_history_event(action, request.reviewer_id, request.review_notes or next_status, created_at))
    record.update(
        {
            "status": next_status,
            "reviewer_id": request.reviewer_id,
            "review_notes": request.review_notes,
            "final_legal_opinion_generated": False,
            "history": history,
            "updated_at": created_at,
            "mock_or_redacted_only": True,
        }
    )
    storage_path = _store_review_record(safe_review_id, record)
    warnings.append("Controlled lawyer review action stored in ignored runtime storage.")
    append_controlled_lawyer_review_audit_log(_audit_event(audit_log_id, safe_review_id, str(record.get("draft_id", "")), str(record.get("case_id", "")), str(record.get("workspace_id", "")), action, next_status, warnings, created_at))
    return _result(
        review_id=safe_review_id,
        draft_id=str(record.get("draft_id", "")),
        case_id=str(record.get("case_id", "")),
        workspace_id=str(record.get("workspace_id", "")),
        status=next_status,
        action=action,
        audit_log_id=audit_log_id,
        allowed_to_continue=True,
        approved=next_status == "approved",
        rejected=next_status == "rejected",
        revision_requested=next_status == "revision_requested",
        review_record_storage_path=storage_path,
        review_record=record,
        history=history,
        guard_results=guard_results,
        warnings=warnings,
        created_at=created_at,
    )


def _result(
    review_id: str,
    draft_id: str,
    case_id: str,
    workspace_id: str,
    status: str,
    action: str,
    audit_log_id: str,
    allowed_to_continue: bool,
    submitted: bool = False,
    approved: bool = False,
    rejected: bool = False,
    revision_requested: bool = False,
    review_record_storage_path: str = RUNTIME_REVIEW_STORAGE_RELATIVE_PATH,
    review_record: dict[str, Any] | None = None,
    history: list[dict[str, Any]] | None = None,
    guard_results: list[dict[str, Any]] | None = None,
    warnings: list[str] | None = None,
    created_at: str = "",
) -> dict[str, Any]:
    return ControlledLawyerReviewResult(
        review_id=review_id,
        draft_id=draft_id,
        case_id=case_id,
        workspace_id=workspace_id,
        status=status,
        action=action,
        submitted=submitted,
        approved=approved,
        rejected=rejected,
        revision_requested=revision_requested,
        final_legal_opinion_generated=False,
        llm_called=False,
        deepseek_live_called=False,
        real_ocr_called=False,
        real_legal_database_called=False,
        skill_published=False,
        workspace_runtime_enabled=False,
        raw_material_text_included=False,
        raw_ocr_text_included=False,
        raw_legal_search_results_included=False,
        review_record_storage_path=review_record_storage_path,
        review_record=review_record or {},
        history=history or [],
        guard_results=guard_results or [],
        audit_log_id=audit_log_id,
        allowed_to_continue=allowed_to_continue,
        warnings=list(dict.fromkeys(warnings or [])),
        created_at=created_at or utc_now(),
    ).model_dump()


def _store_review_record(review_id: str, record: dict[str, Any]) -> str:
    safe_id = _safe_review_id(review_id)
    storage_dir = _runtime_storage_dir()
    storage_dir.mkdir(parents=True, exist_ok=True)
    storage_file = storage_dir / f"{safe_id}.json"
    storage_file.write_text(
        json.dumps(
            {
                "review_id": safe_id,
                "draft_id": record.get("draft_id", ""),
                "case_id": record.get("case_id", ""),
                "workspace_id": record.get("workspace_id", ""),
                "status": record.get("status", ""),
                "submitted_by": record.get("submitted_by", ""),
                "reviewer_id": record.get("reviewer_id", ""),
                "review_notes": record.get("review_notes", ""),
                "final_legal_opinion_generated": False,
                "history": record.get("history", []),
                "created_at": record.get("created_at", utc_now()),
                "updated_at": record.get("updated_at", utc_now()),
                "mock_or_redacted_only": True,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return f"{RUNTIME_REVIEW_STORAGE_RELATIVE_PATH}/{safe_id}.json"


def _load_review_record(review_id: str) -> dict[str, Any]:
    safe_id = _safe_review_id(review_id)
    storage_file = _runtime_storage_dir() / f"{safe_id}.json"
    if not storage_file.exists():
        return {
            "review_id": safe_id,
            "status": "not_found",
            "history": [],
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "warnings": ["Controlled lawyer review record was not found."],
        }
    parsed = json.loads(storage_file.read_text(encoding="utf-8"))
    parsed["warnings"] = ["Loaded controlled lawyer review metadata only. Raw report draft content is not stored."]
    return parsed


def _history_event(action: str, actor_id: str, note: str, created_at: str) -> dict[str, Any]:
    return {
        "action": action,
        "actor_id": actor_id,
        "note": note[:500],
        "created_at": created_at,
        "mock_or_redacted_only": True,
    }


def _collect_warnings(guard_results: list[dict[str, Any]]) -> list[str]:
    warnings = [
        "v4.7 controlled lawyer review only.",
        "Local-only mock review workflow.",
        "No real LLM, DeepSeek live, OCR, or legal database provider was called.",
        "No final legal opinion was generated.",
        "No Skill was published and production was not enabled.",
        "Raw material text, raw OCR text, and raw legal search results are not returned, logged, or stored in Git.",
    ]
    for result in guard_results:
        warnings.extend(str(item) for item in result.get("warnings", []))
    return list(dict.fromkeys(warnings))


def _audit_event(audit_log_id: str, review_id: str, draft_id: str, case_id: str, workspace_id: str, action: str, result: str, warnings: list[str], created_at: str) -> dict[str, Any]:
    return {
        "audit_log_id": audit_log_id,
        "event_type": "controlled_lawyer_review",
        "review_id": review_id,
        "draft_id": draft_id,
        "case_id": case_id,
        "workspace_id": workspace_id,
        "action": action,
        "result": result,
        "warnings": list(dict.fromkeys(warnings)),
        "created_at": created_at,
    }


def _runtime_storage_dir() -> Path:
    return Path("/Users/wazhen/Lawyer-AI-Platform") / RUNTIME_REVIEW_STORAGE_RELATIVE_PATH


def _safe_review_id(review_id: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", review_id or "")
    return safe[:80] or "controlled_lawyer_review_missing"

