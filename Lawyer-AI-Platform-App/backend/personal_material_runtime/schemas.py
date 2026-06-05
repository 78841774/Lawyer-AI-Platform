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
