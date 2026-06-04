from fastapi import APIRouter

from ocr_adapter.mock_provider import MockOCRProvider
from ocr_adapter.schemas import OCRProviderStatus, OCRRequest, OCRResult

router = APIRouter(prefix="/ocr", tags=["ocr-adapter"])
provider = MockOCRProvider()


@router.get("/status")
def get_ocr_status() -> OCRProviderStatus:
    return provider.get_status()


@router.post("/mock-extract")
def mock_extract_ocr(payload: OCRRequest) -> OCRResult:
    return provider.extract_text(payload)
