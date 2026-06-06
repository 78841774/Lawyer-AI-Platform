from pydantic import BaseModel, Field


class PersonalSkillStudioStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_skill_studio"
    version: str = "v7.22"
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    experience_package_runtime_enabled: bool = True
    skill_candidate_runtime_enabled: bool = True
    test_case_runtime_enabled: bool = True
    evaluation_runtime_enabled: bool = True
    promotion_gate_enabled: bool = True
    skill_final_draft_workbench_enabled: bool = True
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    requires_manual_confirmation: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalSkillStudioRuntime(BaseModel):
    runtime_id: str
    display_name: str
    runtime_type: str
    capabilities: list[str] = Field(default_factory=list)
    enabled: bool = True
    live_enabled: bool = False
    mock_available: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    metadata_only: bool = True
    draft_only: bool = True
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    final_skill_published: bool = False
    auto_publish_enabled: bool = False
    warning: str = "当前仅生成草案和模拟评估，不会自动发布 Skill。"


class PersonalSkillStudioRuntimeList(BaseModel):
    runtimes: list[PersonalSkillStudioRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    live_runtime_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackageMockRequest(BaseModel):
    case_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    review_result_ids: list[str] = Field(default_factory=list)
    package_title: str
    legal_area: str
    case_cause: str
    jurisdiction: str
    explicit_mock_confirmation: bool = False
    explicit_source_trace_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False
    explicit_no_auto_publish_confirmation: bool = False


class SkillCandidateMockRequest(BaseModel):
    experience_package_id: str
    skill_title: str
    skill_type: str
    target_legal_area: str
    target_case_cause: str
    explicit_mock_confirmation: bool = False
    explicit_lawyer_review_confirmation: bool = False
    explicit_no_auto_publish_confirmation: bool = False


class TestCaseMockRequest(BaseModel):
    skill_candidate_id: str
    test_case_title: str
    scenario_type: str
    explicit_mock_confirmation: bool = False
    explicit_no_raw_content_confirmation: bool = False


class EvaluationMockRequest(BaseModel):
    skill_candidate_id: str
    test_case_ids: list[str] = Field(default_factory=list)
    evaluation_scope: str
    explicit_mock_confirmation: bool = False
    explicit_manual_review_confirmation: bool = False
    explicit_no_auto_publish_confirmation: bool = False


class PromotionActionRequest(BaseModel):
    action: str
    reviewer_id: str
    reviewer_note: str | None = None
    explicit_manual_confirmation: bool = False
    explicit_no_auto_publish_confirmation: bool = False
    explicit_no_final_opinion_confirmation: bool = False


class SkillStudioSourceTrace(BaseModel):
    source_trace_id: str
    source_type: str
    source_label: str
    linked_object_type: str
    linked_object_id: str
    case_id: str | None = None
    experience_package_id: str | None = None
    skill_candidate_id: str | None = None
    mock_or_placeholder_only: bool = True
    raw_content_stored: bool = False
    raw_content_returned: bool = False
    used_in_ai_prompt: bool = False
    live_call_executed: bool = False
    final_skill_published: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    draft_only: bool = True
    metadata_only: bool = True
    created_at: str


class SkillStudioSourceTraceList(BaseModel):
    source_traces: list[SkillStudioSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackageDraft(BaseModel):
    experience_package_id: str
    case_id: str
    package_title: str
    legal_area: str
    case_cause: str
    jurisdiction: str
    package_status: str = "draft"
    mock_or_placeholder_only: bool = True
    source_trace_ids: list[str] = Field(default_factory=list)
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    lawyer_review_required: bool = True
    raw_content_included: bool = False
    used_in_ai_prompt: bool = False
    live_call_executed: bool = False
    final_skill_published: bool = False
    draft_only: bool = True
    metadata_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    auto_publish_enabled: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    draft_sections: dict[str, str] = Field(default_factory=dict)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackageDraftList(BaseModel):
    experience_packages: list[ExperiencePackageDraft] = Field(default_factory=list)
    package_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillCandidateDraft(BaseModel):
    skill_candidate_id: str
    experience_package_id: str
    skill_title: str
    skill_type: str
    target_legal_area: str
    target_case_cause: str
    candidate_status: str = "draft"
    prompt_template_draft: dict[str, str] = Field(default_factory=dict)
    reasoning_pattern_draft: dict[str, str] = Field(default_factory=dict)
    input_schema_draft: dict[str, str] = Field(default_factory=dict)
    output_schema_draft: dict[str, str] = Field(default_factory=dict)
    limitation_notes: list[str] = Field(default_factory=list)
    requires_lawyer_review: bool = True
    lawyer_review_required: bool = True
    requires_evaluation: bool = True
    source_trace_required: bool = True
    raw_content_included: bool = False
    used_in_ai_prompt: bool = False
    live_call_executed: bool = False
    final_skill_published: bool = False
    draft_only: bool = True
    metadata_only: bool = True
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    created_at: str
    updated_at: str | None = None
    warnings: list[str] = Field(default_factory=list)


class SkillCandidateDraftList(BaseModel):
    skill_candidates: list[SkillCandidateDraft] = Field(default_factory=list)
    candidate_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillTestCaseDraft(BaseModel):
    test_case_id: str
    skill_candidate_id: str
    test_case_title: str
    scenario_type: str
    mock_input_metadata: dict[str, str] = Field(default_factory=dict)
    expected_behavior_metadata: dict[str, str] = Field(default_factory=dict)
    source_trace_ids: list[str] = Field(default_factory=list)
    requires_manual_review: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    raw_content_included: bool = False
    used_in_ai_prompt: bool = False
    live_call_executed: bool = False
    final_skill_published: bool = False
    draft_only: bool = True
    metadata_only: bool = True
    mock_or_placeholder_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    auto_publish_enabled: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class SkillTestCaseDraftList(BaseModel):
    test_cases: list[SkillTestCaseDraft] = Field(default_factory=list)
    test_case_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillEvaluationDraft(BaseModel):
    evaluation_id: str
    skill_candidate_id: str
    test_case_ids: list[str] = Field(default_factory=list)
    evaluation_scope: str
    score_summary: dict[str, int | str | bool] = Field(default_factory=dict)
    checklist_results: list[dict[str, str | bool]] = Field(default_factory=list)
    risk_flags: list[str] = Field(default_factory=list)
    recommendation: str
    requires_manual_review: bool = True
    requires_lawyer_review: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    promotion_ready: bool = False
    raw_content_included: bool = False
    used_in_ai_prompt: bool = False
    live_call_executed: bool = False
    final_skill_published: bool = False
    draft_only: bool = True
    metadata_only: bool = True
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class SkillEvaluationDraftList(BaseModel):
    evaluations: list[SkillEvaluationDraft] = Field(default_factory=list)
    evaluation_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PromotionActionResult(BaseModel):
    skill_candidate_id: str
    action: str
    reviewer_id: str = "redacted_reviewer"
    status: str = "promotion_action_recorded"
    candidate_status: str
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    draft_only: bool = True
    metadata_only: bool = True
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillStudioAuditEvent(BaseModel):
    audit_id: str
    action: str
    actor: str
    object_type: str
    object_id: str
    timestamp: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    no_raw_content: bool = True
    no_live_ai_call: bool = True
    no_auto_publish: bool = True
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    final_skill_published: bool = False
    source_trace_required: bool = True
    lawyer_review_required: bool = True
    draft_only: bool = True
    metadata_only: bool = True
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False


class SkillStudioAuditTimeline(BaseModel):
    events: list[SkillStudioAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillStudioSafetyStatus(BaseModel):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    metadata_only: bool = True
    draft_only: bool = True
    live_ai_call_executed: bool = False
    live_call_executed: bool = False
    used_in_ai_prompt: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillFinalDraftSafetyBase(BaseModel):
    owner_only: bool = True
    downloadable_by_owner_only: bool = True
    baseline_discovered: bool = True
    baseline_complete: bool = False
    gate_reference_only: bool = True
    blocks_next_stage: bool = False
    quality_reference_only: bool = True
    final_skill_published: bool = False
    skill_auto_published: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    open_case_data_used: bool = False
    unresolved_case_data_used: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    third_party_share_enabled: bool = False
    client_auto_delivery: bool = False
    api_key_exposed: bool = False
    raw_content_written_to_git: bool = False
    raw_content_written_to_docs: bool = False
    raw_content_written_to_diagnostics: bool = False
    raw_content_written_to_regression_output: bool = False
    raw_content_returned: bool = False
    local_path_visible: bool = False
    source_trace_required: bool = True
    audit_required: bool = True
    lawyer_review_required: bool = True
    metadata_only: bool = True
    draft_only: bool = True


class SkillBaselineDiscoveryMetadata(SkillFinalDraftSafetyBase):
    source_skill_files: list[str] = Field(default_factory=list)
    source_package_files: list[str] = Field(default_factory=list)
    source_evaluation_files: list[str] = Field(default_factory=list)
    source_gate_files: list[str] = Field(default_factory=list)
    source_test_case_files: list[str] = Field(default_factory=list)
    source_prompt_template_files: list[str] = Field(default_factory=list)
    source_pattern_files: list[str] = Field(default_factory=list)
    missing_baseline_items: list[str] = Field(default_factory=list)
    derived_from: list[str] = Field(default_factory=list)
    missing_baseline_report: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillFinalDraftRecord(SkillFinalDraftSafetyBase):
    skill_id: str
    skill_name: str
    skill_type: str
    version_label: str = "v7.22 final draft metadata"
    source_skill_id: str
    source_package_id: str | None = None
    derived_from: list[str] = Field(default_factory=list)
    fact_patterns: list[str] = Field(default_factory=list)
    evidence_mapping_rules: list[str] = Field(default_factory=list)
    timeline_rules: list[str] = Field(default_factory=list)
    party_relation_rules: list[str] = Field(default_factory=list)
    claim_defense_fact_rules: list[str] = Field(default_factory=list)
    disputed_fact_rules: list[str] = Field(default_factory=list)
    missing_fact_rules: list[str] = Field(default_factory=list)
    confidence_rules: list[str] = Field(default_factory=list)
    source_trace_rules: list[str] = Field(default_factory=list)
    legal_issue_patterns: list[str] = Field(default_factory=list)
    claim_basis_patterns: list[str] = Field(default_factory=list)
    defense_patterns: list[str] = Field(default_factory=list)
    burden_of_proof_rules: list[str] = Field(default_factory=list)
    legal_search_question_patterns: list[str] = Field(default_factory=list)
    citation_selection_rules: list[str] = Field(default_factory=list)
    risk_assessment_rules: list[str] = Field(default_factory=list)
    argument_structure_templates: list[str] = Field(default_factory=list)
    prompt_templates: list[str] = Field(default_factory=list)
    analysis_prompt_templates: list[str] = Field(default_factory=list)
    evaluation_cases: list[str] = Field(default_factory=list)
    test_cases: list[str] = Field(default_factory=list)
    review_checklist: list[str] = Field(default_factory=list)
    optimization_suggestions: list[str] = Field(default_factory=list)
    quality_score: int = 0
    gate_status: str = "reference_only"
    available_formats: list[str] = Field(default_factory=lambda: ["Markdown", "JSON", "PDF draft metadata", "DOCX draft metadata"])
    warnings: list[str] = Field(default_factory=list)


class SkillFinalDraftList(SkillFinalDraftSafetyBase):
    final_drafts: list[SkillFinalDraftRecord] = Field(default_factory=list)
    draft_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillFinalDraftLineage(SkillFinalDraftSafetyBase):
    skill_id: str
    source_skill_id: str
    source_package_id: str | None = None
    derived_from: list[str] = Field(default_factory=list)
    source_skill_files: list[str] = Field(default_factory=list)
    source_evaluation_files: list[str] = Field(default_factory=list)
    source_gate_files: list[str] = Field(default_factory=list)
    source_test_case_files: list[str] = Field(default_factory=list)
    placeholder_lineage_used: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillFinalQualityReport(SkillFinalDraftSafetyBase):
    skill_id: str
    score_status: str = "reference_only"
    quality_score: int = 0
    dimensions: dict[str, int | str | bool] = Field(default_factory=dict)
    missing_evaluation_files: list[str] = Field(default_factory=list)
    suggested_next_optimization: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillFinalGateReport(SkillFinalDraftSafetyBase):
    skill_id: str
    gate_status: str = "reference_only"
    gate_fields: dict[str, bool | str] = Field(default_factory=dict)
    missing_gate_files: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillFinalOptimizationReport(SkillFinalDraftSafetyBase):
    skill_id: str
    optimization_suggestions: list[str] = Field(default_factory=list)
    optimization_reference_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class SkillFinalSourceTraceList(SkillFinalDraftSafetyBase):
    skill_id: str
    source_traces: list[SkillStudioSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillFinalAuditTimeline(SkillFinalDraftSafetyBase):
    skill_id: str
    events: list[SkillStudioAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillFinalOwnerDownloadRequest(BaseModel):
    requested_format: str
    explicit_owner_confirmation: bool = False
    explicit_no_public_link_confirmation: bool = False
    explicit_no_email_confirmation: bool = False
    explicit_no_external_delivery_confirmation: bool = False
    explicit_no_auto_publish_confirmation: bool = False


class SkillFinalOwnerDownloadRecord(SkillFinalDraftSafetyBase):
    download_id: str
    skill_id: str
    requested_format: str
    download_status: str = "draft_metadata_ready"
    file_generated: bool = False
    file_path_visible: bool = False
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class SkillFinalOwnerDownloadList(SkillFinalDraftSafetyBase):
    owner_downloads: list[SkillFinalOwnerDownloadRecord] = Field(default_factory=list)
    download_count: int = 0
    warnings: list[str] = Field(default_factory=list)
