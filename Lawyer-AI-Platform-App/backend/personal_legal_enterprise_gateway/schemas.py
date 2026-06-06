from typing import Any

from pydantic import BaseModel, Field


class LegalEnterpriseSafetyBase(BaseModel):
    metadata_only: bool = True
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
    external_transfer_triggered: bool = False
    owner_confirmation_required: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    review_required: bool = True
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    final_fact_finding: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    third_party_share_enabled: bool = False
    client_auto_delivery: bool = False
    raw_provider_response_exposed: bool = False
    local_path_exposed: bool = False


class LegalEnterpriseProvider(LegalEnterpriseSafetyBase):
    provider_id: str
    provider_name: str
    provider_category: str
    provider_subtype: str
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
    status: str = "registered_live_blocked"
    warnings: list[str] = Field(default_factory=list)


class LegalEnterpriseProviderList(LegalEnterpriseSafetyBase):
    providers: list[LegalEnterpriseProvider] = Field(default_factory=list)
    provider_count: int = 0
    key_loaded_count: int = 0
    dry_run_ready_count: int = 0
    live_disabled_count: int = 0
    blocked_provider_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LegalEnterpriseCategorySummary(LegalEnterpriseSafetyBase):
    category: str
    provider_count: int = 0
    key_loaded_count: int = 0
    dry_run_ready_count: int = 0
    live_disabled_count: int = 0
    blocked_provider_count: int = 0


class LegalEnterpriseCategorySummaryList(LegalEnterpriseSafetyBase):
    categories: list[LegalEnterpriseCategorySummary] = Field(default_factory=list)
    category_count: int = 0


class LegalEnterpriseStatus(LegalEnterpriseSafetyBase):
    enabled: bool = True
    version: str = "v7.29"
    runtime_label: str = "法律检索与企业信息 API 受控接入"
    legal_gateway_ready: bool = True
    enterprise_gateway_ready: bool = True
    legal_source_trace_ready: bool = True
    enterprise_verification_ready: bool = True
    provider_count: int = 0
    legal_provider_count: int = 0
    enterprise_provider_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SecretBoundaryStatus(LegalEnterpriseSafetyBase):
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
    warnings: list[str] = Field(default_factory=list)


class LiveGateMockRequest(BaseModel):
    provider_id: str
    dry_run: bool = True
    explicit_live_confirmation: bool = False
    owner_authorized: bool = False
    lawyer_review_acknowledged: bool = False
    external_transfer_acknowledged: bool = False
    source_trace_acknowledged: bool = False
    no_training_use_acknowledged: bool = False
    audit_acknowledged: bool = False


class LiveGateStatus(LegalEnterpriseSafetyBase):
    gate_id: str
    provider_id: str
    global_live_enabled: bool = False
    provider_live_enabled: bool = False
    key_loaded: bool = False
    explicit_live_confirmation: bool = False
    owner_authorized: bool = False
    lawyer_review_acknowledged: bool = False
    external_transfer_acknowledged: bool = False
    source_trace_acknowledged: bool = False
    no_training_use_acknowledged: bool = False
    audit_acknowledged: bool = False
    live_gate_status: str = "blocked_by_default"
    live_blocked_reason: str = "global_live_disabled"
    next_required_confirmation: str = "explicit_live_confirmation"
    warnings: list[str] = Field(default_factory=list)


class LiveGateList(LegalEnterpriseSafetyBase):
    live_gates: list[LiveGateStatus] = Field(default_factory=list)
    live_gate_count: int = 0


class UsagePolicy(LegalEnterpriseSafetyBase):
    provider_id: str
    usage_meter_enabled: bool = False
    estimated_query_count: int = 1
    estimated_call_count: int = 1
    estimated_result_count: int = 3
    estimated_cost_available: bool = False
    actual_cost_recorded: bool = False
    billable_call_executed: bool = False
    usage_recorded_as_metadata_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class HealthDryRun(LegalEnterpriseSafetyBase):
    provider_id: str
    config_detected: bool = True
    key_loaded: bool = False
    live_gate_status: str = "blocked_by_default"
    adapter_registered: bool = False
    dry_run_ready: bool = True
    network_call_executed: bool = False
    live_blocked_reason: str = "global_live_disabled"
    next_required_confirmation: str = "explicit_live_confirmation"
    warnings: list[str] = Field(default_factory=list)


