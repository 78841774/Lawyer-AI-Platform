from typing import Any

from fastapi import APIRouter, HTTPException

from personal_material_runtime.audit_engine import build_audit_timeline
from personal_material_runtime.material_parser_runtime import build_parse_job_list, create_mock_parse_job, get_parse_job
from personal_material_runtime.ocr_review_queue import build_review_queue, submit_review_action
from personal_material_runtime.ocr_runtime import build_ocr_job_list, create_mock_ocr_job, get_ocr_job, get_ocr_preview
from personal_material_runtime.provider_registry import get_provider, list_providers
from personal_material_runtime.safety_engine import build_safety_status
from personal_material_runtime.schemas import (
    PersonalMaterialRuntimeStatus,
    PersonalMaterialParseJobRequest,
    PersonalOCRJobRequest,
    PersonalOCRReviewActionRequest,
)
from personal_material_runtime.source_trace_engine import build_source_trace_list


router = APIRouter(prefix="/personal-material-runtime", tags=["personal-material-runtime"])


@router.get("/status")
def material_runtime_status() -> dict[str, Any]:
    return PersonalMaterialRuntimeStatus(
        warnings=[
            "v7.2 Material Runtime is mock-first and provider-gated.",
            "No live OCR or file parser provider call is enabled in v7.2.",
            "OCR output is controlled preview only and requires lawyer review.",
        ],
    ).model_dump()


@router.get("/providers")
def providers() -> dict[str, Any]:
    return list_providers()


@router.get("/providers/{provider_id}")
def provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_provider(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Provider metadata not found")
    return provider.model_dump()


@router.post("/parse-jobs/mock")
def parse_job_mock(request: PersonalMaterialParseJobRequest) -> dict[str, Any]:
    return create_mock_parse_job(request)


@router.get("/parse-jobs")
def parse_jobs() -> dict[str, Any]:
    return build_parse_job_list()


@router.get("/parse-jobs/{parse_job_id}")
def parse_job_detail(parse_job_id: str) -> dict[str, Any]:
    job = get_parse_job(parse_job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Parse job metadata not found")
    return job.model_dump()


@router.post("/ocr-jobs/mock")
def ocr_job_mock(request: PersonalOCRJobRequest) -> dict[str, Any]:
    return create_mock_ocr_job(request)


@router.get("/ocr-jobs")
def ocr_jobs() -> dict[str, Any]:
    return build_ocr_job_list()


@router.get("/ocr-jobs/{ocr_job_id}")
def ocr_job_detail(ocr_job_id: str) -> dict[str, Any]:
    job = get_ocr_job(ocr_job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="OCR job metadata not found")
    return job.model_dump()


@router.get("/ocr-jobs/{ocr_job_id}/preview")
def ocr_job_preview(ocr_job_id: str) -> dict[str, Any]:
    preview = get_ocr_preview(ocr_job_id)
    if preview is None:
        raise HTTPException(status_code=404, detail="OCR preview metadata not found")
    return preview.model_dump()


@router.get("/ocr-review-queue")
def ocr_review_queue() -> dict[str, Any]:
    return build_review_queue()


@router.post("/ocr-review-queue/{ocr_job_id}/actions")
def ocr_review_action(ocr_job_id: str, request: PersonalOCRReviewActionRequest) -> dict[str, Any]:
    return submit_review_action(ocr_job_id, request)


@router.get("/source-traces")
def source_traces() -> dict[str, Any]:
    return build_source_trace_list()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
