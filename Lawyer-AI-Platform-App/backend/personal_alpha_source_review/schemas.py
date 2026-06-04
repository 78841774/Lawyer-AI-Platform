from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaSourceReviewStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_source_review"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    requires_manual_review: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaSourceTrace(BaseModel):
    source_ref_id: str
    source_type: str = "personal_alpha_workspace_stage"
    workspace_run_id: str
    case_id: str = ""
    workspace_id: str = ""
    stage_id: str = ""
    evidence_item_id: str = ""
    evidence_status: str = "mock_ready"
    provider: str = "personal_alpha_workspace"
    provider_mode: str = "mock"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    notes: str = "Metadata-only source trace. No raw content included."


class PersonalAlphaEvidenceSummary(BaseModel):
    total_sources: int = 0
    total_evidence_items: int = 0
    blocked_sources: int = 0
    ready_sources: int = 0
    pending_sources: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaSourceReviewSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
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


class PersonalAlphaSourceReviewRunDetail(BaseModel):
    workspace_run_id: str
    case_id: str = ""
    workspace_id: str = ""
    workflow_mode: str = ""
    status: str = "mock_source_review_ready"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    source_traces: list[dict[str, Any]] = Field(default_factory=list)
    evidence_summary: dict[str, Any] = Field(default_factory=dict)
    audit_timeline: list[dict[str, Any]] = Field(default_factory=list)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""
