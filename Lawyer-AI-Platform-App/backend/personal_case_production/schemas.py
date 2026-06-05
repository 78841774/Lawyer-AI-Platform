from pydantic import BaseModel, Field


class PersonalCaseProductionStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_case_production"
    version: str = "v7.5"
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    workflow_registry_enabled: bool = True
    case_production_runtime_enabled: bool = True
    stage_orchestrator_enabled: bool = True
    readiness_engine_enabled: bool = True
    review_gate_enabled: bool = True
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    final_gate_required: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class WorkflowStage(BaseModel):
    stage_id: str
    display_name: str
    stage_type: str
    capabilities: list[str] = Field(default_factory=list)
    enabled: bool = True
    live_provider_required: bool = False
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_gate_required: bool = True
    auto_delivery_enabled: bool = False
    warning: str = "当前仅为受控生产流程骨架，不会自动生成最终法律意见或对外交付。"


class WorkflowStageList(BaseModel):
    workflow_stages: list[WorkflowStage] = Field(default_factory=list)
    stage_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class ProductionCaseMockRequest(BaseModel):
    case_id: str
    production_title: str
    case_type: str
    client_alias: str
    jurisdiction: str
    legal_area: str
    desensitization_status: str
    explicit_mock_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class WorkflowRunMockRequest(BaseModel):
    production_case_id: str
    workflow_scope: str
    selected_stage_ids: list[str] = Field(default_factory=list)
    explicit_mock_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class StageRunMockRequest(BaseModel):
    workflow_run_id: str
    stage_id: str
    linked_runtime_object_ids: list[str] = Field(default_factory=list)
    stage_note: str | None = None
    explicit_mock_confirmation: bool = False
    explicit_no_live_provider_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class ReviewGateActionRequest(BaseModel):
    action: str
    reviewer_id: str
    reviewer_note: str | None = None
    explicit_lawyer_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class CaseProductionSourceTrace(BaseModel):
    source_trace_id: str
    source_type: str
    source_label: str
    linked_object_type: str
    linked_object_id: str
    production_case_id: str | None = None
    workflow_run_id: str | None = None
    stage_run_id: str | None = None
    mock_or_placeholder_only: bool = True
    raw_content_stored: bool = False
    raw_content_returned: bool = False
    used_in_ai_prompt: bool = False
    created_at: str


class CaseProductionSourceTraceList(BaseModel):
    source_traces: list[CaseProductionSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class ProductionCaseRecord(BaseModel):
    production_case_id: str
    case_id: str
    production_title: str
    case_type: str
    client_alias: str
    jurisdiction: str
    legal_area: str
    desensitization_status: str
    production_status: str = "draft"
    mock_or_placeholder_only: bool = True
    raw_content_included: bool = False
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    final_gate_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class ProductionCaseList(BaseModel):
    production_cases: list[ProductionCaseRecord] = Field(default_factory=list)
    case_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class WorkflowRunRecord(BaseModel):
    workflow_run_id: str
    production_case_id: str
    workflow_scope: str
    selected_stage_ids: list[str] = Field(default_factory=list)
    workflow_status: str = "draft"
    stage_summary: dict[str, str | int | bool] = Field(default_factory=dict)
    readiness_summary: dict[str, str | int | bool] = Field(default_factory=dict)
    source_trace_ids: list[str] = Field(default_factory=list)
    requires_lawyer_review: bool = True
    final_gate_required: bool = True
    source_trace_required: bool = True
    mock_or_placeholder_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class WorkflowRunList(BaseModel):
    workflow_runs: list[WorkflowRunRecord] = Field(default_factory=list)
    run_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class StageRunRecord(BaseModel):
    stage_run_id: str
    workflow_run_id: str
    stage_id: str
    stage_status: str = "completed_mock"
    linked_runtime_object_ids: list[str] = Field(default_factory=list)
    stage_result_metadata: dict[str, str | int | bool] = Field(default_factory=dict)
    source_trace_ids: list[str] = Field(default_factory=list)
    requires_manual_review: bool = True
    requires_lawyer_review: bool = True
    final_gate_required: bool = True
    live_provider_called: bool = False
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class StageRunList(BaseModel):
    stage_runs: list[StageRunRecord] = Field(default_factory=list)
    stage_run_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class ProductionReadiness(BaseModel):
    production_case_id: str
    readiness_status: str
    completed_stage_count: int = 0
    required_stage_count: int = 7
    missing_stage_ids: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    lawyer_review_completed: bool = False
    source_trace_complete: bool = False
    final_gate_ready: bool = False
    delivery_ready: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    checklist: list[str] = Field(default_factory=list)


class ProductionReadinessList(BaseModel):
    readiness: list[ProductionReadiness] = Field(default_factory=list)
    readiness_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class ReviewGateActionResult(BaseModel):
    production_case_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    status: str = "review_gate_action_recorded"
    production_status: str
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class CaseProductionAuditEvent(BaseModel):
    audit_id: str
    action: str
    actor: str
    object_type: str
    object_id: str
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    no_raw_content: bool = True
    no_live_provider_call: bool = True
    no_final_opinion: bool = True
    no_final_report: bool = True
    no_external_delivery: bool = True


class CaseProductionAuditTimeline(BaseModel):
    events: list[CaseProductionAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class CaseProductionSafetyStatus(BaseModel):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_provider_call_executed: bool = False
    api_key_accessed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)
