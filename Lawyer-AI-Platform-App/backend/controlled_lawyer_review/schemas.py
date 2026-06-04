from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class ControlledLawyerReviewStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_controlled_lawyer_review"
    production_enabled: bool = False
    mock_review_enabled: bool = True
    requires_explicit_review_confirmation: bool = True
    requires_explicit_assembly_confirmation: bool = True
    requires_manual_review: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    skill_publish_enabled: bool = False
    workspace_runtime_auto_enable: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/controlled_lawyer_reviews"
    source_trace_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    store_raw_material_text_in_git: bool = False
    store_raw_ocr_text_in_git: bool = False
    store_raw_legal_search_results_in_git: bool = False
    store_review_record_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)


class ControlledLawyerReviewSubmitRequest(BaseModel):
    draft_id: str = "controlled_report_draft_demo_001"
    case_id: str = "case_v47_demo_001"
    workspace_id: str = "workspace_demo_001"
    submitted_by: str = "lawyer_demo"
    explicit_review_confirmation: bool = False
    explicit_assembly_confirmation: bool = False
    manual_review_confirmed: bool = False
    review_mode: str = "mock_review"
    draft_status: str = "mock_draft"
    llm_mode: str = "mock"
    provider_mode: str = "controlled_local"
    preview_only: bool = True


class ControlledLawyerReviewActionRequest(BaseModel):
    reviewer_id: str = "lawyer_reviewer_demo"
    review_notes: str = ""
    explicit_review_confirmation: bool = False
    manual_review_confirmed: bool = False
    llm_mode: str = "mock"
    provider_mode: str = "controlled_local"


class ControlledLawyerReviewGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ControlledLawyerReviewResult(BaseModel):
    review_id: str
    draft_id: str
    case_id: str
    workspace_id: str
    status: str
    action: str
    submitted: bool = False
    approved: bool = False
    rejected: bool = False
    revision_requested: bool = False
    final_legal_opinion_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    skill_published: bool = False
    workspace_runtime_enabled: bool = False
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    review_record_storage_path: str = "storage/runtime/controlled_lawyer_reviews"
    review_record: dict[str, Any] = Field(default_factory=dict)
    history: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class ControlledLawyerReviewRecord(BaseModel):
    review_id: str
    draft_id: str
    case_id: str = ""
    workspace_id: str = ""
    status: str = "not_found"
    submitted_by: str = ""
    reviewer_id: str = ""
    review_notes: str = ""
    final_legal_opinion_generated: bool = False
    history: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str


class ControlledLawyerReviewAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    review_id: str
    draft_id: str
    case_id: str
    workspace_id: str
    action: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str

