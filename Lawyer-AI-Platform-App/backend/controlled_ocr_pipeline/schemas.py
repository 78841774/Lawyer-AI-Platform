from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledOCRStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled_ocr"
    production_enabled: bool = False
    ocr_live_enabled: bool = False
    ocr_live_default: bool = False
    mock_ocr_enabled: bool = True
    requires_explicit_ocr_confirmation: bool = True
    requires_manual_review: bool = True
    allowed_file_extensions: list[str] = Field(default_factory=lambda: [".pdf", ".png", ".jpg", ".jpeg", ".txt"])
    max_file_size_bytes: int = 5000000
    read_pdf_binary_enabled: bool = False
    read_image_binary_enabled: bool = False
    extract_real_ocr_text_enabled: bool = False
    store_raw_ocr_text_in_git: bool = False
    store_redacted_ocr_preview_in_git: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_ocr_previews"
    source_trace_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledOCRPreviewRequest(BaseModel):
    case_id: str = "case_v44_demo_001"
    workspace_id: str = "workspace_demo_001"
    local_file_path: str = "~/Lawyer-AI-Local-Cases/demo_case/ocr_seed.txt"
    filename_redacted: str = "<filename_redacted>.txt"
    material_id: str = "material_ocr_demo_001"
    explicit_ocr_confirmation: bool = False
    manual_review_confirmed: bool = False
    ocr_mode: str = "mock"
    provider_mode: str = "controlled_local"
    preview_only: bool = True


class ControlledOCRGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledOCRSourceRef(BaseModel):
    source_ref_id: str
    source_type: str = "controlled_ocr_preview"
    ocr_preview_id: str
    material_id: str
    filename: str = "<filename_redacted>"
    relative_path: str = "<local_file_path_redacted>"
    quote: str
    provider: str = "controlled_ocr"
    provider_mode: str = "mock"
    mock_or_redacted_only: bool = True


class RuntimeOCRStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_ocr_text_stored: bool = False
    redacted_ocr_preview_stored: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledOCRPreviewResult(BaseModel):
    ocr_preview_id: str
    case_id: str
    workspace_id: str
    material_id: str
    filename_redacted: str = "<filename_redacted>"
    local_file_path_redacted: str = "<local_file_path_redacted>"
    file_extension: str
    file_size_bytes: int
    ocr_called: bool = False
    real_ocr_called: bool = False
    mock_ocr_used: bool = False
    raw_ocr_text_stored: bool = False
    redacted_ocr_preview_created: bool = False
    redacted_ocr_preview: str = ""
    redacted_ocr_preview_storage_path: str = "storage/runtime/controlled_ocr_previews"
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledOCRPreviewRecord(BaseModel):
    ocr_preview_id: str
    case_id: str = ""
    workspace_id: str = ""
    material_id: str = ""
    filename_redacted: str = "<filename_redacted>"
    local_file_path_redacted: str = "<local_file_path_redacted>"
    redacted_ocr_preview: str
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledOCRAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    ocr_preview_id: str | None = None
    material_id: str | None = None
    filename_redacted: str | None = "<filename_redacted>"
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str
