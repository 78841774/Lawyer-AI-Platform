from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_skill_studio.audit_engine import record_audit_event
from personal_skill_studio.experience_package_runtime import get_experience_package
from personal_skill_studio.safety_engine import default_safety_flags
from personal_skill_studio.schemas import SkillCandidateDraft, SkillCandidateDraftList, SkillCandidateMockRequest
from personal_skill_studio.source_trace_engine import create_source_trace
from personal_skill_studio.storage import PROMOTION_QUEUE_DIR, SKILL_CANDIDATES_DIR, read_payload, read_payloads, write_payload


def create_mock_skill_candidate(request: SkillCandidateMockRequest) -> dict:
    if get_experience_package(request.experience_package_id) is None:
        raise HTTPException(status_code=404, detail="experience_package_id 不存在")
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "技能候选草案请求被阻断。", "blocked_reasons": blocked})
    skill_candidate_id = f"personal_skill_candidate_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    create_source_trace(
        source_trace_id=f"skill_studio_source_trace_{skill_candidate_id}_1",
        source_type="skill_candidate_metadata",
        source_label="技能候选草案 metadata",
        linked_object_type="skill_candidate",
        linked_object_id=skill_candidate_id,
        experience_package_id=request.experience_package_id,
        skill_candidate_id=skill_candidate_id,
        created_at=created_at,
    )
    record = SkillCandidateDraft(
        skill_candidate_id=skill_candidate_id,
        experience_package_id=request.experience_package_id,
        skill_title=request.skill_title,
        skill_type=request.skill_type,
        target_legal_area=request.target_legal_area,
        target_case_cause=request.target_case_cause,
        prompt_template_draft={"template": "prompt template 草案 placeholder"},
        reasoning_pattern_draft={"pattern": "reasoning pattern 草案 placeholder"},
        input_schema_draft={"input": "metadata only"},
        output_schema_draft={"output": "draft metadata only"},
        limitation_notes=["律师复核必需", "未自动发布", "不生成最终法律意见"],
        safety_flags=default_safety_flags(),
        created_at=created_at,
        warnings=["仅生成技能候选草案，不写入正式 Skill Registry。"],
    )
    payload = record.model_dump()
    write_payload(SKILL_CANDIDATES_DIR, skill_candidate_id, payload)
    write_payload(PROMOTION_QUEUE_DIR, skill_candidate_id, payload)
    record_audit_event(action="skill_candidate_mock_created", actor="system", object_type="skill_candidate", object_id=skill_candidate_id, timestamp=created_at)
    return payload


def get_skill_candidate(skill_candidate_id: str) -> SkillCandidateDraft | None:
    payload = read_payload(SKILL_CANDIDATES_DIR, skill_candidate_id)
    return SkillCandidateDraft(**payload) if payload else None


def save_skill_candidate(record: SkillCandidateDraft) -> None:
    payload = record.model_dump()
    write_payload(SKILL_CANDIDATES_DIR, record.skill_candidate_id, payload)
    write_payload(PROMOTION_QUEUE_DIR, record.skill_candidate_id, payload)


def list_skill_candidates() -> list[SkillCandidateDraft]:
    return [SkillCandidateDraft(**payload) for payload in read_payloads(SKILL_CANDIDATES_DIR)]


def build_skill_candidate_list() -> dict:
    records = sorted(list_skill_candidates(), key=lambda record: record.created_at, reverse=True)
    return SkillCandidateDraftList(skill_candidates=records, candidate_count=len(records), warnings=["技能候选列表仅包含草案 metadata。"]).model_dump()


def validate_request(request: SkillCandidateMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in ["explicit_mock_confirmation", "explicit_lawyer_review_confirmation", "explicit_no_auto_publish_confirmation"]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.skill_title.strip():
        blocked.append("skill_title 不能为空")
    return blocked
