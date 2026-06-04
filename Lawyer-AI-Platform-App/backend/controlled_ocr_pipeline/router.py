from typing import Any

from fastapi import APIRouter

from controlled_ocr_pipeline.audit import list_controlled_ocr_audit_logs
from controlled_ocr_pipeline.mock_ocr import get_controlled_ocr_preview, get_controlled_ocr_status, run_mock_ocr_preview
from controlled_ocr_pipeline.schemas import ControlledOCRPreviewRequest

router = APIRouter(prefix="/controlled-ocr", tags=["controlled-ocr"])


@router.get("/status")
def controlled_ocr_status() -> dict[str, Any]:
    return get_controlled_ocr_status()


@router.post("/preview")
def controlled_ocr_preview(request: ControlledOCRPreviewRequest) -> dict[str, Any]:
    return run_mock_ocr_preview(request)


@router.get("/preview/{ocr_preview_id}")
def controlled_ocr_preview_record(ocr_preview_id: str) -> dict[str, Any]:
    return get_controlled_ocr_preview(ocr_preview_id)


@router.get("/audit-logs")
def controlled_ocr_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_ocr_audit_logs()}
