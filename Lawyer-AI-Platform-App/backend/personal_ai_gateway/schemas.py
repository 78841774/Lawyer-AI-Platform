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
