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
    enterprise_intelligence_runtime_registered: bool = True
    skill_training_runtime_registered: bool = True
    skill_studio_runtime_registered: bool = True
    case_production_runtime_registered: bool = True
    controlled_case_analysis_runtime_registered: bool = True
    personal_production_pilot_runtime_registered: bool = True
    personal_owner_output_center_runtime_registered: bool = True
    personal_trial_readiness_runtime_registered: bool = True
    personal_provider_readiness_runtime_registered: bool = True
    personal_material_live_connection_runtime_registered: bool = True
    personal_live_connection_runtime_registered: bool = True
    personal_legal_enterprise_gateway_runtime_registered: bool = True
    training_artifact_loader_runtime_registered: bool = True
    codex_training_run_runtime_registered: bool = True
    real_closed_case_training_intake_runtime_registered: bool = True
    personal_delivery_packet_runtime_registered: bool = True
    personal_showcase_pack_runtime_registered: bool = True
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
    key_loaded_count: int = 0
    material_live_provider_count: int = 0
    material_key_loaded_count: int = 0
    intelligence_live_provider_count: int = 0
    intelligence_key_loaded_count: int = 0
    ai_live_gateway_status: str = "planned_gated_disabled_by_default"
    ocr_document_live_gateway_status: str = "planned_gated_disabled_by_default"
    legal_enterprise_live_gateway_status: str = "planned_gated_disabled_by_default"
    controlled_case_analysis_runtime_status: str = "planned_gated_draft_only"
    fact_skill_baseline_detected: bool = False
    legal_analysis_skill_baseline_detected: bool = False
    open_case_analysis_draft_ready: bool = True
    training_data_generation_disabled: bool = True
    skill_auto_update_disabled: bool = True
    evaluation_reference_only: bool = True
    personal_production_pilot_status: str = "ready_gated_owner_download_only"
    personal_case_workspace_status: str = "owner_only_metadata_ready"
    fact_preview_correction_workbench_status: str = "fact_preview_correction_metadata_ready"
    legal_analysis_draft_workbench_status: str = "legal_analysis_draft_metadata_ready"
    skill_final_draft_workbench_status: str = "skill_final_draft_metadata_ready"
    owner_output_center_status: str = "owner_output_center_metadata_ready"
    personal_trial_readiness_status: str = "trial_readiness_metadata_ready"
    personal_provider_readiness_status: str = "provider_readiness_metadata_ready"
    personal_material_live_connection_status: str = "ocr_document_live_connection_metadata_ready"
    personal_live_connection_status: str = "personal_live_connection_metadata_ready"
    personal_legal_enterprise_gateway_status: str = "legal_enterprise_gateway_metadata_ready"
    training_artifact_loader_status: str = "training_artifact_loader_metadata_ready"
    codex_training_run_status: str = "codex_training_run_metadata_ready"
    real_closed_case_training_intake_status: str = "real_closed_case_training_intake_metadata_ready"
    personal_production_pilot_dashboard_status: str = "dashboard_metadata_ready"
    pilot_ai_ocr_legal_enterprise_skill_case_analysis_connected: bool = True
    case_workspace_owner_raw_view_gated: bool = True
    fact_preview_owner_correction_ready: bool = True
    fact_preview_legal_analysis_input_ready: bool = True
    fact_preview_legal_analysis_auto_triggered: bool = False
    fact_preview_gate_reference_only: bool = True
    legal_analysis_draft_only: bool = True
    legal_analysis_draft_review_ready: bool = True
    legal_analysis_final_opinion_blocked: bool = True
    legal_analysis_final_report_blocked: bool = True
    legal_analysis_owner_download_metadata_ready: bool = True
    fact_skill_final_draft_ready: bool = True
    legal_analysis_skill_final_draft_ready: bool = True
    skill_final_draft_owner_download_ready: bool = True
    skill_final_draft_auto_publish_disabled: bool = True
    skill_final_draft_open_case_training_disabled: bool = True
    skill_final_draft_gate_reference_only: bool = True
    owner_output_center_ready: bool = True
    skill_final_drafts_aggregated: bool = True
    fact_outputs_aggregated: bool = True
    legal_drafts_aggregated: bool = True
    pilot_delivery_outputs_aggregated: bool = True
    pilot_dashboard_quality_panels_ready: bool = True
    pilot_dashboard_optimization_suggestions_ready: bool = True
    owner_only_downloads_ready: bool = True
    owner_output_center_download_ready: bool = True
    trial_readiness_ready: bool = True
    trial_checklist_ready: bool = True
    trial_issue_log_ready: bool = True
    trial_quality_review_ready: bool = True
    trial_safety_confirmation_ready: bool = True
    trial_optimization_backlog_ready: bool = True
    trial_issue_log_reference_only: bool = True
    trial_quality_review_reference_only: bool = True
    provider_readiness_ready: bool = True
    provider_registry_ready: bool = True
    secret_boundary_ready: bool = True
    live_gate_ready: bool = True
    usage_cost_metadata_ready: bool = True
    dry_run_health_ready: bool = True
    real_provider_calls_still_disabled: bool = True
    material_live_connection_ready: bool = True
    material_live_provider_registry_ready: bool = True
    material_live_secret_boundary_ready: bool = True
    material_live_gate_ready: bool = True
    material_live_dry_run_health_ready: bool = True
    material_live_raw_content_blocked: bool = True
    material_live_ai_prompt_injection_blocked: bool = True
    personal_live_connection_ready: bool = True
    personal_live_connection_provider_registry_ready: bool = True
    personal_live_connection_secret_boundary_ready: bool = True
    personal_live_connection_gate_ready: bool = True
    personal_live_connection_usage_cost_ready: bool = True
    personal_live_connection_health_ready: bool = True
    personal_live_connection_audit_ready: bool = True
    legal_enterprise_gateway_ready: bool = True
    legal_provider_readiness_ready: bool = True
    enterprise_provider_readiness_ready: bool = True
    legal_source_trace_ready: bool = True
    enterprise_verification_ready: bool = True
    legal_enterprise_review_required: bool = True
    training_artifact_loader_ready: bool = True
    codex_training_scheme_ready: bool = True
    case_cause_taxonomy_ready: bool = True
    multi_level_case_cause_loader_ready: bool = True
    experience_package_manifest_ready: bool = True
    skill_manifest_loader_ready: bool = True
    case_cause_fallback_ready: bool = True
    skill_context_dry_run_ready: bool = True
    codex_fine_tune_training_disabled: bool = True
    training_artifact_open_case_training_disabled: bool = True
    training_artifact_skill_auto_publish_disabled: bool = True
    closed_case_training_run_ready: bool = True
    synthetic_closed_case_samples_ready: bool = True
    training_run_manifest_ready: bool = True
    generated_experience_packages_ready: bool = True
    generated_skill_manifests_ready: bool = True
    generated_evaluation_gate_test_cases_ready: bool = True
    generated_loading_manifest_ready: bool = True
    training_run_load_dry_run_ready: bool = True
    training_run_open_case_training_disabled: bool = True
    training_run_skill_auto_publish_disabled: bool = True
    training_run_fine_tune_disabled: bool = True
    training_run_real_case_material_read_disabled: bool = True
    real_closed_case_training_intake_ready: bool = True
    real_closed_case_redaction_pipeline_ready: bool = True
    real_closed_case_classification_ready: bool = True
    real_closed_case_training_sample_segmentation_ready: bool = True
    real_closed_case_source_trace_ready: bool = True
    real_closed_case_review_queue_ready: bool = True
    real_closed_case_open_case_training_disabled: bool = True
    real_closed_case_raw_content_blocked: bool = True
    real_closed_case_ready_for_codex_training: bool = False
    external_delivery_disabled: bool = True
    public_link_disabled: bool = True
    email_sending_disabled: bool = True
    final_legal_opinion_auto_generation_disabled: bool = True
    final_report_auto_generation_disabled: bool = True
    open_case_training_data_generation_disabled: bool = True
    dry_run_ready: bool = True
    document_dry_run_ready: bool = True
    ocr_dry_run_ready: bool = True
    legal_dry_run_ready: bool = True
    enterprise_dry_run_ready: bool = True
    live_call_requires_confirmation: bool = True
    draft_only_output: bool = True
    raw_content_blocked_by_default: bool = True
    ai_prompt_injection_blocked_by_default: bool = True
    citation_finalization_blocked_by_default: bool = True
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
    next_action: str = "validate_v7_5_real_case_production_workflow"
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
    v7_23_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_25_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_26_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_27_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_28_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_29_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_30_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_31_readiness: dict[str, bool] = Field(default_factory=dict)
    v7_31a_readiness: dict[str, bool] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)
