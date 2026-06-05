from datetime import datetime, timezone
from uuid import uuid4

from personal_material_runtime.audit_engine import record_audit_event
from personal_material_runtime.provider_registry import validate_provider
from personal_material_runtime.schemas import (
    PersonalOCRJobList,
    PersonalOCRJobRecord,
    PersonalOCRJobRequest,
    PersonalOCRJobResult,
    PersonalOCRPreview,
    PersonalOCRReviewItem,
)
from personal_material_runtime.source_trace_engine import create_source_traces
from personal_material_runtime.storage import OCR_JOBS_DIR, REVIEW_QUEUE_DIR, read_payload, read_payloads, write_payload


OCR_JOB_TYPES = {
    "image_ocr_preview",
    "scanned_pdf_ocr_preview",
    "table_ocr_preview",
    "layout_analysis_preview",
    "key_information_preview",
}


def create_mock_ocr_job(request: PersonalOCRJobRequest) -> dict:
    blocked_reasons = [
        *validate_provider(request.ocr_provider_id, "ocr"),
        *validate_ocr_request(request),
    ]
    if blocked_reasons:
        return PersonalOCRJobResult(
            case_id=request.case_id,
            material_id=request.material_id,
            ocr_provider_id=request.ocr_provider_id,
            ocr_job_type=request.ocr_job_type,
            status="blocked",
            blocked_reasons=blocked_reasons,
            warnings=["Mock OCR job blocked. No job was created and no OCR provider call was attempted."],
        ).model_dump()

    ocr_job_id = f"personal_ocr_job_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    preview = build_mock_ocr_preview(
        ocr_job_id=ocr_job_id,
        case_id=request.case_id,
        material_id=request.material_id,
        ocr_provider_id=request.ocr_provider_id,
        ocr_job_type=request.ocr_job_type,
    )
    record = PersonalOCRJobRecord(
        ocr_job_id=ocr_job_id,
        case_id=request.case_id,
        material_id=request.material_id,
        ocr_provider_id=request.ocr_provider_id,
        ocr_job_type=request.ocr_job_type,
        ocr_preview=preview,
        created_at=created_at,
        warnings=["Mock OCR metadata only. No image or PDF was read."],
    )
    review_item = PersonalOCRReviewItem(
        ocr_job_id=ocr_job_id,
        case_id=request.case_id,
        material_id=request.material_id,
        ocr_provider_id=request.ocr_provider_id,
        confidence=preview.average_confidence,
        low_confidence_block_count=preview.low_confidence_block_count,
        created_at=created_at,
        updated_at=created_at,
    )
    write_payload(OCR_JOBS_DIR, ocr_job_id, record.model_dump())
    write_payload(REVIEW_QUEUE_DIR, ocr_job_id, review_item.model_dump())
    create_source_traces(
        case_id=request.case_id,
        material_id=request.material_id,
        job_id=ocr_job_id,
        source_type="ocr_preview",
        provider_id=request.ocr_provider_id,
        created_at=created_at,
        block_count=preview.recognized_block_count,
    )
    record_audit_event(
        event_type="mock_ocr_job_created",
        case_id=request.case_id,
        material_id=request.material_id,
        provider_id=request.ocr_provider_id,
        job_id=ocr_job_id,
        created_at=created_at,
        manual_approval_confirmed=request.manual_approval_confirmed,
    )
    return PersonalOCRJobResult(
        ocr_job_id=ocr_job_id,
        case_id=request.case_id,
        material_id=request.material_id,
        ocr_provider_id=request.ocr_provider_id,
        ocr_job_type=request.ocr_job_type,
        ocr_preview=preview,
        warnings=[],
    ).model_dump()


def build_mock_ocr_preview(
    *,
    ocr_job_id: str,
    case_id: str,
    material_id: str,
    ocr_provider_id: str,
    ocr_job_type: str,
) -> PersonalOCRPreview:
    table_detected = ocr_job_type == "table_ocr_preview"
    low_confidence_count = 1 if ocr_job_type == "key_information_preview" else 0
    return PersonalOCRPreview(
        ocr_job_id=ocr_job_id,
        case_id=case_id,
        material_id=material_id,
        ocr_provider_id=ocr_provider_id,
        page_count=1,
        recognized_block_count=3,
        average_confidence=0.86 if low_confidence_count else 0.91,
        low_confidence_block_count=low_confidence_count,
        table_detected=table_detected,
        layout_detected=True,
        key_information_detected=ocr_job_type in {"key_information_preview", "scanned_pdf_ocr_preview"},
        preview_blocks=[
            {"block_id": "mock_block_1", "type": "redacted_text_preview", "confidence": 0.93, "bbox_redacted": True},
            {"block_id": "mock_block_2", "type": "mock_text_block", "confidence": 0.88, "bbox_redacted": True},
            {"block_id": "mock_block_3", "type": "placeholder_table_summary", "confidence": 0.91, "bbox_redacted": True},
        ],
        warnings=["Controlled preview metadata only. Recognized source text is not returned."],
    )


def list_ocr_jobs() -> list[PersonalOCRJobRecord]:
    return [PersonalOCRJobRecord(**payload) for payload in read_payloads(OCR_JOBS_DIR)]


def get_ocr_job(ocr_job_id: str) -> PersonalOCRJobRecord | None:
    payload = read_payload(OCR_JOBS_DIR, ocr_job_id)
    return PersonalOCRJobRecord(**payload) if payload else None


def build_ocr_job_list() -> dict:
    jobs = sorted(list_ocr_jobs(), key=lambda job: job.created_at, reverse=True)
    return PersonalOCRJobList(
        ocr_jobs=jobs,
        job_count=len(jobs),
        warnings=["OCR jobs are mock metadata only and do not include recognized source text."],
    ).model_dump()


def get_ocr_preview(ocr_job_id: str) -> PersonalOCRPreview | None:
    job = get_ocr_job(ocr_job_id)
    return job.ocr_preview if job else None


def save_ocr_job(record: PersonalOCRJobRecord) -> None:
    write_payload(OCR_JOBS_DIR, record.ocr_job_id, record.model_dump())


def validate_ocr_request(request: PersonalOCRJobRequest) -> list[str]:
    missing: list[str] = []
    if request.ocr_job_type not in OCR_JOB_TYPES:
        missing.append("ocr_job_type is not supported")
    if not request.manual_approval_confirmed:
        missing.append("manual_approval_confirmed is required")
    if not request.lawyer_review_required_confirmation:
        missing.append("lawyer_review_required_confirmation is required")
    if not request.source_trace_required_confirmation:
        missing.append("source_trace_required_confirmation is required")
    if not request.no_raw_ocr_exposure_confirmation:
        missing.append("no_raw_ocr_exposure_confirmation is required")
    if not request.no_final_legal_opinion_confirmation:
        missing.append("no_final_legal_opinion_confirmation is required")
    if not request.no_final_report_generation_confirmation:
        missing.append("no_final_report_generation_confirmation is required")
    return missing
