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
    provider_secrets_visible: bool = False
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
