from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaCaseOSStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_case_os"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    aggregates_personal_alpha_workflow: bool = True
    aggregated_versions: list[str] = Field(default_factory=list)
    case_os_enabled: bool = True
    final_report_generation_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    manual_review_required: bool = True
    lawyer_review_required: bool = True
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    raw_quote_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False


class PersonalAlphaCaseOSProfile(BaseModel):
    case_id: str
    title: str = "Personal Alpha Demo Case"
    case_type: str = "personal_alpha_mock"
    jurisdiction: str = "mock_or_redacted"
    client_name: str = "redacted_or_mock"
    opposing_party: str = "redacted_or_mock"
    mock_or_redacted_only: bool = True


class PersonalAlphaCaseOSStageState(BaseModel):
    stage_id: str
    label: str
    status: str = "pending"
    ready: bool = False
    blocked: bool = False
    required: bool = True
    next_action: str | None = None
    target_route: str | None = None
    target_id: str | None = None
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False


class PersonalAlphaCaseOSStageSummary(BaseModel):
    workspace: dict[str, Any] = Field(default_factory=dict)
    source_review: dict[str, Any] = Field(default_factory=dict)
    source_review_decision: dict[str, Any] = Field(default_factory=dict)
    final_readiness: dict[str, Any] = Field(default_factory=dict)
    final_gate: dict[str, Any] = Field(default_factory=dict)
    final_packet: dict[str, Any] = Field(default_factory=dict)
    lawyer_final_review: dict[str, Any] = Field(default_factory=dict)
    final_lock: dict[str, Any] = Field(default_factory=dict)


class PersonalAlphaCaseOSNextAction(BaseModel):
    case_id: str
    current_stage: str
    next_action: str
    next_action_label: str
    target_route: str
    target_id: str | None = None
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSActionEligibilityItem(BaseModel):
    action: str
    label: str
    eligible: bool = False
    target_route: str
    blocked_reasons: list[str] = Field(default_factory=list)
    required_confirmations: list[str] = Field(default_factory=list)
    requires: list[str] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False


class PersonalAlphaCaseOSActionEligibility(BaseModel):
    case_id: str
    actions: list[PersonalAlphaCaseOSActionEligibilityItem] = Field(default_factory=list)
    action: str | None = None
    eligible: bool = False
    requires: list[str] = Field(default_factory=list)
    blocked_reasons: list[str] = Field(default_factory=list)
    current_stage: str
    next_action: str
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSStageTransition(BaseModel):
    from_stage: str
    to_stage: str
    transition_status: str
    allowed: bool = False
    reason: str
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False


class PersonalAlphaCaseOSStageTransitions(BaseModel):
    case_id: str
    transitions: list[PersonalAlphaCaseOSStageTransition] = Field(default_factory=list)
    current_stage: str
    next_action: str
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSStageBlocker(BaseModel):
    stage_id: str
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False


class PersonalAlphaCaseOSBlockers(BaseModel):
    case_id: str
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    stage_blockers: list[PersonalAlphaCaseOSStageBlocker] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSStageOrchestration(BaseModel):
    case_id: str
    current_stage: str
    next_action: str
    next_action_label: str
    target_route: str
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    stage_order: list[str] = Field(default_factory=list)
    stages: list[PersonalAlphaCaseOSStageState] = Field(default_factory=list)
    action_eligibility: PersonalAlphaCaseOSActionEligibility
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSCaseListItem(BaseModel):
    case_id: str
    title: str
    workspace_id: str = ""
    current_stage: str
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    next_action: str
    latest_workspace_run_id: str | None = None
    latest_packet_id: str | None = None
    latest_lock_id: str | None = None
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    updated_at: str = ""


class PersonalAlphaCaseOSAuditEvent(BaseModel):
    timeline_event_id: str
    case_id: str
    workspace_run_id: str = ""
    stage_id: str
    event_type: str = "metadata_stage_status"
    result: str = "metadata_ready"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    created_at: str = ""


class PersonalAlphaCaseOSAuditTimeline(BaseModel):
    case_id: str
    timeline: list[dict[str, Any]] = Field(default_factory=list)
    event_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSAuditTimelineFilters(BaseModel):
    stage_id: str | None = None
    event_type: str | None = None
    result: str | None = None
    safety_status: str | None = None
    limit: int = 100
    offset: int = 0


