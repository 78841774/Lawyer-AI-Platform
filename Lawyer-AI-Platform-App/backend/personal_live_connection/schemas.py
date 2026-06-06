from typing import Any

from pydantic import BaseModel, Field


class LiveConnectionSafetyBase(BaseModel):
    owner_only: bool = True
    lawyer_gated: bool = True
    metadata_only: bool = True
    draft_only: bool = True
    dry_run: bool = True
    provider_gated: bool = True
    live_default_enabled: bool = False
    live_call_allowed: bool = False
    live_call_executed: bool = False
    network_call_executed: bool = False
    api_key_exposed: bool = False
    secret_value_returned: bool = False
    secret_logged: bool = False
    frontend_key_input_enabled: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    raw_provider_response_exposed: bool = False
    local_path_exposed: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    audit_required: bool = True
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    real_pdf_generated: bool = False
    real_docx_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class LiveConnectionProvider(LiveConnectionSafetyBase):
    provider_id: str
    display_name: str
    provider_category: str
    provider_type: str
    key_env_name: str | None = None
    key_loaded: bool = False
    key_source: str = "unavailable"
    key_required: bool = True
    dry_run_ready: bool = True
    live_supported: bool = True
    provider_live_enabled: bool = False
    adapter_registered: bool = False
    health_status: str = "dry_run_ready_live_blocked"
    usage_meter_supported: bool = True
    cost_metadata_supported: bool = True
    status: str = "registered_live_blocked"
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionProviderList(LiveConnectionSafetyBase):
    providers: list[LiveConnectionProvider] = Field(default_factory=list)
    provider_count: int = 0
    category_count: int = 0
    dry_run_ready_count: int = 0
    key_loaded_count: int = 0
    live_disabled_count: int = 0
    blocked_provider_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionRuntime(BaseModel):
    runtime_id: str
    label: str
    category: str
    target_route: str
    status: str = "dry_run_ready_live_blocked"
    enabled: bool = True
    dry_run_ready: bool = True
    live_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionRuntimeList(LiveConnectionSafetyBase):
    runtimes: list[LiveConnectionRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionStatus(LiveConnectionSafetyBase):
    enabled: bool = True
    version: str = "v7.28"
    runtime_label: str = "个人生产受控接口接入"
    provider_count: int = 0
    dry_run_ready_count: int = 0
    key_loaded_count: int = 0
    live_disabled_count: int = 0
    live_connection_ready: bool = True
    quality_metadata_ready: bool = True
    usage_cost_metadata_ready: bool = True
    health_check_ready: bool = True
    audit_ready: bool = True
    safety_ready: bool = True
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionSecretBoundary(LiveConnectionSafetyBase):
    provider_id: str
    key_env_name: str | None = None
    key_loaded: bool = False
    key_source: str = "unavailable"
    key_required: bool = True
    key_value_exposed: bool = False
    key_prefix_returned: bool = False
    key_suffix_returned: bool = False
    masked_key_returned: bool = False
    token_value_returned: bool = False
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionLiveGate(LiveConnectionSafetyBase):
    gate_id: str
    provider_id: str
    global_live_enabled: bool = False
    provider_live_enabled: bool = False
    key_loaded: bool = False
    manual_confirmation_received: bool = False
    owner_confirmation_received: bool = False
    lawyer_gate_acknowledged: bool = False
    raw_content_boundary_acknowledged: bool = False
    live_gate_status: str = "blocked_by_default"
    live_blocked_reason: str = "global_live_disabled"
    next_required_confirmation: str = "manual_live_confirmation"
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionUsagePolicy(LiveConnectionSafetyBase):
    provider_id: str
    estimated_token_count: int = 0
    estimated_page_count: int = 0
    estimated_query_count: int = 0
    estimated_call_count: int = 1
    estimated_cost_available: bool = False
    actual_cost_recorded: bool = False
    billable_call_executed: bool = False
    usage_recorded_as_metadata_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionHealthDryRun(LiveConnectionSafetyBase):
    provider_id: str
    config_detected: bool = True
    key_loaded: bool = False
    adapter_registered: bool = False
    dry_run_ready: bool = True
    health_status: str = "dry_run_ready_live_blocked"
    network_call_executed: bool = False
    upload_executed: bool = False
    live_blocked_reason: str = "global_live_disabled"
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionRunRequest(BaseModel):
    provider_id: str
    run_type: str = "ai_draft"
    case_id: str = "case_v55_approve_all"
    material_id: str | None = None
    query_purpose: str = "controlled_live_connection_readiness"
    dry_run: bool = True
    manual_confirmation: bool = False
    owner_confirmation: bool = False
    lawyer_gate_acknowledged: bool = False
    source_trace_acknowledged: bool = False
    raw_content_boundary_acknowledged: bool = False
    draft_only_acknowledged: bool = False


class LiveConnectionRunRecord(LiveConnectionSafetyBase):
    run_id: str
    provider_id: str
    provider_category: str
    run_type: str
    case_id: str
    material_id: str | None = None
    status: str = "dry_run_completed"
    dry_run: bool = True
    live_call_requested: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    quality_score: int = 82
    quality_reference_only: bool = True
    usage_metadata: dict[str, Any] = Field(default_factory=dict)
    cost_metadata: dict[str, Any] = Field(default_factory=dict)
    health_metadata: dict[str, Any] = Field(default_factory=dict)
    source_trace_ids: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionRunActionRequest(BaseModel):
    action: str = "confirm_for_lawyer_review"
    owner_confirmation: bool = False
    lawyer_gate_acknowledged: bool = False
    source_trace_acknowledged: bool = False


class LiveConnectionRunActionResult(LiveConnectionSafetyBase):
    run_id: str
    action: str
    status: str = "action_recorded"
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionRunList(LiveConnectionSafetyBase):
    runs: list[LiveConnectionRunRecord] = Field(default_factory=list)
    run_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionAuditEvent(LiveConnectionSafetyBase):
    event_id: str
    provider_id: str
    action: str
    run_id: str | None = None
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionAuditTimeline(LiveConnectionSafetyBase):
    events: list[LiveConnectionAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LiveConnectionSafetyStatus(LiveConnectionSafetyBase):
    safety_items: list[str] = Field(default_factory=list)
    safety_item_count: int = 0
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)