class LegalSearchRequest(BaseModel):
    provider_id: str = "legal_search_placeholder"
    query_type: str = "statute_search"
    query_text_metadata: str = "合同违约责任争议焦点 metadata"
    case_id: str = "case_v55_approve_all"
    dry_run: bool = True
    explicit_live_confirmation: bool = False
    owner_authorized: bool = False
    lawyer_review_acknowledged: bool = False
    source_trace_acknowledged: bool = True
    no_training_use_acknowledged: bool = True
    audit_acknowledged: bool = True


class LegalSearchRun(LegalEnterpriseSafetyBase):
    legal_query_id: str
    provider_id: str
    query_type: str
    query_text_metadata: str
    case_id: str
    status: str = "dry_run_completed"
    search_results_metadata: list[dict[str, Any]] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    final_citation_selected: bool = False
    review_status: str = "pending_lawyer_review"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class EnterpriseLookupRequest(BaseModel):
    provider_id: str = "enterprise_registry_placeholder"
    lookup_type: str = "company_registry"
    company_query_metadata: str = "企业主体核验 metadata"
    case_id: str = "case_v55_approve_all"
    dry_run: bool = True
    explicit_live_confirmation: bool = False
    owner_authorized: bool = False
    lawyer_review_acknowledged: bool = False
    source_trace_acknowledged: bool = True
    no_training_use_acknowledged: bool = True
    audit_acknowledged: bool = True


class EnterpriseLookupRun(LegalEnterpriseSafetyBase):
    enterprise_lookup_id: str
    provider_id: str
    lookup_type: str
    company_query_metadata: str
    case_id: str
    status: str = "dry_run_completed"
    enterprise_results_metadata: list[dict[str, Any]] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    verification_required: bool = True
    review_status: str = "pending_verification_review"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class RunList(LegalEnterpriseSafetyBase):
    runs: list[LegalSearchRun | EnterpriseLookupRun] = Field(default_factory=list)
    run_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ReviewItem(LegalEnterpriseSafetyBase):
    review_item_id: str
    run_id: str
    provider_id: str
    review_type: str
    review_status: str = "pending_review"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class ReviewQueue(LegalEnterpriseSafetyBase):
    items: list[ReviewItem] = Field(default_factory=list)
    item_count: int = 0
    pending_review_count: int = 0


class ReviewActionRequest(BaseModel):
    action: str = "confirm_metadata_for_review"
    owner_confirmation: bool = False
    lawyer_review_acknowledged: bool = False
    source_trace_acknowledged: bool = False


class ReviewActionResult(LegalEnterpriseSafetyBase):
    review_item_id: str
    action: str
    status: str = "action_recorded_metadata_only"
    blocked_reasons: list[str] = Field(default_factory=list)


class SourceTraceRecord(LegalEnterpriseSafetyBase):
    source_trace_id: str
    run_id: str
    provider_id: str
    source_type: str
    review_required: bool = True
    created_at: str


class SourceTraceList(LegalEnterpriseSafetyBase):
    source_traces: list[SourceTraceRecord] = Field(default_factory=list)
    source_trace_count: int = 0


class AuditEvent(LegalEnterpriseSafetyBase):
    event_id: str
    provider_id: str
    action: str
    run_id: str | None = None
    created_at: str


class AuditTimeline(LegalEnterpriseSafetyBase):
    events: list[AuditEvent] = Field(default_factory=list)
    event_count: int = 0


class SafetyStatus(LegalEnterpriseSafetyBase):
    safety_items: list[str] = Field(default_factory=list)
    safety_item_count: int = 0
    all_safety_checks_passed: bool = True

