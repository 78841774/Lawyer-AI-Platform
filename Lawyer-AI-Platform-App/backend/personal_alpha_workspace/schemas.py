from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class PersonalAlphaWorkspaceStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_workspace"
    production_enabled: bool = False
    end_to_end_workflow_enabled: bool = True
    mock_first_enabled: bool = True
    requires_manual_review: bool = True
    requires_explicit_workspace_confirmation: bool = True
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/personal_alpha_workspace"
    unified_audit_timeline_enabled: bool = True
    source_trace_enabled: bool = True
    final_legal_opinion_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    store_raw_material_text_in_git: bool = False
    store_raw_ocr_text_in_git: bool = False
    store_raw_legal_search_results_in_git: bool = False
    store_workspace_snapshot_in_git: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaWorkspaceRequest(BaseModel):
    case_id: str = "case_v50_demo_001"
    workspace_id: str = "workspace_demo_001"
    workflow_mode: str = "end_to_end_mock"
    material_preview_id: str = "controlled_preview_demo_001"
    ocr_preview_id: str = "ocr_preview_demo_001"
    legal_search_preview_id: str = "legal_search_preview_demo_001"
    draft_id: str = "draft_demo_001"
    review_id: str = "review_demo_001"
    revision_id: str = "revision_demo_001"
    final_lock_id: str = "final_lock_demo_001"
    explicit_workspace_confirmation: bool = False
    manual_review_confirmed: bool = False
    provider_mode: str = "controlled_local"
    llm_mode: str = "mock"
    preview_only: bool = True


class PersonalAlphaWorkspaceStageStatus(BaseModel):
    stage_id: str
    label: str
    status: str = "mock_ready"
    required: bool = True
    mock_only: bool = True
    source_ref_id: str
    notes: str = ""


class PersonalAlphaWorkspaceSnapshot(BaseModel):
    title: str = "Personal Alpha End-to-End Local Case Workspace"
    status: str = "mock_workspace_ready"
    case_id: str
    workspace_id: str
    workflow_mode: str
    stages: list[dict[str, Any]] = Field(default_factory=list)
    source_trace_summary: dict[str, Any] = Field(default_factory=dict)
    audit_timeline_summary: dict[str, Any] = Field(default_factory=dict)
    safety_boundaries: list[str] = Field(default_factory=list)
    final_legal_opinion_generated: bool = False
    requires_human_review: bool = True
    mock_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaWorkspaceGuardResult(BaseModel):
    guard_name: str
    allowed: bool
    status: str
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class PersonalAlphaWorkspaceRunResult(BaseModel):
    workspace_run_id: str
    case_id: str
    workspace_id: str
    workflow_mode: str
    status: str
    end_to_end_mock_run_created: bool = False
    final_legal_opinion_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    stage_statuses: list[dict[str, Any]] = Field(default_factory=list)
    workspace_snapshot: dict[str, Any] = Field(default_factory=dict)
    unified_audit_timeline: list[dict[str, Any]] = Field(default_factory=list)
    source_refs: list[dict[str, Any]] = Field(default_factory=list)
    guard_results: list[dict[str, Any]] = Field(default_factory=list)
    audit_log_id: str
    allowed_to_continue: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class PersonalAlphaWorkspaceAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    workspace_run_id: str
    workflow_mode: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class RuntimePersonalAlphaWorkspaceStorageResult(BaseModel):
    stored: bool
    storage_path: str
    raw_material_text_stored: bool = False
    raw_ocr_text_stored: bool = False
    raw_legal_search_results_stored: bool = False
    workspace_snapshot_stored_in_git: bool = False
    mock_or_redacted_only: bool = True
    warnings: list[str] = Field(default_factory=list)
