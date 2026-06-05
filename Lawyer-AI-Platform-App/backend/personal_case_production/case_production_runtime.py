from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_production.audit_engine import record_audit_event
from personal_case_production.safety_engine import default_safety_flags
from personal_case_production.schemas import ProductionCaseList, ProductionCaseMockRequest, ProductionCaseRecord
from personal_case_production.source_trace_engine import create_source_trace
from personal_case_production.storage import PRODUCTION_CASES_DIR, REVIEW_GATES_DIR, read_payload, read_payloads, write_payload


def create_mock_production_case(request: ProductionCaseMockRequest) -> dict:
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "生产案件记录请求被阻断。", "blocked_reasons": blocked})
    production_case_id = f"personal_production_case_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    create_source_trace(
        source_trace_id=f"case_production_source_trace_{production_case_id}_1",
        source_type="case_metadata",
        source_label="生产案件 metadata placeholder",
        linked_object_type="production_case",
        linked_object_id=production_case_id,
        production_case_id=production_case_id,
        created_at=created_at,
    )
    record = ProductionCaseRecord(
        production_case_id=production_case_id,
        case_id=request.case_id,
        production_title=request.production_title,
        case_type=request.case_type,
        client_alias=request.client_alias,
        jurisdiction=request.jurisdiction,
        legal_area=request.legal_area,
        desensitization_status=request.desensitization_status,
        safety_flags=default_safety_flags(),
        created_at=created_at,
        warnings=["仅创建真实案件生产工作流 metadata，不读取真实案件原文。"],
    )
    payload = record.model_dump()
    write_payload(PRODUCTION_CASES_DIR, production_case_id, payload)
    write_payload(REVIEW_GATES_DIR, production_case_id, payload)
    record_audit_event(action="production_case_mock_created", actor="system", object_type="production_case", object_id=production_case_id, timestamp=created_at)
    return payload


def get_production_case(production_case_id: str) -> ProductionCaseRecord | None:
    payload = read_payload(PRODUCTION_CASES_DIR, production_case_id)
    return ProductionCaseRecord(**payload) if payload else None


def save_production_case(record: ProductionCaseRecord) -> None:
    payload = record.model_dump()
    write_payload(PRODUCTION_CASES_DIR, record.production_case_id, payload)
    write_payload(REVIEW_GATES_DIR, record.production_case_id, payload)


def list_production_cases() -> list[ProductionCaseRecord]:
    return [ProductionCaseRecord(**payload) for payload in read_payloads(PRODUCTION_CASES_DIR)]


def build_production_case_list() -> dict:
    records = sorted(list_production_cases(), key=lambda record: record.created_at, reverse=True)
    return ProductionCaseList(production_cases=records, case_count=len(records), warnings=["生产案件列表仅包含 metadata。"]).model_dump()


def validate_request(request: ProductionCaseMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in ["explicit_mock_confirmation", "explicit_no_raw_content_confirmation", "explicit_no_final_opinion_confirmation", "explicit_no_external_delivery_confirmation"]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.production_title.strip():
        blocked.append("production_title 不能为空")
    return blocked
