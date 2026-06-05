from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_showcase_pack.audit_engine import record_audit_event
from personal_showcase_pack.safety_engine import default_safety_flags, validate_mock_metadata_text
from personal_showcase_pack.schemas import PilotSampleList, PilotSampleMockRequest, PilotSampleRecord, WorkflowProgress
from personal_showcase_pack.storage import PILOT_SAMPLES_DIR, read_payload, read_payloads, write_payload


ALLOWED_SAMPLE_TYPES = {
    "contract_dispute_demo",
    "labor_dispute_demo",
    "debt_collection_demo",
    "enterprise_risk_demo",
    "general_civil_demo",
}
ALLOWED_RISK_LEVELS = {"low", "medium", "controlled_demo"}


def create_mock_pilot_sample(request: PilotSampleMockRequest) -> dict:
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "试点样本请求被阻断。", "blocked_reasons": blocked})
    pilot_sample_id = f"personal_pilot_sample_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    record = PilotSampleRecord(
        pilot_sample_id=pilot_sample_id,
        sample_title=request.sample_title.strip(),
        sample_type=request.sample_type,
        legal_area=request.legal_area.strip(),
        case_cause=request.case_cause.strip(),
        risk_level=request.risk_level,
        demo_persona=request.demo_persona.strip(),
        linked_runtime_ids=request.linked_runtime_ids,
        workflow_progress=WorkflowProgress(completed_stage_count=7, total_stage_count=7, progress_percent=100, current_stage="final_lock"),
        safety_flags=default_safety_flags(),
        created_at=created_at,
        warnings=["试点样本仅为 synthetic mock metadata，不包含真实客户、案件、材料、判决或企业信息。"],
    )
    write_payload(PILOT_SAMPLES_DIR, pilot_sample_id, record.model_dump())
    record_audit_event(action="pilot_sample_mock_created", actor="system", object_type="pilot_sample", object_id=pilot_sample_id, timestamp=created_at)
    return record.model_dump()


def get_pilot_sample(pilot_sample_id: str) -> PilotSampleRecord | None:
    payload = read_payload(PILOT_SAMPLES_DIR, pilot_sample_id)
    return PilotSampleRecord(**payload) if payload else None


def list_pilot_samples() -> list[PilotSampleRecord]:
    return [PilotSampleRecord(**payload) for payload in read_payloads(PILOT_SAMPLES_DIR)]


def build_pilot_sample_list() -> dict:
    records = sorted(list_pilot_samples(), key=lambda record: record.created_at, reverse=True)
    return PilotSampleList(pilot_samples=records, sample_count=len(records), warnings=["试点样本列表仅包含 mock metadata。"]).model_dump()


def validate_request(request: PilotSampleMockRequest) -> list[str]:
    blocked = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_no_real_case_confirmation",
        "explicit_no_raw_content_confirmation",
        "explicit_no_final_opinion_confirmation",
        "explicit_no_external_delivery_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if request.sample_type not in ALLOWED_SAMPLE_TYPES:
        blocked.append("sample_type 不支持")
    if request.risk_level not in ALLOWED_RISK_LEVELS:
        blocked.append("risk_level 仅允许 low / medium / controlled_demo")
    blocked.extend(validate_mock_metadata_text(request.sample_title, "sample_title"))
    blocked.extend(validate_mock_metadata_text(request.legal_area, "legal_area"))
    blocked.extend(validate_mock_metadata_text(request.case_cause, "case_cause"))
    blocked.extend(validate_mock_metadata_text(request.demo_persona, "demo_persona"))
    return blocked
