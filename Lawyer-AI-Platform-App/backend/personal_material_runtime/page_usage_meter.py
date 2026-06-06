from personal_material_runtime.provider_config import get_live_provider_config
from personal_material_runtime.schemas import PersonalMaterialLiveMetadataPreview, PersonalMaterialLiveRunRequest


def build_document_metadata_preview(request: PersonalMaterialLiveRunRequest) -> PersonalMaterialLiveMetadataPreview:
    provider = get_live_provider_config(request.provider_id)
    file_type = request.file_type.strip().lower().lstrip(".") or "pdf"
    page_count = _estimate_pages(file_type, request.byte_size)
    return PersonalMaterialLiveMetadataPreview(
        page_count=page_count,
        page_count_estimate=page_count,
        file_type=file_type,
        byte_size=max(request.byte_size, 0),
        parse_status="would_parse_metadata_only" if request.dry_run else "blocked_or_adapter_unavailable",
        confidence_summary="metadata_only_no_text_confidence",
        layout_blocks_count=3 if provider and provider.supports_layout_extraction else 0,
        table_count=1 if provider and provider.supports_table_extraction else 0,
        image_count=1 if file_type in {"pdf", "pptx"} else 0,
        bbox_available=bool(provider and provider.supports_bbox),
        supports_bbox=bool(provider and provider.supports_bbox),
        supports_confidence=True,
        redacted_preview_available=True,
    )


def build_ocr_metadata_preview(request: PersonalMaterialLiveRunRequest) -> PersonalMaterialLiveMetadataPreview:
    provider = get_live_provider_config(request.provider_id)
    file_type = request.file_type.strip().lower().lstrip(".") or "pdf"
    page_count = _estimate_pages(file_type, request.byte_size)
    return PersonalMaterialLiveMetadataPreview(
        page_count=page_count,
        page_count_estimate=page_count,
        file_type=file_type,
        byte_size=max(request.byte_size, 0),
        parse_status="would_ocr_metadata_only" if request.dry_run else "blocked_or_adapter_unavailable",
        confidence_summary="estimated_confidence_metadata_only",
        layout_blocks_count=4 if provider and provider.supports_layout_extraction else 0,
        table_count=1 if provider and provider.supports_table_extraction else 0,
        image_count=max(page_count, 1),
        bbox_available=bool(provider and provider.supports_bbox),
        supports_bbox=bool(provider and provider.supports_bbox),
        supports_confidence=True,
        redacted_preview_available=True,
    )


def _estimate_pages(file_type: str, byte_size: int) -> int:
    if file_type in {"png", "jpg", "jpeg", "tiff"}:
        return 1
    if byte_size <= 0:
        return 1
    return max(1, min(20, int(byte_size / 750_000) + 1))
