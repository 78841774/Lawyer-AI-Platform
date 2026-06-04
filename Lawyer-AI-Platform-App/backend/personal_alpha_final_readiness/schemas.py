from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaFinalReadinessStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_final_readiness"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    requires_manual_review: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/personal_alpha_final_readiness"
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaFinalReadinessSafetyChecklist(BaseModel):
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
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    runtime_storage_ignored: bool = True


class PersonalAlphaFinalReadinessStage(BaseModel):
    stage_id: str
    label: str
    required: bool = True
    source_ref_id: str = ""
    workspace_stage_status: str = "mock_pending_reference"
    latest_decision: str = "pending_review"
    decision_count: int = 0
    stage_ready: bool = False
    blocked: bool = False
    requires_additional_review: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    notes: str = "Metadata-only final readiness stage."


class PersonalAlphaFinalReadinessSummary(BaseModel):
    workspace_run_id: str
    total_stages: int = 0
    mandatory_stage_count: int = 0
    ready_stage_count: int = 0
    blocked_stage_count: int = 0
    pending_stage_count: int = 0
    decision_count: int = 0
    approved_decision_count: int = 0
    rejected_decision_count: int = 0
    revision_requested_count: int = 0
    unclear_decision_count: int = 0
    stage_ready: bool = False
    requires_additional_review: bool = True
    final_review_ready: bool = False
    final_legal_opinion_generated: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaFinalReadinessRunDetail(BaseModel):
    workspace_run_id: str
    case_id: str = ""
    workspace_id: str = ""
    workflow_mode: str = ""
    status: str = "mock_final_readiness_ready"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    advisory_only: bool = True
    summary: dict[str, Any] = Field(default_factory=dict)
    stages: list[dict[str, Any]] = Field(default_factory=list)
    blocked_stages: list[dict[str, Any]] = Field(default_factory=list)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    decision_metadata: dict[str, Any] = Field(default_factory=dict)
    run_metadata: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""
