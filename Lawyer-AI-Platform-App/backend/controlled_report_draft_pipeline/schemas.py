from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledReportDraftStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled_report_draft"
    production_enabled: bool = False
    mock_report_assembly_enabled: bool = True
    requires_manual_review: bool = True
    requires_explicit_assembly_confirmation: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_report_drafts"
    source_trace_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    store_raw_material_text_in_git: bool = False
    store_raw_ocr_text_in_git: bool = False
    store_raw_legal_search_results_in_git: bool = False
    store_report_draft_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledReportDraftAssembleRequest(BaseModel):
    case_id: str = "case_v46_demo_001"
    workspace_id: str = "workspace_demo_001"
    material_preview_ids: list[str] = Field(default_factory=list)
    ocr_preview_ids: list[str] = Field(default_factory=list)
    legal_search_preview_ids: list[str] = Field(default_factory=list)
    citation_ids: list[str] = Field(default_factory=list)
    explicit_assembly_confirmation: bool = False
    manual_review_confirmed: bool = False
    report_mode: str = "mock_draft"
    llm_mode: str = "mock"
    provider_mode: str = "controlled_local"
    preview_only: bool = True


class ControlledReportDraftGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledReportDraftSourceRef(BaseModel):
    source_ref_id: str
    source_type: str = "controlled_report_draft"
    draft_id: str
    quote: str = "Mock report draft source trace placeholder. No raw content included."
    provider: str = "controlled_report_draft_pipeline"
    provider_mode: str = "mock"
    mock_or_redacted_only: bool = True
    linked_source_id: str | None = None
    linked_source_type: str | None = None


class ControlledReportDraftResult(BaseModel):
    draft_id: str
    case_id: str
    workspace_id: str
    status: str
    mock_report_assembled: bool = False
    final_legal_opinion_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    report_draft_storage_path: str = "storage/runtime/controlled_report_drafts"
    mock_assembled_report: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    citations: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledReportDraftRecord(BaseModel):
    draft_id: str
    case_id: str = ""
    workspace_id: str = ""
    mock_assembled_report: dict[str, Any] = Field(default_factory=dict)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    citations: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledReportDraftAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    draft_id: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class RuntimeControlledReportDraftStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_material_text_stored: bool = False
    raw_ocr_text_stored: bool = False
    raw_legal_search_results_stored: bool = False
    report_draft_stored_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)

