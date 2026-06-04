from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaFinalLockStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_final_lock"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    requires_lawyer_final_review_approval: bool = True
    requires_manual_review: bool = True
    requires_lawyer_review: bool = True
    final_report_generation_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/personal_alpha_final_lock/locks"
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaFinalLockReadinessRequirements(BaseModel):
    requires_packet_exists: bool = True
    requires_latest_lawyer_action_approve_packet: bool = True
    requires_metadata_only: bool = True
    requires_no_raw_content: bool = True
    requires_no_final_legal_opinion: bool = True
    requires_no_final_report: bool = True


class PersonalAlphaFinalLockSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    requires_lawyer_final_review_approval: bool = True
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    raw_quote_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    runtime_storage_ignored: bool = True


class PersonalAlphaFinalLockReadiness(BaseModel):
    packet_id: str
    workspace_run_id: str = ""
    status: str = "mock_final_lock_readiness_ready"
    can_create_final_lock: bool = False
    requires_lawyer_final_review_approval: bool = True
    latest_lawyer_review_action: str | None = None
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    readiness_requirements: dict[str, Any] = Field(default_factory=dict)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalLockCreateRequest(BaseModel):
    reviewer_id: str = "local_demo_lawyer"
    manual_review_confirmed: bool = False
    lawyer_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False


class PersonalAlphaFinalLockRecord(BaseModel):
    lock_id: str
    packet_id: str
    workspace_run_id: str
    status: str = "final_lock_created"
    reviewer_id: str = "local_demo_lawyer"
    lock_record: dict[str, Any] = Field(default_factory=dict)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    manual_review_confirmed: bool = True
    lawyer_review_confirmed: bool = True
    metadata_only_confirmation: bool = True
    no_final_legal_opinion_confirmation: bool = True
    no_final_report_generation_confirmation: bool = True
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalLockCreateResult(BaseModel):
    lock_id: str = ""
    packet_id: str
    workspace_run_id: str = ""
    status: str = "blocked"
    reviewer_id: str = "local_demo_lawyer"
    lock_record: dict[str, Any] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    manual_review_confirmed: bool = False
    lawyer_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalLockList(BaseModel):
    locks: list[dict[str, Any]] = Field(default_factory=list)
    lock_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)
