from pydantic import BaseModel, Field


class PersonalMaterialRuntimeStatus(BaseModel):
    enabled: bool = True
    mode: str = "controlled_material_parsing_paddleocr_runtime"
    version: str = "v7.2"
    mock_first_enabled: bool = True
    controlled_live_supported: bool = True
    live_provider_call_enabled: bool = False
    material_parser_runtime_enabled: bool = True
    ocr_runtime_enabled: bool = True
    ocr_review_queue_enabled: bool = True
    source_trace_enabled: bool = True
    manual_approval_required: bool = True
    lawyer_review_required: bool = True
    raw_ocr_controlled: bool = True
    raw_ocr_text_exposed: bool = False
    external_delivery_enabled: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialProvider(BaseModel):
    provider_id: str
    label: str
    category: str
    configured: bool = False
    live_enabled: bool = False
    mock_supported: bool = True
    controlled_live_supported: bool = True
    requires_api_key: bool = False
    api_key_present: bool = False
    api_key_visible: bool = False
    status: str = "placeholder_not_configured"
    target_version: str = "v7.2"
    target_route: str = "/personal-material-runtime"
    next_action: str
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialProviderList(BaseModel):
    providers: list[PersonalMaterialProvider] = Field(default_factory=list)
    provider_count: int = 0
    configured_provider_count: int = 0
    live_provider_count: int = 0
    provider_secrets_visible: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialParseSummary(BaseModel):
    page_count: int = 0
    section_count: int = 0
    table_count: int = 0
    image_count: int = 0
    mock_preview_only: bool = True


class PersonalMaterialParseJobRequest(BaseModel):
    case_id: str
    material_id: str
    parser_provider_id: str
    parse_type: str
    manual_approval_confirmed: bool = False
    mock_data_only_confirmation: bool = False
    no_raw_content_confirmation: bool = False
    no_external_upload_confirmation: bool = False


class PersonalMaterialParseJobResult(BaseModel):
    parse_job_id: str | None = None
    case_id: str
    material_id: str
    parser_provider_id: str
    parse_type: str
    mode: str = "mock"
    status: str = "mock_parse_job_created"
    would_call_provider: bool = False
    live_call_executed: bool = False
    parse_summary: PersonalMaterialParseSummary = Field(default_factory=PersonalMaterialParseSummary)
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_material_text_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    controlled_preview_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_enabled: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialParseJobRecord(BaseModel):
    parse_job_id: str
    case_id: str
    material_id: str
    parser_provider_id: str
    parse_type: str
    mode: str = "mock"
    status: str = "mock_parse_job_created"
    would_call_provider: bool = False
    live_call_executed: bool = False
    parse_summary: PersonalMaterialParseSummary = Field(default_factory=PersonalMaterialParseSummary)
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_material_text_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    controlled_preview_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_enabled: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialParseJobList(BaseModel):
    parse_jobs: list[PersonalMaterialParseJobRecord] = Field(default_factory=list)
    job_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRPreview(BaseModel):
    ocr_job_id: str | None = None
    case_id: str | None = None
    material_id: str | None = None
    ocr_provider_id: str | None = None
    status: str = "mock_preview_available"
    page_count: int = 1
    recognized_block_count: int = 3
    average_confidence: float = 0.91
    low_confidence_block_count: int = 0
    table_detected: bool = False
    layout_detected: bool = True
    key_information_detected: bool = True
    preview_blocks: list[dict[str, str | int | float | bool]] = Field(default_factory=list)
    controlled_preview_only: bool = True
    raw_ocr_text_exposed: bool = False
    requires_lawyer_review: bool = True
    source_trace_required: bool = True
    used_in_ai_prompt: bool = False
    used_in_final_output: bool = False
    eligible_for_ai_prompt_after_review: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRJobRequest(BaseModel):
    case_id: str
    material_id: str
    ocr_provider_id: str
    ocr_job_type: str
    manual_approval_confirmed: bool = False
    lawyer_review_required_confirmation: bool = False
    source_trace_required_confirmation: bool = False
    no_raw_ocr_exposure_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False


