import re
from datetime import datetime, timezone

from fastapi import HTTPException

from personal_intelligence_gateway.audit_engine import record_audit_event
from personal_intelligence_gateway.schemas import (
    PersonalIntelligenceConfirmationActionRequest,
    PersonalIntelligenceConfirmationActionResult,
)
from personal_intelligence_gateway.source_trace_engine import build_source_trace_list, get_source_trace, update_trace_confirmation


ALLOWED_ACTIONS = {
    "confirm": ("confirmed", True),
    "reject": ("rejected", False),
    "request_verification": ("verification_requested", False),
    "mark_low_confidence": ("low_confidence", False),
    "mark_not_relevant": ("not_relevant", False),
}
SAFE_REVIEWER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def build_confirmation_queue() -> dict:
    queue = build_source_trace_list()
    pending = [trace for trace in queue["source_traces"] if not trace.get("lawyer_confirmed", False)]
    queue["source_traces"] = pending
    queue["source_trace_count"] = len(pending)
    queue["pending_confirmation_count"] = len(pending)
    queue["warnings"] = ["律师确认队列仅包含 Source Trace metadata，不包含外部原文。"]
    return queue


def submit_confirmation_action(source_trace_id: str, request: PersonalIntelligenceConfirmationActionRequest) -> dict:
    trace = get_source_trace(source_trace_id)
    if trace is None:
        raise HTTPException(status_code=404, detail="source_trace_id 不存在")
    blocked = validate_confirmation_action_request(request)
    if request.action not in ALLOWED_ACTIONS:
        raise HTTPException(status_code=400, detail="action 不支持")
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "律师确认动作被阻断。", "blocked_reasons": blocked})

    citation_status, lawyer_confirmed = ALLOWED_ACTIONS[request.action]
    updated = update_trace_confirmation(source_trace_id, citation_status, lawyer_confirmed)
    assert updated is not None
    now = datetime.now(timezone.utc).isoformat()
    record_audit_event(
        action="source_trace_confirmation_action",
        actor=request.reviewer_id,
        provider_id=updated.provider_id,
        query_id=updated.query_id,
        source_trace_id=updated.source_trace_id,
        timestamp=now,
    )
    return PersonalIntelligenceConfirmationActionResult(
        source_trace_id=source_trace_id,
        action=request.action,
        status="confirmation_action_recorded",
        citation_status=citation_status,
        lawyer_confirmed=lawyer_confirmed,
        warnings=["确认动作仅更新 metadata，不生成最终法律意见或最终报告，也不会自动送入 AI Prompt。"],
    ).model_dump()


def validate_confirmation_action_request(request: PersonalIntelligenceConfirmationActionRequest) -> list[str]:
    blocked: list[str] = []
    if not SAFE_REVIEWER_ID_PATTERN.match(request.reviewer_id):
        blocked.append("reviewer_id 不安全")
    if not request.explicit_lawyer_confirmation:
        blocked.append("explicit_lawyer_confirmation 必须为 true")
    if not request.explicit_no_final_opinion_confirmation:
        blocked.append("explicit_no_final_opinion_confirmation 必须为 true")
    return blocked
