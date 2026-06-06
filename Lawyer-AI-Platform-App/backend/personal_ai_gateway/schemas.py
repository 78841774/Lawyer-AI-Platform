from typing import Any

from pydantic import BaseModel, Field


class PersonalAIGatewayStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_ai_gateway_prompt_runtime"
    version: str = "v7.1"
    mock_first_enabled: bool = True
    controlled_live_supported: bool = True
    live_provider_call_enabled: bool = False
    provider_gateway_enabled: bool = True
    prompt_registry_enabled: bool = True
    prompt_render_preview_enabled: bool = True
    mock_ai_run_enabled: bool = True
    manual_approval_required: bool = True
    lawyer_review_required: bool = True
    draft_only: bool = True
    source_trace_required: bool = True
    external_delivery_enabled: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAIProvider(BaseModel):
    provider_id: str
    label: str
    category: str = "ai_model"
    configured: bool = False
    live_enabled: bool = False
    mock_supported: bool = True
    controlled_live_supported: bool = True
    requires_api_key: bool = True
    api_key_present: bool = False
    api_key_visible: bool = False
    status: str = "placeholder_not_configured"
    target_route: str = "/personal-ai-gateway"
    warnings: list[str] = Field(default_factory=list)


class PersonalAIProviderList(BaseModel):
    providers: list[PersonalAIProvider] = Field(default_factory=list)
    provider_count: int = 0
    configured_provider_count: int = 0
    live_provider_count: int = 0
    provider_secrets_visible: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAIPromptTemplate(BaseModel):
    template_id: str
    name: str
    purpose: str
    case_type: str
    input_schema: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] = Field(default_factory=dict)
    draft_only: bool = True
    requires_lawyer_review: bool = True
    source_trace_required: bool = True
    allowed_provider_categories: list[str] = Field(default_factory=lambda: ["ai_model"])
    version: str = "v7.1"
    enabled: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAIPromptTemplateList(BaseModel):
    templates: list[PersonalAIPromptTemplate] = Field(default_factory=list)
    template_count: int = 0
    enabled_template_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAIPromptRenderPreviewRequest(BaseModel):
    template_id: str
    case_id: str | None = None
    variables: dict[str, Any] = Field(default_factory=dict)
    manual_review_confirmed: bool = False
    mock_data_only_confirmation: bool = False
    no_raw_content_confirmation: bool = False


class PersonalAIPromptRenderPreviewResult(BaseModel):
    template_id: str
    case_id: str | None = None
    status: str = "preview_rendered"
    rendered_prompt_preview: str = ""
    would_call_provider: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    requires_lawyer_review: bool = True
    draft_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalAITokenUsage(BaseModel):
    estimated_input_tokens: int = 0
    estimated_output_tokens: int = 0
    estimated_total_tokens: int = 0
    actual_input_tokens: int | None = None
    actual_output_tokens: int | None = None
    actual_total_tokens: int | None = None
    live_usage_available: bool = False


class PersonalAIDraftOutput(BaseModel):
    title: str
    content: str
    draft_only: bool = True
    requires_lawyer_review: bool = True
    source_trace_required: bool = True


class PersonalAIMockRunRequest(BaseModel):
    provider_id: str
    template_id: str
    case_id: str | None = None
    manual_approval_confirmed: bool = False
    lawyer_review_required_confirmation: bool = False
    draft_only_confirmation: bool = False
    source_trace_required_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False


class PersonalAIMockRunResult(BaseModel):
    ai_run_id: str | None = None
    provider_id: str
    template_id: str
    case_id: str | None = None
    mode: str = "mock"
    status: str = "mock_ai_run_created"
    would_call_provider: bool = False
    live_call_executed: bool = False
    draft_output: PersonalAIDraftOutput | None = None
    token_usage: PersonalAITokenUsage = Field(default_factory=PersonalAITokenUsage)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalAIRunRecord(BaseModel):
    ai_run_id: str
    provider_id: str
    template_id: str
    case_id: str | None = None
    purpose: str
    mode: str = "mock"
    status: str = "mock_ai_run_created"
    would_call_provider: bool = False
    live_call_executed: bool = False
    manual_approval_confirmed: bool = True
    draft_only: bool = True
    requires_lawyer_review: bool = True
    source_trace_required: bool = True
    token_usage: PersonalAITokenUsage = Field(default_factory=PersonalAITokenUsage)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalAIRunList(BaseModel):
    runs: list[PersonalAIRunRecord] = Field(default_factory=list)
    run_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAIAuditEvent(BaseModel):
    ai_run_id: str
    provider_id: str
    template_id: str
    case_id: str | None = None
    purpose: str
    mode: str = "mock"
    would_call_provider: bool = False
    live_call_executed: bool = False
    manual_approval_confirmed: bool = True
    draft_only: bool = True
    requires_lawyer_review: bool = True
    token_usage_estimate: dict[str, int] = Field(default_factory=dict)
    created_at: str
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False


