from pydantic import BaseModel, Field


class PersonalIntelligenceStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_intelligence_gateway"
    version: str = "v7.3"
    mock_first_enabled: bool = True
    provider_gated: bool = True
    legal_search_runtime_enabled: bool = True
    enterprise_intelligence_runtime_enabled: bool = True
    source_trace_enabled: bool = True
    confirmation_queue_enabled: bool = True
    live_provider_call_enabled: bool = False
    requires_lawyer_confirmation: bool = True
    source_trace_required: bool = True
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceProvider(BaseModel):
    provider_id: str
    label: str
    display_name: str
    category: str
    provider_type: str
    capabilities: list[str] = Field(default_factory=list)
    enabled: bool = False
    configured: bool = False
    live_enabled: bool = False
    mock_available: bool = True
    provider_gated: bool = True
    api_key_required_for_live: bool = True
    api_key_present: bool = False
    api_key_visible: bool = False
    live_call_executed: bool = False
    status: str = "placeholder_not_configured"
    target_version: str = "v7.3"
    target_route: str = "/personal-intelligence"
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceProviderList(BaseModel):
    providers: list[PersonalIntelligenceProvider] = Field(default_factory=list)
    provider_count: int = 0
    configured_provider_count: int = 0
    live_provider_count: int = 0
    provider_credentials_visible: bool = False
    mock_metadata_only: bool = True
    raw_external_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalLegalSearchMockRequest(BaseModel):
    case_id: str
    query: str
    search_scope: str
    jurisdiction: str
    legal_area: str
    provider_id: str
    explicit_mock_confirmation: bool = False
    explicit_no_live_call_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PersonalEnterpriseQueryMockRequest(BaseModel):
    case_id: str
    company_name: str
    unified_social_credit_code: str | None = None
    query_scope: str
    provider_id: str
    explicit_mock_confirmation: bool = False
    explicit_no_live_call_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PersonalIntelligenceSourceTrace(BaseModel):
    source_trace_id: str
    source_type: str
    provider_id: str
    external_source_label: str
    source_category: str
    query_id: str
    citation_status: str = "pending_confirmation"
    lawyer_confirmed: bool = False
    mock_or_placeholder_only: bool = True
    raw_content_stored: bool = False
    raw_content_returned: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    created_at: str
    updated_at: str | None = None


