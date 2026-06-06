from pydantic import BaseModel, Field


class CaseAnalysisSafetyBase(BaseModel):
    owner_only: bool = True
    legal_analysis_draft_only: bool = True
    draft_only: bool = True
    metadata_only: bool = True
    open_case_runtime: bool = True
    closed_case_training: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_skill_published: bool = False
    future_training_candidate: bool = False
    requires_manual_training_selection: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    lawyer_review_required: bool = True
    gate_reference_only: bool = True
    blocks_next_stage: bool = False
    raw_content_included: bool = False
    raw_ocr_text_included: bool = False
    raw_content_written_to_git: bool = False
    raw_content_written_to_docs: bool = False
    raw_content_written_to_diagnostics: bool = False
    raw_content_written_to_regression_output: bool = False
    ai_prompt_injected: bool = False
    controlled_prompt_only: bool = True
    live_call_executed: bool = False
    api_key_accessed: bool = False
    api_key_exposed: bool = False
    final_fact_finding: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    third_party_share_enabled: bool = False
    client_auto_delivery: bool = False
    external_delivery_triggered: bool = False
    email_sent: bool = False
    real_pdf_docx_generated: bool = False


class PersonalCaseAnalysisStatus(CaseAnalysisSafetyBase):
    enabled: bool = True
    mode: str = "personal_case_analysis"
    version: str = "v7.21"
    runtime_label: str = "法律分析草稿工作台"
    fact_analysis_enabled: bool = True
    legal_analysis_enabled: bool = True
    legal_analysis_draft_workbench_enabled: bool = True
    review_readiness_enabled: bool = True
    training_runtime_separated: bool = True
    open_case_analysis_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisRuntime(CaseAnalysisSafetyBase):
    runtime_id: str
    display_name: str
    runtime_type: str
    stage: str
    enabled: bool = True
    live_enabled: bool = False
    skill_required: bool = True
    target_route: str = "/personal-case-analysis"
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisRuntimeList(CaseAnalysisSafetyBase):
    runtimes: list[CaseAnalysisRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    live_runtime_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillBaselineMetadata(CaseAnalysisSafetyBase):
    skill_key: str
    skill_title_cn: str
    expected_skill_id: str
    source_skill_id: str
    source_package_id: str | None = None
    source_candidate_id: str | None = None
    source_evaluation_files: list[str] = Field(default_factory=list)
    source_gate_files: list[str] = Field(default_factory=list)
    source_test_case_ids: list[str] = Field(default_factory=list)
    derived_from: list[str] = Field(default_factory=list)
    baseline_detected: bool = False
    prompt_template_detected: bool = False
    evaluation_detected: bool = False
    gate_detected: bool = False
    missing_baseline_report: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillBaselineReport(CaseAnalysisSafetyBase):
    baselines: list[SkillBaselineMetadata] = Field(default_factory=list)
    baseline_count: int = 0
    detected_count: int = 0
    missing_baseline_report: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisRunMockRequest(BaseModel):
    case_id: str
    case_alias: str = "未结案件样本"
    analysis_scope: str = "fact_and_legal_analysis"
    material_metadata_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    selected_skill_ids: list[str] = Field(default_factory=list)
    explicit_mock_confirmation: bool = False
    explicit_open_case_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class FactDraftMockRequest(BaseModel):
    case_id: str
    run_id: str | None = None
    source_trace_ids: list[str] = Field(default_factory=list)
    material_metadata_ids: list[str] = Field(default_factory=list)
    case_fact_extraction_skill_id: str = "case_fact_extraction_skill"
    explicit_mock_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False


class LegalDraftMockRequest(BaseModel):
    case_id: str
    fact_draft_id: str | None = None
    source_trace_ids: list[str] = Field(default_factory=list)
    legal_search_metadata_ids: list[str] = Field(default_factory=list)
    enterprise_metadata_ids: list[str] = Field(default_factory=list)
    case_legal_analysis_skill_id: str = "case_legal_analysis_skill"
    explicit_mock_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class ReviewActionRequest(BaseModel):
    action: str
    reviewer_id: str
    reviewer_note: str | None = None
    explicit_lawyer_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class CaseAnalysisRunRecord(CaseAnalysisSafetyBase):
    run_id: str
    case_id: str
    case_alias: str
    analysis_scope: str
    run_status: str = "draft_metadata_created"
    stage_status: dict[str, str] = Field(default_factory=dict)
    selected_skill_ids: list[str] = Field(default_factory=list)
    skill_baseline_ids: list[str] = Field(default_factory=list)
    fact_draft_id: str | None = None
    legal_draft_id: str | None = None
    evaluation_id: str | None = None
    gate_id: str | None = None
    review_item_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisRunList(CaseAnalysisSafetyBase):
    runs: list[CaseAnalysisRunRecord] = Field(default_factory=list)
    run_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class FactAnalysisDraft(CaseAnalysisSafetyBase):
    fact_draft_id: str
    run_id: str | None = None
    case_id: str
    source_skill_id: str = "case_fact_extraction_skill"
    source_package_id: str | None = None
    fact_summary_draft: str
    evidence_mapping_draft: list[dict[str, str]] = Field(default_factory=list)
    timeline_draft: list[dict[str, str]] = Field(default_factory=list)
    disputed_facts_draft: list[str] = Field(default_factory=list)
    missing_facts_draft: list[str] = Field(default_factory=list)
    confidence_metadata: dict[str, str | int | bool] = Field(default_factory=dict)
    source_trace_ids: list[str] = Field(default_factory=list)
    review_required: bool = True
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class FactAnalysisDraftList(CaseAnalysisSafetyBase):
    fact_drafts: list[FactAnalysisDraft] = Field(default_factory=list)
    draft_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LegalAnalysisDraft(CaseAnalysisSafetyBase):
    legal_draft_id: str
    fact_draft_id: str | None = None
    fact_preview_id: str | None = None
    case_id: str
    source_skill_id: str = "case_legal_analysis_skill"
    source_package_id: str | None = None
    legal_analysis_summary_draft: str = "法律分析摘要 draft metadata，需律师复核。"
    legal_relationship_draft: str
    legal_reasoning_draft: list[str] = Field(default_factory=list)
    dispute_focus_draft: list[str] = Field(default_factory=list)
    issue_spotting_draft: list[str] = Field(default_factory=list)
    claim_basis_draft: list[str] = Field(default_factory=list)
    defense_path_draft: list[str] = Field(default_factory=list)
    burden_of_proof_draft: list[str] = Field(default_factory=list)
    legal_search_questions_draft: list[str] = Field(default_factory=list)
    risk_flags_draft: list[str] = Field(default_factory=list)
    next_action_checklist_draft: list[str] = Field(default_factory=list)
    version_status: str = "ai_draft_metadata"
    owner_confirmed: bool = False
    review_ready: bool = False
    owner_download_ready: bool = True
    source_trace_ids: list[str] = Field(default_factory=list)
    review_required: bool = True
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class LegalAnalysisDraftList(CaseAnalysisSafetyBase):
    legal_drafts: list[LegalAnalysisDraft] = Field(default_factory=list)
    draft_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LegalDraftVersionMockRequest(BaseModel):
    created_from: str = "owner_correction"
    change_summary: str = "基于用户修订生成法律分析草稿版本 metadata"
    explicit_owner_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_training_data_confirmation: bool = False


class LegalDraftVersionRecord(CaseAnalysisSafetyBase):
    version_id: str
    legal_draft_id: str
    version_number: int
    version_type: str = "legal_analysis_draft_version"
    created_from: str
    change_summary: str
    owner_confirmed: bool = False
    review_ready: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class LegalDraftVersionList(CaseAnalysisSafetyBase):
    legal_draft_id: str
    versions: list[LegalDraftVersionRecord] = Field(default_factory=list)
    version_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LegalDraftQualityReport(CaseAnalysisSafetyBase):
    legal_draft_id: str
    overall_score: int
    dimension_scores: dict[str, int] = Field(default_factory=dict)
    optimization_suggestions: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LegalDraftGateReport(CaseAnalysisSafetyBase):
    gate_id: str
    legal_draft_id: str
    gate_status: str = "reference_only"
    gate_score: int
    optimization_required: bool = True
    low_confidence_flags: list[str] = Field(default_factory=list)
    missing_information_checklist: list[str] = Field(default_factory=list)
    review_ready: bool = False
    warnings: list[str] = Field(default_factory=list)


class LegalDraftReviewConfirmRequest(BaseModel):
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str | None = None
    explicit_owner_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_final_report_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False


class LegalDraftReviewConfirmation(CaseAnalysisSafetyBase):
    legal_draft_id: str
    review_item_id: str
    review_status: str = "pending_lawyer_review"
    owner_confirmed: bool = False
    review_ready: bool = False
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisEvaluation(CaseAnalysisSafetyBase):
    evaluation_id: str
    run_id: str | None = None
    fact_draft_id: str | None = None
    legal_draft_id: str | None = None
    evaluation_scope: str = "draft_quality_reference"
    fact_scores: dict[str, int] = Field(default_factory=dict)
    legal_scores: dict[str, int] = Field(default_factory=dict)
    optimization_notes: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisEvaluationList(CaseAnalysisSafetyBase):
    evaluations: list[CaseAnalysisEvaluation] = Field(default_factory=list)
    evaluation_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisGate(CaseAnalysisSafetyBase):
    gate_id: str
    run_id: str | None = None
    fact_draft_id: str | None = None
    legal_draft_id: str | None = None
    gate_status: str = "reference_only"
    readiness: dict[str, str | int | bool] = Field(default_factory=dict)
    low_confidence_flags: list[str] = Field(default_factory=list)
    missing_information_checklist: list[str] = Field(default_factory=list)
    source_trace_complete: bool = False
    analysis_readiness: str = "draft_review_required"
    delivery_packet_readiness: str = "not_ready"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisGateList(CaseAnalysisSafetyBase):
    gates: list[CaseAnalysisGate] = Field(default_factory=list)
    gate_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisReviewItem(CaseAnalysisSafetyBase):
    review_item_id: str
    linked_object_type: str
    linked_object_id: str
    case_id: str
    review_status: str = "pending_lawyer_review"
    review_focus: list[str] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisReviewQueue(CaseAnalysisSafetyBase):
    review_items: list[CaseAnalysisReviewItem] = Field(default_factory=list)
    item_count: int = 0
    pending_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisReviewActionResult(CaseAnalysisSafetyBase):
    review_item_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    review_status: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisSourceTrace(CaseAnalysisSafetyBase):
    source_trace_id: str
    source_type: str
    source_label: str
    linked_object_type: str
    linked_object_id: str
    case_id: str | None = None
    run_id: str | None = None
    created_at: str
    raw_content_stored: bool = False
    raw_content_returned: bool = False
    used_in_ai_prompt: bool = False


class CaseAnalysisSourceTraceList(CaseAnalysisSafetyBase):
    source_traces: list[CaseAnalysisSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisAuditEvent(CaseAnalysisSafetyBase):
    audit_id: str
    action: str
    actor: str
    object_type: str
    object_id: str
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)


class CaseAnalysisAuditTimeline(CaseAnalysisSafetyBase):
    events: list[CaseAnalysisAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisSafetyStatus(CaseAnalysisSafetyBase):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    warnings: list[str] = Field(default_factory=list)
