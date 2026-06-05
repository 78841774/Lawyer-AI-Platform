from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_skill_studio.audit_engine import record_audit_event
from personal_skill_studio.schemas import EvaluationMockRequest, SkillEvaluationDraft, SkillEvaluationDraftList
from personal_skill_studio.skill_candidate_runtime import get_skill_candidate
from personal_skill_studio.source_trace_engine import create_source_trace
from personal_skill_studio.storage import EVALUATIONS_DIR, read_payload, read_payloads, write_payload
from personal_skill_studio.test_case_runtime import get_test_case


def create_mock_evaluation(request: EvaluationMockRequest) -> dict:
    if get_skill_candidate(request.skill_candidate_id) is None:
        raise HTTPException(status_code=404, detail="skill_candidate_id 不存在")
    missing_tests = [test_case_id for test_case_id in request.test_case_ids if get_test_case(test_case_id) is None]
    if missing_tests:
        raise HTTPException(status_code=404, detail={"message": "test_case_id 不存在", "missing_test_case_ids": missing_tests})
    if not request.explicit_mock_confirmation or not request.explicit_manual_review_confirmation or not request.explicit_no_auto_publish_confirmation:
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    evaluation_id = f"personal_skill_evaluation_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    create_source_trace(
        source_trace_id=f"skill_studio_source_trace_{evaluation_id}_1",
        source_type="evaluation_metadata",
        source_label="模拟评估 metadata",
        linked_object_type="evaluation",
        linked_object_id=evaluation_id,
        skill_candidate_id=request.skill_candidate_id,
        created_at=created_at,
    )
    record = SkillEvaluationDraft(
        evaluation_id=evaluation_id,
        skill_candidate_id=request.skill_candidate_id,
        test_case_ids=request.test_case_ids,
        evaluation_scope=request.evaluation_scope,
        score_summary={"overall_score": 72, "promotion_ready": False, "mode": "mock"},
        checklist_results=[
            {"item": "来源追踪必需", "passed": True},
            {"item": "律师复核必需", "passed": True},
            {"item": "未自动发布", "passed": True},
        ],
        risk_flags=["需要人工复核", "仅模拟评估"],
        recommendation="建议进入后续人工复核，不自动发布。",
        created_at=created_at,
        warnings=["模拟评估不触发发布，不写入正式 Skill Registry。"],
    )
    write_payload(EVALUATIONS_DIR, evaluation_id, record.model_dump())
    record_audit_event(action="evaluation_mock_created", actor="system", object_type="evaluation", object_id=evaluation_id, timestamp=created_at)
    return record.model_dump()


def get_evaluation(evaluation_id: str) -> SkillEvaluationDraft | None:
    payload = read_payload(EVALUATIONS_DIR, evaluation_id)
    return SkillEvaluationDraft(**payload) if payload else None


def list_evaluations() -> list[SkillEvaluationDraft]:
    return [SkillEvaluationDraft(**payload) for payload in read_payloads(EVALUATIONS_DIR)]


def build_evaluation_list() -> dict:
    records = sorted(list_evaluations(), key=lambda record: record.created_at, reverse=True)
    return SkillEvaluationDraftList(evaluations=records, evaluation_count=len(records), warnings=["评估列表仅包含模拟 metadata。"]).model_dump()
