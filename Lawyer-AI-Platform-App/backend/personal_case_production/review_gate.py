import re
from datetime import datetime, timezone

from fastapi import HTTPException

from personal_case_production.audit_engine import record_audit_event
from personal_case_production.case_production_runtime import get_production_case, save_production_case
from personal_case_production.schemas import ProductionCaseList, ReviewGateActionRequest, ReviewGateActionResult
from personal_case_production.source_trace_engine import create_source_trace
from personal_case_production.storage import REVIEW_GATES_DIR, read_payloads


ALLOWED_ACTIONS = {
    "approve_for_final_gate": "ready_for_final_gate_review",
    "request_revision": "revision_requested",
    "reject": "rejected",
    "mark_not_ready": "not_ready",
    "mark_low_confidence": "low_confidence",
}
SAFE_REVIEWER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def build_review_gate_queue() -> dict:
    records = [get_production_case(payload["production_case_id"]) for payload in read_payloads(REVIEW_GATES_DIR) if payload.get("production_case_id")]
    cases = [record for record in records if record is not None and record.production_status in {"draft", "revision_requested", "not_ready", "low_confidence"}]
    cases = sorted(cases, key=lambda record: record.created_at, reverse=True)
    return ProductionCaseList(production_cases=cases, case_count=len(cases), warnings=["复核门禁队列仅为 metadata，不触发最终交付。"]).model_dump()


def submit_review_gate_action(production_case_id: str, request: ReviewGateActionRequest) -> dict:
    case = get_production_case(production_case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="production_case_id 不存在")
    if request.action not in ALLOWED_ACTIONS:
        raise HTTPException(status_code=400, detail="action 不支持")
    if not SAFE_REVIEWER_ID_PATTERN.match(request.reviewer_id):
        raise HTTPException(status_code=400, detail="reviewer_id 不安全")
    if not request.explicit_lawyer_confirmation or not request.explicit_no_final_opinion_confirmation or not request.explicit_no_external_delivery_confirmation:
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    now = datetime.now(timezone.utc).isoformat()
    updated = case.model_copy(update={"production_status": ALLOWED_ACTIONS[request.action], "updated_at": now})
    save_production_case(updated)
    create_source_trace(
        source_trace_id=f"case_production_source_trace_review_{production_case_id}_{now.replace(':', '').replace('.', '')}",
        source_type="lawyer_review_metadata",
        source_label="律师复核动作 metadata",
        linked_object_type="review_gate",
        linked_object_id=production_case_id,
        production_case_id=production_case_id,
        created_at=now,
    )
    record_audit_event(action="review_gate_action", actor=request.reviewer_id, object_type="production_case", object_id=production_case_id, timestamp=now)
    return ReviewGateActionResult(
        production_case_id=production_case_id,
        action=request.action,
        production_status=updated.production_status,
        warnings=["复核门禁动作仅更新 metadata，不生成最终法律意见、最终报告或对外交付。"],
    ).model_dump()
