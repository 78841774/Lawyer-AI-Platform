from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaLawyerFinalReviewStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_lawyer_final_review"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    requires_final_packet: bool = True
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
    runtime_storage_path: str = "storage/runtime/personal_alpha_lawyer_final_review/actions"
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaLawyerFinalReviewSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    requires_final_packet: bool = True
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


class PersonalAlphaLawyerFinalReviewSummary(BaseModel):
    review_status: str = "pending_lawyer_review"
    action_count: int = 0
    approved_packet_count: int = 0
    revision_requested_count: int = 0
    rejected_packet_count: int = 0
    latest_action: str | None = None
    ready_for_controlled_final_lock: bool = False
    requires_packet_revision: bool = False
    requires_additional_lawyer_review: bool = True


class PersonalAlphaLawyerFinalReviewPacketDetail(BaseModel):
    packet_id: str
    workspace_run_id: str
    status: str = "mock_lawyer_final_review_ready"
    packet_status: str = "packet_created"
    review_status: str = "pending_lawyer_review"
    latest_action: str | None = None
    can_submit_review_action: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    packet_summary: dict[str, Any] = Field(default_factory=dict)
    review_actions: list[dict[str, Any]] = Field(default_factory=list)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaLawyerFinalReviewActionRequest(BaseModel):
    action: str
    reviewer_id: str = "local_demo_lawyer"
    reason: str = ""
    manual_review_confirmed: bool = False
    lawyer_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False


class PersonalAlphaLawyerFinalReviewActionRecord(BaseModel):
    action_id: str
    packet_id: str
    workspace_run_id: str
    action: str
    reviewer_id: str = "local_demo_lawyer"
    reason: str = ""
    status: str = "lawyer_final_review_action_recorded"
    ready_for_controlled_final_lock: bool = False
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


class PersonalAlphaLawyerFinalReviewActionResult(PersonalAlphaLawyerFinalReviewActionRecord):
    pass


class PersonalAlphaLawyerFinalReviewActionList(BaseModel):
    packet_id: str
    actions: list[dict[str, Any]] = Field(default_factory=list)
    action_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)
