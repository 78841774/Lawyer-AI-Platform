from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledMaterialStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled"
    production_enabled: bool = False
    real_material_reading_enabled: bool = True
    real_material_reading_default: bool = False
    requires_explicit_read_confirmation: bool = True
    requires_manual_review: bool = True
    allowed_file_extensions: list[str] = Field(default_factory=lambda: [".txt", ".md", ".json"])
    max_file_size_bytes: int = 200000
    read_pdf_enabled: bool = False
    read_docx_enabled: bool = False
    read_image_enabled: bool = False
    ocr_live_enabled: bool = False
    llm_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    store_raw_content_in_git: bool = False
    store_redacted_preview_in_git: bool = False
    store_extracted_text_in_git: bool = False
    store_material_content_in_git: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_material_previews"
    source_trace_enabled: bool = True
    report_draft_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledMaterialReadRequest(BaseModel):
    case_id: str = "case_v42_demo_001"
    workspace_id: str = "workspace_demo_001"
    local_case_root: str | None = "~/Lawyer-AI-Local-Cases/demo_case"
    material_id: str = "material_demo_001"
    filename_redacted: str = "<filename_redacted>.pdf"
    read_mode: str = "controlled_local"
    explicit_read_confirmation: bool = False
    manual_review_confirmed: bool = False
    provider_mode: str = "controlled_local"
    ocr_mode: str = "mock"
    llm_mode: str = "mock"
    legal_search_mode: str = "mock"


class ControlledMaterialGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)


class ControlledLocalFileGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledProviderGateResult(BaseModel):
    provider_mode: str
    ocr_mode: str
    llm_mode: str
    legal_search_mode: str
    allowed: bool
    blocked_modes: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ControlledMaterialReadResult(BaseModel):
    controlled_read_id: str
    case_id: str
    workspace_id: str
    material_id: str
    filename_redacted: str = "<filename_redacted>"
    local_case_root_redacted: str = "<local_case_root_redacted>"
    content_read: bool = False
    controlled_read_ready: bool = False
    requires_next_stage_real_read: bool = True
    extracted_text_stored: bool = False
    git_storage_allowed: bool = False
    allowed_to_continue: bool
    guard_results: list[dict[str, Any]]
    source_refs: list[dict[str, Any]]
    warnings: list[str] = Field(default_factory=list)
    audit_log_id: str
    created_at: str


class ControlledReportDraftRequest(BaseModel):
    case_id: str = "case_v42_demo_001"
    workspace_id: str = "workspace_demo_001"
    controlled_read_id: str = "controlled_read_demo_001"
    report_mode: str = "mock_draft"
    manual_review_confirmed: bool = False
    llm_mode: str = "mock"


class ControlledReportDraftResult(BaseModel):
    report_draft_id: str
    case_id: str
    workspace_id: str
    controlled_read_id: str
    status: str = "mock_draft"
    legal_opinion_finalized: bool = False
    requires_human_review: bool = True
    final_legal_opinion_enabled: bool = False
    llm_called: bool = False
    content_read: bool = False
    mock_only: bool = True
    source_refs: list[dict[str, Any]]
    warnings: list[str] = Field(default_factory=list)
    audit_log_id: str
    created_at: str


class ControlledLocalReadPreviewRequest(BaseModel):
    case_id: str = "case_v43_demo_001"
    workspace_id: str = "workspace_demo_001"
    local_file_path: str = "~/Lawyer-AI-Local-Cases/demo_case/sample_redacted.txt"
    filename_redacted: str = "<filename_redacted>.txt"
    material_id: str = "material_demo_001"
    explicit_read_confirmation: bool = False
    manual_review_confirmed: bool = False
    provider_mode: str = "controlled_local"
    ocr_mode: str = "disabled"
    llm_mode: str = "disabled"
    legal_search_mode: str = "disabled"
    preview_only: bool = True


class RedactedPreviewResult(BaseModel):
    redacted_preview: str
    redaction_applied: bool
    sensitive_patterns_detected: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class RuntimeStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_content_stored: bool = False
    redacted_preview_stored: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledLocalReadPreviewResult(BaseModel):
    preview_id: str
    case_id: str
    workspace_id: str
    material_id: str
    filename_redacted: str = "<filename_redacted>"
    local_file_path_redacted: str = "<local_file_path_redacted>"
    file_extension: str
    file_size_bytes: int
    content_read: bool = False
    raw_content_stored: bool = False
    redacted_preview_created: bool = False
    redacted_preview: str = ""
    redacted_preview_storage_path: str = "storage/runtime/controlled_material_previews"
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledReadPreviewRecord(BaseModel):
    preview_id: str
    case_id: str = ""
    workspace_id: str = ""
    material_id: str = ""
    filename_redacted: str = "<filename_redacted>"
    local_file_path_redacted: str = "<local_file_path_redacted>"
    redacted_preview: str
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledMaterialAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    controlled_read_id: str | None = None
    preview_id: str | None = None
    material_id: str | None = None
    filename_redacted: str | None = "<filename_redacted>"
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str
