from ocr_adapter.provider import OCRProvider
from ocr_adapter.schemas import OCRPageResult, OCRProviderStatus, OCRRequest, OCRResult, OCRSourceRef, utc_now


class MockOCRProvider(OCRProvider):
    def get_status(self) -> OCRProviderStatus:
        return OCRProviderStatus(
            provider="mock_ocr",
            connected=False,
            mock_only=True,
            supports_pdf=True,
            supports_images=True,
            notes="OCR adapter prepared. Real OCR provider not connected."
        )

    def extract_text(self, request: OCRRequest) -> OCRResult:
        text = f"Mock OCR text for material {request.filename}. No real file content was read."
        source_ref = OCRSourceRef(
            source_ref_id=f"source_ref_ocr_mock_{request.material_id}",
            source_type="ocr",
            material_id=request.material_id,
            filename=request.filename,
            relative_path=request.relative_path,
            page_number=1,
            char_start=0,
            char_end=len(text),
            bbox=None,
            quote=text,
            provider="mock_ocr",
            provider_mode="mock",
            mock_only=True
        )
        page = OCRPageResult(
            page_number=1,
            text=text,
            confidence=0.0,
            source_ref=source_ref
        )
        return OCRResult(
            ocr_run_id=f"ocr_mock_{request.material_id}",
            material_id=request.material_id,
            filename=request.filename,
            relative_path=request.relative_path,
            provider="mock_ocr",
            provider_mode="mock",
            status="completed_mock",
            text_available=True,
            pages=[page],
            source_refs=[source_ref],
            warnings=[
                "Mock OCR only.",
                "No real OCR provider connected.",
                "No real file content read."
            ],
            created_at=utc_now()
        )
