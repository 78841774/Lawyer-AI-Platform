from pydantic import BaseModel, Field


class PilotSafetyBase(BaseModel):
    owner_only: bool = True
    owner_access_required: bool = True
    downloadable_by_owner_only: bool = True
    metadata_only: bool = True
    draft_only: bool = True
    dry_run_default: bool = True
    internal_case_analysis: bool = True
    draft_output_allowed: bool = True
    pdf_docx_generation_allowed_for_owner: bool = True
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    third_party_share_enabled: bool = False
    client_auto_delivery: bool = False
    final_legal_opinion_auto_generated: bool = False
    final_report_auto_generated: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    final_lock_required: bool = True
    provider_gated: bool = True
    api_key_exposed: bool = False
    raw_content_written_to_git: bool = False
    raw_content_written_to_docs: bool = False
    raw_content_written_to_diagnostics: bool = False
    raw_content_written_to_regression_output: bool = False
    local_path_visible: bool = False
    raw_content_returned: bool = False
    real_pdf_docx_generated: bool = False


class PilotStatus(PilotSafetyBase):
    enabled: bool = True
    mode: str = "personal_production_pilot"
    version: str = "v7.17"
    runtime_label: str = "个人生产实战 Pilot"
    live_mode_default_enabled: bool = False
    real_provider_default_disabled: bool = True
    workflow_connected: bool = True
    warnings: list[str] = Field(default_factory=list)


class PilotRuntime(PilotSafetyBase):
    runtime_id: str
    display_name: str
    category: str
    target_route: str
    connected: bool = True
    live_enabled: bool = False
    dry_run_ready: bool = True
    status: str = "gated_ready"
    warnings: list[str] = Field(default_factory=list)


class PilotRuntimeList(PilotSafetyBase):
    runtimes: list[PilotRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    connected_count: int = 0
    live_enabled_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PilotWorkflowStep(PilotSafetyBase):
    step_id: str
    display_name: str
    target_runtime_id: str
    stage: str
    status: str = "gated_ready"
    warnings: list[str] = Field(default_factory=list)


class PilotWorkflow(PilotSafetyBase):
    steps: list[PilotWorkflowStep] = Field(default_factory=list)
    step_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ProviderGate(PilotSafetyBase):
    provider_id: str
    display_name: str
    category: str
    live_enabled: bool = False
    dry_run_ready: bool = True
    external_provider_requires_confirmation: bool = True
    adapter_status: str = "gated_or_adapter_unavailable"
    api_key_frontend_visible: bool = False
    warnings: list[str] = Field(default_factory=list)


class ProviderGateSummary(PilotSafetyBase):
    provider_gates: list[ProviderGate] = Field(default_factory=list)
    provider_count: int = 0
    live_enabled_count: int = 0
    dry_run_ready_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PilotReadiness(PilotSafetyBase):
    pilot_ready: bool = True
    readiness: dict[str, bool] = Field(default_factory=dict)
    missing_requirements: list[str] = Field(default_factory=list)
    next_action: str = "v7_10_v7_17_unified_validation_security_audit"
    warnings: list[str] = Field(default_factory=list)


class PilotRunMockRequest(BaseModel):
    case_id: str
    case_alias: str = "未结案件实战 Pilot 样本"
    workflow_scope: str = "personal_production_pilot"
    selected_runtime_ids: list[str] = Field(default_factory=list)
    explicit_owner_confirmation: bool = False
    explicit_provider_gated_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PilotRunRecord(PilotSafetyBase):
    run_id: str
    case_id: str
    case_alias: str
    workflow_scope: str
    selected_runtime_ids: list[str] = Field(default_factory=list)
    run_status: str = "pilot_metadata_created"
    workflow_step_status: dict[str, str] = Field(default_factory=dict)
    case_analysis_summary_id: str | None = None
    output_ids: list[str] = Field(default_factory=list)
    download_ids: list[str] = Field(default_factory=list)
    review_item_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PilotRunList(PilotSafetyBase):
    runs: list[PilotRunRecord] = Field(default_factory=list)
    run_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillFinalDraft(PilotSafetyBase):
    draft_id: str
    skill_key: str
    title: str
    source_skill_id: str
    source_package_id: str | None = None
    available_formats: list[str] = Field(default_factory=lambda: ["Markdown", "JSON", "PDF draft", "DOCX draft"])
    owner_download_ready: bool = True
    publish_action_available: bool = False
    content_preview: str = "Skill final draft metadata only; owner download placeholder."
    warnings: list[str] = Field(default_factory=list)


class SkillFinalDraftList(PilotSafetyBase):
    skill_final_drafts: list[SkillFinalDraft] = Field(default_factory=list)
    draft_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PilotOutputMockRequest(BaseModel):
    run_id: str | None = None
    output_type: str = "case_analysis_draft"
    title: str = "案件分析草稿"
    format: str = "Markdown"
    explicit_owner_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PilotOutputRecord(PilotSafetyBase):
    output_id: str
    run_id: str | None = None
    output_type: str
    title: str
    format: str
    output_status: str = "owner_download_draft_ready"
    fact_part_available: bool = True
    legal_part_available: bool = True
    delivery_packet_draft_available: bool = True
    content_metadata_only: bool = True
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PilotOutputList(PilotSafetyBase):
    outputs: list[PilotOutputRecord] = Field(default_factory=list)
    output_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class OwnerDownloadMockRequest(BaseModel):
    requested_format: str = "Markdown"
    explicit_owner_confirmation: bool = False
    explicit_no_public_link_confirmation: bool = False
    explicit_no_email_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class OwnerDownloadRecord(PilotSafetyBase):
    download_id: str
    output_id: str
    requested_format: str
    download_status: str = "owner_download_metadata_ready"
    file_generated: bool = False
    file_path_visible: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class OwnerDownloadList(PilotSafetyBase):
    owner_downloads: list[OwnerDownloadRecord] = Field(default_factory=list)
    download_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PilotReviewItem(PilotSafetyBase):
    review_item_id: str
    linked_object_type: str
    linked_object_id: str
    review_status: str = "pending_lawyer_review"
    review_focus: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class PilotReviewQueue(PilotSafetyBase):
    review_items: list[PilotReviewItem] = Field(default_factory=list)
    item_count: int = 0
    pending_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PilotReviewActionRequest(BaseModel):
    action: str
    reviewer_id: str
    reviewer_note: str | None = None
    explicit_lawyer_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class PilotReviewActionResult(PilotSafetyBase):
    review_item_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    review_status: str
    warnings: list[str] = Field(default_factory=list)


class PilotSourceTrace(PilotSafetyBase):
    source_trace_id: str
    source_type: str
    source_label: str
    linked_object_type: str
    linked_object_id: str
    run_id: str | None = None
    created_at: str
    raw_content_returned: bool = False
    diagnostics_content_included: bool = False


class PilotSourceTraceList(PilotSafetyBase):
    source_traces: list[PilotSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PilotAuditEvent(PilotSafetyBase):
    audit_id: str
    action: str
    actor: str
    object_type: str
    object_id: str
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)


class PilotAuditTimeline(PilotSafetyBase):
    events: list[PilotAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ExportBoundary(PilotSafetyBase):
    export_boundary_id: str = "personal_production_pilot_export_boundary"
    owner_download_enabled: bool = True
    public_share_disabled: bool = True
    email_disabled: bool = True
    external_delivery_disabled: bool = True
    final_labeling_disabled: bool = True
    warnings: list[str] = Field(default_factory=list)


class PilotSafetyStatus(PilotSafetyBase):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)
