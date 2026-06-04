from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledMaterialStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled"
    production_enabled: bool = False
    real_material_reading_enabled: bool = False
    real_material_reading_default: bool = False
    requires_explicit_read_confirmation: bool = True
    requires_manual_review: bool = True
    ocr_live_enabled: bool = False
    llm_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    store_extracted_text_in_git: bool = False
    store_material_content_in_git: bool = False
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


class ControlledMaterialAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    controlled_read_id: str | None = None
    material_id: str | None = None
    filename_redacted: str | None = "<filename_redacted>"
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str