class PersonalOCRJobResult(BaseModel):
    ocr_job_id: str | None = None
    case_id: str
    material_id: str
    ocr_provider_id: str
    ocr_job_type: str
    mode: str = "mock"
    status: str = "mock_ocr_job_created"
    would_call_provider: bool = False
    live_call_executed: bool = False
    ocr_preview: PersonalOCRPreview = Field(default_factory=PersonalOCRPreview)
    review_status: str = "pending_review"
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    controlled_preview_only: bool = True
    used_in_ai_prompt: bool = False
    used_in_final_output: bool = False
    eligible_for_ai_prompt_after_review: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_enabled: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRJobRecord(BaseModel):
    ocr_job_id: str
    case_id: str
    material_id: str
    ocr_provider_id: str
    ocr_job_type: str
    mode: str = "mock"
    status: str = "mock_ocr_job_created"
    would_call_provider: bool = False
    live_call_executed: bool = False
    ocr_preview: PersonalOCRPreview = Field(default_factory=PersonalOCRPreview)
    review_status: str = "pending_review"
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    controlled_preview_only: bool = True
    used_in_ai_prompt: bool = False
    used_in_final_output: bool = False
    eligible_for_ai_prompt_after_review: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_enabled: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRJobList(BaseModel):
    ocr_jobs: list[PersonalOCRJobRecord] = Field(default_factory=list)
    job_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRReviewItem(BaseModel):
    ocr_job_id: str
    case_id: str
    material_id: str
    ocr_provider_id: str
    review_status: str = "pending_review"
    confidence: float = 0.91
    low_confidence_block_count: int = 0
    requires_lawyer_review: bool = True
    source_trace_required: bool = True
    controlled_preview_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    used_in_ai_prompt: bool = False
    used_in_final_output: bool = False
    eligible_for_ai_prompt_after_review: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRReviewQueue(BaseModel):
    items: list[PersonalOCRReviewItem] = Field(default_factory=list)
    item_count: int = 0
    pending_review_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalOCRReviewActionRequest(BaseModel):
    action: str
    reviewer_id: str
    manual_review_confirmed: bool = False
    no_raw_ocr_exposure_confirmation: bool = False
    lawyer_review_required_confirmation: bool = False


class PersonalOCRReviewActionResult(BaseModel):
    ocr_job_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    status: str = "review_action_recorded"
    review_status: str = "pending_review"
    manual_review_confirmed: bool = False
    controlled_preview_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    used_in_ai_prompt: bool = False
    used_in_final_output: bool = False
    eligible_for_ai_prompt_after_review: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialSourceTrace(BaseModel):
    source_trace_id: str
    case_id: str
    material_id: str
    job_id: str
    source_type: str
    provider_id: str
    page_number: int = 1
    block_id: str
    bbox_redacted: bool = True
    bbox: dict[str, int] = Field(default_factory=dict)
    confidence: float = 0.91
    created_at: str
    manual_review_status: str = "pending_review"
    controlled_preview_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    used_in_ai_prompt: bool = False
    used_in_final_output: bool = False
    eligible_for_ai_prompt_after_review: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False