class PersonalAIAuditTimeline(BaseModel):
    events: list[PersonalAIAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAITokenUsageSummary(BaseModel):
    run_count: int = 0
    estimated_total_tokens: int = 0
    actual_total_tokens: int | None = None
    live_usage_available: bool = False
    provider_usage_breakdown: dict[str, int] = Field(default_factory=dict)
    template_usage_breakdown: dict[str, int] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAISafetyStatus(BaseModel):
    safety: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAILiveProviderConfig(BaseModel):
    provider_id: str
    display_name: str
    provider_type: str = "ai_model"
    live_supported: bool = True
    live_enabled: bool = False
    key_required: bool = True
    key_loaded: bool = False
    key_source: str = "unavailable"
    model_options: list[str] = Field(default_factory=list)
    timeout_seconds: int = 30
    safety_notes: list[str] = Field(default_factory=list)
    api_key_exposed: bool = False


class PersonalAILiveProviderConfigList(BaseModel):
    providers: list[PersonalAILiveProviderConfig] = Field(default_factory=list)
    provider_count: int = 0
    live_provider_count: int = 0
    key_loaded_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAILiveGatewayStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_ai_provider_live_gateway"
    version: str = "v7.12"
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    dry_run_enabled: bool = True
    provider_count: int = 0
    live_provider_count: int = 0
    key_loaded_count: int = 0
    explicit_live_confirmation_required: bool = True
    lawyer_review_acknowledged_required: bool = True
    draft_only_acknowledged_required: bool = True
    no_final_opinion_acknowledged_required: bool = True
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAILiveRunRequest(BaseModel):
    provider_id: str
    model: str | None = None
    prompt_template_id: str
    prompt_purpose: str
    case_id: str | None = None
    source_trace_ids: list[str] = Field(default_factory=list)
    dry_run: bool = True
    actor_id: str = "local_demo_lawyer"
    explicit_live_confirmation: bool = False
    lawyer_review_acknowledged: bool = False
    draft_only_acknowledged: bool = False
    no_final_opinion_acknowledged: bool = False
    no_final_report_acknowledged: bool = False
    no_external_delivery_acknowledged: bool = False
    raw_content_included: bool = False
    final_legal_opinion_requested: bool = False
    final_report_requested: bool = False


class PersonalAILiveDraftMetadata(BaseModel):
    ai_draft: str = "AI draft metadata placeholder"
    draft_type: str = "controlled_ai_draft"
    provider_id: str
    model: str
    token_usage: dict[str, int | None] = Field(default_factory=dict)
    latency_ms: int | None = None
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False


class PersonalAILiveRunRecord(BaseModel):
    run_id: str
    provider_id: str
    model: str
    prompt_template_id: str
    prompt_purpose: str
    case_id: str | None = None
    source_trace_ids: list[str] = Field(default_factory=list)
    status: str = "dry_run_completed"
    dry_run: bool = True
    would_call_provider: bool = False
    live_call_requested: bool = False
    live_call_executed: bool = False
    blocked_reason: str | None = None
    confirmations: dict[str, bool] = Field(default_factory=dict)
    draft_output_metadata: PersonalAILiveDraftMetadata | None = None
    created_at: str
    live_mode_enabled: bool = False
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAILiveRunList(BaseModel):
    runs: list[PersonalAILiveRunRecord] = Field(default_factory=list)
    run_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAILiveAuditEvent(BaseModel):
    event_id: str
    provider_id: str
    action: str
    actor_id: str
    live_call_requested: bool = False
    live_call_executed: bool = False
    blocked_reason: str | None = None
    confirmations: dict[str, bool] = Field(default_factory=dict)
    token_usage: dict[str, int | None] = Field(default_factory=dict)
    created_at: str
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False


class PersonalAILiveAuditTimeline(BaseModel):
    events: list[PersonalAILiveAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAILiveSafetyStatus(BaseModel):
    safety: dict[str, bool] = Field(default_factory=dict)
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_included: bool = False
    draft_only: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)
