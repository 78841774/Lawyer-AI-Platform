from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaDashboardStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_dashboard"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    requires_manual_review: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    source_runtime_path: str = "storage/runtime/personal_alpha_workspace"
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaWorkspaceSummary(BaseModel):
    total_workspace_runs: int = 0
    ready_stage_count: int = 0
    pending_stage_count: int = 0
    blocked_stage_count: int = 0
    audit_event_count: int = 0
    source_trace_count: int = 0
    mock_or_redacted_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaDashboardStageHealth(BaseModel):
    stage_id: str
    label: str
    status: str = "mock_pending_reference"
    required: bool = True
    mock_only: bool = True
    source_ref_id: str = ""
    notes: str = ""


class PersonalAlphaDashboardAuditTimeline(BaseModel):
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaDashboardSourceTraceSummary(BaseModel):
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    source_trace_count: int = 0
    mock_or_redacted_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaRunStageDetail(BaseModel):
    stage_id: str
    label: str
    status: str = "mock_pending_reference"
    required: bool = True
    mock_only: bool = True
    source_ref_id: str = ""
    notes: str = "Metadata-only stage detail. No raw content included."


class PersonalAlphaRunGuardSummary(BaseModel):
    guard_count: int = 0
    blocked_count: int = 0
    passed_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaRunSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    manual_review_required: bool = True
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    final_legal_opinion_generated: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False


class PersonalAlphaRunDetail(BaseModel):
    workspace_run_id: str
    case_id: str = ""
    workspace_id: str = ""
    workflow_mode: str = ""
    status: str = "mock_run_detail_ready"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    stage_details: list[dict[str, Any]] = Field(default_factory=list)
    audit_timeline: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_summary: dict[str, Any] = Field(default_factory=dict)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""
