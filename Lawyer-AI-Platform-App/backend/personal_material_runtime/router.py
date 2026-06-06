from typing import Any

from fastapi import APIRouter, HTTPException

from personal_material_runtime.audit_engine import build_audit_timeline, build_live_audit_timeline
from personal_material_runtime.document_live_gateway import (
    build_live_review_queue,
    execute_document_live_run,
    get_document_live_run,
    list_document_live_runs,
    submit_live_review_action,
)
from personal_material_runtime.material_parser_runtime import build_parse_job_list, create_mock_parse_job, get_parse_job
from personal_material_runtime.ocr_review_queue import build_review_queue, submit_review_action
from personal_material_runtime.ocr_live_gateway import execute_ocr_live_run, get_ocr_live_run, list_ocr_live_runs
from personal_material_runtime.ocr_runtime import build_ocr_job_list, create_mock_ocr_job, get_ocr_job, get_ocr_preview
from personal_material_runtime.provider_config import (
    document_live_mode_enabled,
    get_live_provider_config,
    list_live_provider_configs,
    ocr_live_mode_enabled,
)
from personal_material_runtime.provider_registry import get_provider, list_providers
from personal_material_runtime.safety_engine import build_live_safety_status, build_safety_status
from personal_material_runtime.schemas import (
    PersonalMaterialLiveGatewayStatus,
    PersonalMaterialLiveReviewActionRequest,
    PersonalMaterialLiveRunRequest,
    PersonalMaterialRuntimeStatus,
    PersonalMaterialParseJobRequest,
    PersonalOCRJobRequest,
    PersonalOCRReviewActionRequest,
)
from personal_material_runtime.source_trace_engine import build_live_source_trace_list, build_source_trace_list


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


@router.get("/live/status")
def material_live_status() -> dict[str, Any]:
    ocr_enabled = ocr_live_mode_enabled()
    document_enabled = document_live_mode_enabled()
    return PersonalMaterialLiveGatewayStatus(
        ocr_live_mode_enabled=ocr_enabled,
        document_live_mode_enabled=document_enabled,
        live_mode_enabled=ocr_enabled or document_enabled,
        warnings=[
            "OCR / Document Live Gateway is disabled by default in v7.13.",
            "Dry-run is available and does not call OCR or document parser providers.",
            "Raw OCR text and raw document content are blocked by default and never injected into AI prompts.",
        ],
    ).model_dump()


@router.get("/live/providers")
def material_live_providers() -> dict[str, Any]:
    return list_live_provider_configs()


@router.get("/live/providers/{provider_id}")
def material_live_provider_detail(provider_id: str) -> dict[str, Any]:
    provider = get_live_provider_config(provider_id)
    if provider is None:
        raise HTTPException(status_code=404, detail="Live provider metadata not found")
    return provider.model_dump()


@router.post("/live/document/dry-run")
def document_live_dry_run(request: PersonalMaterialLiveRunRequest) -> dict[str, Any]:
    return execute_document_live_run(request, dry_run=True)


@router.post("/live/document/runs")
def document_live_run(request: PersonalMaterialLiveRunRequest) -> dict[str, Any]:
    return execute_document_live_run(request, dry_run=False)


@router.get("/live/document/runs")
def document_live_runs() -> dict[str, Any]:
    return list_document_live_runs()


@router.get("/live/document/runs/{run_id}")
def document_live_run_detail(run_id: str) -> dict[str, Any]:
    run = get_document_live_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Document live run metadata not found")
    return run.model_dump()


@router.post("/live/ocr/dry-run")
def ocr_live_dry_run(request: PersonalMaterialLiveRunRequest) -> dict[str, Any]:
    return execute_ocr_live_run(request, dry_run=True)


@router.post("/live/ocr/runs")
def ocr_live_run(request: PersonalMaterialLiveRunRequest) -> dict[str, Any]:
    return execute_ocr_live_run(request, dry_run=False)


@router.get("/live/ocr/runs")
def ocr_live_runs() -> dict[str, Any]:
    return list_ocr_live_runs()


@router.get("/live/ocr/runs/{run_id}")
def ocr_live_run_detail(run_id: str) -> dict[str, Any]:
    run = get_ocr_live_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="OCR live run metadata not found")
    return run.model_dump()


@router.get("/live/review-queue")
def material_live_review_queue() -> dict[str, Any]:
    return build_live_review_queue()


@router.post("/live/review-queue/{review_item_id}/actions")
def material_live_review_action(review_item_id: str, request: PersonalMaterialLiveReviewActionRequest) -> dict[str, Any]:
    return submit_live_review_action(review_item_id, request)


@router.get("/live/source-traces")
def material_live_source_traces() -> dict[str, Any]:
    return build_live_source_trace_list()


@router.get("/live/audit")
def material_live_audit() -> dict[str, Any]:
    return build_live_audit_timeline()


@router.get("/live/safety")
def material_live_safety() -> dict[str, Any]:
    return build_live_safety_status()
