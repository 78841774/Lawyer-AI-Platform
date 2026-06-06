from pydantic import BaseModel, Field


class OwnerOutputSafetyBase(BaseModel):
    owner_only: bool = True
    owner_access_required: bool = True
    downloadable_by_owner_only: bool = True
    draft_or_metadata: bool = True
    metadata_only: bool = True
    draft_only: bool = True
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    third_party_share_enabled: bool = False
    client_auto_delivery: bool = False
    final_legal_opinion_auto_generated: bool = False
    final_report_auto_generated: bool = False
    final_skill_published: bool = False
    skill_auto_published: bool = False
    skill_published: bool = False
    skill_updated: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    gate_reference_only: bool = True
    blocks_next_stage: bool = False
    quality_reference_only: bool = True
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    audit_required: bool = True
    api_key_exposed: bool = False
    raw_content_written_to_git: bool = False
    raw_content_written_to_docs: bool = False
    raw_content_written_to_diagnostics: bool = False
    raw_content_written_to_regression_output: bool = False
    raw_content_returned: bool = False
    local_path_visible: bool = False
    real_pdf_docx_generated: bool = False


class OutputFormatOptions(BaseModel):
    markdown_available: bool = True
    json_available: bool = True
    pdf_draft_metadata_available: bool = True
    docx_draft_metadata_available: bool = True


class OwnerOutputRecord(OwnerOutputSafetyBase):
    output_id: str
    output_type: str
    output_title: str
    source_runtime: str
    source_module: str
    source_id: str
    case_id: str | None = None
    skill_id: str | None = None
    owner_user_id: str = "local_owner"
    format_options: OutputFormatOptions = Field(default_factory=OutputFormatOptions)
    quality_score: int
    gate_status: str
    dimension_scores: dict[str, int] = Field(default_factory=dict)
    optimization_suggestions: list[str] = Field(default_factory=list)
    source_trace_count: int = 0
    review_status: str = "pending_lawyer_review"
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputList(OwnerOutputSafetyBase):
    outputs: list[OwnerOutputRecord] = Field(default_factory=list)
    output_count: int = 0
    skill_final_draft_count: int = 0
    fact_output_count: int = 0
    legal_draft_count: int = 0
    pilot_delivery_count: int = 0
    owner_download_ready: bool = True
    external_delivery_disabled: bool = True
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputStatus(OwnerOutputSafetyBase):
    enabled: bool = True
    mode: str = "personal_owner_output_center"
    version: str = "v7.23"
    runtime_label: str = "用户本人产出下载中心"
    output_center_ready: bool = True
    skill_final_drafts_aggregated: bool = True
    fact_outputs_aggregated: bool = True
    legal_drafts_aggregated: bool = True
    pilot_delivery_outputs_aggregated: bool = True
    owner_only_download_ready: bool = True
    public_link_disabled: bool = True
    email_sending_disabled: bool = True
    external_delivery_disabled: bool = True
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputQuality(OwnerOutputSafetyBase):
    output_id: str
    quality_score: int
    dimension_scores: dict[str, int] = Field(default_factory=dict)
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputGate(OwnerOutputSafetyBase):
    output_id: str
    gate_status: str
    gate_score: int
    low_confidence_flags: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputOptimization(OwnerOutputSafetyBase):
    output_id: str
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputSourceTrace(OwnerOutputSafetyBase):
    source_trace_id: str
    output_id: str
    source_type: str
    source_label: str
    source_module: str
    linked_source_id: str
    trace_status: str = "metadata_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputSourceTraceList(OwnerOutputSafetyBase):
    output_id: str | None = None
    source_traces: list[OwnerOutputSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class OwnerDownloadMockRequest(BaseModel):
    owner_user_id: str = "local_owner"
    requested_format: str = "markdown"
    explicit_owner_confirmation: bool = False
    explicit_no_public_link_confirmation: bool = False
    explicit_no_email_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class OwnerDownloadRecord(OwnerOutputSafetyBase):
    download_id: str
    output_id: str
    owner_user_id: str
    requested_format: str
    download_status: str = "owner_download_metadata_ready"
    file_generated: bool = False
    file_path_visible: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class OwnerDownloadList(OwnerOutputSafetyBase):
    owner_downloads: list[OwnerDownloadRecord] = Field(default_factory=list)
    download_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputAuditEvent(OwnerOutputSafetyBase):
    event_id: str
    action: str
    object_type: str
    object_id: str
    actor: str = "system"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputAuditTimeline(OwnerOutputSafetyBase):
    events: list[OwnerOutputAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class OwnerOutputSafetyStatus(OwnerOutputSafetyBase):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_item_count: int = 0
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)
