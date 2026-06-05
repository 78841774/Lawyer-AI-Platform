from pydantic import BaseModel, Field


class PersonalProductionStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_production_runtime_showcase_foundation"
    version: str = "v7.0"
    personal_production_phase: bool = True
    showcase_ready: bool = True
    production_validation_ready: bool = False
    external_client_delivery_ready: bool = False
    team_workspace_enabled: bool = False
    real_provider_call_enabled: bool = False
    ai_runtime_registered: bool = True
    ai_gateway_registered: bool = True
    material_parsing_runtime_registered: bool = True
    ocr_runtime_registered: bool = True
    legal_search_runtime_registered: bool = True
    skill_training_runtime_registered: bool = True
    delivery_runtime_registered: bool = True
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    lawyer_review_required: bool = True
    manual_final_lock_required: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionMode(BaseModel):
    personal_production_mode: str = "controlled_ready"
    personal_production_enabled: bool = False
    real_provider_enabled: bool = False
    external_delivery_enabled: bool = False
    team_workspace_enabled: bool = False
    showcase_mode_enabled: bool = True
    developer_diagnostics_enabled: bool = True
    lawyer_review_required: bool = True
    manual_final_lock_required: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionShowcase(BaseModel):
    showcase_mode_enabled: bool = True
    showcase_safe: bool = True
    public_demo_safe: bool = True
    developer_diagnostics_collapsed: bool = True
    raw_content_visible: bool = False
    internal_paths_visible: bool = False
    provider_secrets_visible: bool = False
    headline: str = "AIHome.law Personal Production Console"
    subheadline: str = "Controlled AI-assisted legal workflow for personal production validation."
    trust_badges: list[str] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionRuntimeItem(BaseModel):
    runtime_id: str
    label: str
    category: str
    mode: str = "registered_mock_first"
    enabled: bool = True
    live_enabled: bool = False
    mock_available: bool = True
    controlled_available: bool = True
    production_ready: bool = False
    provider_configured: bool = False
    gateway_registered: bool = False
    manual_approval_required: bool = True
    lawyer_review_required: bool = True
    status: str = "registered_not_live"
    target_route: str = "/personal-production"
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionRuntimeRegistry(BaseModel):
    runtimes: list[PersonalProductionRuntimeItem] = Field(default_factory=list)
    registered_runtime_count: int = 0
    live_runtime_count: int = 0
    controlled_runtime_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionProviderCapability(BaseModel):
    provider_id: str
    label: str
    category: str
    configured: bool = False
    live_enabled: bool = False
    mock_supported: bool = True
    controlled_live_supported: bool = True
    requires_api_key: bool = True
    api_key_present: bool = False
    api_key_visible: bool = False
    status: str = "placeholder_not_configured"
    next_action: str
    target_route: str = "/personal-production"
    gateway_registered: bool = False


class PersonalProductionProviderCapabilities(BaseModel):
    providers: list[PersonalProductionProviderCapability] = Field(default_factory=list)
    provider_count: int = 0
    configured_provider_count: int = 0
    live_provider_count: int = 0
    provider_secrets_visible: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionReadiness(BaseModel):
    personal_production_ready: bool = False
    showcase_ready: bool = True
    readiness: dict[str, bool] = Field(default_factory=dict)
    missing_requirements: list[str] = Field(default_factory=list)
    next_action: str = "continue_to_v7_3_legal_enterprise_intelligence_gateway"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionSafety(BaseModel):
    safety: dict[str, bool] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalProductionConsoleSummary(BaseModel):
    title: str = "AIHome.law Personal Production Console"
    phase: str = "Personal Production & Showcase Foundation"
    version: str = "v7.0"
    showcase_ready: bool = True
    personal_production_ready: bool = False
    external_client_delivery_ready: bool = False
    team_workspace_enabled: bool = False
    next_steps: list[str] = Field(default_factory=list)
    runtime_summary: dict[str, int] = Field(default_factory=dict)
    trust_summary: dict[str, bool] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)