class PersonalAlphaCaseOSUnifiedAuditEvent(BaseModel):
    timeline_event_id: str
    case_id: str
    workspace_run_id: str | None = None
    packet_id: str | None = None
    lock_id: str | None = None
    stage_id: str
    module: str
    event_type: str = "metadata_stage_status"
    result: str = "metadata_ready"
    safety_status: str = "safe_metadata_only"
    actor_id: str = "local_metadata_reviewer"
    action: str | None = None
    target_id: str | None = None
    message: str = ""
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    redacted: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaCaseOSUnifiedAuditTimeline(BaseModel):
    case_id: str
    filters: PersonalAlphaCaseOSAuditTimelineFilters
    timeline: list[PersonalAlphaCaseOSUnifiedAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    returned_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSAuditStageSummary(BaseModel):
    stage_id: str
    event_count: int = 0
    latest_result: str | None = None
    blocked: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSAuditTimelineSummaryStats(BaseModel):
    total_events: int = 0
    stage_count: int = 0
    blocked_event_count: int = 0
    warning_event_count: int = 0
    redacted_event_count: int = 0
    unsafe_event_count: int = 0
    raw_content_event_count: int = 0
    latest_event_at: str | None = None
    modules: list[str] = Field(default_factory=list)
    stages: list[PersonalAlphaCaseOSAuditStageSummary] = Field(default_factory=list)


class PersonalAlphaCaseOSAuditTimelineSummary(BaseModel):
    case_id: str
    summary: PersonalAlphaCaseOSAuditTimelineSummaryStats
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSUnsafeAuditEventSummary(BaseModel):
    timeline_event_id: str
    field_name: str
    reason: str


class PersonalAlphaCaseOSAuditTimelineRedactionStats(BaseModel):
    passed: bool = True
    unsafe_event_count: int = 0
    raw_content_event_count: int = 0
    path_like_value_count: int = 0
    api_key_like_value_count: int = 0
    personal_identifier_like_value_count: int = 0
    redacted_event_count: int = 0
    checked_fields: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSAuditTimelineRedactionCheck(BaseModel):
    case_id: str
    redaction_check: PersonalAlphaCaseOSAuditTimelineRedactionStats
    unsafe_events: list[PersonalAlphaCaseOSUnsafeAuditEventSummary] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSAuditTimelineAvailableFilters(BaseModel):
    case_id: str
    available_filters: dict[str, list[str]] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSReviewState(BaseModel):
    case_id: str
    review_state: str
    review_state_label: str
    current_stage: str
    next_action: str
    target_route: str | None = None
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    terminal: bool = False
    completed_metadata_review: bool = False
    state_source: str = "derived_from_case_os_metadata"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSReviewStateHistoryItem(BaseModel):
    state_history_id: str
    from_state: str
    to_state: str
    transition: str
    result: str = "metadata_transition_available"
    source_event_id: str
    stage_id: str
    module: str
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    created_at: str = ""


class PersonalAlphaCaseOSReviewStateHistory(BaseModel):
    case_id: str
    history: list[PersonalAlphaCaseOSReviewStateHistoryItem] = Field(default_factory=list)
    history_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSReviewStateTransition(BaseModel):
    transition: str
    from_state: str
    to_state: str
    allowed: bool = False
    reason: str
    target_action: str | None = None
    target_route: str | None = None
    required_confirmations: list[str] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False


class PersonalAlphaCaseOSReviewStateTransitions(BaseModel):
    case_id: str
    current_state: str
    available_transitions: list[PersonalAlphaCaseOSReviewStateTransition] = Field(default_factory=list)
    blocked_transitions: list[PersonalAlphaCaseOSReviewStateTransition] = Field(default_factory=list)
    terminal: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSReviewStateTransitionValidation(BaseModel):
    case_id: str
    from_state: str
    to_state: str
    transition: str
    allowed: bool = False
    valid_transition: bool = False
    would_execute_action: bool = False
    target_action: str | None = None
    target_route: str | None = None
    blocked_reasons: list[str] = Field(default_factory=list)
    required_confirmations: list[str] = Field(default_factory=list)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSReviewStateSummaryStats(BaseModel):
    review_state: str
    terminal: bool = False
    completed_metadata_review: bool = False
    blocked: bool = False
    history_count: int = 0
    available_transition_count: int = 0
    blocked_transition_count: int = 0
    next_action: str
    target_route: str | None = None
    requires_manual_review: bool = True
    requires_lawyer_review: bool = True


class PersonalAlphaCaseOSReviewStateSummary(BaseModel):
    case_id: str
    summary: PersonalAlphaCaseOSReviewStateSummaryStats
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSFinalLockSummary(BaseModel):
    lock_id: str | None = None
    packet_id: str | None = None
    workspace_run_id: str | None = None
    lock_status: str = "final_lock_pending"
    locked_metadata_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    created_at: str | None = None


class PersonalAlphaCaseOSLinkedMetadata(BaseModel):
    workspace_run_id: str | None = None
    packet_id: str | None = None
    lawyer_review_action_id: str | None = None
    lock_id: str | None = None


class PersonalAlphaCaseOSFinalLockConsolidation(BaseModel):
    case_id: str
    consolidation_status: str = "final_lock_pending"
    final_lock_created: bool = False
    latest_lock_id: str | None = None
    latest_packet_id: str | None = None
    latest_lawyer_review_action: str | None = None
    review_state: str = "blocked"
    completed_metadata_review: bool = False
    final_lock_summary: PersonalAlphaCaseOSFinalLockSummary
    linked_metadata: PersonalAlphaCaseOSLinkedMetadata
    safety_checklist: PersonalAlphaCaseOSSafetyChecklist
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSMetadataClosureSummary(BaseModel):
    workspace_run_ready: bool = False
    source_review_completed: bool = False
    source_decision_completed: bool = False
    final_readiness_ready: bool = False
    final_gate_approved: bool = False
    final_packet_created: bool = False
    lawyer_review_approved: bool = False
    final_lock_created: bool = False
    audit_timeline_available: bool = False
    redaction_check_passed: bool = False


class PersonalAlphaCaseOSMetadataClosureChecklistItem(BaseModel):
    check_id: str
    label: str
    passed: bool = False
    required: bool = True
    source: str
    mock_or_redacted_only: bool = True


class PersonalAlphaCaseOSMetadataClosureChecklist(BaseModel):
    case_id: str
    checklist: list[PersonalAlphaCaseOSMetadataClosureChecklistItem] = Field(default_factory=list)
    passed_count: int = 0
    failed_count: int = 0
    required_failed_count: int = 0
    closure_ready: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSMetadataClosure(BaseModel):
    case_id: str
    closure_status: str = "blocked"
    completed_metadata_review: bool = False
    closure_ready: bool = False
    review_state: str = "blocked"
    terminal: bool = False
    blocked: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    closure_summary: PersonalAlphaCaseOSMetadataClosureSummary
    next_action: str = "resolve_blockers"
    target_route: str = "/case-os"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSMetadataClosureBlocker(BaseModel):
    blocker_id: str
    stage_id: str
    blocked: bool = False
    reason: str | None = None
    required_action: str | None = None
    target_route: str | None = None
    mock_or_redacted_only: bool = True


class PersonalAlphaCaseOSMetadataClosureBlockers(BaseModel):
    case_id: str
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    closure_blockers: list[PersonalAlphaCaseOSMetadataClosureBlocker] = Field(default_factory=list)
    required_blocker_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSMetadataClosureExportSection(BaseModel):
    section_id: str
    title: str
    included: bool = True
    raw_content_included: bool = False
    item_count: int = 0


class PersonalAlphaCaseOSMetadataClosureExportPreviewPayload(BaseModel):
    title: str = "Personal Alpha Metadata Closure Preview"
    export_type: str = "metadata_only_preview"
    sections: list[PersonalAlphaCaseOSMetadataClosureExportSection] = Field(default_factory=list)


class PersonalAlphaCaseOSMetadataClosureExportPreview(BaseModel):
    case_id: str
    export_preview: PersonalAlphaCaseOSMetadataClosureExportPreviewPayload
    can_export_metadata_preview: bool = False
    would_create_file: bool = False
    would_include_raw_content: bool = False
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaCaseOSCaseDetail(BaseModel):
    case_id: str
    title: str
    workspace_id: str = ""
    current_stage: str
    blocked: bool = False
    blocked_reasons: list[str] = Field(default_factory=list)
    next_action: str
    profile: dict[str, Any] = Field(default_factory=dict)
    workspace_runs: list[dict[str, Any]] = Field(default_factory=list)
    stage_summary: dict[str, Any] = Field(default_factory=dict)
    source_review: dict[str, Any] = Field(default_factory=dict)
    source_review_decision: dict[str, Any] = Field(default_factory=dict)
    final_readiness: dict[str, Any] = Field(default_factory=dict)
    final_gate: dict[str, Any] = Field(default_factory=dict)
    final_packet: dict[str, Any] = Field(default_factory=dict)
    lawyer_final_review: dict[str, Any] = Field(default_factory=dict)
    final_lock: dict[str, Any] = Field(default_factory=dict)
    audit_timeline: list[dict[str, Any]] = Field(default_factory=list)
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)
