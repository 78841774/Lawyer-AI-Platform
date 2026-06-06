from pydantic import BaseModel, Field


class CaseWorkspaceSafetyBase(BaseModel):
    owner_only: bool = True
    owner_access_required: bool = True
    downloadable_by_owner_only: bool = True
    metadata_only: bool = True
    draft_only: bool = True
    provider_gated: bool = True
    dry_run_default: bool = True
    preview_only: bool = False
    correction_allowed: bool = True
    owner_correction_allowed: bool = True
    legal_analysis_input_allowed: bool = True
    legal_analysis_auto_triggered: bool = False
    export_allowed: bool = True
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    third_party_share_enabled: bool = False
    client_auto_delivery: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    gate_reference_only: bool = True
    blocks_next_stage: bool = False
    final_fact_finding: bool = False
    raw_content_written_to_git: bool = False
    raw_content_written_to_docs: bool = False
    raw_content_written_to_diagnostics: bool = False
    raw_content_written_to_regression_output: bool = False
    source_trace_required: bool = True
    audit_required: bool = True
    lawyer_review_required: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    real_pdf_docx_generated: bool = False
    raw_content_returned: bool = False
    local_path_visible: bool = False
    api_key_exposed: bool = False


class CaseWorkspaceStatus(CaseWorkspaceSafetyBase):
    enabled: bool = True
    mode: str = "personal_case_workspace"
    version: str = "v7.18"
    runtime_label: str = "个人案件与材料工作台"
    case_workspace_ready: bool = True
    material_workspace_ready: bool = True
    owner_raw_view_gated: bool = True
    fact_input_correction_ready: bool = True
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceCase(CaseWorkspaceSafetyBase):
    case_id: str
    case_alias: str
    case_status: str = "mock_open_case_metadata"
    material_count: int = 0
    source_trace_count: int = 0
    review_status: str = "lawyer_review_required"
    current_stage: str = "material_workspace_metadata"
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceCaseList(CaseWorkspaceSafetyBase):
    cases: list[CaseWorkspaceCase] = Field(default_factory=list)
    case_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceMaterial(CaseWorkspaceSafetyBase):
    material_id: str
    case_id: str
    material_title: str
    material_type: str
    owner_raw_view_available: bool = True
    owner_raw_view_requires_confirmation: bool = True
    ocr_status: str = "metadata_ready"
    fact_input_status: str = "draft_metadata_ready"
    source_trace_ids: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceMaterialList(CaseWorkspaceSafetyBase):
    case_id: str
    materials: list[CaseWorkspaceMaterial] = Field(default_factory=list)
    material_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class OwnerRawViewRequest(BaseModel):
    explicit_owner_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_ai_prompt_confirmation: bool = False


class OwnerRawViewResponse(CaseWorkspaceSafetyBase):
    material_id: str
    action: str = "owner_raw_view_metadata"
    owner_confirmation_received: bool = False
    owner_raw_view_allowed: bool = False
    owner_raw_view_status: str = "blocked_until_owner_confirmation"
    preview_placeholder: str = "用户本人原文查看入口已受控占位；API 不返回真实原文。"
    raw_content_loaded: bool = False
    raw_content_included_in_prompt: bool = False
    warnings: list[str] = Field(default_factory=list)


class OCRStatus(CaseWorkspaceSafetyBase):
    material_id: str
    ocr_job_id: str
    ocr_status: str = "mock_metadata_ready"
    raw_ocr_text_returned: bool = False
    ocr_provider_called: bool = False
    review_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class FactInputStatus(CaseWorkspaceSafetyBase):
    material_id: str
    fact_input_id: str
    fact_input_status: str = "draft_metadata_ready"
    correction_queue_ready: bool = True
    raw_material_used_in_ai_prompt: bool = False
    warnings: list[str] = Field(default_factory=list)


