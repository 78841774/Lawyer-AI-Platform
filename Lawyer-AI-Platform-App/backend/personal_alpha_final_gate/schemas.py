from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaFinalGateStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_final_gate"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    advisory_only: bool = True
    requires_final_readiness: bool = True
    requires_manual_review: bool = True
    final_report_generation_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaFinalGateRequirements(BaseModel):
    requires_final_review_ready: bool = True
    requires_no_blocked_stages: bool = True
    requires_manual_gate_decision: bool = True
    requires_metadata_only: bool = True
    requires_no_raw_content: bool = True


class PersonalAlphaFinalGateSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    manual_review_required: bool = True
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False


class PersonalAlphaFinalGateSummary(BaseModel):
    gate_open: bool = False
    final_review_ready: bool = False
    requires_additional_review: bool = True
    latest_gate_decision: str | None = None
    gate_decision_count: int = 0
    approved_gate_count: int = 0
    blocked_gate_count: int = 0
    more_review_requested_count: int = 0
    can_proceed_to_controlled_final_review: bool = False


class PersonalAlphaFinalGateRunDetail(BaseModel):
    workspace_run_id: str
    status: str = "mock_final_gate_ready"
    final_review_ready: bool = False
    gate_open: bool = False
    requires_additional_review: bool = True
    blocked: bool = False
    can_proceed_to_controlled_final_review: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    readiness_summary: dict[str, Any] = Field(default_factory=dict)
    gate_requirements: dict[str, Any] = Field(default_factory=dict)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    gate_summary: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalGateDecisionRequest(BaseModel):
    decision: str
    reviewer_id: str = "local_demo_reviewer"
    reason: str = ""
    manual_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False


class PersonalAlphaFinalGateDecisionRecord(BaseModel):
    gate_decision_id: str
    workspace_run_id: str
    decision: str
    reviewer_id: str
    reason: str = ""
    status: str = "gate_decision_recorded"
    can_proceed_to_controlled_final_review: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    manual_review_confirmed: bool = True
    metadata_only_confirmation: bool = True
    no_final_legal_opinion_confirmation: bool = True
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class PersonalAlphaFinalGateDecisionResult(BaseModel):
    gate_decision_id: str
    workspace_run_id: str
    decision: str
    reviewer_id: str
    reason: str = ""
    status: str
    can_proceed_to_controlled_final_review: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    manual_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class PersonalAlphaFinalGateDecisionList(BaseModel):
    workspace_run_id: str
    decisions: list[dict[str, Any]] = Field(default_factory=list)
    decision_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)
