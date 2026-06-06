from datetime import UTC, datetime
from uuid import uuid4

from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import v731b_safety_flags
from personal_skill_studio.training_artifacts.schemas import OcrJob, OcrJobRequest, OcrParseSummary


def build_ocr_job(request: OcrJobRequest) -> OcrJob:
    job_id = f"v731b_ocr_job_{uuid4().hex[:12]}"
    source_trace_id = f"{job_id}_source_trace"
    audit_id = f"{job_id}_audit_create"
    summary = OcrParseSummary(
        parse_summary_id=f"{job_id}_summary",
        job_id=job_id,
        document_type=request.document_type,
        page_count=request.page_count,
        structured_summary=[
            "案件背景结构摘要",
            "争议焦点结构摘要",
            "证据目录结构摘要",
            "律师工作思路结构摘要",
        ],
        section_labels=["case_background", "issues", "evidence_index", "work_product_notes"],
        source_trace_id=source_trace_id,
        audit_id=audit_id,
        **v731b_safety_flags(),
    )
    return OcrJob(
        job_id=job_id,
        material_label=request.material_label,
        owner_user_id=request.owner_user_id,
        document_type=request.document_type,
        page_count=request.page_count,
        parse_summary=summary,
        source_trace_id=source_trace_id,
        audit_events=[
            _event(audit_id, "create_demo_safe_ocr_parse_job", source_trace_id),
            _event(f"{job_id}_audit_parse", "generate_structured_parse_summary", source_trace_id),
        ],
        warnings=["OCR / document parsing is demo-safe metadata only; no provider call is executed."],
        **v731b_safety_flags(),
    )


def _event(event_id: str, action: str, source_trace_id: str) -> dict[str, str | bool]:
    return {
        "event_id": event_id,
        "actor": "owner_local_demo",
        "action": action,
        "timestamp": datetime.now(UTC).isoformat(),
        "source_trace_id": source_trace_id,
        "material_boundary_decision": "controlled_internal_processing_only",
        "metadata_only": True,
        "safety_decision": "demo_safe_redacted_summary_only",
    }
