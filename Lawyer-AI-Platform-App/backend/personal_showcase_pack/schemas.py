from pydantic import BaseModel, Field


class PersonalShowcasePackStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_showcase_pack"
    version: str = "v7.7"
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    showcase_pack_runtime_enabled: bool = True
    pilot_sample_runtime_enabled: bool = True
    story_flow_runtime_enabled: bool = True
    showcase_metrics_runtime_enabled: bool = True
    trust_panel_runtime_enabled: bool = True
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ShowcaseRuntime(BaseModel):
    runtime_id: str
    display_name: str
    runtime_type: str
    capabilities: list[str] = Field(default_factory=list)
    enabled: bool = True
    live_enabled: bool = False
    mock_available: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_lock_required: bool = True
    auto_delivery_enabled: bool = False
    warning: str = "当前仅为试点展示和 mock metadata，不会自动生成最终法律意见或对外交付。"


class ShowcaseRuntimeList(BaseModel):
    runtimes: list[ShowcaseRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    live_runtime_count: int = 0
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PilotSampleMockRequest(BaseModel):
    sample_title: str
    sample_type: str
    legal_area: str
    case_cause: str
    risk_level: str
    demo_persona: str
    linked_runtime_ids: list[str] = Field(default_factory=list)
    explicit_mock_confirmation: bool = False
    explicit_no_real_case_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class WorkflowProgress(BaseModel):
    completed_stage_count: int = 0
    total_stage_count: int = 7
    progress_percent: int = 0
    current_stage: str = "case_intake"


class PilotSampleRecord(BaseModel):
    pilot_sample_id: str
    sample_title: str
    sample_type: str
    legal_area: str
    case_cause: str
    risk_level: str
    demo_persona: str
    linked_runtime_ids: list[str] = Field(default_factory=list)
    sample_status: str = "draft"
    workflow_progress: WorkflowProgress = Field(default_factory=WorkflowProgress)
    readiness_status: str = "mock_ready"
    review_status: str = "lawyer_review_required"
    final_lock_status: str = "not_locked"
    source_trace_coverage: int = 100
    mock_or_placeholder_only: bool = True
    synthetic_demo_data_only: bool = True
    synthetic_demo_only: bool = True
    real_case_data_included: bool = False
    raw_content_included: bool = False
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PilotSampleList(BaseModel):
    pilot_samples: list[PilotSampleRecord] = Field(default_factory=list)
    sample_count: int = 0
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class StoryFlowMockRequest(BaseModel):
    pilot_sample_id: str
    story_title: str
    story_scope: str
    selected_stage_ids: list[str] = Field(default_factory=list)
    explicit_mock_confirmation: bool = False
    explicit_no_real_case_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class StoryStageCard(BaseModel):
    stage_id: str
    display_name: str
    status: str = "mock_metadata_ready"
    linked_runtime: str
    mock_metadata_summary: str
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    final_output_generated: bool = False


class StoryFlowRecord(BaseModel):
    story_flow_id: str
    pilot_sample_id: str
    story_title: str
    story_scope: str
    selected_stage_ids: list[str] = Field(default_factory=list)
    story_status: str = "draft"
    stage_cards: list[StoryStageCard] = Field(default_factory=list)
    source_trace_summary: dict[str, bool | int | str] = Field(default_factory=dict)
    lawyer_review_summary: dict[str, bool | str] = Field(default_factory=dict)
    final_lock_summary: dict[str, bool | str] = Field(default_factory=dict)
    trust_summary: dict[str, bool] = Field(default_factory=dict)
    mock_or_placeholder_only: bool = True
    synthetic_demo_data_only: bool = True
    synthetic_demo_only: bool = True
    real_case_data_included: bool = False
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    source_trace_required: bool = True
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class StoryFlowList(BaseModel):
    story_flows: list[StoryFlowRecord] = Field(default_factory=list)
    story_flow_count: int = 0
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ShowcaseMetrics(BaseModel):
    pilot_sample_count: int = 0
    story_flow_count: int = 0
    source_trace_coverage_rate: int = 0
    lawyer_review_required_count: int = 0
    final_lock_ready_count: int = 0
    external_delivery_count: int = 0
    final_legal_opinion_count: int = 0
    final_report_count: int = 0
    real_provider_call_count: int = 0
    synthetic_demo_only: bool = True
    mock_metadata_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class TrustPanel(BaseModel):
    trust_items: list[str] = Field(default_factory=list)
    flags: dict[str, bool] = Field(default_factory=dict)
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    source_trace_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class ShowcaseAuditEvent(BaseModel):
    audit_id: str
    action: str
    actor: str
    object_type: str
    object_id: str
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    no_raw_content: bool = True
    no_real_case_data: bool = True
    no_live_provider_call: bool = True
    no_final_opinion: bool = True
    no_final_report: bool = True
    no_external_delivery: bool = True
    no_email_sent: bool = True


class ShowcaseAuditTimeline(BaseModel):
    events: list[ShowcaseAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ShowcaseSafetyStatus(BaseModel):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_metadata_only: bool = True
    synthetic_demo_only: bool = True
    real_provider_called: bool = False
    api_key_accessed: bool = False
    real_case_data_included: bool = False
    raw_content_included: bool = False
    raw_content_returned: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    final_file_generated: bool = False
    requires_lawyer_review: bool = True
    final_lock_required: bool = True
    source_trace_required: bool = True
    warnings: list[str] = Field(default_factory=list)
