from pydantic import BaseModel, Field


class ProviderReadinessSafetyBase(BaseModel):
    metadata_only: bool = True
    dry_run: bool = True
    provider_gated: bool = True
    live_default_enabled: bool = False
    live_call_allowed: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    secret_value_returned: bool = False
    secret_logged: bool = False
    frontend_key_input_enabled: bool = False
    external_transfer_triggered: bool = False
    owner_confirmation_required: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class ProviderDefinition(BaseModel):
    provider_id: str
    provider_name: str
    provider_category: str
    live_supported: bool = True
    live_default_enabled: bool = False
    dry_run_supported: bool = True
    provider_gated: bool = True
    requires_api_key: bool = True
    key_env_names: list[str] = Field(default_factory=list)
    external_transfer_required: bool = True
    usage_meter_supported: bool = True
    cost_metadata_supported: bool = True
    adapter_registered: bool = False
    status: str = "registered_dry_run_only"


class ProviderMetadata(ProviderReadinessSafetyBase):
    provider_id: str
    provider_name: str
    provider_category: str
    live_supported: bool = True
    dry_run_supported: bool = True
    requires_api_key: bool = True
    key_env_names: list[str] = Field(default_factory=list)
    key_loaded: bool = False
    key_source: str = "unavailable"
    key_value_exposed: bool = False
    external_transfer_required: bool = True
    usage_meter_supported: bool = True
    cost_metadata_supported: bool = True
    adapter_registered: bool = False
    status: str = "registered_dry_run_only"
    warnings: list[str] = Field(default_factory=list)


class ProviderList(ProviderReadinessSafetyBase):
    providers: list[ProviderMetadata] = Field(default_factory=list)
    provider_count: int = 0
    key_loaded_count: int = 0
    dry_run_ready_count: int = 0
    live_disabled_count: int = 0
    blocked_provider_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CategorySummary(ProviderReadinessSafetyBase):
    category: str
    provider_count: int = 0
    key_loaded_count: int = 0
    dry_run_ready_count: int = 0
    live_disabled_count: int = 0
    blocked_provider_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CategorySummaryList(ProviderReadinessSafetyBase):
    categories: list[CategorySummary] = Field(default_factory=list)
    category_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ProviderStatus(ProviderReadinessSafetyBase):
    enabled: bool = True
    version: str = "v7.26"
    runtime_label: str = "真实接口接入准备与密钥边界"
    provider_readiness_ready: bool = True
    provider_registry_ready: bool = True
    secret_boundary_ready: bool = True
    live_gate_ready: bool = True
    usage_cost_metadata_ready: bool = True
    dry_run_health_ready: bool = True
    real_provider_calls_still_disabled: bool = True
    provider_count: int = 0
    key_loaded_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SecretBoundaryStatus(ProviderReadinessSafetyBase):
    provider_id: str
    key_env_names: list[str] = Field(default_factory=list)
    requires_api_key: bool = True
    key_loaded: bool = False
    key_source: str = "unavailable"
    key_value_exposed: bool = False
    key_prefix_returned: bool = False
    key_suffix_returned: bool = False
    masked_key_returned: bool = False
    token_value_returned: bool = False
    secret_value_stored: bool = False
    warnings: list[str] = Field(default_factory=list)


class LiveGateMockRequest(BaseModel):
    provider_id: str = "openai"
    explicit_live_confirmation: bool = False
    owner_authorized: bool = False
    external_transfer_acknowledged: bool = False
    no_training_use_acknowledged: bool = False
    audit_acknowledged: bool = False


class LiveGateStatus(ProviderReadinessSafetyBase):
    gate_id: str
    provider_id: str
    global_live_enabled: bool = False
    provider_live_enabled: bool = False
    key_loaded: bool = False
    explicit_live_confirmation: bool = False
    owner_authorized: bool = False
    external_transfer_acknowledged: bool = False
    no_training_use_acknowledged: bool = False
    audit_acknowledged: bool = False
    live_gate_status: str = "blocked_by_default"
    live_blocked_reason: str = "global_live_disabled"
    next_required_confirmation: str = "explicit_live_confirmation"
    warnings: list[str] = Field(default_factory=list)


class LiveGateList(ProviderReadinessSafetyBase):
    live_gates: list[LiveGateStatus] = Field(default_factory=list)
    live_gate_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class UsagePolicy(ProviderReadinessSafetyBase):
    provider_id: str
    usage_meter_enabled: bool = False
    estimated_token_count: int = 0
    estimated_page_count: int = 0
    estimated_document_count: int = 0
    estimated_call_count: int = 1
    estimated_cost_available: bool = False
    actual_cost_recorded: bool = False
    billable_call_executed: bool = False
    usage_recorded_as_metadata_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class ProviderHealthDryRun(ProviderReadinessSafetyBase):
    provider_id: str
    config_detected: bool = True
    key_loaded: bool = False
    live_gate_status: str = "blocked_by_default"
    adapter_registered: bool = False
    dry_run_ready: bool = True
    live_blocked_reason: str = "global_live_disabled"
    next_required_confirmation: str = "explicit_live_confirmation"
    network_call_executed: bool = False
    warnings: list[str] = Field(default_factory=list)


class ProviderAuditEvent(ProviderReadinessSafetyBase):
    event_id: str
    provider_id: str
    action: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class ProviderAuditTimeline(ProviderReadinessSafetyBase):
    events: list[ProviderAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ProviderSafetyStatus(ProviderReadinessSafetyBase):
    safety_items: list[str] = Field(default_factory=list)
    safety_item_count: int = 0
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)

