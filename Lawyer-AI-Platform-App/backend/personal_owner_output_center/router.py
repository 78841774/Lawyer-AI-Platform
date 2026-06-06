from typing import Any

from fastapi import APIRouter, HTTPException

from personal_owner_output_center.audit_engine import build_audit_timeline
from personal_owner_output_center.output_collection_engine import build_output_list, build_status
from personal_owner_output_center.output_gate_engine import build_output_gate
from personal_owner_output_center.output_optimization_engine import build_output_optimization
from personal_owner_output_center.output_quality_engine import build_output_quality
from personal_owner_output_center.output_registry import get_registry_output
from personal_owner_output_center.owner_download_engine import create_owner_download, get_owner_download, list_owner_downloads
from personal_owner_output_center.safety_engine import build_safety_status
from personal_owner_output_center.schemas import OwnerDownloadMockRequest
from personal_owner_output_center.source_trace_engine import build_source_trace_list


router = APIRouter(prefix="/personal-owner-output-center", tags=["personal-owner-output-center"])


@router.get("/status")
def status() -> dict[str, Any]:
    return build_status()


@router.get("/outputs")
def outputs() -> dict[str, Any]:
    return build_output_list()


@router.get("/outputs/{output_id}")
def output_detail(output_id: str) -> dict[str, Any]:
    output = get_registry_output(output_id)
    if output is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    return output.model_dump()


@router.get("/outputs/{output_id}/quality")
def output_quality(output_id: str) -> dict[str, Any]:
    quality = build_output_quality(output_id)
    if quality is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    return quality.model_dump()


@router.get("/outputs/{output_id}/gate")
def output_gate(output_id: str) -> dict[str, Any]:
    gate = build_output_gate(output_id)
    if gate is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    return gate.model_dump()


@router.get("/outputs/{output_id}/optimization")
def output_optimization(output_id: str) -> dict[str, Any]:
    optimization = build_output_optimization(output_id)
    if optimization is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    return optimization.model_dump()


@router.get("/outputs/{output_id}/source-traces")
def output_source_traces(output_id: str) -> dict[str, Any]:
    if get_registry_output(output_id) is None:
        raise HTTPException(status_code=404, detail="output_id 不存在")
    return build_source_trace_list(output_id).model_dump()


@router.post("/outputs/{output_id}/downloads/mock")
def owner_download_mock(output_id: str, request: OwnerDownloadMockRequest) -> dict[str, Any]:
    return create_owner_download(output_id, request)


@router.get("/downloads")
def downloads() -> dict[str, Any]:
    return list_owner_downloads()


@router.get("/downloads/{download_id}")
def download_detail(download_id: str) -> dict[str, Any]:
    download = get_owner_download(download_id)
    if download is None:
        raise HTTPException(status_code=404, detail="download_id 不存在")
    return download.model_dump()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit_timeline()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety_status()
