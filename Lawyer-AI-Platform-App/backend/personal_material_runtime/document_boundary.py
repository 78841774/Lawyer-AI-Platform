from personal_material_runtime.schemas import PersonalMaterialLiveRunRequest


SUPPORTED_DOCUMENT_TYPES = {"pdf", "docx", "pptx", "xlsx", "html", "md", "txt"}
SUPPORTED_OCR_TYPES = {"pdf", "png", "jpg", "jpeg", "tiff"}


def validate_document_boundary(request: PersonalMaterialLiveRunRequest) -> list[str]:
    blocked: list[str] = []
    file_type = request.file_type.strip().lower().lstrip(".")
    if file_type not in SUPPORTED_DOCUMENT_TYPES:
        blocked.append("file_type is not supported for document metadata preview")
    if request.byte_size < 0:
        blocked.append("byte_size cannot be negative")
    if not _safe_short_value(request.case_id):
        blocked.append("case_id is unsafe")
    if not _safe_short_value(request.material_id):
        blocked.append("material_id is unsafe")
    return blocked


def validate_ocr_boundary(request: PersonalMaterialLiveRunRequest) -> list[str]:
    blocked: list[str] = []
    file_type = request.file_type.strip().lower().lstrip(".")
    if file_type not in SUPPORTED_OCR_TYPES:
        blocked.append("file_type is not supported for OCR metadata preview")
    if request.byte_size < 0:
        blocked.append("byte_size cannot be negative")
    if not _safe_short_value(request.case_id):
        blocked.append("case_id is unsafe")
    if not _safe_short_value(request.material_id):
        blocked.append("material_id is unsafe")
    return blocked


def _safe_short_value(value: str) -> bool:
    if not value or len(value) > 96:
        return False
    return all(ch.isalnum() or ch in {"_", "-", "."} for ch in value)
