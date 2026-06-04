from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledRevisionStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled_revision"
    production_enabled: bool = False
    mock_revision_enabled: bool = True
    requires_review_id: bool = True
    requires_manual_review: bool = True
    requires_explicit_revision_confirmation: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_revisions"
    source_trace_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    store_raw_material_text_in_git: bool = False
    store_raw_ocr_text_in_git: bool = False
    store_raw_legal_search_results_in_git: bool = False
    store_revision_output_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledRevisionRequest(BaseModel):
    case_id: str = "case_v48_demo_001"
    workspace_id: str = "workspace_demo_001"
    review_id: str = "review_demo_001"
    draft_id: str = "draft_demo_001"
    revision_reason: str = ""
    revision_instructions: str = ""
    requested_action: str = "revise_summary"
    explicit_revision_confirmation: bool = False
    manual_review_confirmed: bool = False
    llm_mode: str = "mock"
    provider_mode: str = "controlled_local"
    preview_only: bool = True


class ControlledRevisionGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledRevisionChecklistItem(BaseModel):
    item_id: str
    label: str
    status: str = "pending_lawyer_re_review"
    required: bool = True
    notes: str = ""


class ControlledRevisionSourceRef(BaseModel):
    source_ref_id: str
    source_type: str = "controlled_revision"
    revision_id: str
    quote: str = "Mock revision source trace placeholder. No raw content included."
    provider: str = "controlled_revision_workflow"
    provider_mode: str = "mock"
    mock_or_redacted_only: bool = True
    linked_review_id: str | None = None
    linked_draft_id: str | None = None


class ControlledRevisionResult(BaseModel):
    revision_id: str
    case_id: str
    workspace_id: str
    review_id: str
    draft_id: str
    status: str
    requested_action: str
    mock_revision_created: bool = False
    final_legal_opinion_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    revision_storage_path: str = "storage/runtime/controlled_revisions"
    mock_revision_plan: dict[str, Any] = Field(default_factory=dict)
    revision_checklist: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledRevisionRecord(BaseModel):
    revision_id: str
    case_id: str = ""
    workspace_id: str = ""
    review_id: str = ""
    draft_id: str = ""
    requested_action: str = ""
    mock_revision_plan: dict[str, Any] = Field(default_factory=dict)
    revision_checklist: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledRevisionAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    review_id: str
    draft_id: str
    revision_id: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class RuntimeControlledRevisionStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_material_text_stored: bool = False
    raw_ocr_text_stored: bool = False
    raw_legal_search_results_stored: bool = False
    revision_output_stored_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)

