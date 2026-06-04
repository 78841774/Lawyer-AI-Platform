from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledFinalReviewLockStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled_final_review_lock"
    production_enabled: bool = False
    mock_final_lock_enabled: bool = True
    requires_revision_id: bool = True
    requires_review_id: bool = True
    requires_draft_id: bool = True
    requires_manual_final_confirmation: bool = True
    requires_explicit_final_lock_confirmation: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_final_review_locks"
    source_trace_enabled: bool = True
    immutable_snapshot_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    store_raw_material_text_in_git: bool = False
    store_raw_ocr_text_in_git: bool = False
    store_raw_legal_search_results_in_git: bool = False
    store_final_lock_snapshot_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledFinalReviewLockRequest(BaseModel):
    case_id: str = "case_v49_demo_001"
    workspace_id: str = "workspace_demo_001"
    draft_id: str = "draft_demo_001"
    review_id: str = "review_demo_001"
    revision_id: str = "revision_demo_001"
    final_review_notes: str = ""
    final_checklist_confirmed: bool = False
    explicit_final_lock_confirmation: bool = False
    manual_final_review_confirmed: bool = False
    lock_mode: str = "mock_final_review_candidate"
    llm_mode: str = "mock"
    provider_mode: str = "controlled_local"
    preview_only: bool = True


class ControlledFinalReviewLockGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledFinalReviewChecklistItem(BaseModel):
    item_id: str
    label: str
    status: str = "pending_lawyer_final_confirmation"
    required: bool = True
    notes: str = ""


class ControlledFinalReviewSourceRef(BaseModel):
    source_ref_id: str
    source_type: str = "controlled_final_review_lock"
    final_lock_id: str
    quote: str = "Mock final review lock source trace placeholder. No raw content included."
    provider: str = "controlled_final_review_lock"
    provider_mode: str = "mock"
    mock_or_redacted_only: bool = True
    linked_draft_id: str | None = None
    linked_review_id: str | None = None
    linked_revision_id: str | None = None


class ControlledFinalReviewLockResult(BaseModel):
    final_lock_id: str
    case_id: str
    workspace_id: str
    draft_id: str
    review_id: str
    revision_id: str
    status: str
    lock_mode: str
    mock_final_lock_created: bool = False
    immutable_snapshot_created: bool = False
    final_legal_opinion_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    final_lock_storage_path: str = "storage/runtime/controlled_final_review_locks"
    mock_final_review_snapshot: dict[str, Any] = Field(default_factory=dict)
    final_review_checklist: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledFinalReviewLockRecord(BaseModel):
    final_lock_id: str
    case_id: str = ""
    workspace_id: str = ""
    draft_id: str = ""
    review_id: str = ""
    revision_id: str = ""
    lock_mode: str = ""
    mock_final_review_snapshot: dict[str, Any] = Field(default_factory=dict)
    final_review_checklist: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str
    immutable_snapshot: bool = True


class ControlledFinalReviewLockAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    draft_id: str
    review_id: str
    revision_id: str
    final_lock_id: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class RuntimeControlledFinalReviewLockStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_material_text_stored: bool = False
    raw_ocr_text_stored: bool = False
    raw_legal_search_results_stored: bool = False
    final_lock_snapshot_stored_in_git: bool = False
    immutable_snapshot: bool = True
    warnings: list[str] = Field(default_factory=list)
