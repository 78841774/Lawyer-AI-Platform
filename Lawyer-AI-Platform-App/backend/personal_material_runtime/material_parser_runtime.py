from datetime import datetime, timezone
from uuid import uuid4

from personal_material_runtime.audit_engine import record_audit_event
from personal_material_runtime.provider_registry import validate_provider
from personal_material_runtime.schemas import (
    PersonalMaterialParseJobList,
    PersonalMaterialParseJobRecord,
    PersonalMaterialParseJobRequest,
    PersonalMaterialParseJobResult,
    PersonalMaterialParseSummary,
)
from personal_material_runtime.source_trace_engine import create_source_traces
from personal_material_runtime.storage import PARSE_JOBS_DIR, read_payload, read_payloads, write_payload


PARSE_TYPES = {
    "pdf_text_extract_preview",
    "pdf_to_images_preview",
    "docx_structure_preview",
    "excel_table_preview",
    "image_metadata_preview",
    "archive_listing_preview",
}


def create_mock_parse_job(request: PersonalMaterialParseJobRequest) -> dict:
    blocked_reasons = [
        *validate_provider(request.parser_provider_id, "file_parser"),
        *validate_parse_request(request),
    ]
    if blocked_reasons:
        return PersonalMaterialParseJobResult(
            case_id=request.case_id,
            material_id=request.material_id,
            parser_provider_id=request.parser_provider_id,
            parse_type=request.parse_type,
            status="blocked",
            blocked_reasons=blocked_reasons,
            warnings=["Mock parse job blocked. No job was created and no parser call was attempted."],
        ).model_dump()

    parse_job_id = f"personal_material_parse_job_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    summary = _summary_for_parse_type(request.parse_type)
    record = PersonalMaterialParseJobRecord(
        parse_job_id=parse_job_id,
        case_id=request.case_id,
        material_id=request.material_id,
        parser_provider_id=request.parser_provider_id,
        parse_type=request.parse_type,
        parse_summary=summary,
        created_at=created_at,
        warnings=["Mock parse metadata only. No source document was read."],
    )
    write_payload(PARSE_JOBS_DIR, parse_job_id, record.model_dump())
    create_source_traces(
        case_id=request.case_id,
        material_id=request.material_id,
        job_id=parse_job_id,
        source_type="material_parse_preview",
        provider_id=request.parser_provider_id,
        created_at=created_at,
        block_count=1,
    )
    record_audit_event(
        event_type="mock_parse_job_created",
        case_id=request.case_id,
        material_id=request.material_id,
        provider_id=request.parser_provider_id,
        job_id=parse_job_id,
        created_at=created_at,
        manual_approval_confirmed=request.manual_approval_confirmed,
    )
    return PersonalMaterialParseJobResult(
        parse_job_id=parse_job_id,
        case_id=request.case_id,
        material_id=request.material_id,
        parser_provider_id=request.parser_provider_id,
        parse_type=request.parse_type,
        parse_summary=summary,
        warnings=[],
    ).model_dump()


def list_parse_jobs() -> list[PersonalMaterialParseJobRecord]:
    return [PersonalMaterialParseJobRecord(**payload) for payload in read_payloads(PARSE_JOBS_DIR)]


def get_parse_job(parse_job_id: str) -> PersonalMaterialParseJobRecord | None:
    payload = read_payload(PARSE_JOBS_DIR, parse_job_id)
    return PersonalMaterialParseJobRecord(**payload) if payload else None


def build_parse_job_list() -> dict:
    jobs = sorted(list_parse_jobs(), key=lambda job: job.created_at, reverse=True)
    return PersonalMaterialParseJobList(
        parse_jobs=jobs,
        job_count=len(jobs),
        warnings=["Parse jobs are mock metadata only and do not include source document text."],
    ).model_dump()


def validate_parse_request(request: PersonalMaterialParseJobRequest) -> list[str]:
    missing: list[str] = []
    if request.parse_type not in PARSE_TYPES:
        missing.append("parse_type is not supported")
    if not request.manual_approval_confirmed:
        missing.append("manual_approval_confirmed is required")
    if not request.mock_data_only_confirmation:
        missing.append("mock_data_only_confirmation is required")
    if not request.no_raw_content_confirmation:
        missing.append("no_raw_content_confirmation is required")
    if not request.no_external_upload_confirmation:
        missing.append("no_external_upload_confirmation is required")
    return missing


def _summary_for_parse_type(parse_type: str) -> PersonalMaterialParseSummary:
    if parse_type == "excel_table_preview":
        return PersonalMaterialParseSummary(table_count=1)
    if parse_type == "docx_structure_preview":
        return PersonalMaterialParseSummary(section_count=3)
    if parse_type == "pdf_to_images_preview":
        return PersonalMaterialParseSummary(page_count=1, image_count=1)
    if parse_type == "image_metadata_preview":
        return PersonalMaterialParseSummary(image_count=1)
    if parse_type == "archive_listing_preview":
        return PersonalMaterialParseSummary(section_count=1)
    return PersonalMaterialParseSummary(page_count=1)
