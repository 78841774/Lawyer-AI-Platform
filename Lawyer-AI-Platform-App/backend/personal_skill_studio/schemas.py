from pydantic import BaseModel, Field


class PersonalSkillStudioStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_skill_studio"
    version: str = "v7.4"
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    experience_package_runtime_enabled: bool = True
    skill_candidate_runtime_enabled: bool = True
    test_case_runtime_enabled: bool = True
    evaluation_runtime_enabled: bool = True
    promotion_gate_enabled: bool = True
    source_trace_required: bool = True
    requires_lawyer_review: bool = True
    requires_manual_confirmation: bool = True
    raw_content_included: bool = False
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    auto_publish_enabled: bool = False
    warning: str = "当前仅生成草案和模拟评估，不会自动发布 Skill。"


class PersonalSkillStudioRuntimeList(BaseModel):
    runtimes: list[PersonalSkillStudioRuntime] = Field(default_factory=list)
    runtime_count: int = 0
    live_runtime_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    created_at: str


class SkillStudioSourceTraceList(BaseModel):
    source_traces: list[SkillStudioSourceTrace] = Field(default_factory=list)
    source_trace_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    raw_content_included: bool = False
    used_in_ai_prompt: bool = False
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
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    requires_evaluation: bool = True
    source_trace_required: bool = True
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
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    source_trace_required: bool = True
    raw_content_included: bool = False
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
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    source_trace_required: bool = True
    promotion_ready: bool = False
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
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
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
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False


class SkillStudioAuditTimeline(BaseModel):
    events: list[SkillStudioAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class SkillStudioSafetyStatus(BaseModel):
    safety_checklist: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    all_safety_checks_passed: bool = True
    mock_metadata_only: bool = True
    raw_content_included: bool = False
    live_ai_call_executed: bool = False
    auto_publish_enabled: bool = False
    published_to_registry: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)