class PersonalIntelligenceSourceTraceList(BaseModel):
    source_traces: list[PersonalIntelligenceSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    pending_confirmation_count: int = 0
    mock_metadata_only: bool = True
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalLegalSearchResult(BaseModel):
    legal_search_id: str
    case_id: str
    provider_id: str
    query_summary: str
    search_scope: str
    jurisdiction: str
    legal_area: str
    result_count: int = 0
    mock_results: list[dict[str, str | int | float | bool]] = Field(default_factory=list)
    citation_candidates: list[dict[str, str | bool]] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    requires_lawyer_confirmation: bool = True
    source_trace_required: bool = True
    live_call_executed: bool = False
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalLegalSearchList(BaseModel):
    legal_search: list[PersonalLegalSearchResult] = Field(default_factory=list)
    result_count: int = 0
    mock_metadata_only: bool = True
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalEnterpriseQueryResult(BaseModel):
    enterprise_query_id: str
    case_id: str
    provider_id: str
    company_match_summary: str
    risk_signal_summary: str
    query_scope: str
    mock_results: list[dict[str, str | int | float | bool]] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    requires_lawyer_confirmation: bool = True
    source_trace_required: bool = True
    live_call_executed: bool = False
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalEnterpriseQueryList(BaseModel):
    enterprise_query: list[PersonalEnterpriseQueryResult] = Field(default_factory=list)
    result_count: int = 0
    mock_metadata_only: bool = True
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceConfirmationActionRequest(BaseModel):
    action: str
    reviewer_id: str
    reviewer_note: str | None = None
    explicit_lawyer_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PersonalIntelligenceConfirmationActionResult(BaseModel):
    source_trace_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    status: str = "confirmation_action_recorded"
    citation_status: str
    lawyer_confirmed: bool = False
    live_call_executed: bool = False
    raw_content_returned: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceAuditEvent(BaseModel):
    audit_id: str
    action: str
    actor: str
    provider_id: str
    query_id: str
    source_trace_id: str | None = None
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    no_live_call: bool = True
    no_raw_external_content: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False


class PersonalIntelligenceAuditTimeline(BaseModel):
    events: list[PersonalIntelligenceAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_metadata_only: bool = True
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceSafetyStatus(BaseModel):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_metadata_only: bool = True
    raw_external_content_included: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveProviderConfig(BaseModel):
    provider_id: str
    display_name: str
    provider_type: str
    live_supported: bool = True
    live_enabled: bool = False
    key_required: bool = True
    key_loaded: bool = False
    key_source: str = "unavailable"
    supported_query_types: list[str] = Field(default_factory=list)
    max_query_size: int = 500
    supports_case_search: bool = False
    supports_law_search: bool = False
    supports_company_profile: bool = False
    supports_company_risk: bool = False
    supports_citation_metadata: bool = True
    timeout_seconds: int = 30
    safety_notes: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveProviderConfigList(BaseModel):
    providers: list[PersonalIntelligenceLiveProviderConfig] = Field(default_factory=list)
    provider_count: int = 0
    live_provider_count: int = 0
    key_loaded_count: int = 0
    provider_credentials_visible: bool = False
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    citation_finalized: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveGatewayStatus(BaseModel):
    enabled: bool = True
    mode: str = "legal_enterprise_api_live_gateway"
    version: str = "v7.14"
    legal_live_mode_enabled: bool = False
    enterprise_live_mode_enabled: bool = False
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    legal_dry_run_ready: bool = True
    enterprise_dry_run_ready: bool = True
    live_call_requires_confirmation: bool = True
    provider_gated: bool = True
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveRunRequest(BaseModel):
    provider_id: str
    query_text: str = "示例查询"
    query_type: str = "case_law_search"
    case_id: str = "case_v55_approve_all"
    jurisdiction: str = "中国大陆"
    actor_id: str = "local_demo_lawyer"
    dry_run: bool = True
    explicit_live_confirmation: bool = False
    query_owner_confirmation: bool = False
    raw_content_handling_acknowledged: bool = False
    no_ai_prompt_injection_acknowledged: bool = False
    lawyer_review_acknowledged: bool = False
    draft_only_acknowledged: bool = False
    no_final_citation_acknowledged: bool = False


class PersonalIntelligenceLiveMetadataPreview(BaseModel):
    query_id: str
    query_text_redacted: str
    query_type: str
    provider_id: str
    provider_type: str
    jurisdiction: str = "中国大陆"
    result_count_estimate: int = 0
    citation_candidate_count: int = 0
    enterprise_candidate_count: int = 0
    confidence_summary: str = "metadata_only"
    source_trace_ids: list[str] = Field(default_factory=list)
    review_required: bool = True
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    citation_finalized: bool = False


class PersonalIntelligenceLiveRunRecord(BaseModel):
    run_id: str
    run_type: str
    provider_id: str
    provider_type: str
    query_type: str
    status: str = "dry_run_completed"
    dry_run: bool = True
    would_call_provider: bool = False
    live_mode_enabled: bool = False
    live_call_requested: bool = False
    live_call_executed: bool = False
    blocked_reason: str | None = None
    blocked_reasons: list[str] = Field(default_factory=list)
    provider_adapter_unavailable: bool = False
    query_metadata_only: bool = True
    citation_metadata_only: bool = True
    metadata_preview: PersonalIntelligenceLiveMetadataPreview
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    source_trace_created: bool = False
    review_required: bool = True
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveRunList(BaseModel):
    runs: list[PersonalIntelligenceLiveRunRecord] = Field(default_factory=list)
    run_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveReviewItem(BaseModel):
    review_item_id: str
    run_id: str
    run_type: str
    provider_id: str
    provider_type: str
    query_type: str
    review_status: str = "pending_review"
    confidence_summary: str = "metadata_only"
    citation_candidate: bool = False
    enterprise_candidate: bool = False
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    citation_finalized: bool = False
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveReviewQueue(BaseModel):
    items: list[PersonalIntelligenceLiveReviewItem] = Field(default_factory=list)
    item_count: int = 0
    pending_review_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveReviewActionRequest(BaseModel):
    action: str
    actor_id: str = "local_demo_lawyer"
    explicit_review_confirmation: bool = False
    raw_content_handling_acknowledged: bool = False
    no_ai_prompt_injection_acknowledged: bool = False
    no_final_citation_acknowledged: bool = False


class PersonalIntelligenceLiveReviewActionResult(BaseModel):
    review_item_id: str
    action: str
    actor_id: str = "redacted_actor"
    status: str = "review_action_recorded"
    review_status: str = "pending_review"
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveSourceTrace(BaseModel):
    source_trace_id: str
    provider_id: str
    provider_type: str
    query_id: str
    query_type: str
    source_title: str
    source_type: str
    source_reference: str
    citation_candidate: bool = False
    enterprise_candidate: bool = False
    lawyer_confirmed: bool = False
    raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    created_at: str


class PersonalIntelligenceLiveSourceTraceList(BaseModel):
    source_traces: list[PersonalIntelligenceLiveSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    citation_finalized: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveAuditEvent(BaseModel):
    event_id: str
    provider_id: str
    action: str
    actor_id: str = "redacted_actor"
    query_type: str
    run_id: str | None = None
    review_item_id: str | None = None
    live_call_requested: bool = False
    live_call_executed: bool = False
    blocked_reason: str | None = None
    raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    source_trace_created: bool = False
    review_required: bool = True
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    created_at: str


class PersonalIntelligenceLiveAuditTimeline(BaseModel):
    events: list[PersonalIntelligenceLiveAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalIntelligenceLiveSafetyStatus(BaseModel):
    safety: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    legal_raw_content_exposed: bool = False
    enterprise_raw_content_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    citation_finalized: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)