class PersonalMaterialSourceTraceList(BaseModel):
    source_traces: list[PersonalMaterialSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialAuditEvent(BaseModel):
    event_id: str
    event_type: str
    case_id: str
    material_id: str
    provider_id: str
    job_id: str
    mode: str = "mock"
    live_call_executed: bool = False
    manual_approval_confirmed: bool = True
    raw_ocr_text_exposed: bool = False
    controlled_preview_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    created_at: str


class PersonalMaterialAuditTimeline(BaseModel):
    events: list[PersonalMaterialAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialSafetyStatus(BaseModel):
    safety: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    raw_ocr_text_exposed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveProviderConfig(BaseModel):
    provider_id: str
    display_name: str
    provider_type: str
    live_supported: bool = True
    live_enabled: bool = False
    key_required: bool = False
    key_loaded: bool = False
    key_source: str = "unavailable"
    supported_file_types: list[str] = Field(default_factory=list)
    max_file_size_mb: int = 25
    supports_page_range: bool = False
    supports_bbox: bool = False
    supports_table_extraction: bool = False
    supports_layout_extraction: bool = False
    timeout_seconds: int = 30
    safety_notes: list[str] = Field(default_factory=list)


class PersonalMaterialLiveProviderConfigList(BaseModel):
    providers: list[PersonalMaterialLiveProviderConfig] = Field(default_factory=list)
    provider_count: int = 0
    live_provider_count: int = 0
    key_loaded_count: int = 0
    provider_secrets_visible: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveGatewayStatus(BaseModel):
    enabled: bool = True
    mode: str = "ocr_document_provider_live_gateway"
    version: str = "v7.13"
    ocr_live_mode_enabled: bool = False
    document_live_mode_enabled: bool = False
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    dry_run_ready: bool = True
    document_dry_run_ready: bool = True
    ocr_dry_run_ready: bool = True
    live_call_requires_confirmation: bool = True
    provider_gated: bool = True
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveRunRequest(BaseModel):
    provider_id: str
    case_id: str = "case_v55_approve_all"
    material_id: str = "material_demo_001"
    file_name: str = "controlled_demo_material.pdf"
    file_type: str = "pdf"
    byte_size: int = 0
    page_range: str | None = None
    actor_id: str = "local_demo_lawyer"
    dry_run: bool = True
    explicit_live_confirmation: bool = False
    material_owner_confirmation: bool = False
    raw_content_handling_acknowledged: bool = False
    no_ai_prompt_injection_acknowledged: bool = False
    lawyer_review_acknowledged: bool = False
    draft_only_acknowledged: bool = False


class PersonalMaterialLiveMetadataPreview(BaseModel):
    page_count: int = 0
    page_count_estimate: int = 0
    file_type: str = "pdf"
    byte_size: int = 0
    parse_status: str = "metadata_preview_only"
    confidence_summary: str = "not_applicable"
    layout_blocks_count: int = 0
    table_count: int = 0
    image_count: int = 0
    bbox_available: bool = False
    supports_bbox: bool = False
    supports_confidence: bool = True
    redacted_preview_available: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False


class PersonalMaterialLiveRunRecord(BaseModel):
    run_id: str
    run_type: str
    provider_id: str
    case_id: str
    material_id: str
    file_name: str
    file_type: str
    status: str = "dry_run_completed"
    dry_run: bool = True
    would_call_provider: bool = False
    live_mode_enabled: bool = False
    live_call_requested: bool = False
    live_call_executed: bool = False
    blocked_reason: str | None = None
    blocked_reasons: list[str] = Field(default_factory=list)
    provider_adapter_unavailable: bool = False
    file_metadata_only: bool = True
    document_metadata: PersonalMaterialLiveMetadataPreview = Field(default_factory=PersonalMaterialLiveMetadataPreview)
    ocr_metadata: PersonalMaterialLiveMetadataPreview = Field(default_factory=PersonalMaterialLiveMetadataPreview)
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    source_trace_created: bool = False
    review_required: bool = True
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveRunList(BaseModel):
    runs: list[PersonalMaterialLiveRunRecord] = Field(default_factory=list)
    run_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveReviewItem(BaseModel):
    review_item_id: str
    run_id: str
    run_type: str
    provider_id: str
    case_id: str
    material_id: str
    review_status: str = "pending_review"
    confidence_summary: str = "metadata_only"
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    redacted_preview_allowed: bool = False
    raw_content_blocked: bool = True
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveReviewQueue(BaseModel):
    items: list[PersonalMaterialLiveReviewItem] = Field(default_factory=list)
    item_count: int = 0
    pending_review_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveReviewActionRequest(BaseModel):
    action: str
    actor_id: str = "local_demo_lawyer"
    explicit_review_confirmation: bool = False
    raw_content_handling_acknowledged: bool = False
    no_ai_prompt_injection_acknowledged: bool = False


class PersonalMaterialLiveReviewActionResult(BaseModel):
    review_item_id: str
    action: str
    actor_id: str = "redacted_actor"
    status: str = "review_action_recorded"
    review_status: str = "pending_review"
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveSourceTrace(BaseModel):
    source_trace_id: str
    run_id: str
    run_type: str
    provider_id: str
    case_id: str
    material_id: str
    source_type: str = "metadata_preview"
    page_count: int = 0
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    created_at: str


class PersonalMaterialLiveSourceTraceList(BaseModel):
    source_traces: list[PersonalMaterialLiveSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveAuditEvent(BaseModel):
    event_id: str
    provider_id: str
    action: str
    actor_id: str = "redacted_actor"
    run_id: str | None = None
    review_item_id: str | None = None
    live_call_requested: bool = False
    live_call_executed: bool = False
    blocked_reason: str | None = None
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    source_trace_created: bool = False
    review_required: bool = True
    page_count: int = 0
    created_at: str


class PersonalMaterialLiveAuditTimeline(BaseModel):
    events: list[PersonalMaterialLiveAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class PersonalMaterialLiveSafetyStatus(BaseModel):
    safety: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    live_mode_enabled: bool = False
    live_call_executed: bool = False
    api_key_exposed: bool = False
    raw_content_exposed: bool = False
    raw_ocr_text_exposed: bool = False
    ai_prompt_injected: bool = False
    fact_extraction_triggered: bool = False
    legal_analysis_triggered: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    external_delivery_triggered: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    warnings: list[str] = Field(default_factory=list)
