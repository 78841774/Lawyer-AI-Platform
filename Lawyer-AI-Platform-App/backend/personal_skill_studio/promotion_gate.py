import re
from datetime import datetime, timezone

from fastapi import HTTPException

from personal_skill_studio.audit_engine import record_audit_event
from personal_skill_studio.schemas import PromotionActionRequest, PromotionActionResult, SkillCandidateDraftList
from personal_skill_studio.skill_candidate_runtime import get_skill_candidate, save_skill_candidate
from personal_skill_studio.storage import PROMOTION_QUEUE_DIR, read_payloads


ALLOWED_ACTIONS = {
    "approve_for_future_review": "future_review",
    "request_revision": "revision_requested",
    "reject": "rejected",
    "mark_low_confidence": "low_confidence",
    "mark_not_ready": "not_ready",
}
SAFE_REVIEWER_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def build_promotion_queue() -> dict:
    records = [get_skill_candidate(payload["skill_candidate_id"]) for payload in read_payloads(PROMOTION_QUEUE_DIR) if payload.get("skill_candidate_id")]
    candidates = [record for record in records if record is not None and record.candidate_status in {"draft", "revision_requested", "low_confidence", "not_ready"}]
    candidates = sorted(candidates, key=lambda record: record.created_at, reverse=True)
    return SkillCandidateDraftList(skill_candidates=candidates, candidate_count=len(candidates), warnings=["发布门禁队列仅为 metadata，不会自动发布 Skill。"]).model_dump()


def submit_promotion_action(skill_candidate_id: str, request: PromotionActionRequest) -> dict:
    candidate = get_skill_candidate(skill_candidate_id)
    if candidate is None:
        raise HTTPException(status_code=404, detail="skill_candidate_id 不存在")
    if request.action not in ALLOWED_ACTIONS:
        raise HTTPException(status_code=400, detail="action 不支持")
    if not SAFE_REVIEWER_ID_PATTERN.match(request.reviewer_id):
        raise HTTPException(status_code=400, detail="reviewer_id 不安全")
    if not request.explicit_manual_confirmation or not request.explicit_no_auto_publish_confirmation or not request.explicit_no_final_opinion_confirmation:
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    now = datetime.now(timezone.utc).isoformat()
    updated = candidate.model_copy(update={"candidate_status": ALLOWED_ACTIONS[request.action], "updated_at": now})
    save_skill_candidate(updated)
    record_audit_event(action="promotion_gate_action", actor=request.reviewer_id, object_type="skill_candidate", object_id=skill_candidate_id, timestamp=now)
    return PromotionActionResult(
        skill_candidate_id=skill_candidate_id,
        action=request.action,
        candidate_status=updated.candidate_status,
        warnings=["发布门禁动作仅更新 metadata，不发布 Skill，不生成最终法律意见或最终报告。"],
    ).model_dump()
