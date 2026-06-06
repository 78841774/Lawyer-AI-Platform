from pydantic import BaseModel, Field


class TrialSafetyBase(BaseModel):
    owner_only: bool = True
    trial_metadata_only: bool = True
    metadata_only: bool = True
    draft_only: bool = True
    raw_case_content_included: bool = False
    raw_ocr_content_included: bool = False
    api_key_exposed: bool = False
    provider_live_call_triggered: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    gate_reference_only: bool = True
    blocks_next_stage: bool = False
    audit_required: bool = True
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    local_path_visible: bool = False
    raw_content_written_to_git_docs_regression: bool = False


class TrialSessionMockRequest(BaseModel):
    trial_name: str = "个人版实战试运行样本"
    case_mode: str = "synthetic_case"
    owner_user_id: str = "local_owner"
    case_reference_label: str = "本地试运行样本"
    explicit_owner_confirmation: bool = True
    explicit_no_raw_content_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_external_delivery_confirmation: bool = True


class TrialSession(TrialSafetyBase):
    trial_id: str
    trial_name: str
    case_mode: str = "synthetic_case"
    owner_user_id: str = "local_owner"
    case_reference_label: str = "本地试运行样本"
    trial_status: str = "planned"
    started_at: str
    completed_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class TrialSessionList(TrialSafetyBase):
    trials: list[TrialSession] = Field(default_factory=list)
    trial_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrialReadinessStatus(TrialSafetyBase):
    enabled: bool = True
    version: str = "v7.25"
    runtime_label: str = "个人版实战案件试运行准备"
    trial_readiness_ready: bool = True
    trial_checklist_ready: bool = True
    issue_log_ready: bool = True
    quality_review_ready: bool = True
    safety_confirmation_ready: bool = True
    optimization_backlog_ready: bool = True
    live_provider_disabled: bool = True
    open_case_training_disabled: bool = True
    skill_auto_publish_disabled: bool = True
    warnings: list[str] = Field(default_factory=list)


class TrialChecklist(TrialSafetyBase):
    trial_id: str = "trial_mock_001"
    case_workspace_checked: bool = True
    material_workspace_checked: bool = True
    ocr_status_checked: bool = True
    fact_preview_checked: bool = True
    fact_correction_checked: bool = True
    legal_draft_checked: bool = True
    skill_final_drafts_checked: bool = True
    owner_output_center_checked: bool = True
    source_trace_checked: bool = True
    review_queue_checked: bool = True
    trust_safety_checked: bool = True
    diagnostics_collapsed_checked: bool = True
    checked_item_count: int = 12
    warnings: list[str] = Field(default_factory=list)


class StageObservationMockRequest(BaseModel):
    stage_id: str = "case_intake"
    notes: str = "仅记录试运行观察 metadata"
    issue_count: int = 0


class StageObservation(TrialSafetyBase):
    trial_id: str
    stage_id: str
    stage_name: str
    observation_status: str = "observed_metadata_only"
    usability_score: int = 82
    quality_score: int = 80
    issue_count: int = 0
    notes: str = "仅记录试运行观察 metadata"
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class StageObservationList(TrialSafetyBase):
    trial_id: str
    observations: list[StageObservation] = Field(default_factory=list)
    observation_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class IssueLogMockRequest(BaseModel):
    stage_id: str = "case_intake"
    issue_type: str = "ui"
    severity: str = "low"
    title: str = "试运行记录样本"
    description: str = "仅用于记录优化点，不阻断下一步。"
    suggested_fix: str = "在后续优化阶段统一处理。"


class IssueLogItem(TrialSafetyBase):
    issue_id: str
    trial_id: str
    stage_id: str
    issue_type: str
    severity: str
    title: str
    description: str
    suggested_fix: str
    status: str = "open"
    blocks_trial: bool = False
    warnings: list[str] = Field(default_factory=list)


class IssueLogList(TrialSafetyBase):
    trial_id: str | None = None
    issues: list[IssueLogItem] = Field(default_factory=list)
    issue_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class QualityReview(TrialSafetyBase):
    review_id: str
    trial_id: str
    overall_score: int = 82
    stage_scores: dict[str, int] = Field(default_factory=dict)
    fact_quality_score: int = 82
    legal_draft_quality_score: int = 80
    skill_helpfulness_score: int = 79
    source_trace_score: int = 86
    owner_download_score: int = 84
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SafetyConfirmation(TrialSafetyBase):
    trial_id: str = "trial_mock_001"
    owner_only_confirmed: bool = True
    draft_only_confirmed: bool = True
    no_public_link_confirmed: bool = True
    no_email_confirmed: bool = True
    no_external_delivery_confirmed: bool = True
    no_final_legal_opinion_confirmed: bool = True
    no_final_report_confirmed: bool = True
    no_open_case_training_confirmed: bool = True
    no_skill_auto_publish_confirmed: bool = True
    no_api_key_exposed_confirmed: bool = True
    no_raw_content_in_diagnostics_confirmed: bool = True
    no_raw_content_in_git_docs_regression_confirmed: bool = True
    warnings: list[str] = Field(default_factory=list)


class OptimizationBacklogMockRequest(BaseModel):
    source_trial_id: str = "trial_mock_001"
    source_issue_ids: list[str] = Field(default_factory=list)
    priority: str = "medium"
    target_area: str = "trial_readiness"
    title: str = "试运行优化建议"
    description: str = "汇总试运行问题记录，用于 v7.26 优化。"
    recommended_version: str = "v7.26"


class OptimizationBacklogItem(TrialSafetyBase):
    backlog_id: str
    source_trial_id: str
    source_issue_ids: list[str] = Field(default_factory=list)
    priority: str
    target_area: str
    title: str
    description: str
    recommended_version: str = "v7.26"
    status: str = "proposed"
    warnings: list[str] = Field(default_factory=list)


class OptimizationBacklogList(TrialSafetyBase):
    backlog_items: list[OptimizationBacklogItem] = Field(default_factory=list)
    backlog_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrialAuditEvent(TrialSafetyBase):
    event_id: str
    action: str
    object_type: str
    object_id: str
    actor: str = "system"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class TrialAuditTimeline(TrialSafetyBase):
    events: list[TrialAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrialSafetyStatus(TrialSafetyBase):
    safety_items: list[str] = Field(default_factory=list)
    safety_item_count: int = 0
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)

