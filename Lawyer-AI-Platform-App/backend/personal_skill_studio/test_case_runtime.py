from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_skill_studio.audit_engine import record_audit_event
from personal_skill_studio.schemas import SkillTestCaseDraft, SkillTestCaseDraftList, TestCaseMockRequest
from personal_skill_studio.skill_candidate_runtime import get_skill_candidate
from personal_skill_studio.source_trace_engine import create_source_trace
from personal_skill_studio.storage import TEST_CASES_DIR, read_payload, read_payloads, write_payload


def create_mock_test_case(request: TestCaseMockRequest) -> dict:
    if get_skill_candidate(request.skill_candidate_id) is None:
        raise HTTPException(status_code=404, detail="skill_candidate_id 不存在")
    if not request.explicit_mock_confirmation or not request.explicit_no_raw_content_confirmation:
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    test_case_id = f"personal_skill_test_case_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    trace = create_source_trace(
        source_trace_id=f"skill_studio_source_trace_{test_case_id}_1",
        source_type="skill_candidate_metadata",
        source_label="测试用例草案 metadata",
        linked_object_type="test_case",
        linked_object_id=test_case_id,
        skill_candidate_id=request.skill_candidate_id,
        created_at=created_at,
    )
    record = SkillTestCaseDraft(
        test_case_id=test_case_id,
        skill_candidate_id=request.skill_candidate_id,
        test_case_title=request.test_case_title,
        scenario_type=request.scenario_type,
        mock_input_metadata={"input": "测试输入 metadata placeholder"},
        expected_behavior_metadata={"expected": "预期行为 metadata placeholder"},
        source_trace_ids=[trace.source_trace_id],
        created_at=created_at,
        warnings=["测试用例草案不包含真实案件材料原文。"],
    )
    write_payload(TEST_CASES_DIR, test_case_id, record.model_dump())
    record_audit_event(action="test_case_mock_created", actor="system", object_type="test_case", object_id=test_case_id, timestamp=created_at)
    return record.model_dump()


def get_test_case(test_case_id: str) -> SkillTestCaseDraft | None:
    payload = read_payload(TEST_CASES_DIR, test_case_id)
    return SkillTestCaseDraft(**payload) if payload else None


def list_test_cases() -> list[SkillTestCaseDraft]:
    return [SkillTestCaseDraft(**payload) for payload in read_payloads(TEST_CASES_DIR)]


def build_test_case_list() -> dict:
    records = sorted(list_test_cases(), key=lambda record: record.created_at, reverse=True)
    return SkillTestCaseDraftList(test_cases=records, test_case_count=len(records), warnings=["测试用例列表仅包含草案 metadata。"]).model_dump()