class FactCorrectionMockRequest(BaseModel):
    correction_note: str = "仅更新事实输入纠正 metadata"
    explicit_owner_confirmation: bool = False
    explicit_lawyer_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class FactCorrectionResult(CaseWorkspaceSafetyBase):
    material_id: str
    correction_id: str
    correction_status: str = "mock_fact_correction_metadata_created"
    correction_note_redacted: str = "correction metadata accepted"
    raw_correction_text_stored: bool = False
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceSourceTrace(CaseWorkspaceSafetyBase):
    source_trace_id: str
    linked_object_type: str
    linked_object_id: str
    source_label: str
    trace_status: str = "metadata_confirmable"
    confirmed: bool = False
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceSourceTraceList(CaseWorkspaceSafetyBase):
    source_traces: list[CaseWorkspaceSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    confirmed_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceAuditEvent(CaseWorkspaceSafetyBase):
    event_id: str
    event_type: str
    linked_object_type: str
    linked_object_id: str
    message: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceAuditTimeline(CaseWorkspaceSafetyBase):
    events: list[CaseWorkspaceAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseWorkspaceSafetyStatus(CaseWorkspaceSafetyBase):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)


class FactPreviewMockRequest(BaseModel):
    case_id: str = "case_workspace_mock_001"
    material_ids: list[str] = Field(default_factory=list)
    explicit_owner_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_auto_legal_analysis_confirmation: bool = False


class FactPreviewRecord(CaseWorkspaceSafetyBase):
    fact_preview_id: str
    case_id: str
    material_ids: list[str] = Field(default_factory=list)
    ocr_job_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    fact_summary_draft: str = "事实摘要 draft metadata，供用户本人核对。"
    evidence_mapping_draft: str = "证据映射 draft metadata，需来源追踪和人工确认。"
    timeline_draft: str = "时间线 draft metadata，待用户纠正。"
    disputed_facts_draft: str = "争议事实 draft metadata，非最终事实认定。"
    missing_facts_draft: str = "缺失事实 draft metadata，用于提示补充。"
    confidence_metadata: dict[str, float | str] = Field(default_factory=dict)
    preview_status: str = "ai_draft_metadata_ready"
    correction_status: str = "correction_allowed"
    legal_analysis_input_ready: bool = False
    owner_confirmed: bool = False
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class FactPreviewList(CaseWorkspaceSafetyBase):
    fact_previews: list[FactPreviewRecord] = Field(default_factory=list)
    fact_preview_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class FactCorrectionMockRequestV20(BaseModel):
    corrected_sections: list[str] = Field(default_factory=lambda: ["fact_summary_correction"])
    correction_reason: str = "用户本人纠正事实输入 metadata"
    correction_type: str = "fact_summary_correction"
    explicit_owner_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_skill_update_confirmation: bool = False
    explicit_no_auto_legal_analysis_confirmation: bool = False


class FactCorrectionRecord(CaseWorkspaceSafetyBase):
    correction_id: str
    fact_preview_id: str
    corrected_sections: list[str] = Field(default_factory=list)
    correction_reason: str
    correction_type: str
    corrected_by_owner: bool = True
    correction_status: str = "owner_correction_metadata_created"
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class FactCorrectionList(CaseWorkspaceSafetyBase):
    fact_preview_id: str
    corrections: list[FactCorrectionRecord] = Field(default_factory=list)
    correction_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class FactVersionMockRequest(BaseModel):
    created_from: str = "owner_correction"
    change_summary: str = "基于用户纠正生成事实版本 metadata"
    explicit_owner_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False


class FactVersionRecord(CaseWorkspaceSafetyBase):
    version_id: str
    fact_preview_id: str
    version_number: int
    version_type: str
    created_from: str
    change_summary: str
    owner_confirmed: bool = False
    legal_analysis_input_ready: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class FactVersionList(CaseWorkspaceSafetyBase):
    fact_preview_id: str
    versions: list[FactVersionRecord] = Field(default_factory=list)
    version_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class FactQualityReport(CaseWorkspaceSafetyBase):
    fact_preview_id: str
    overall_score: int
    dimension_scores: dict[str, int] = Field(default_factory=dict)
    gate_status: str
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class FactGateReport(CaseWorkspaceSafetyBase):
    gate_id: str
    fact_preview_id: str
    gate_status: str
    gate_score: int
    optimization_required: bool = False
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LegalAnalysisInputConfirmRequest(BaseModel):
    explicit_owner_confirmation: bool = False
    explicit_source_trace_confirmation: bool = False
    explicit_no_auto_legal_analysis_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False


class LegalAnalysisInputReadiness(CaseWorkspaceSafetyBase):
    readiness_id: str
    fact_preview_id: str
    legal_analysis_input_ready: bool = False
    owner_confirmed: bool = False
    source_trace_ready: bool = False
    missing_fact_flags: list[str] = Field(default_factory=list)
    low_confidence_flags: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LegalAnalysisInputReadinessList(CaseWorkspaceSafetyBase):
    readiness_items: list[LegalAnalysisInputReadiness] = Field(default_factory=list)
    readiness_count: int = 0
    warnings: list[str] = Field(default_factory=list)
