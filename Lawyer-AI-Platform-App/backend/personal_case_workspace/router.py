from typing import Any

from fastapi import APIRouter, HTTPException

from personal_case_workspace.audit_engine import build_audit_timeline, build_fact_audit_timeline
from personal_case_workspace.case_workspace_service import build_case_detail, build_case_list, build_status
from personal_case_workspace.fact_correction_engine import create_fact_correction_v20, get_fact_correction, list_fact_corrections
from personal_case_workspace.fact_correction_service import build_fact_input, create_fact_correction
from personal_case_workspace.fact_gate_engine import (
    confirm_for_legal_analysis,
    list_legal_analysis_input_readiness,
    build_fact_gate,
)
from personal_case_workspace.fact_preview_engine import create_fact_preview, get_fact_preview, list_fact_previews
from personal_case_workspace.fact_quality_engine import build_fact_quality
from personal_case_workspace.fact_source_trace_engine import build_fact_source_traces
from personal_case_workspace.fact_version_engine import create_fact_version, list_fact_versions
from personal_case_workspace.material_workspace_service import build_material_detail, build_material_list
from personal_case_workspace.ocr_status_service import build_ocr_status
from personal_case_workspace.owner_access_guard import build_owner_raw_view_response
from personal_case_workspace.safety_engine import build_fact_safety_status, build_safety_status
from personal_case_workspace.schemas import (
    FactCorrectionMockRequest,
    FactCorrectionMockRequestV20,
    FactPreviewMockRequest,
    FactVersionMockRequest,
    LegalAnalysisInputConfirmRequest,
    OwnerRawViewRequest,
)
from personal_case_workspace.source_trace_service import build_source_traces


router = APIRouter(prefix="/personal-case-workspace", tags=["personal-case-workspace"])


def _ensure_material(material_id: str) -> None:
    if build_material_detail(material_id) is None:
        raise HTTPException(status_code=404, detail="material_id 不存在")


@router.get("/status")
def status() -> dict[str, Any]:
    return build_status().model_dump()


@router.get("/cases")
def cases() -> dict[str, Any]:
    return build_case_list().model_dump()


@router.get("/cases/{case_id}")
def case_detail(case_id: str) -> dict[str, Any]:
    record = build_case_detail(case_id)
    if record is None:
        raise HTTPException(status_code=404, detail="case_id 不存在")
    return record.model_dump()


@router.get("/cases/{case_id}/materials")
def case_materials(case_id: str) -> dict[str, Any]:
    if build_case_detail(case_id) is None:
        raise HTTPException(status_code=404, detail="case_id 不存在")
    return build_material_list(case_id).model_dump()


@router.get("/materials/{material_id}")
def material_detail(material_id: str) -> dict[str, Any]:
    record = build_material_detail(material_id)
    if record is None:
        raise HTTPException(status_code=404, detail="material_id 不存在")
    return record.model_dump()


@router.post("/materials/{material_id}/owner-raw-view")
def owner_raw_view(material_id: str, request: OwnerRawViewRequest) -> dict[str, Any]:
    _ensure_material(material_id)
    return build_owner_raw_view_response(material_id, request).model_dump()


@router.get("/materials/{material_id}/ocr-status")
def ocr_status(material_id: str) -> dict[str, Any]:
    _ensure_material(material_id)
    return build_ocr_status(material_id).model_dump()


@router.get("/materials/{material_id}/source-traces")
def material_source_traces(material_id: str) -> dict[str, Any]:
    _ensure_material(material_id)
    return build_source_traces(material_id).model_dump()


@router.get("/materials/{material_id}/fact-input")
def fact_input(material_id: str) -> dict[str, Any]:
    _ensure_material(material_id)
    return build_fact_input(material_id).model_dump()


@router.post("/materials/{material_id}/fact-input/corrections/mock")
def fact_input_correction(material_id: str, request: FactCorrectionMockRequest) -> dict[str, Any]:
    _ensure_material(material_id)
    return create_fact_correction(material_id, request).model_dump()


@router.get("/source-traces")
def source_traces() -> dict[str, Any]:
    return build_source_traces().model_dump()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline().model_dump()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status().model_dump()


@router.get("/fact-previews")
def fact_previews() -> dict[str, Any]:
    return list_fact_previews().model_dump()


@router.post("/fact-previews/mock")
def fact_preview_mock(request: FactPreviewMockRequest) -> dict[str, Any]:
    return create_fact_preview(request).model_dump()


@router.get("/fact-previews/{fact_preview_id}")
def fact_preview_detail(fact_preview_id: str) -> dict[str, Any]:
    record = get_fact_preview(fact_preview_id)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.post("/fact-previews/{fact_preview_id}/corrections/mock")
def fact_preview_correction_mock(fact_preview_id: str, request: FactCorrectionMockRequestV20) -> dict[str, Any]:
    record = create_fact_correction_v20(fact_preview_id, request)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.get("/fact-previews/{fact_preview_id}/corrections")
def fact_preview_corrections(fact_preview_id: str) -> dict[str, Any]:
    record = list_fact_corrections(fact_preview_id)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.get("/fact-corrections/{correction_id}")
def fact_correction_detail(correction_id: str) -> dict[str, Any]:
    record = get_fact_correction(correction_id)
    if record is None:
        raise HTTPException(status_code=404, detail="correction_id 不存在")
    return record.model_dump()


@router.get("/fact-previews/{fact_preview_id}/versions")
def fact_preview_versions(fact_preview_id: str) -> dict[str, Any]:
    record = list_fact_versions(fact_preview_id)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.post("/fact-previews/{fact_preview_id}/versions/mock")
def fact_preview_version_mock(fact_preview_id: str, request: FactVersionMockRequest) -> dict[str, Any]:
    record = create_fact_version(fact_preview_id, request)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.get("/fact-previews/{fact_preview_id}/quality")
def fact_preview_quality(fact_preview_id: str) -> dict[str, Any]:
    record = build_fact_quality(fact_preview_id)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.get("/fact-previews/{fact_preview_id}/gate")
def fact_preview_gate(fact_preview_id: str) -> dict[str, Any]:
    record = build_fact_gate(fact_preview_id)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.get("/fact-previews/{fact_preview_id}/source-traces")
def fact_preview_source_traces(fact_preview_id: str) -> dict[str, Any]:
    record = build_fact_source_traces(fact_preview_id)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.post("/fact-previews/{fact_preview_id}/confirm-for-legal-analysis/mock")
def confirm_fact_for_legal_analysis(fact_preview_id: str, request: LegalAnalysisInputConfirmRequest) -> dict[str, Any]:
    record = confirm_for_legal_analysis(fact_preview_id, request)
    if record is None:
        raise HTTPException(status_code=404, detail="fact_preview_id 不存在")
    return record.model_dump()


@router.get("/fact-input-readiness")
def fact_input_readiness() -> dict[str, Any]:
    return list_legal_analysis_input_readiness().model_dump()


@router.get("/fact-audit")
def fact_audit() -> dict[str, Any]:
    return build_fact_audit_timeline().model_dump()


@router.get("/fact-safety")
def fact_safety() -> dict[str, Any]:
    return build_fact_safety_status().model_dump()
