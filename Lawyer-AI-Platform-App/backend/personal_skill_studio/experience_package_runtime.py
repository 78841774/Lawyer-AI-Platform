from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_skill_studio.audit_engine import record_audit_event
from personal_skill_studio.safety_engine import default_safety_flags
from personal_skill_studio.schemas import ExperiencePackageDraft, ExperiencePackageDraftList, ExperiencePackageMockRequest
from personal_skill_studio.source_trace_engine import create_source_trace
from personal_skill_studio.storage import EXPERIENCE_PACKAGES_DIR, read_payload, read_payloads, write_payload


def create_mock_experience_package(request: ExperiencePackageMockRequest) -> dict:
    blocked = validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "经验包草案请求被阻断。", "blocked_reasons": blocked})
    experience_package_id = f"personal_experience_package_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    trace = create_source_trace(
        source_trace_id=f"skill_studio_source_trace_{experience_package_id}_1",
        source_type="case_metadata",
        source_label="案件 metadata 聚合 placeholder",
        linked_object_type="experience_package",
        linked_object_id=experience_package_id,
        case_id=request.case_id,
        experience_package_id=experience_package_id,
        created_at=created_at,
    )
    source_trace_ids = list(dict.fromkeys([*request.source_trace_ids, trace.source_trace_id]))
    record = ExperiencePackageDraft(
        experience_package_id=experience_package_id,
        case_id=request.case_id,
        package_title=request.package_title,
        legal_area=request.legal_area,
        case_cause=request.case_cause,
        jurisdiction=request.jurisdiction,
        source_trace_ids=source_trace_ids,
        safety_flags=default_safety_flags(),
        draft_sections={
            "fact_pattern_summary_placeholder": "事实模式摘要占位 metadata",
            "issue_pattern_summary_placeholder": "争议焦点模式占位 metadata",
            "source_trace_summary_placeholder": "来源追踪汇总占位 metadata",
            "limitation_notes_placeholder": "限制说明占位 metadata",
            "lawyer_review_notes_placeholder": "律师复核记录占位 metadata",
        },
        created_at=created_at,
        warnings=["仅生成经验包草案 metadata，未读取案件正文。"],
    )
    write_payload(EXPERIENCE_PACKAGES_DIR, experience_package_id, record.model_dump())
    record_audit_event(action="experience_package_mock_created", actor="system", object_type="experience_package", object_id=experience_package_id, timestamp=created_at)
    return record.model_dump()


def get_experience_package(experience_package_id: str) -> ExperiencePackageDraft | None:
    payload = read_payload(EXPERIENCE_PACKAGES_DIR, experience_package_id)
    return ExperiencePackageDraft(**payload) if payload else None


def list_experience_packages() -> list[ExperiencePackageDraft]:
    return [ExperiencePackageDraft(**payload) for payload in read_payloads(EXPERIENCE_PACKAGES_DIR)]


def build_experience_package_list() -> dict:
    records = sorted(list_experience_packages(), key=lambda record: record.created_at, reverse=True)
    return ExperiencePackageDraftList(experience_packages=records, package_count=len(records), warnings=["经验包列表仅包含草案 metadata。"]).model_dump()


def validate_request(request: ExperiencePackageMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_source_trace_confirmation",
        "explicit_no_raw_content_confirmation",
        "explicit_no_final_opinion_confirmation",
        "explicit_no_auto_publish_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.package_title.strip():
        blocked.append("package_title 不能为空")
    return blocked
