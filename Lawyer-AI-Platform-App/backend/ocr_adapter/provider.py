from ocr_adapter.schemas import OCRProviderStatus, OCRRequest, OCRResult


class OCRProvider:
    def get_status(self) -> OCRProviderStatus:
        raise NotImplementedError

    def extract_text(self, request: OCRRequest) -> OCRResult:
        raise NotImplementedError
