from pydantic import BaseModel, Field


SAFETY_FLAGS: dict[str, bool] = {
    "owner_only": True,
    "metadata_only": True,
    "training_artifact_only": True,
    "codex_training_scheme": True,
    "fine_tune_model_training": False,
    "closed_case_only": True,
    "open_case_data_used": False,
    "raw_content_included": False,
    "raw_ocr_content_included": False,
    "api_key_exposed": False,
    "secret_value_returned": False,
    "local_path_exposed": False,
    "training_data_generated": False,
    "writes_to_training_set": False,
    "skill_updated": False,
    "skill_published": False,
    "skill_auto_published": False,
    "case_cause_taxonomy_required": True,
    "multi_level_case_cause_enabled": True,
    "case_cause_match_required": True,
    "fallback_supported": True,
    "load_dry_run": True,
    "load_executed": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "public_link_created": False,
    "email_sent": False,
    "external_delivery_triggered": False,
    "gate_reference_only": True,
    "blocks_next_stage": False,
    "audit_required": True,
}


def safety_flags() -> dict[str, bool]:
    return dict(SAFETY_FLAGS)


class TrainingArtifactSafetyBase(BaseModel):
    owner_only: bool = True
    metadata_only: bool = True
    training_artifact_only: bool = True
    codex_training_scheme: bool = True
    fine_tune_model_training: bool = False
    closed_case_only: bool = True
    open_case_data_used: bool = False
    raw_content_included: bool = False
    raw_ocr_content_included: bool = False
    api_key_exposed: bool = False
    secret_value_returned: bool = False
    local_path_exposed: bool = False
    training_data_generated: bool = False
    writes_to_training_set: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    skill_auto_published: bool = False
    case_cause_taxonomy_required: bool = True
    multi_level_case_cause_enabled: bool = True
    case_cause_match_required: bool = True
    fallback_supported: bool = True
    load_dry_run: bool = True
    load_executed: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False
    gate_reference_only: bool = True
    blocks_next_stage: bool = False
    audit_required: bool = True


class CodexTrainingScheme(TrainingArtifactSafetyBase):
    scheme_id: str = "codex_training_scheme_v7_30"
    scheme_version: str = "v7.30"
    display_name: str = "Codex Training Scheme & Multi-Level Case-Cause Artifact Loader"
    display_name_cn: str = "Codex 训练方案与多层级案由产物加载器"
    target_skill_ids: list[str] = Field(default_factory=lambda: ["case_fact_extraction_skill", "case_legal_analysis_skill"])
    source_material_policy: dict[str, bool] = Field(default_factory=lambda: {
        "closed_case_only": True,
        "open_case_forbidden": True,
        "redaction_required": True,
        "raw_content_allowed": False,
    })
    case_cause_taxonomy_required: bool = True
    multi_level_case_cause_enabled: bool = True
    training_steps: list[str] = Field(default_factory=list)
    output_artifacts: list[str] = Field(default_factory=list)
    validation_steps: list[str] = Field(default_factory=list)
    loading_requirements: list[str] = Field(default_factory=list)
    safety_boundaries: dict[str, bool] = Field(default_factory=safety_flags)
    warnings: list[str] = Field(default_factory=list)


class CaseCauseNode(TrainingArtifactSafetyBase):
    case_cause_id: str
    case_domain: str
    case_cause_code: str
    case_cause_name: str
    level: int
    case_cause_path: list[str]
    parent_id: str | None = None
    child_ids: list[str] = Field(default_factory=list)
    applicable_dispute_types: list[str] = Field(default_factory=list)
    applicable_fact_patterns: list[str] = Field(default_factory=list)
    applicable_legal_patterns: list[str] = Field(default_factory=list)
    evidence_types: list[str] = Field(default_factory=list)
    jurisdiction_scope: str = "中国大陆"


class CaseCauseTaxonomyManifest(TrainingArtifactSafetyBase):
    taxonomy_id: str = "case_cause_taxonomy_v7_30"
    taxonomy_version: str = "v7.30"
    nodes: list[CaseCauseNode] = Field(default_factory=list)
    node_count: int = 0
    supported_levels: list[int] = Field(default_factory=lambda: [1, 2, 3])
    warnings: list[str] = Field(default_factory=list)


class CaseCauseMatchRequest(BaseModel):
    case_domain: str = "civil"
    case_cause_level_1: str = "contract_dispute"
    case_cause_level_2: str = "sales_contract_dispute"
    case_cause_level_3: str | None = None
    case_cause_name: str = "买卖合同纠纷"
    case_cause_code: str = "civil.contract.sales"
    case_cause_path: list[str] = Field(default_factory=lambda: ["civil", "contract_dispute", "sales_contract_dispute"])
    evidence_types: list[str] = Field(default_factory=lambda: ["contract", "invoice", "delivery_record"])


class ExperiencePackageManifest(TrainingArtifactSafetyBase):
    package_id: str
    package_name: str
    package_type: str
    source_case_mode: str = "closed_case"
    source_case_count: int = 0
    redaction_required: bool = True
    target_skill_ids: list[str] = Field(default_factory=list)
    case_cause_scope: str
    case_cause_path: list[str] = Field(default_factory=list)
    case_cause_level: int = 0
    case_cause_ids: list[str] = Field(default_factory=list)
    parent_package_ids: list[str] = Field(default_factory=list)
    fallback_package_ids: list[str] = Field(default_factory=list)
    priority: int = 100
    load_strategy: str
    applicable_patterns: list[str] = Field(default_factory=list)
    extracted_patterns: list[str] = Field(default_factory=list)
    reasoning_templates: list[str] = Field(default_factory=list)
    source_trace_policy: dict[str, bool] = Field(default_factory=dict)
    evidence_types: list[str] = Field(default_factory=list)


class SkillManifest(TrainingArtifactSafetyBase):
    skill_id: str
    skill_name: str
    skill_type: str
    source_package_ids: list[str] = Field(default_factory=list)
    derived_from: list[str] = Field(default_factory=list)
    baseline_complete: bool = True
    case_cause_scope: str = "multi_level_case_cause"
    supported_case_cause_paths: list[list[str]] = Field(default_factory=list)
    fallback_supported: bool = True
    pattern_sections: dict[str, list[str]] = Field(default_factory=dict)
    prompt_templates: list[str] = Field(default_factory=list)
    test_case_ids: list[str] = Field(default_factory=list)
    evaluation_id: str
    gate_id: str
    loading_status: str = "metadata_ready"
    optimization_suggestions: list[str] = Field(default_factory=list)


class EvaluationManifest(TrainingArtifactSafetyBase):
    evaluation_id: str
    target_skill_id: str
    dimensions: list[str] = Field(default_factory=list)
    score_policy: str = "reference_only"
    optimization_fields: list[str] = Field(default_factory=list)


class GateManifest(TrainingArtifactSafetyBase):
    gate_id: str
    target_skill_id: str
    gate_fields: list[str] = Field(default_factory=list)
    gate_status: str = "reference_only"


class TestCaseManifest(TrainingArtifactSafetyBase):
    test_case_id: str
    target_skill_id: str
    scenario_type: str
    case_cause_path: list[str] = Field(default_factory=list)
    expected_metadata_fields: list[str] = Field(default_factory=list)


class LoadingManifest(TrainingArtifactSafetyBase):
    loading_manifest_id: str
    supported_load_strategies: list[str] = Field(default_factory=list)
    merge_order: list[str] = Field(default_factory=list)
    conflict_resolution: list[str] = Field(default_factory=list)
    dry_run_required: bool = True


class CaseCauseMatchResult(TrainingArtifactSafetyBase):
    match_id: str
    requested_case_cause_path: list[str] = Field(default_factory=list)
    matched_case_cause_id: str | None = None
    exact_package_ids: list[str] = Field(default_factory=list)
    ancestor_fallback_package_ids: list[str] = Field(default_factory=list)
    common_package_ids: list[str] = Field(default_factory=list)
    evidence_overlay_package_ids: list[str] = Field(default_factory=list)
    selected_package_ids: list[str] = Field(default_factory=list)
    fallback_chain: list[str] = Field(default_factory=list)
    merge_order: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LoadDryRunRequest(CaseCauseMatchRequest):
    target_skill_ids: list[str] = Field(default_factory=lambda: ["case_fact_extraction_skill", "case_legal_analysis_skill"])
    explicit_dry_run_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_open_case_training_confirmation: bool = True
    explicit_no_auto_publish_confirmation: bool = True


class SkillContextManifest(TrainingArtifactSafetyBase):
    skill_context_id: str
    source_match_id: str
    selected_skill_ids: list[str] = Field(default_factory=list)
    selected_package_ids: list[str] = Field(default_factory=list)
    case_cause_path: list[str] = Field(default_factory=list)
    fallback_chain: list[str] = Field(default_factory=list)
    merge_metadata: dict[str, list[str] | str | bool] = Field(default_factory=dict)
    lineage: dict[str, list[str] | str] = Field(default_factory=dict)
    quality: dict[str, int | str | list[str]] = Field(default_factory=dict)
    gate: dict[str, bool | str] = Field(default_factory=dict)
    optimization_suggestions: list[str] = Field(default_factory=list)


class LoadDryRunRecord(TrainingArtifactSafetyBase):
    run_id: str
    run_status: str = "dry_run_completed"
    match_result: CaseCauseMatchResult
    skill_context: SkillContextManifest
    warnings: list[str] = Field(default_factory=list)


class ArtifactListResponse(TrainingArtifactSafetyBase):
    artifacts: list[dict] = Field(default_factory=list)
    artifact_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrainingArtifactStatus(TrainingArtifactSafetyBase):
    version: str = "v7.30"
    status: str = "metadata_ready"
    training_artifact_loader_ready: bool = True
    codex_training_scheme_ready: bool = True
    case_cause_taxonomy_ready: bool = True
    multi_level_loader_ready: bool = True
    experience_package_manifest_ready: bool = True
    skill_manifest_loader_ready: bool = True
    fallback_ready: bool = True
    skill_context_dry_run_ready: bool = True
    package_count: int = 0
    skill_count: int = 0
    taxonomy_node_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CodexTrainingRunSafetyBase(TrainingArtifactSafetyBase):
    codex_training: bool = True
    training_run_generated: bool = True
    redaction_completed: bool = True
    quality_reference_only: bool = True


class CodexTrainingRunRequest(BaseModel):
    source_case_mode: str = "synthetic_closed_case"
    target_case_cause_paths: list[list[str]] = Field(
        default_factory=lambda: [
            ["civil", "contract_dispute", "sales_contract_dispute"],
            ["civil", "contract_dispute", "loan_contract_dispute"],
            ["civil", "tort_dispute", "traffic_accident_dispute"],
            ["civil", "marriage_inheritance", "divorce_dispute"],
            ["civil", "labor_dispute", "labor_contract_dispute"],
        ]
    )
    target_skill_ids: list[str] = Field(default_factory=lambda: ["case_fact_extraction_skill", "case_legal_analysis_skill"])
    explicit_closed_case_only_confirmation: bool = True
    explicit_redaction_confirmation: bool = True
    explicit_no_raw_content_confirmation: bool = True
    explicit_no_open_case_training_confirmation: bool = True
    explicit_no_auto_publish_confirmation: bool = True


class ClosedCaseTrainingSample(CodexTrainingRunSafetyBase):
    sample_id: str
    source_case_mode: str = "synthetic_closed_case"
    case_domain: str
    case_cause_level_1: str
    case_cause_level_2: str
    case_cause_level_3: str | None = None
    case_cause_name: str
    case_cause_code: str
    case_cause_path: list[str]
    parent_case_cause_id: str
    case_cause_scope: str
    applicable_fact_patterns: list[str] = Field(default_factory=list)
    applicable_legal_relationships: list[str] = Field(default_factory=list)
    applicable_evidence_types: list[str] = Field(default_factory=list)
    applicable_claim_basis: list[str] = Field(default_factory=list)
    applicable_defense_patterns: list[str] = Field(default_factory=list)
    fallback_case_cause_path: list[str] = Field(default_factory=list)


class GeneratedTrainingRunManifest(CodexTrainingRunSafetyBase):
    training_run_id: str
    version: str = "v7.31"
    source_case_mode: str = "synthetic_closed_case"
    source_case_count: int
    synthetic_case_count: int
    target_skill_ids: list[str]
    case_cause_paths: list[list[str]]
    generated_artifact_ids: list[str]
    loading_manifest_id: str
    safety_status: dict[str, bool] = Field(default_factory=safety_flags)
    created_at: str


class GeneratedExperiencePackageManifest(CodexTrainingRunSafetyBase):
    package_id: str
    package_name: str
    case_cause_scope: str
    case_cause_path: list[str]
    case_cause_level: int
    parent_package_ids: list[str] = Field(default_factory=list)
    fallback_package_ids: list[str] = Field(default_factory=list)
    priority: int
    load_strategy: str
    source_case_mode: str = "synthetic_closed_case"
    target_skill_ids: list[str] = Field(default_factory=list)
    extracted_patterns: list[str] = Field(default_factory=list)
    reasoning_templates: list[str] = Field(default_factory=list)
    evidence_rules: list[str] = Field(default_factory=list)
    source_trace_policy: dict[str, bool] = Field(default_factory=dict)


class GeneratedSkillManifest(CodexTrainingRunSafetyBase):
    skill_id: str
    skill_name: str
    skill_type: str
    version_label: str = "v7.31"
    source_package_ids: list[str] = Field(default_factory=list)
    case_cause_scope: str = "multi_level_case_cause"
    derived_from: list[str] = Field(default_factory=list)
    baseline_complete: bool = False
    pattern_sections: dict[str, list[str]] = Field(default_factory=dict)
    prompt_templates: list[str] = Field(default_factory=list)
    test_case_ids: list[str] = Field(default_factory=list)
    evaluation_manifest_id: str
    gate_manifest_id: str
    loading_status: str = "generated_metadata_ready"
    skill_published: bool = False
    optimization_suggestions: list[str] = Field(default_factory=list)


class GeneratedEvaluationManifest(CodexTrainingRunSafetyBase):
    evaluation_id: str
    skill_id: str
    case_cause_scope: str
    evaluation_scope: str
    dimension_scores_schema: dict[str, str] = Field(default_factory=dict)
    overall_score_schema: dict[str, str] = Field(default_factory=dict)
    optimization_suggestions_schema: dict[str, str] = Field(default_factory=dict)
    quality_reference_only: bool = True


class GeneratedGateManifest(CodexTrainingRunSafetyBase):
    gate_id: str
    skill_id: str
    case_cause_scope: str
    gate_status_values: list[str] = Field(default_factory=list)
    optimization_required: bool = False
    no_auto_publish: bool = True


class GeneratedTestCaseManifest(CodexTrainingRunSafetyBase):
    test_case_id: str
    skill_id: str
    case_cause_path: list[str]
    test_case_name: str
    source_package_id: str
    input_metadata_schema: dict[str, str] = Field(default_factory=dict)
    expected_output_metadata_schema: dict[str, str] = Field(default_factory=dict)


class GeneratedLoadingManifest(CodexTrainingRunSafetyBase):
    loading_manifest_id: str
    artifact_version: str = "v7.31"
    skill_ids: list[str] = Field(default_factory=list)
    package_ids: list[str] = Field(default_factory=list)
    evaluation_ids: list[str] = Field(default_factory=list)
    gate_ids: list[str] = Field(default_factory=list)
    test_case_ids: list[str] = Field(default_factory=list)
    case_cause_match_strategy: str
    load_order_by_case_cause: list[str] = Field(default_factory=list)
    fallback_order: list[str] = Field(default_factory=list)
    conflict_resolution_policy: list[str] = Field(default_factory=list)
    checksum_metadata: dict[str, str] = Field(default_factory=dict)
    compatible_runtime_modules: list[str] = Field(default_factory=list)
    validation_required: bool = True
    system_loads_metadata_only: bool = True


class CodexTrainingRunRecord(CodexTrainingRunSafetyBase):
    training_run_id: str
    run_status: str = "generated_metadata_ready"
    manifest: GeneratedTrainingRunManifest
    baseline_discovery: dict[str, bool | list[str] | str] = Field(default_factory=dict)
    training_samples: list[ClosedCaseTrainingSample] = Field(default_factory=list)
    experience_packages: list[GeneratedExperiencePackageManifest] = Field(default_factory=list)
    generated_skills: list[GeneratedSkillManifest] = Field(default_factory=list)
    evaluations: list[GeneratedEvaluationManifest] = Field(default_factory=list)
    gates: list[GeneratedGateManifest] = Field(default_factory=list)
    test_cases: list[GeneratedTestCaseManifest] = Field(default_factory=list)
    loading_manifest: GeneratedLoadingManifest
    load_dry_run_result: dict | None = None
    warnings: list[str] = Field(default_factory=list)


class CodexTrainingRunList(CodexTrainingRunSafetyBase):
    training_runs: list[CodexTrainingRunRecord] = Field(default_factory=list)
    run_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class RealClosedCaseIntakeSafetyBase(TrainingArtifactSafetyBase):
    real_closed_case_intake: bool = True
    redaction_required: bool = True
    redaction_completed: bool = False
    source_trace_required: bool = True
    manual_review_required: bool = True
    ready_for_codex_training: bool = False


class RealClosedCaseTrainingIntakeRequest(BaseModel):
    case_reference_label: str = "closed_case_training_intake_metadata_001"
    owner_user_id: str = "owner_local_demo"
    authorization_confirmed: bool = True
    case_closed_confirmed: bool = True
    target_case_cause_path: list[str] = Field(default_factory=lambda: ["civil", "contract_dispute", "sales_contract_dispute"])
    target_skill_ids: list[str] = Field(default_factory=lambda: ["case_fact_extraction_skill", "case_legal_analysis_skill"])
    explicit_no_raw_content_confirmation: bool = True
    explicit_no_open_case_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True


class RealClosedCaseTrainingIntake(RealClosedCaseIntakeSafetyBase):
    intake_id: str
    source_case_mode: str = "real_closed_case"
    case_reference_label: str
    owner_user_id: str
    authorization_confirmed: bool = True
    case_closed_confirmed: bool = True
    redaction_status: str = "pending_redaction"
    raw_content_retained: bool = False
    raw_content_exported: bool = False
    target_case_cause_path: list[str] = Field(default_factory=list)
    target_skill_ids: list[str] = Field(default_factory=list)
    status: str = "intake_metadata_created"
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class RedactionReport(RealClosedCaseIntakeSafetyBase):
    redaction_report_id: str
    intake_id: str
    redaction_completed: bool = True
    personal_identifiers_removed: bool = True
    client_identity_removed: bool = True
    phone_removed: bool = True
    id_number_removed: bool = True
    address_removed: bool = True
    raw_ocr_removed: bool = True
    legal_relevance_preserved: bool = True
    jurisdiction_context_preserved: bool = True
    age_capacity_context_preserved: bool = True
    redaction_notes: list[str] = Field(default_factory=list)
    safety_status: dict[str, bool] = Field(default_factory=dict)


class CaseCauseClassification(RealClosedCaseIntakeSafetyBase):
    classification_id: str
    intake_id: str
    case_domain: str = "civil"
    case_cause_level_1: str = "contract_dispute"
    case_cause_level_2: str = "sales_contract_dispute"
    case_cause_level_3: str | None = None
    case_cause_name: str = "买卖合同纠纷"
    case_cause_code: str = "civil.contract.sales"
    case_cause_path: list[str] = Field(default_factory=lambda: ["civil", "contract_dispute", "sales_contract_dispute"])
    confidence_score: float = 0.82
    fallback_case_cause_path: list[str] = Field(default_factory=lambda: ["civil", "contract_dispute"])
    classification_notes: list[str] = Field(default_factory=list)


class TrainingSampleSegment(RealClosedCaseIntakeSafetyBase):
    segment_id: str
    intake_id: str
    segment_type: str
    case_cause_path: list[str] = Field(default_factory=list)
    target_skill_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    review_status: str = "manual_review_required"
    segment_metadata: dict[str, str | bool | list[str]] = Field(default_factory=dict)


class TrainingIntakeReviewItem(RealClosedCaseIntakeSafetyBase):
    review_item_id: str
    intake_id: str
    review_type: str
    review_status: str = "pending_manual_review"
    action_allowed: list[str] = Field(default_factory=list)
    reviewed_by: str | None = None
    reviewer_note: str | None = None


class TrainingIntakeReviewActionRequest(BaseModel):
    action: str = "approve_metadata_only"
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str = "metadata review only"
    explicit_manual_review_confirmation: bool = True
    explicit_no_raw_content_confirmation: bool = True
    explicit_no_training_set_write_confirmation: bool = True


class TrainingIntakeSourceTrace(RealClosedCaseIntakeSafetyBase):
    source_trace_id: str
    intake_id: str
    source_type: str
    source_label: str
    retained_metadata_fields: list[str] = Field(default_factory=list)
    raw_content_returned: bool = False


class RealClosedCaseTrainingIntakeRecord(RealClosedCaseIntakeSafetyBase):
    intake: RealClosedCaseTrainingIntake
    redaction_report: RedactionReport | None = None
    classification: CaseCauseClassification | None = None
    segments: list[TrainingSampleSegment] = Field(default_factory=list)
    review_queue: list[TrainingIntakeReviewItem] = Field(default_factory=list)
    source_traces: list[TrainingIntakeSourceTrace] = Field(default_factory=list)
    audit_events: list[dict[str, str | bool]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class RealClosedCaseTrainingIntakeList(RealClosedCaseIntakeSafetyBase):
    intakes: list[RealClosedCaseTrainingIntake] = Field(default_factory=list)
    intake_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class RealClosedCaseIntakeStatus(RealClosedCaseIntakeSafetyBase):
    version: str = "v7.31a"
    status: str = "real_closed_case_intake_metadata_ready"
    intake_pipeline_ready: bool = True
    redaction_pipeline_ready: bool = True
    case_cause_classification_ready: bool = True
    training_sample_segmentation_ready: bool = True
    source_trace_ready: bool = True
    review_queue_ready: bool = True
    audit_ready: bool = True
    safety_ready: bool = True
    intake_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731bSafetyBase(BaseModel):
    owner_only: bool = True
    local_private_processing_only: bool = True
    authorized_case_only: bool = True
    closed_case_preferred: bool = True
    work_product_sensitive: bool = True
    raw_material_controlled: bool = True
    raw_material_allowed_for_internal_processing: bool = True
    raw_material_return_allowed: bool = False
    raw_material_provider_export_allowed: bool = False
    raw_material_skill_ingest_allowed: bool = False
    redacted_output_only: bool = True
    redacted_experience_output_required: bool = True
    manual_review_required: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_raw_response_returned: bool = False
    original_material_returned: bool = False
    open_case_data_used: bool = False
    formal_training_set_generated: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class RawWorkProductBoundaryStatus(V731bSafetyBase):
    version: str = "v7.31b"
    status: str = "raw_work_product_controlled_boundary_ready"
    boundary_runtime_ready: bool = True
    ordinary_frontend_return_blocked: bool = True
    skill_direct_ingest_blocked: bool = True
    training_result_direct_ingest_blocked: bool = True
    provider_export_blocked: bool = True
    warnings: list[str] = Field(default_factory=list)


class OcrJobRequest(BaseModel):
    material_label: str = "lawyer_work_product_demo_material"
    owner_user_id: str = "owner_local_demo"
    document_type: str = "case_work_product"
    page_count: int = 8
    explicit_authorized_case_confirmation: bool = True
    explicit_internal_processing_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_raw_return_confirmation: bool = True


class OcrParseSummary(V731bSafetyBase):
    parse_summary_id: str
    job_id: str
    document_type: str
    page_count: int
    confidence_score: float = 0.86
    parse_status: str = "demo_safe_parse_completed"
    redacted_preview: str = "已脱敏办案底稿结构摘要"
    structured_summary: list[str] = Field(default_factory=list)
    section_labels: list[str] = Field(default_factory=list)
    source_trace_id: str
    audit_id: str


class OcrJob(V731bSafetyBase):
    job_id: str
    material_label: str
    owner_user_id: str
    document_type: str
    page_count: int
    parse_status: str = "demo_safe_parse_completed"
    parse_summary: OcrParseSummary
    source_trace_id: str
    audit_events: list[dict[str, str | bool]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class OcrJobList(V731bSafetyBase):
    ocr_jobs: list[OcrJob] = Field(default_factory=list)
    job_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class LegalRetrievalJobRequest(BaseModel):
    source_ocr_job_id: str | None = None
    query_label: str = "contract_dispute_experience_basis"
    owner_user_id: str = "owner_local_demo"
    explicit_no_provider_confirmation: bool = True
    explicit_no_key_value_confirmation: bool = True
    explicit_demo_safe_confirmation: bool = True


class LegalRetrievalCandidate(V731bSafetyBase):
    candidate_id: str
    candidate_type: str
    title: str
    summary: str
    source_trace_id: str


class LegalRetrievalJob(V731bSafetyBase):
    retrieval_job_id: str
    source_ocr_job_id: str | None = None
    query_label: str
    retrieval_status: str = "demo_safe_retrieval_completed"
    retrieval_timestamp: str
    statute_candidates: list[LegalRetrievalCandidate] = Field(default_factory=list)
    similar_case_candidates: list[LegalRetrievalCandidate] = Field(default_factory=list)
    source_trace_id: str
    audit_events: list[dict[str, str | bool]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class LegalRetrievalJobList(V731bSafetyBase):
    legal_retrieval_jobs: list[LegalRetrievalJob] = Field(default_factory=list)
    job_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ExperienceCandidateBuildRequest(BaseModel):
    source_ocr_job_id: str | None = None
    source_legal_retrieval_job_id: str | None = None
    owner_user_id: str = "owner_local_demo"
    explicit_redaction_required_confirmation: bool = True
    explicit_manual_review_required_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class ExperienceCandidate(V731bSafetyBase):
    candidate_id: str
    candidate_type: str
    owner_user_id: str
    source_ocr_job_id: str | None = None
    source_legal_retrieval_job_id: str | None = None
    candidate_status: str = "candidate_requires_redaction_review"
    review_status: str = "pending_review"
    skill_experience_ready: bool = False
    redaction_status: str = "requires_redaction"
    pattern_label: str
    structured_summary: list[str] = Field(default_factory=list)
    source_trace_id: str
    audit_events: list[dict[str, str | bool]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ExperienceCandidateList(V731bSafetyBase):
    candidates: list[ExperienceCandidate] = Field(default_factory=list)
    candidate_count: int = 0
    approved_for_skill_experience_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ExperienceCandidateRedaction(V731bSafetyBase):
    candidate_id: str
    redaction_status: str = "redacted_output_ready"
    redacted_summary: str = "已脱敏经验摘要"
    abstracted_pattern: str = "抽象化办案经验模式"
    removed_sensitive_fields_count: int = 6
    redaction_warnings: list[str] = Field(default_factory=list)
    source_trace_id: str
    audit_events: list[dict[str, str | bool]] = Field(default_factory=list)


class ExperienceCandidateReviewRequest(BaseModel):
    action: str = "approve"
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str = "experience candidate metadata review only"
    explicit_manual_review_confirmation: bool = True
    explicit_no_raw_return_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class ExperienceCandidateReview(V731bSafetyBase):
    candidate_id: str
    action: str
    review_status: str
    reviewer_id: str
    reviewer_note: str
    approved_for_skill_experience: bool = False
    skill_experience_ready: bool = False
    skill_published: bool = False
    warnings: list[str] = Field(default_factory=list)


class ExperienceCandidateAudit(V731bSafetyBase):
    candidate_id: str
    events: list[dict[str, str | bool]] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731bTrainingExperiencePipelineStatus(V731bSafetyBase):
    version: str = "v7.31b"
    status: str = "training_experience_pipeline_metadata_ready"
    raw_work_product_boundary_ready: bool = True
    ocr_document_parse_ready: bool = True
    legal_retrieval_ready: bool = True
    experience_candidate_runtime_ready: bool = True
    redacted_experience_output_ready: bool = True
    manual_review_queue_ready: bool = True
    source_trace_ready: bool = True
    audit_ready: bool = True
    safety_ready: bool = True
    ocr_job_count: int = 0
    legal_retrieval_job_count: int = 0
    experience_candidate_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731cSafetyBase(BaseModel):
    owner_only: bool = True
    local_private_processing_only: bool = True
    authorized_case_only: bool = True
    controlled_material_boundary: bool = True
    source_content_returned: bool = False
    redacted_output_only: bool = True
    abstracted_experience_only: bool = True
    approved_experience_only: bool = True
    manual_review_required: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    local_sensitive_reference_returned: bool = False
    unreviewed_experience_imported: bool = False
    unsafe_experience_imported: bool = False
    missing_source_trace_imported: bool = False
    formal_training_set_generated: bool = False
    real_codex_training_triggered: bool = False
    skill_published: bool = False
    skill_publishable: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class SkillExperienceImportRequest(BaseModel):
    source_candidate_ids: list[str] = Field(default_factory=list)
    owner_user_id: str = "owner_local_demo"
    explicit_approved_experience_only_confirmation: bool = True
    explicit_redacted_output_only_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class SkillExperiencePoolEntry(V731cSafetyBase):
    experience_id: str
    source_candidate_id: str
    case_cause: str = "demo_safe_case_cause_scope"
    experience_type: str
    fact_pattern: str
    issue_pattern: str
    evidence_pattern: str
    rule_application_pattern: str
    argument_strategy_pattern: str
    drafting_pattern: str
    risk_warning_pattern: str
    review_checklist_pattern: str
    redaction_summary: str
    abstraction_summary: str
    source_trace_id: str
    audit_id: str
    reviewer_confirmation: str = "approved_for_skill_experience"
    created_at: str
    updated_at: str
    skill_binding_status: str = "unbound"
    warnings: list[str] = Field(default_factory=list)


class SkillExperiencePoolList(V731cSafetyBase):
    experiences: list[SkillExperiencePoolEntry] = Field(default_factory=list)
    experience_count: int = 0
    rejected_import_count: int = 0
    unbound_experience_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillExperiencePoolStatus(V731cSafetyBase):
    version: str = "v7.31c"
    status: str = "skill_experience_pool_metadata_ready"
    pool_ready: bool = True
    import_approved_ready: bool = True
    binding_ready: bool = True
    skill_draft_builder_ready: bool = True
    experience_count: int = 0
    rejected_import_count: int = 0
    unbound_experience_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillExperienceImportResponse(V731cSafetyBase):
    imported_experiences: list[SkillExperiencePoolEntry] = Field(default_factory=list)
    imported_count: int = 0
    rejected_count: int = 0
    rejected_candidate_ids: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillExperienceBindingRequest(BaseModel):
    experience_ids: list[str] = Field(default_factory=list)
    skill_domain: str = "case_analysis"
    skill_name_candidate: str = "案件经验提炼 Skill 草案"
    case_cause_scope: str = "demo_safe_case_cause_scope"
    experience_types: list[str] = Field(default_factory=list)
    draft_target_id: str = "codex_skill_draft_target_v731c"


class SkillExperienceBinding(V731cSafetyBase):
    binding_id: str
    experience_ids: list[str] = Field(default_factory=list)
    skill_domain: str
    skill_name_candidate: str
    case_cause_scope: str
    experience_types: list[str] = Field(default_factory=list)
    draft_target_id: str
    binding_status: str = "bound_to_draft_target"
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class SkillExperienceBindingList(V731cSafetyBase):
    bindings: list[SkillExperienceBinding] = Field(default_factory=list)
    binding_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CodexSkillDraftBuildRequest(BaseModel):
    experience_ids: list[str] = Field(default_factory=list)
    binding_id: str | None = None
    draft_name: str = "Codex Skill 草案 v7.31c"
    draft_target_id: str = "codex_skill_draft_target_v731c"
    explicit_approved_experience_only_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_real_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class CodexSkillDraftSection(V731cSafetyBase):
    section_id: str
    section_type: str
    title: str
    metadata_items: list[str] = Field(default_factory=list)
    source_experience_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)


class CodexSkillDraftAuditEvent(BaseModel):
    event_id: str
    draft_id: str
    action: str
    timestamp: str
    metadata_only: bool = True
    skill_published: bool = False


class CodexSkillDraftReviewRequest(BaseModel):
    action: str = "approve_draft_structure"
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str = "draft structure review only"
    explicit_manual_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True
    explicit_no_real_training_confirmation: bool = True


class CodexSkillDraftReviewResponse(V731cSafetyBase):
    draft_id: str
    action: str
    confirmation_status: str
    reviewer_id: str
    reviewer_note: str
    skill_published: bool = False
    real_training_triggered: bool = False
    warnings: list[str] = Field(default_factory=list)


class CodexSkillDraft(V731cSafetyBase):
    draft_id: str
    draft_name: str
    draft_version: str = "v7.31c"
    draft_status: str = "requires_manual_confirmation"
    publish_status: str = "not_publishable"
    training_status: str = "not_training_ready"
    confirmation_status: str = "pending_confirmation"
    skill_purpose: str
    trigger_conditions: list[str] = Field(default_factory=list)
    input_requirements: list[str] = Field(default_factory=list)
    workflow_steps: list[str] = Field(default_factory=list)
    experience_patterns: list[str] = Field(default_factory=list)
    case_cause_scope: str
    evidence_handling_rules: list[str] = Field(default_factory=list)
    legal_retrieval_usage_rules: list[str] = Field(default_factory=list)
    redaction_rules: list[str] = Field(default_factory=list)
    source_trace_rules: list[str] = Field(default_factory=list)
    audit_rules: list[str] = Field(default_factory=list)
    manual_review_rules: list[str] = Field(default_factory=list)
    prohibited_usage: list[str] = Field(default_factory=list)
    quality_checklist: list[str] = Field(default_factory=list)
    sample_safe_prompts: list[str] = Field(default_factory=list)
    sample_safe_outputs: list[str] = Field(default_factory=list)
    created_from_experience_ids: list[str] = Field(default_factory=list)
    source_candidate_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    not_publishable_reason: str = "v7.31c only creates a draft requiring manual confirmation and pre-publish gate in a later stage."
    sections: list[CodexSkillDraftSection] = Field(default_factory=list)
    audit_events: list[CodexSkillDraftAuditEvent] = Field(default_factory=list)
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class CodexSkillDraftList(V731cSafetyBase):
    drafts: list[CodexSkillDraft] = Field(default_factory=list)
    draft_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CodexSkillDraftBuildResponse(V731cSafetyBase):
    draft: CodexSkillDraft
    included_experience_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CodexSkillDraftAudit(V731cSafetyBase):
    draft_id: str
    events: list[CodexSkillDraftAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731cSkillExperiencePipelineStatus(V731cSafetyBase):
    version: str = "v7.31c"
    status: str = "skill_experience_pool_and_draft_builder_metadata_ready"
    skill_experience_pool_ready: bool = True
    approved_experience_import_ready: bool = True
    experience_binding_ready: bool = True
    codex_skill_draft_builder_ready: bool = True
    manual_confirmation_queue_ready: bool = True
    source_trace_ready: bool = True
    audit_ready: bool = True
    safety_ready: bool = True
    experience_count: int = 0
    binding_count: int = 0
    draft_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731dSafetyBase(BaseModel):
    owner_only: bool = True
    local_private_processing_only: bool = True
    approved_experience_only: bool = True
    redacted_output_only: bool = True
    abstracted_experience_only: bool = True
    system_validation_required: bool = True
    system_validation_only: bool = True
    final_review_status: str = "not_applicable"
    practice_load_review_required_later: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    unreviewed_experience_packaged: bool = False
    unsafe_experience_packaged: bool = False
    missing_source_trace_packaged: bool = False
    formal_training_set_generated: bool = False
    real_codex_training_triggered: bool = False
    skill_published: bool = False
    skill_publishable: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class SkillPackageBuildRequest(BaseModel):
    source_draft_id: str | None = None
    package_name: str = "Codex Skill Package v7.31d"
    package_version: str = "0.1.0-draft"
    supersedes_package_id: str | None = None
    explicit_system_validation_gate_confirmation: bool = True
    explicit_no_manual_training_output_review_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_real_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class SkillPackageManifest(V731dSafetyBase):
    manifest_id: str
    package_id: str
    package_name: str
    package_version: str
    source_draft_id: str
    experience_ids: list[str] = Field(default_factory=list)
    experience_count: int = 0
    section_count: int = 0
    manifest_status: str = "generated"
    package_status: str = "draft_package"
    validation_requirements: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class SkillPackageSourceTraceBundle(V731dSafetyBase):
    source_trace_bundle_id: str
    package_id: str
    source_draft_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    experience_ids: list[str] = Field(default_factory=list)
    trace_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillPackageAuditEvent(BaseModel):
    event_id: str
    package_id: str
    action: str
    timestamp: str
    metadata_only: bool = True
    system_validation_event: bool = True
    skill_published: bool = False
    real_training_triggered: bool = False


class SkillPackageAudit(V731dSafetyBase):
    package_id: str
    events: list[SkillPackageAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillPackageValidationResult(V731dSafetyBase):
    package_id: str
    pre_publish_gate_status: str
    package_status: str
    gate_passed: bool = False
    all_experiences_redacted: bool = False
    all_experiences_approved: bool = False
    all_source_traces_present: bool = False
    audit_complete: bool = False
    draft_structure_confirmed: bool = False
    manifest_generated: bool = False
    sensitive_field_scan_passed: bool = False
    package_status_valid: bool = False
    ready_for_training_package_build: bool = False
    validation_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillPackage(V731dSafetyBase):
    package_id: str
    package_name: str
    package_version: str
    source_draft_id: str
    experience_ids: list[str] = Field(default_factory=list)
    experience_count: int = 0
    manifest_id: str
    source_trace_bundle_id: str
    audit_bundle_id: str
    pre_publish_gate_status: str = "draft"
    package_status: str = "draft_package"
    final_review_status: str = "not_applicable"
    created_at: str
    updated_at: str
    supersedes_package_id: str | None = None
    superseded_by_package_id: str | None = None
    rollback_available: bool = False
    manifest: SkillPackageManifest
    source_trace_bundle: SkillPackageSourceTraceBundle
    audit_events: list[SkillPackageAuditEvent] = Field(default_factory=list)
    validation_result: SkillPackageValidationResult | None = None
    warnings: list[str] = Field(default_factory=list)


class SkillPackageList(V731dSafetyBase):
    skill_packages: list[SkillPackage] = Field(default_factory=list)
    package_count: int = 0
    system_validated_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class SkillPackageBuildResponse(V731dSafetyBase):
    skill_package: SkillPackage
    packaged_experience_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731dSkillPackagePipelineStatus(V731dSafetyBase):
    version: str = "v7.31d"
    status: str = "skill_package_versioning_system_validation_metadata_ready"
    skill_package_registry_ready: bool = True
    skill_package_builder_ready: bool = True
    manifest_ready: bool = True
    source_trace_bundle_ready: bool = True
    audit_bundle_ready: bool = True
    system_validation_gate_ready: bool = True
    package_count: int = 0
    system_validated_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731eSafetyBase(BaseModel):
    owner_only: bool = True
    local_private_processing_only: bool = True
    system_validated_package_required: bool = True
    approved_experience_only: bool = True
    redacted_output_only: bool = True
    abstracted_experience_only: bool = True
    structured_training_metadata_only: bool = True
    practice_load_review_required_later: bool = True
    training_output_manual_review_status: str = "not_applicable"
    practice_load_review_status: str = "pending_practice_load_review"
    source_trace_required: bool = True
    audit_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    non_validated_package_used: bool = False
    unreviewed_experience_used: bool = False
    unsafe_experience_used: bool = False
    missing_source_trace_used: bool = False
    real_codex_training_triggered: bool = False
    formal_training_set_written: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    skill_publishable: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class TrainingTaskBuildRequest(BaseModel):
    source_skill_package_id: str | None = None
    task_name: str = "Internal Training Task v7.31e"
    explicit_system_validated_package_confirmation: bool = True
    explicit_no_manual_training_output_review_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_real_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class ExperiencePackageBuildRequest(BaseModel):
    source_training_task_id: str | None = None
    source_skill_package_id: str | None = None
    package_name: str = "Internal Experience Package v7.31e"
    package_version: str = "v7.31e.0"
    explicit_pending_practice_load_review_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_real_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class TrainingSample(V731eSafetyBase):
    sample_id: str
    source_skill_package_id: str
    source_draft_id: str
    source_experience_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    prompt_template: str
    input_metadata: dict[str, str | list[str]] = Field(default_factory=dict)
    expected_output_metadata: dict[str, str | list[str]] = Field(default_factory=dict)
    input_output_pair_id: str
    sample_status: str = "training_completed"
    created_at: str


class TrainingPackageAuditEvent(BaseModel):
    event_id: str
    artifact_id: str
    action: str
    timestamp: str
    metadata_only: bool = True
    provider_call_executed: bool = False
    real_training_triggered: bool = False
    skill_published: bool = False


class TrainingPackageSourceTraceBundle(V731eSafetyBase):
    source_trace_bundle_id: str
    artifact_id: str
    source_skill_package_id: str
    source_training_task_id: str | None = None
    source_trace_ids: list[str] = Field(default_factory=list)
    source_experience_ids: list[str] = Field(default_factory=list)
    source_draft_id: str
    trace_count: int = 0
    trace_status: str = "source_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class TrainingTask(V731eSafetyBase):
    training_task_id: str
    task_name: str
    source_skill_package_id: str
    source_draft_id: str
    source_manifest_id: str
    source_trace_bundle_id: str
    source_audit_bundle_id: str
    source_experience_ids: list[str] = Field(default_factory=list)
    sample_count: int = 0
    training_task_status: str = "training_completed"
    lifecycle_statuses: list[str] = Field(default_factory=lambda: ["training_task_created", "training_completed"])
    samples: list[TrainingSample] = Field(default_factory=list)
    audit_events: list[TrainingPackageAuditEvent] = Field(default_factory=list)
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class TrainingTaskList(V731eSafetyBase):
    training_tasks: list[TrainingTask] = Field(default_factory=list)
    task_count: int = 0
    training_completed_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrainingTaskBuildResponse(V731eSafetyBase):
    training_task: TrainingTask
    sample_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackage(V731eSafetyBase):
    package_id: str
    package_name: str
    package_version: str
    source_training_task_id: str
    source_skill_package_id: str
    source_draft_id: str
    source_experience_ids: list[str] = Field(default_factory=list)
    source_trace_bundle_id: str
    audit_bundle_id: str
    training_task_status: str = "training_completed"
    build_status: str = "experience_package_built"
    package_status: str = "pending_practice_load_review"
    experience_package_status: str = "pending_practice_load_review"
    sample_count: int = 0
    samples: list[TrainingSample] = Field(default_factory=list)
    source_trace_bundle: TrainingPackageSourceTraceBundle
    audit_events: list[TrainingPackageAuditEvent] = Field(default_factory=list)
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackageList(V731eSafetyBase):
    training_packages: list[ExperiencePackage] = Field(default_factory=list)
    package_count: int = 0
    pending_practice_load_review_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackageBuildResponse(V731eSafetyBase):
    training_package: ExperiencePackage
    sample_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrainingPackageAudit(V731eSafetyBase):
    package_id: str
    events: list[TrainingPackageAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731eTrainingPipelineStatus(V731eSafetyBase):
    version: str = "v7.31e"
    status: str = "internal_training_experience_package_metadata_ready"
    training_task_builder_ready: bool = True
    experience_package_builder_ready: bool = True
    training_package_registry_ready: bool = True
    training_task_count: int = 0
    training_package_count: int = 0
    pending_practice_load_review_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731fSafetyBase(BaseModel):
    owner_only: bool = True
    local_private_processing_only: bool = True
    generated_package_read_only: bool = True
    lawyer_review_required: bool = True
    practice_load_review_required: bool = True
    approved_for_practice_load_required: bool = True
    redacted_output_only: bool = True
    abstracted_experience_only: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    sensitive_field_scan_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    unreviewed_package_loaded: bool = False
    unredacted_content_loaded: bool = False
    non_pending_review_package_loaded: bool = False
    missing_source_trace_loaded: bool = False
    real_codex_training_triggered: bool = False
    formal_training_set_written: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class ExperienceCard(BaseModel):
    card_id: str
    source_sample_id: str
    source_experience_id: str
    title: str
    generated_experience_text: str
    lawyer_experience_text: str
    applicable_scenarios: list[str] = Field(default_factory=list)
    not_applicable_scenarios: list[str] = Field(default_factory=list)
    risk_warnings: list[str] = Field(default_factory=list)
    usage_boundaries: list[str] = Field(default_factory=list)
    gray_load_enabled: bool = False
    review_status: str = "pending_practice_load_review"
    metadata_safe: bool = True


class PracticeLoadReviewAuditEvent(BaseModel):
    event_id: str
    package_id: str
    action: str
    timestamp: str
    reviewer_id: str | None = None
    reviewer_note: str | None = None
    metadata_only: bool = True
    provider_call_executed: bool = False
    real_training_triggered: bool = False
    skill_published: bool = False
    practice_runtime_loaded: bool = False


class PracticeLoadReviewSourceTraceBundle(V731fSafetyBase):
    source_trace_bundle_id: str
    package_id: str
    source_training_package_id: str
    source_training_task_id: str
    source_skill_package_id: str
    source_trace_ids: list[str] = Field(default_factory=list)
    source_experience_ids: list[str] = Field(default_factory=list)
    trace_count: int = 0
    trace_status: str = "source_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class PracticeLoadRevalidationResult(V731fSafetyBase):
    package_id: str
    validation_status: str = "system_revalidated"
    revalidation_passed: bool = True
    all_cards_metadata_safe: bool = True
    source_trace_complete: bool = True
    audit_complete: bool = True
    sensitive_field_scan_passed: bool = True
    generated_package_preserved: bool = True
    lawyer_approved_package_ready: bool = True
    validation_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PracticeLoadReviewEditRequest(BaseModel):
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str = "practice load review editing started"
    explicit_lawyer_review_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_raw_content_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class ExperienceCardEdit(BaseModel):
    card_id: str
    title: str
    lawyer_experience_text: str
    applicable_scenarios: list[str] = Field(default_factory=list)
    not_applicable_scenarios: list[str] = Field(default_factory=list)
    risk_warnings: list[str] = Field(default_factory=list)
    usage_boundaries: list[str] = Field(default_factory=list)
    gray_load_enabled: bool = False


class PracticeLoadReviewSaveRequest(BaseModel):
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str = "lawyer experience edits saved"
    edited_cards: list[ExperienceCardEdit] = Field(default_factory=list)
    gray_load_enabled: bool = False
    explicit_lawyer_review_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_raw_content_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class PracticeLoadReviewDecisionRequest(BaseModel):
    reviewer_id: str = "local_demo_lawyer"
    reviewer_note: str = "practice load review decision metadata"
    gray_load_enabled: bool = False
    explicit_lawyer_review_confirmation: bool = True
    explicit_system_revalidated_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_real_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class PracticeLoadReviewPackage(V731fSafetyBase):
    package_id: str
    source_training_package_id: str
    source_training_task_id: str
    source_skill_package_id: str
    package_name: str
    package_version: str = "v7.31f.0"
    review_status: str = "pending_practice_load_review"
    load_gate_status: str = "pending_practice_load_review"
    validation_status: str = "system_revalidation_required"
    can_load_to_practice_runtime: bool = False
    gray_load_enabled: bool = False
    generated_experience_package: dict[str, str | int | bool | list[str]] = Field(default_factory=dict)
    lawyer_approved_experience_package: dict[str, str | int | bool | list[str]] | None = None
    experience_cards: list[ExperienceCard] = Field(default_factory=list)
    source_trace_bundle: PracticeLoadReviewSourceTraceBundle
    audit_events: list[PracticeLoadReviewAuditEvent] = Field(default_factory=list)
    revalidation_result: PracticeLoadRevalidationResult | None = None
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class PracticeLoadReviewPackageList(V731fSafetyBase):
    packages: list[PracticeLoadReviewPackage] = Field(default_factory=list)
    package_count: int = 0
    pending_practice_load_review_count: int = 0
    approved_for_practice_load_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeLoadReviewPackageAudit(V731fSafetyBase):
    package_id: str
    events: list[PracticeLoadReviewAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731fPracticeLoadPipelineStatus(V731fSafetyBase):
    version: str = "v7.31f"
    status: str = "practice_load_review_gate_metadata_ready"
    review_gate_ready: bool = True
    lawyer_experience_editor_ready: bool = True
    system_revalidation_ready: bool = True
    package_count: int = 0
    pending_practice_load_review_count: int = 0
    system_revalidated_count: int = 0
    approved_for_practice_load_count: int = 0
    rejected_for_practice_load_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731gSafetyBase(BaseModel):
    owner_only: bool = True
    local_private_processing_only: bool = True
    lawyer_approved_package_only: bool = True
    metadata_safe: bool = True
    redacted_abstracted_experience_only: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    runtime_monitoring_required: bool = True
    rollback_available: bool = True
    controlled_runtime_loading_only: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    unreviewed_package_loaded: bool = False
    system_revalidation_failed_package_loaded: bool = False
    generated_only_package_loaded: bool = False
    unredacted_content_loaded: bool = False
    automatic_training_triggered: bool = False
    formal_training_set_written: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    feedback_auto_mutates_loaded_package: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class PracticeRuntimeLoadRequest(BaseModel):
    experience_package_id: str
    loaded_by: str = "local_demo_lawyer"
    rollout_mode: str = "disabled"
    rollout_percentage: int = 0
    allowed_case_causes: list[str] = Field(default_factory=list)
    allowed_workspaces: list[str] = Field(default_factory=list)
    allowed_runtime_modes: list[str] = Field(default_factory=lambda: ["assistive_draft"])
    allowed_task_types: list[str] = Field(default_factory=lambda: ["fact_review", "legal_analysis_draft"])
    usage_limit_per_day: int = 20
    emergency_disable_enabled: bool = True
    explicit_lawyer_approved_package_confirmation: bool = True
    explicit_system_revalidated_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_source_content_confirmation: bool = True
    explicit_no_final_opinion_confirmation: bool = True


class PracticeRuntimeRolloutRequest(BaseModel):
    operator_id: str = "local_demo_lawyer"
    operator_note: str = "practice runtime rollout metadata update"
    rollout_percentage: int = 10
    usage_limit_per_day: int | None = None
    explicit_manual_control_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_external_delivery_confirmation: bool = True


class PracticeRuntimeDisableRequest(BaseModel):
    operator_id: str = "local_demo_lawyer"
    operator_note: str = "practice runtime load disabled"
    mark_blocked: bool = False
    explicit_manual_control_confirmation: bool = True
    explicit_no_package_delete_confirmation: bool = True


class PracticeRuntimeRollbackRequest(BaseModel):
    operator_id: str = "local_demo_lawyer"
    operator_note: str = "practice runtime rollback metadata"
    rollback_to_load_id: str | None = None
    explicit_manual_rollback_confirmation: bool = True
    explicit_no_package_delete_confirmation: bool = True
    explicit_no_external_delivery_confirmation: bool = True


class PracticeRuntimePolicyEvaluateRequest(BaseModel):
    case_cause: str = "买卖合同纠纷"
    workspace_id: str = "owner_workspace"
    user_id: str = "local_demo_lawyer"
    runtime_mode: str = "assistive_draft"
    requested_task_type: str = "legal_analysis_draft"
    request_context_metadata: dict[str, str | int | bool | list[str]] = Field(default_factory=dict)


class PracticeRuntimeAuditEvent(BaseModel):
    event_id: str
    runtime_load_id: str
    action: str
    timestamp: str
    operator_id: str | None = None
    operator_note: str | None = None
    metadata_only: bool = True
    provider_call_executed: bool = False
    source_content_returned: bool = False
    package_deleted: bool = False
    external_delivery_triggered: bool = False


class PracticeRuntimeSourceTraceBundle(V731gSafetyBase):
    source_trace_bundle_id: str
    runtime_load_id: str
    experience_package_id: str
    lawyer_approved_package_id: str
    source_review_package_id: str
    source_training_package_id: str
    source_skill_package_id: str
    inherited_source_trace_ids: list[str] = Field(default_factory=list)
    source_experience_ids: list[str] = Field(default_factory=list)
    trace_status: str = "runtime_source_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class PracticeRuntimeSafetyReport(V731gSafetyBase):
    safety_report_id: str
    runtime_load_id: str
    load_allowed: bool = False
    safety_status: str = "blocked"
    approval_status_valid: bool = False
    lawyer_approved_package_exists: bool = False
    system_revalidated: bool = False
    source_trace_exists: bool = False
    audit_exists: bool = False
    sensitive_scan_passed: bool = False
    generated_package_preserved: bool = False
    provider_call_absent: bool = True
    source_content_absent: bool = True
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PracticeRuntimeLoadRecord(V731gSafetyBase):
    runtime_load_id: str
    experience_package_id: str
    lawyer_approved_package_id: str
    package_name: str
    package_version: str
    load_status: str = "pending_load"
    load_scope: dict[str, list[str] | str | int | bool] = Field(default_factory=dict)
    enabled_case_causes: list[str] = Field(default_factory=list)
    enabled_workspaces: list[str] = Field(default_factory=list)
    enabled_runtime_modes: list[str] = Field(default_factory=list)
    enabled_task_types: list[str] = Field(default_factory=list)
    rollout_mode: str = "disabled"
    rollout_percentage: int = 0
    usage_limit_per_day: int = 20
    emergency_disable_enabled: bool = True
    loaded_at: str
    loaded_by: str
    disabled_at: str | None = None
    rollback_from_load_id: str | None = None
    rollback_to_load_id: str | None = None
    source_trace_bundle_id: str
    audit_bundle_id: str
    safety_report_id: str
    source_trace_bundle: PracticeRuntimeSourceTraceBundle
    safety_report: PracticeRuntimeSafetyReport
    audit_events: list[PracticeRuntimeAuditEvent] = Field(default_factory=list)
    usage_count_today: int = 0
    blocked_reasons: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class PracticeRuntimeLoadList(V731gSafetyBase):
    runtime_loads: list[PracticeRuntimeLoadRecord] = Field(default_factory=list)
    load_count: int = 0
    loaded_disabled_count: int = 0
    loaded_gray_count: int = 0
    loaded_active_count: int = 0
    disabled_count: int = 0
    rolled_back_count: int = 0
    blocked_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeRuntimeUsageEvent(V731gSafetyBase):
    usage_event_id: str
    package_id: str
    package_version: str
    runtime_load_id: str
    runtime_mode: str
    case_cause: str
    task_type: str
    user_id: str
    owner_id: str = "owner"
    workspace_id: str
    timestamp: str
    allowed: bool = False
    block_reason: str | None = None
    safety_flags: list[str] = Field(default_factory=list)
    audit_id: str


class PracticeRuntimeRiskEvent(V731gSafetyBase):
    risk_event_id: str
    usage_event_id: str
    runtime_load_id: str
    package_id: str
    severity: str = "medium"
    risk_type: str = "policy_block"
    risk_summary: str = "Practice runtime request was blocked by metadata policy."
    immediate_action_required: bool = False
    suggested_action: str = "Review load scope or keep package disabled."
    created_at: str
    audit_id: str


class PracticeRuntimeUsageList(V731gSafetyBase):
    usage_events: list[PracticeRuntimeUsageEvent] = Field(default_factory=list)
    usage_event_count: int = 0
    risk_events: list[PracticeRuntimeRiskEvent] = Field(default_factory=list)
    risk_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeRuntimePolicyEvaluateResult(V731gSafetyBase):
    allowed: bool = False
    blocked_reason: str | None = None
    matched_package_ids: list[str] = Field(default_factory=list)
    active_package_versions: list[str] = Field(default_factory=list)
    usage_boundary: dict[str, str | int | bool | list[str]] = Field(default_factory=dict)
    safety_notice: str = "仅可作为律师复核前的实战辅助经验提示，不生成最终法律意见。"
    audit_id: str
    usage_event: PracticeRuntimeUsageEvent


class PracticeRuntimeLoadAudit(V731gSafetyBase):
    runtime_load_id: str
    events: list[PracticeRuntimeAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731gPracticeRuntimeStatus(V731gSafetyBase):
    version: str = "v7.31g"
    status: str = "practice_runtime_controlled_loading_monitoring_ready"
    loader_ready: bool = True
    registry_ready: bool = True
    policy_engine_ready: bool = True
    monitor_ready: bool = True
    rollback_engine_ready: bool = True
    runtime_load_count: int = 0
    loaded_gray_count: int = 0
    loaded_active_count: int = 0
    disabled_count: int = 0
    blocked_count: int = 0
    usage_event_count: int = 0
    risk_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731hSafetyBase(BaseModel):
    owner_only: bool = True
    metadata_only: bool = True
    local_private_processing_only: bool = True
    lawyer_approved_package_only: bool = True
    redacted_abstracted_experience_only: bool = True
    output_observation_metadata_only: bool = True
    lawyer_feedback_metadata_only: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    full_output_returned: bool = False
    case_material_returned: bool = False
    feedback_auto_mutates_loaded_package: bool = False
    candidate_pack_auto_mutates_loaded_package: bool = False
    package_auto_disabled_by_feedback: bool = False
    package_auto_rolled_back_by_feedback: bool = False
    practice_runtime_package_auto_replaced: bool = False
    automatic_training_triggered: bool = False
    formal_training_set_written: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class PracticeOutputObservationRequest(BaseModel):
    usage_event_id: str
    output_category: str = "analysis_suggestion"
    output_summary_redacted: str = "脱敏后的实战输出摘要 metadata"
    observed_issue_summary: str = "暂无明显问题，仅记录观察 metadata"
    observed_by: str = "local_demo_lawyer"
    safety_flags: list[str] = Field(default_factory=lambda: ["metadata_only", "source_trace_required", "lawyer_review_required"])
    explicit_no_raw_output_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True


class PracticeLawyerFeedbackRequest(BaseModel):
    observation_id: str
    feedback_type: str = "useful"
    feedback_summary: str = "律师反馈摘要 metadata"
    suggested_change: str = "保持当前经验提示，仅作为后续迭代参考。"
    severity: str = "low"
    applies_to_experience_card_id: str | None = None
    applies_to_usage_boundary: str | None = None
    created_by: str = "local_demo_lawyer"
    explicit_no_auto_disable_confirmation: bool = True
    explicit_no_auto_rollback_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True
    explicit_no_training_confirmation: bool = True


class PracticeRiskEventRequest(BaseModel):
    observation_id: str
    severity: str = "medium"
    risk_type: str = "output_quality_issue"
    risk_summary: str = "实战输出观察风险 metadata"
    immediate_action_required: bool = False
    suggested_action: str = "进入律师反馈 triage，不自动禁用或回滚。"
    created_by: str = "local_demo_lawyer"
    explicit_no_auto_disable_confirmation: bool = True
    explicit_no_auto_rollback_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True


class PracticeFeedbackTriageRequest(BaseModel):
    triaged_by: str = "local_demo_lawyer"
    feedback_status: str = "triaged"
    triage_note: str = "规则分类后保留为后续迭代候选 metadata。"
    explicit_no_auto_disable_confirmation: bool = True
    explicit_no_auto_rollback_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True
    explicit_no_training_confirmation: bool = True


class PracticeFeedbackAuditEvent(BaseModel):
    event_id: str
    object_id: str
    object_type: str
    action: str
    timestamp: str
    actor_id: str | None = None
    actor_note: str | None = None
    metadata_only: bool = True
    provider_call_executed: bool = False
    full_output_returned: bool = False
    source_content_returned: bool = False
    package_mutated: bool = False
    package_auto_disabled: bool = False
    package_auto_rolled_back: bool = False
    training_triggered: bool = False
    external_delivery_triggered: bool = False


class PracticeFeedbackSourceTrace(V731hSafetyBase):
    source_trace_id: str
    source_trace_type: str
    object_id: str
    usage_event_id: str
    runtime_load_id: str
    package_id: str
    source_usage_event_id: str
    source_runtime_load_id: str
    inherited_runtime_source_trace_id: str | None = None
    trace_status: str = "feedback_source_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackClassification(V731hSafetyBase):
    feedback_category: str = "useful"
    severity: str = "low"
    suggested_next_action: str = "keep_as_reference"
    auto_disable_recommended: bool = False
    rollback_recommended: bool = False
    create_iteration_candidate_recommended: bool = False
    warnings: list[str] = Field(default_factory=list)


class PracticeOutputObservation(V731hSafetyBase):
    observation_id: str
    usage_event_id: str
    runtime_load_id: str
    package_id: str
    package_version: str
    case_cause: str
    task_type: str
    runtime_mode: str
    output_category: str
    output_summary_redacted: str
    observed_issue_summary: str
    safety_flags: list[str] = Field(default_factory=list)
    generated_at: str
    observed_by: str
    audit_id: str
    source_trace_id: str
    audit_events: list[PracticeFeedbackAuditEvent] = Field(default_factory=list)
    source_trace: PracticeFeedbackSourceTrace
    warnings: list[str] = Field(default_factory=list)


class PracticeOutputObservationList(V731hSafetyBase):
    observations: list[PracticeOutputObservation] = Field(default_factory=list)
    observation_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeLawyerFeedback(V731hSafetyBase):
    feedback_id: str
    observation_id: str
    usage_event_id: str
    runtime_load_id: str
    package_id: str
    package_version: str
    feedback_type: str
    feedback_status: str = "submitted"
    feedback_summary: str
    suggested_change: str
    severity: str
    applies_to_experience_card_id: str | None = None
    applies_to_usage_boundary: str | None = None
    created_by: str
    created_at: str
    audit_id: str
    source_trace_id: str
    classification: PracticeFeedbackClassification
    audit_events: list[PracticeFeedbackAuditEvent] = Field(default_factory=list)
    source_trace: PracticeFeedbackSourceTrace
    warnings: list[str] = Field(default_factory=list)


class PracticeLawyerFeedbackList(V731hSafetyBase):
    feedback_items: list[PracticeLawyerFeedback] = Field(default_factory=list)
    feedback_count: int = 0
    submitted_count: int = 0
    triaged_count: int = 0
    accepted_as_candidate_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackRiskEvent(V731hSafetyBase):
    risk_event_id: str
    observation_id: str
    usage_event_id: str
    runtime_load_id: str
    package_id: str
    package_version: str
    severity: str
    risk_type: str
    risk_summary: str
    immediate_action_required: bool = False
    suggested_action: str
    created_at: str
    audit_id: str
    source_trace_id: str
    audit_events: list[PracticeFeedbackAuditEvent] = Field(default_factory=list)
    source_trace: PracticeFeedbackSourceTrace
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackRiskEventList(V731hSafetyBase):
    risk_events: list[PracticeFeedbackRiskEvent] = Field(default_factory=list)
    risk_event_count: int = 0
    high_severity_count: int = 0
    immediate_action_required_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackSummary(V731hSafetyBase):
    observation_count: int = 0
    feedback_count: int = 0
    risk_event_count: int = 0
    triaged_feedback_count: int = 0
    iteration_candidate_recommended_count: int = 0
    auto_disable_recommended_count: int = 0
    rollback_recommended_count: int = 0
    immediate_action_required_count: int = 0
    package_ids: list[str] = Field(default_factory=list)
    runtime_load_ids: list[str] = Field(default_factory=list)
    feedback_type_counts: dict[str, int] = Field(default_factory=dict)
    risk_type_counts: dict[str, int] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class V731hPracticeFeedbackStatus(V731hSafetyBase):
    version: str = "v7.31h"
    status: str = "practice_output_observation_lawyer_feedback_ready"
    observation_registry_ready: bool = True
    lawyer_feedback_registry_ready: bool = True
    risk_event_registry_ready: bool = True
    feedback_classifier_ready: bool = True
    feedback_summary_ready: bool = True
    observation_count: int = 0
    feedback_count: int = 0
    risk_event_count: int = 0
    triaged_feedback_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731iSafetyBase(BaseModel):
    owner_only: bool = True
    metadata_only: bool = True
    local_private_processing_only: bool = True
    feedback_candidate_pack_only: bool = True
    next_iteration_candidate_only: bool = True
    redacted_abstracted_experience_only: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    feedback_auto_mutates_loaded_package: bool = False
    candidate_pack_auto_mutates_loaded_package: bool = False
    loaded_package_mutated: bool = False
    lawyer_approved_package_mutated: bool = False
    runtime_policy_changed: bool = False
    package_auto_disabled: bool = False
    package_auto_rolled_back: bool = False
    next_package_draft_auto_loaded: bool = False
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    full_output_returned: bool = False
    case_material_returned: bool = False
    automatic_training_triggered: bool = False
    formal_training_set_written: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class PracticeFeedbackCandidatePackBuildRequest(BaseModel):
    source_package_id: str | None = None
    source_runtime_load_id: str | None = None
    proposed_next_package_name: str | None = None
    proposed_next_package_version: str | None = None
    build_requested_by: str = "local_demo_lawyer"
    explicit_triaged_feedback_only_confirmation: bool = True
    explicit_no_loaded_package_mutation_confirmation: bool = True
    explicit_no_lawyer_approved_package_mutation_confirmation: bool = True
    explicit_no_runtime_policy_change_confirmation: bool = True
    explicit_no_auto_disable_confirmation: bool = True
    explicit_no_auto_rollback_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class PracticeFeedbackCandidatePackActionRequest(BaseModel):
    actor_id: str = "local_demo_lawyer"
    actor_note: str = "候选包状态更新 metadata，不自动改包或加载。"
    explicit_no_loaded_package_mutation_confirmation: bool = True
    explicit_no_lawyer_approved_package_mutation_confirmation: bool = True
    explicit_no_runtime_policy_change_confirmation: bool = True
    explicit_no_training_confirmation: bool = True


class IterationCandidateAuditEvent(BaseModel):
    event_id: str
    object_id: str
    object_type: str
    action: str
    timestamp: str
    actor_id: str | None = None
    actor_note: str | None = None
    metadata_only: bool = True
    provider_call_executed: bool = False
    loaded_package_mutated: bool = False
    lawyer_approved_package_mutated: bool = False
    runtime_policy_changed: bool = False
    package_auto_disabled: bool = False
    package_auto_rolled_back: bool = False
    training_triggered: bool = False
    external_delivery_triggered: bool = False


class IterationCandidateSourceTrace(V731iSafetyBase):
    source_trace_id: str
    source_trace_type: str
    object_id: str
    source_package_id: str
    source_package_version: str
    source_runtime_load_id: str
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_risk_event_ids: list[str] = Field(default_factory=list)
    source_observation_ids: list[str] = Field(default_factory=list)
    inherited_runtime_source_trace_id: str | None = None
    trace_status: str = "iteration_candidate_source_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class ExperienceIterationCandidate(V731iSafetyBase):
    iteration_candidate_id: str
    candidate_pack_id: str
    change_type: str
    target_experience_card_id: str | None = None
    current_text_summary: str = "当前经验摘要 metadata"
    proposed_change_summary: str
    proposed_lawyer_review_text: str
    reason_from_feedback: str
    risk_basis: str
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_risk_event_ids: list[str] = Field(default_factory=list)
    severity: str = "medium"
    suggested_action: str = "prepare_for_next_experience_build"
    status: str = "candidate"
    warnings: list[str] = Field(default_factory=list)


class ExperienceIterationDiff(V731iSafetyBase):
    candidate_pack_id: str
    added_cards: list[ExperienceIterationCandidate] = Field(default_factory=list)
    revised_cards: list[ExperienceIterationCandidate] = Field(default_factory=list)
    removed_cards: list[ExperienceIterationCandidate] = Field(default_factory=list)
    narrowed_boundaries: list[ExperienceIterationCandidate] = Field(default_factory=list)
    expanded_boundaries: list[ExperienceIterationCandidate] = Field(default_factory=list)
    added_risk_warnings: list[ExperienceIterationCandidate] = Field(default_factory=list)
    rollback_recommendations: list[ExperienceIterationCandidate] = Field(default_factory=list)
    disable_recommendations: list[ExperienceIterationCandidate] = Field(default_factory=list)
    next_version_recommendation: bool = False
    proposed_changes_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackCandidatePack(V731iSafetyBase):
    candidate_pack_id: str
    source_package_id: str
    source_package_version: str
    source_runtime_load_id: str
    feedback_ids: list[str] = Field(default_factory=list)
    risk_event_ids: list[str] = Field(default_factory=list)
    observation_ids: list[str] = Field(default_factory=list)
    candidate_status: str = "draft_candidate_pack"
    proposed_next_package_name: str
    proposed_next_package_version: str
    proposed_changes_count: int = 0
    created_at: str
    audit_id: str
    source_trace_id: str
    iteration_candidates: list[ExperienceIterationCandidate] = Field(default_factory=list)
    diff: ExperienceIterationDiff
    audit_events: list[IterationCandidateAuditEvent] = Field(default_factory=list)
    source_trace: IterationCandidateSourceTrace
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackCandidatePackList(V731iSafetyBase):
    candidate_packs: list[PracticeFeedbackCandidatePack] = Field(default_factory=list)
    candidate_pack_count: int = 0
    draft_count: int = 0
    ready_count: int = 0
    blocked_count: int = 0
    archived_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class PracticeFeedbackCandidatePackAudit(V731iSafetyBase):
    candidate_pack_id: str
    events: list[IterationCandidateAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731iPracticeFeedbackCandidatePackStatus(V731iSafetyBase):
    version: str = "v7.31i"
    status: str = "practice_feedback_candidate_pack_iteration_ready"
    candidate_pack_registry_ready: bool = True
    iteration_candidate_builder_ready: bool = True
    diff_engine_ready: bool = True
    next_package_proposal_registry_ready: bool = True
    candidate_pack_count: int = 0
    ready_for_next_build_count: int = 0
    triaged_feedback_count: int = 0
    risk_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731jSafetyBase(BaseModel):
    owner_only: bool = True
    metadata_only: bool = True
    local_private_processing_only: bool = True
    next_experience_package_draft_only: bool = True
    candidate_pack_required: bool = True
    ready_candidate_pack_required: bool = True
    practice_load_review_required: bool = True
    redacted_abstracted_experience_only: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    loaded_package_mutated: bool = False
    lawyer_approved_package_mutated: bool = False
    runtime_package_replaced: bool = False
    runtime_policy_changed: bool = False
    next_package_draft_auto_loaded: bool = False
    package_auto_disabled: bool = False
    package_auto_rolled_back: bool = False
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    full_output_returned: bool = False
    case_material_returned: bool = False
    automatic_training_triggered: bool = False
    formal_training_set_written: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class NextExperiencePackageRebuildRequest(BaseModel):
    candidate_pack_id: str | None = None
    rebuilt_by: str = "local_demo_lawyer"
    next_package_name: str | None = None
    next_package_version: str | None = None
    explicit_ready_candidate_pack_confirmation: bool = True
    explicit_no_loaded_package_mutation_confirmation: bool = True
    explicit_no_lawyer_approved_package_mutation_confirmation: bool = True
    explicit_no_runtime_policy_change_confirmation: bool = True
    explicit_no_auto_load_confirmation: bool = True
    explicit_practice_load_review_required_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class NextExperiencePackageActionRequest(BaseModel):
    actor_id: str = "local_demo_lawyer"
    actor_note: str = "下一版经验包草案状态更新 metadata。"
    explicit_no_auto_load_confirmation: bool = True
    explicit_practice_load_review_required_confirmation: bool = True
    explicit_no_loaded_package_mutation_confirmation: bool = True
    explicit_no_lawyer_approved_package_mutation_confirmation: bool = True


class NextPackageAuditEvent(BaseModel):
    event_id: str
    next_package_id: str
    action: str
    timestamp: str
    actor_id: str | None = None
    actor_note: str | None = None
    metadata_only: bool = True
    provider_call_executed: bool = False
    loaded_package_mutated: bool = False
    lawyer_approved_package_mutated: bool = False
    runtime_package_replaced: bool = False
    runtime_policy_changed: bool = False
    practice_runtime_loaded: bool = False
    training_triggered: bool = False
    external_delivery_triggered: bool = False


class NextPackageSourceTrace(V731jSafetyBase):
    source_trace_id: str
    next_package_id: str
    source_package_id: str
    source_package_version: str
    candidate_pack_id: str
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_risk_event_ids: list[str] = Field(default_factory=list)
    source_observation_ids: list[str] = Field(default_factory=list)
    source_iteration_candidate_ids: list[str] = Field(default_factory=list)
    inherited_candidate_pack_source_trace_id: str | None = None
    trace_status: str = "next_package_source_trace_ready"
    warnings: list[str] = Field(default_factory=list)


class NextPackageLawyerReviewView(V731jSafetyBase):
    lawyer_review_view_id: str
    next_package_id: str
    candidate_pack_id: str
    change_summary: str
    added_experience_cards: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    revised_experience_cards: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    removed_experience_cards: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    usage_boundary_changes: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    risk_warning_changes: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    feedback_summary: list[str] = Field(default_factory=list)
    risk_event_summary: list[str] = Field(default_factory=list)
    current_next_comparison: str = "下一版草案仅应用候选 diff metadata，不修改当前已加载包。"
    suggested_load_review_action: str = "进入 v7.31f Practice Load Review Gate 重新复核。"
    final_lawyer_confirmation_required: bool = True
    warnings: list[str] = Field(default_factory=list)


class NextPackageManifest(V731jSafetyBase):
    manifest_id: str
    next_package_id: str
    candidate_pack_id: str
    source_package_id: str
    source_package_version: str
    next_package_name: str
    next_package_version: str
    draft_status: str
    applied_candidate_ids: list[str] = Field(default_factory=list)
    pending_practice_load_review_required: bool = True
    load_executed: bool = False
    warnings: list[str] = Field(default_factory=list)


class NextPackageValidationResult(V731jSafetyBase):
    validation_id: str
    next_package_id: str
    validation_status: str = "metadata_validated"
    ready_for_practice_load_review: bool = True
    candidate_pack_ready: bool = True
    source_trace_complete: bool = True
    audit_complete: bool = True
    sensitive_scan_passed: bool = True
    loaded_package_preserved: bool = True
    validation_errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class NextExperiencePackageDraft(V731jSafetyBase):
    next_package_id: str
    source_package_id: str
    source_package_version: str
    candidate_pack_id: str
    next_package_name: str
    next_package_version: str
    draft_status: str = "draft_rebuilt"
    applied_candidate_ids: list[str] = Field(default_factory=list)
    added_experience_cards: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    revised_experience_cards: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    removed_experience_cards: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    usage_boundary_changes: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    risk_warning_changes: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    rollback_recommendations: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    disable_recommendations: list[dict[str, str | list[str] | bool]] = Field(default_factory=list)
    lawyer_review_view_id: str
    manifest_id: str
    audit_id: str
    source_trace_id: str
    created_at: str
    lawyer_review_view: NextPackageLawyerReviewView
    manifest: NextPackageManifest
    validation_result: NextPackageValidationResult
    audit_events: list[NextPackageAuditEvent] = Field(default_factory=list)
    source_trace: NextPackageSourceTrace
    warnings: list[str] = Field(default_factory=list)


class NextExperiencePackageDraftList(V731jSafetyBase):
    next_packages: list[NextExperiencePackageDraft] = Field(default_factory=list)
    next_package_count: int = 0
    draft_rebuilt_count: int = 0
    pending_practice_load_review_count: int = 0
    blocked_count: int = 0
    archived_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class NextExperiencePackageAudit(V731jSafetyBase):
    next_package_id: str
    events: list[NextPackageAuditEvent] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V731jNextExperiencePackageStatus(V731jSafetyBase):
    version: str = "v7.31j"
    status: str = "next_experience_package_rebuild_ready"
    next_package_rebuilder_ready: bool = True
    candidate_pack_apply_engine_ready: bool = True
    lawyer_review_view_regenerator_ready: bool = True
    manifest_builder_ready: bool = True
    validation_engine_ready: bool = True
    next_package_count: int = 0
    ready_candidate_pack_count: int = 0
    pending_practice_load_review_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V732SafetyBase(BaseModel):
    owner_only: bool = True
    metadata_only: bool = True
    lifecycle_view_only: bool = True
    redacted_abstracted_experience_only: bool = True
    lawyer_approval_required_for_runtime_load: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    feedback_does_not_mutate_loaded_package: bool = True
    candidate_pack_does_not_mutate_loaded_package: bool = True
    next_package_requires_load_review: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_result_payload_returned: bool = False
    source_content_returned: bool = False
    source_material_returned: bool = False
    full_output_returned: bool = False
    case_material_returned: bool = False
    loaded_package_mutated: bool = False
    next_package_draft_auto_loaded: bool = False
    automatic_training_triggered: bool = False
    skill_updated: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class ExperienceLifecycleStageEvent(V732SafetyBase):
    stage_event_id: str
    lifecycle_id: str
    stage_name: str
    stage_status: str
    linked_object_type: str
    linked_object_id: str | None = None
    previous_stage_event_id: str | None = None
    next_stage_candidates: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    blocked_reason: str | None = None
    safety_flags: list[str] = Field(default_factory=list)
    audit_id: str
    source_trace_id: str
    created_at: str


class ExperienceLifecycleRecord(V732SafetyBase):
    lifecycle_id: str
    root_material_batch_id: str | None = None
    current_stage: str
    current_status: str
    case_cause_scope: list[str] = Field(default_factory=list)
    source_candidate_ids: list[str] = Field(default_factory=list)
    experience_ids: list[str] = Field(default_factory=list)
    skill_draft_ids: list[str] = Field(default_factory=list)
    skill_package_ids: list[str] = Field(default_factory=list)
    training_task_ids: list[str] = Field(default_factory=list)
    experience_package_ids: list[str] = Field(default_factory=list)
    practice_load_review_ids: list[str] = Field(default_factory=list)
    runtime_load_ids: list[str] = Field(default_factory=list)
    usage_event_ids: list[str] = Field(default_factory=list)
    observation_ids: list[str] = Field(default_factory=list)
    feedback_ids: list[str] = Field(default_factory=list)
    risk_event_ids: list[str] = Field(default_factory=list)
    candidate_pack_ids: list[str] = Field(default_factory=list)
    next_package_ids: list[str] = Field(default_factory=list)
    latest_loaded_package_id: str | None = None
    latest_lawyer_approved_package_id: str | None = None
    latest_next_package_draft_id: str | None = None
    blocked_reason: str | None = None
    safety_flags: list[str] = Field(default_factory=list)
    source_trace_root_id: str
    audit_timeline_id: str
    stage_events: list[ExperienceLifecycleStageEvent] = Field(default_factory=list)
    next_allowed_actions: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class ExperiencePackageLineage(V732SafetyBase):
    lineage_id: str
    root_package_id: str
    package_id: str
    package_version: str
    package_kind: str
    parent_package_id: str | None = None
    supersedes_package_id: str | None = None
    superseded_by_package_id: str | None = None
    derived_from_candidate_pack_id: str | None = None
    derived_from_feedback_ids: list[str] = Field(default_factory=list)
    derived_from_risk_event_ids: list[str] = Field(default_factory=list)
    loaded_runtime_load_ids: list[str] = Field(default_factory=list)
    rollback_from_load_id: str | None = None
    rollback_to_load_id: str | None = None
    lineage_status: str
    created_at: str


class ExperienceLifecycleGraphNode(V732SafetyBase):
    id: str
    type: str
    label: str
    status: str
    version: str | None = None
    created_at: str | None = None
    safety_status: str = "metadata_safe"


class ExperienceLifecycleGraphEdge(BaseModel):
    from_id: str
    to_id: str
    relation: str
    created_at: str | None = None


class ExperienceLifecycleGraph(V732SafetyBase):
    lifecycle_id: str
    nodes: list[ExperienceLifecycleGraphNode] = Field(default_factory=list)
    edges: list[ExperienceLifecycleGraphEdge] = Field(default_factory=list)
    lineage: list[ExperiencePackageLineage] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class ExperienceLifecycleAuditEventView(V732SafetyBase):
    audit_event_id: str
    lifecycle_id: str
    event_type: str
    stage_name: str
    linked_object_type: str
    linked_object_id: str | None = None
    actor: str | None = None
    timestamp: str
    summary: str
    safety_flags: list[str] = Field(default_factory=list)
    source_trace_id: str | None = None


class ExperienceLifecycleAuditTimeline(V732SafetyBase):
    audit_timeline_id: str
    lifecycle_id: str
    events: list[ExperienceLifecycleAuditEventView] = Field(default_factory=list)
    events_count: int = 0
    latest_event_at: str | None = None
    risk_events_count: int = 0
    blocked_events_count: int = 0
    manual_load_review_events_count: int = 0
    runtime_events_count: int = 0
    feedback_events_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class ExperienceLifecycleSourceTraceView(V732SafetyBase):
    source_trace_view_id: str
    lifecycle_id: str
    root_source_trace_id: str
    material_trace_summary: list[str] = Field(default_factory=list)
    ocr_trace_summary: list[str] = Field(default_factory=list)
    legal_retrieval_trace_summary: list[str] = Field(default_factory=list)
    experience_candidate_trace_summary: list[str] = Field(default_factory=list)
    skill_draft_trace_summary: list[str] = Field(default_factory=list)
    skill_package_trace_summary: list[str] = Field(default_factory=list)
    training_package_trace_summary: list[str] = Field(default_factory=list)
    practice_load_trace_summary: list[str] = Field(default_factory=list)
    runtime_usage_trace_summary: list[str] = Field(default_factory=list)
    feedback_trace_summary: list[str] = Field(default_factory=list)
    next_package_trace_summary: list[str] = Field(default_factory=list)
    missing_trace_warnings: list[str] = Field(default_factory=list)
    created_at: str


class ExperienceLifecycleIntegrityCheck(V732SafetyBase):
    integrity_check_id: str
    lifecycle_id: str
    status: str
    passed_checks: list[str] = Field(default_factory=list)
    failed_checks: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    blocked_reason: str | None = None
    recommended_actions: list[str] = Field(default_factory=list)
    created_at: str


class ExperienceLifecycleSafetySummary(V732SafetyBase):
    lifecycle_id: str
    raw_content_absent: bool = True
    ocr_payload_absent: bool = True
    filesystem_location_absent: bool = True
    credential_value_absent: bool = True
    provider_payload_absent: bool = True
    lawyer_approval_required_for_runtime_load: bool = True
    loaded_package_is_lawyer_approved: bool = True
    feedback_does_not_mutate_loaded_package: bool = True
    next_package_requires_load_review: bool = True
    overall_safety_status: str = "passed"
    warnings: list[str] = Field(default_factory=list)


class ExperienceLifecycleList(V732SafetyBase):
    lifecycles: list[ExperienceLifecycleRecord] = Field(default_factory=list)
    lifecycle_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V732ExperienceLifecycleStatus(V732SafetyBase):
    version: str = "v7.32"
    status: str = "experience_lifecycle_consolidation_ready"
    lifecycle_registry_ready: bool = True
    state_machine_ready: bool = True
    lineage_graph_ready: bool = True
    audit_timeline_ready: bool = True
    source_trace_view_ready: bool = True
    integrity_check_ready: bool = True
    safety_summary_ready: bool = True
    lifecycle_count: int = 0
    stage_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V733SafetyBase(BaseModel):
    owner_only: bool = True
    metadata_only: bool = True
    schema_driven_output_only: bool = True
    redacted_abstracted_output_only: bool = True
    frontend_output_definition_forbidden: bool = True
    lawyer_review_required: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    provider_call_executed: bool = False
    key_value_read: bool = False
    credential_value_returned: bool = False
    provider_payload_returned: bool = False
    source_content_returned: bool = False
    case_material_returned: bool = False
    loaded_package_mutated: bool = False
    next_package_auto_generated: bool = False
    training_triggered: bool = False
    skill_published: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    public_link_created: bool = False
    email_sent: bool = False
    external_delivery_triggered: bool = False


class CaseAnalysisOutputFeedbackRequest(BaseModel):
    reviewer_id: str = "owner_lawyer"
    feedback_type: str = "improvement_suggestion"
    feedback_summary: str = "建议优化该项输出的事实边界与风险提示。"
    severity: str = "low"
    explicit_metadata_only_confirmation: bool = True
    explicit_no_training_confirmation: bool = True


class CaseAnalysisOutputRiskEventRequest(BaseModel):
    reporter_id: str = "owner_lawyer"
    risk_level: str = "medium"
    risk_summary: str = "该项输出需要律师复核后再作为实战参考。"
    mitigation_note: str = "保留为辅助提示，不作为最终法律意见。"
    explicit_metadata_only_confirmation: bool = True
    explicit_no_external_delivery_confirmation: bool = True


class CaseAnalysisOutputGroup(V733SafetyBase):
    group_id: str
    group_title: str
    group_type: str
    expected_count: int
    actual_count: int
    display_order: int
    description: str
    outputs: list["CaseAnalysisRuntimeOutput"] = Field(default_factory=list)


class CaseAnalysisSkillOutputSchema(V733SafetyBase):
    skill_id: str
    skill_name: str
    skill_version: str
    schema_version: str = "v7.33"
    package_id: str
    package_version: str
    runtime_load_id: str
    output_groups: list[CaseAnalysisOutputGroup] = Field(default_factory=list)
    created_at: str
    audit_id: str
    source_trace_id: str
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisRuntimeOutput(V733SafetyBase):
    output_id: str
    group_id: str
    output_type: str
    output_title: str
    output_order: int
    output_status: str = "visible"
    output_summary_redacted: str
    output_detail_redacted: str
    risk_level: str = "low"
    confidence_label: str = "schema_defined_demo"
    source_experience_ids: list[str] = Field(default_factory=list)
    source_runtime_load_id: str
    source_usage_event_id: str | None = None
    source_trace_id: str
    audit_id: str
    feedback_count: int = 0
    risk_event_count: int = 0
    allowed_actions: list[str] = Field(default_factory=list)
    created_at: str
    updated_at: str


class CaseAnalysisSummaryMetrics(V733SafetyBase):
    total_outputs: int = 0
    fact_output_count: int = 0
    legal_analysis_output_count: int = 0
    risk_flagged_count: int = 0
    feedback_count: int = 0
    high_risk_count: int = 0
    reviewed_count: int = 0


class CaseAnalysisWorkbenchView(V733SafetyBase):
    view_id: str
    case_id: str
    case_cause_name: str
    package_id: str
    package_version: str
    runtime_load_id: str
    runtime_load_status: str
    skill_id: str
    skill_name: str
    skill_version: str
    output_groups: list[CaseAnalysisOutputGroup] = Field(default_factory=list)
    summary_metrics: CaseAnalysisSummaryMetrics
    safety_summary: dict[str, bool | str] = Field(default_factory=dict)
    audit_id: str
    source_trace_id: str
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisWorkbenchViewList(V733SafetyBase):
    views: list[CaseAnalysisWorkbenchView] = Field(default_factory=list)
    view_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisRuntimeOutputList(V733SafetyBase):
    outputs: list[CaseAnalysisRuntimeOutput] = Field(default_factory=list)
    output_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputFeedback(V733SafetyBase):
    feedback_id: str
    output_id: str
    reviewer_id: str
    feedback_type: str
    feedback_summary: str
    severity: str
    feedback_status: str = "submitted"
    source_trace_id: str
    audit_id: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputFeedbackList(V733SafetyBase):
    output_id: str
    feedback: list[CaseAnalysisOutputFeedback] = Field(default_factory=list)
    feedback_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputRiskEvent(V733SafetyBase):
    risk_event_id: str
    output_id: str
    reporter_id: str
    risk_level: str
    risk_summary: str
    mitigation_note: str
    risk_status: str = "logged_for_lawyer_review"
    source_trace_id: str
    audit_id: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputRiskEventList(V733SafetyBase):
    output_id: str
    risk_events: list[CaseAnalysisOutputRiskEvent] = Field(default_factory=list)
    risk_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputAudit(V733SafetyBase):
    output_id: str
    audit_id: str
    events: list[dict[str, str]] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputSourceTrace(V733SafetyBase):
    output_id: str
    source_trace_id: str
    source_experience_ids: list[str] = Field(default_factory=list)
    source_runtime_load_id: str
    source_usage_event_id: str | None = None
    trace_status: str = "complete"
    trace_summary: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class V733CaseAnalysisWorkbenchStatus(V733SafetyBase):
    version: str = "v7.33"
    status: str = "case_analysis_schema_driven_workbench_ready"
    skill_output_schema_ready: bool = True
    runtime_output_registry_ready: bool = True
    output_view_builder_ready: bool = True
    feedback_engine_ready: bool = True
    risk_event_engine_ready: bool = True
    view_count: int = 0
    output_count: int = 0
    fact_group_count: int = 0
    legal_analysis_group_count: int = 0
    feedback_count: int = 0
    risk_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V734SafetyBase(V733SafetyBase):
    improvement_candidate_only: bool = True
    redacted_abstracted_metadata_only: bool = True
    output_feedback_input_only: bool = True
    risk_event_input_only: bool = True
    loaded_package_auto_mutated: bool = False
    lawyer_approved_package_auto_mutated: bool = False
    output_schema_auto_mutated: bool = False
    runtime_package_auto_replaced: bool = False
    training_dataset_auto_built: bool = False
    training_gate_required: bool = True
    package_disable_auto_executed: bool = False
    package_rollback_auto_executed: bool = False


class CaseAnalysisImprovementBuildRequest(BaseModel):
    explicit_metadata_only_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_schema_mutation_confirmation: bool = True


class CaseAnalysisImprovementActionRequest(BaseModel):
    actor_id: str = "owner_lawyer"
    action_reason: str = "metadata status update only"
    explicit_metadata_only_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True


class CaseAnalysisOutputToExperienceTrace(V734SafetyBase):
    trace_id: str
    output_id: str
    output_group: str
    output_type: str
    runtime_load_id: str
    package_id: str
    package_version: str
    experience_package_id: str
    experience_card_ids: list[str] = Field(default_factory=list)
    skill_schema_id: str
    skill_schema_version: str
    usage_event_id: str | None = None
    audit_id: str
    source_trace_id: str
    trace_status: str = "complete"
    missing_trace_warnings: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisOutputToExperienceTraceList(V734SafetyBase):
    output_traces: list[CaseAnalysisOutputToExperienceTrace] = Field(default_factory=list)
    trace_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisImprovementCandidate(V734SafetyBase):
    candidate_id: str
    source_output_id: str
    source_output_group: str
    source_output_type: str
    source_output_title: str
    source_output_order: int
    source_output_summary_redacted: str
    source_case_analysis_view_id: str
    source_runtime_load_id: str
    source_usage_event_id: str | None = None
    source_package_id: str
    source_package_version: str
    source_experience_card_ids: list[str] = Field(default_factory=list)
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_risk_event_ids: list[str] = Field(default_factory=list)
    source_audit_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    source_feedback_types: list[str] = Field(default_factory=list)
    source_risk_types: list[str] = Field(default_factory=list)
    candidate_type: str
    candidate_status: str = "mapped"
    candidate_severity: str = "medium"
    candidate_title: str
    candidate_summary: str
    candidate_reason: str
    proposed_change_type: str
    proposed_change_summary: str
    target_object_type: str
    target_object_id: str
    affected_output_schema_group: str
    affected_output_schema_type: str
    affected_usage_boundary: str
    affected_risk_warning: str
    affected_experience_card_id: str | None = None
    training_relevance: str = "requires_dataset_gate"
    practice_relevance: str = "practice_improvement_candidate"
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    blocked_reason: str | None = None
    readiness_status: str = "ready_for_candidate_pack"
    created_at: str
    updated_at: str
    audit_id: str
    source_trace_id: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisImprovementCandidateList(V734SafetyBase):
    candidates: list[CaseAnalysisImprovementCandidate] = Field(default_factory=list)
    candidate_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisImprovementReadinessReport(V734SafetyBase):
    readiness_report_id: str
    candidate_id: str
    status: str
    passed_checks: list[str] = Field(default_factory=list)
    failed_checks: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    blocked_reason: str | None = None
    recommended_next_action: str
    created_at: str
    audit_id: str


class CaseAnalysisImprovementDiff(V734SafetyBase):
    diff_id: str
    candidate_ids: list[str] = Field(default_factory=list)
    source_package_id: str
    source_package_version: str
    target_next_package_version_hint: str
    added_cards_count: int = 0
    revised_cards_count: int = 0
    deleted_cards_count: int = 0
    boundary_changes_count: int = 0
    risk_warning_changes_count: int = 0
    schema_metadata_changes_count: int = 0
    training_update_recommendations_count: int = 0
    disable_recommendations_count: int = 0
    rollback_recommendations_count: int = 0
    diff_summary: str
    risk_summary: str
    readiness_status: str
    audit_id: str
    source_trace_id: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisImprovementDiffList(V734SafetyBase):
    diffs: list[CaseAnalysisImprovementDiff] = Field(default_factory=list)
    diff_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisImprovementAudit(V734SafetyBase):
    candidate_id: str
    audit_id: str
    events: list[dict[str, str]] = Field(default_factory=list)
    event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class CaseAnalysisImprovementSourceTrace(V734SafetyBase):
    candidate_id: str
    source_trace_id: str
    source_output_id: str
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_risk_event_ids: list[str] = Field(default_factory=list)
    source_audit_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    trace_status: str = "candidate_trace_ready"
    trace_summary: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class V734CaseAnalysisImprovementStatus(V734SafetyBase):
    version: str = "v7.34"
    status: str = "case_analysis_improvement_candidate_ready"
    feedback_to_improvement_mapper_ready: bool = True
    candidate_registry_ready: bool = True
    output_to_experience_trace_ready: bool = True
    diff_engine_ready: bool = True
    readiness_engine_ready: bool = True
    source_trace_required: bool = True
    audit_required: bool = True
    candidate_count: int = 0
    ready_for_training_dataset_build_count: int = 0
    trace_count: int = 0
    diff_count: int = 0
    feedback_count: int = 0
    risk_event_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V735TrainingDatasetSafetyBase(V734SafetyBase):
    training_dataset_manifest_generated: bool = True
    training_examples_generated: bool = True
    training_task_plan_generated: bool = True
    training_gate_report_generated: bool = True
    gate_reference_only: bool = True
    quality_reference_only: bool = True
    blocks_next_stage: bool = False
    ready_candidate_only: bool = True
    candidate_audit_checked: bool = True
    source_trace_checked: bool = True
    sensitive_metadata_scan_required: bool = True
    sensitive_metadata_scan_passed: bool = True
    experience_package_loaded_as_metadata: bool = True
    skill_output_schema_loaded_as_metadata: bool = True
    output_to_experience_trace_loaded_as_metadata: bool = True
    loaded_package_auto_mutated: bool = False
    lawyer_approved_package_auto_mutated: bool = False
    runtime_package_auto_replaced: bool = False
    formal_training_set_written: bool = False
    real_training_triggered: bool = False
    real_training_output_generated: bool = False
    skill_updated: bool = False


class TrainingDatasetBuildRequest(BaseModel):
    actor_id: str = "owner_lawyer"
    explicit_metadata_only_confirmation: bool = True
    explicit_ready_candidate_only_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_package_mutation_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class TrainingDatasetExample(V735TrainingDatasetSafetyBase):
    example_id: str
    candidate_id: str
    source_output_id: str
    source_output_group: str
    source_output_type: str
    source_package_id: str
    source_package_version: str
    source_experience_card_ids: list[str] = Field(default_factory=list)
    source_feedback_ids: list[str] = Field(default_factory=list)
    source_risk_event_ids: list[str] = Field(default_factory=list)
    source_audit_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    output_trace_id: str | None = None
    output_trace_status: str = "pending"
    skill_schema_id: str
    skill_schema_version: str
    training_input_summary: str
    training_target_summary: str
    training_task_type: str
    gate_input_status: str
    metadata_safety_status: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class TrainingTaskPlan(V735TrainingDatasetSafetyBase):
    task_plan_id: str
    dataset_id: str
    task_plan_status: str = "planned_metadata_only"
    target_skill_ids: list[str] = Field(default_factory=list)
    source_package_ids: list[str] = Field(default_factory=list)
    source_candidate_ids: list[str] = Field(default_factory=list)
    example_count: int = 0
    planned_steps: list[str] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class TrainingDatasetManifest(V735TrainingDatasetSafetyBase):
    dataset_id: str
    dataset_version: str = "v7.35"
    dataset_status: str
    source_candidate_ids: list[str] = Field(default_factory=list)
    source_package_ids: list[str] = Field(default_factory=list)
    source_skill_ids: list[str] = Field(default_factory=list)
    source_output_ids: list[str] = Field(default_factory=list)
    source_trace_ids: list[str] = Field(default_factory=list)
    source_audit_ids: list[str] = Field(default_factory=list)
    candidate_count: int = 0
    example_count: int = 0
    examples: list[TrainingDatasetExample] = Field(default_factory=list)
    task_plan: TrainingTaskPlan
    audit_id: str
    source_trace_id: str
    created_at: str
    updated_at: str
    warnings: list[str] = Field(default_factory=list)


class TrainingDatasetManifestList(V735TrainingDatasetSafetyBase):
    manifests: list[TrainingDatasetManifest] = Field(default_factory=list)
    manifest_count: int = 0
    latest_dataset_id: str | None = None
    warnings: list[str] = Field(default_factory=list)


class TrainingDatasetExampleList(V735TrainingDatasetSafetyBase):
    dataset_id: str | None = None
    examples: list[TrainingDatasetExample] = Field(default_factory=list)
    example_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class TrainingGateReport(V735TrainingDatasetSafetyBase):
    gate_report_id: str
    dataset_id: str | None = None
    gate_status: str
    candidate_count: int = 0
    example_count: int = 0
    passed_checks: list[str] = Field(default_factory=list)
    failed_checks: list[str] = Field(default_factory=list)
    gate_summary: str
    candidate_metadata_safe: bool = True
    audit_source_trace_safe: bool = True
    provider_boundary_safe: bool = True
    package_mutation_safe: bool = True
    training_boundary_safe: bool = True
    recommended_next_action: str
    created_at: str
    audit_id: str
    source_trace_id: str
    warnings: list[str] = Field(default_factory=list)


class V735TrainingDatasetStatus(V735TrainingDatasetSafetyBase):
    version: str = "v7.35"
    status: str = "training_dataset_builder_ready"
    dataset_builder_ready: bool = True
    training_gate_ready: bool = True
    ready_candidate_count: int = 0
    dataset_manifest_count: int = 0
    latest_dataset_id: str | None = None
    latest_gate_status: str = "not_built"
    example_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V736CodexTrainingDryRunSafetyBase(V735TrainingDatasetSafetyBase):
    codex_skill_dry_run: bool = True
    internal_training_simulation_only: bool = True
    provider_access_attempted: bool = False
    provider_call_executed: bool = False
    key_value_read: bool = False
    runtime_package_written: bool = False
    runtime_package_replaced: bool = False
    loaded_package_auto_mutated: bool = False
    lawyer_approved_package_auto_mutated: bool = False
    real_training_triggered: bool = False
    real_training_output_generated: bool = False
    skill_published: bool = False


class CodexTrainingDryRunRequest(BaseModel):
    actor_id: str = "owner_lawyer"
    explicit_internal_dry_run_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_key_read_confirmation: bool = True
    explicit_no_runtime_package_write_confirmation: bool = True
    explicit_no_training_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True


class CodexTrainingDryRunLogEntry(V736CodexTrainingDryRunSafetyBase):
    log_id: str
    run_id: str
    step_name: str
    step_status: str
    message: str
    candidate_ids: list[str] = Field(default_factory=list)
    dataset_id: str | None = None
    gate_report_id: str | None = None
    loaded_metadata_refs: list[dict[str, str]] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CodexTrainingDryRun(V736CodexTrainingDryRunSafetyBase):
    run_id: str
    run_status: str
    dataset_id: str | None = None
    gate_report_id: str | None = None
    candidate_ids: list[str] = Field(default_factory=list)
    example_count: int = 0
    training_gate_status: str
    loaded_metadata_refs: list[dict[str, str]] = Field(default_factory=list)
    logs: list[CodexTrainingDryRunLogEntry] = Field(default_factory=list)
    audit_id: str
    source_trace_id: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CodexTrainingDryRunLogList(V736CodexTrainingDryRunSafetyBase):
    logs: list[CodexTrainingDryRunLogEntry] = Field(default_factory=list)
    log_count: int = 0
    latest_run_id: str | None = None
    warnings: list[str] = Field(default_factory=list)


class CodexTrainingDryRunGateReport(V736CodexTrainingDryRunSafetyBase):
    gate_report_id: str
    run_id: str | None = None
    dataset_gate_report_id: str | None = None
    gate_status: str
    passed_checks: list[str] = Field(default_factory=list)
    failed_checks: list[str] = Field(default_factory=list)
    gate_summary: str
    provider_boundary_safe: bool = True
    key_boundary_safe: bool = True
    runtime_package_boundary_safe: bool = True
    training_boundary_safe: bool = True
    publication_boundary_safe: bool = True
    created_at: str
    audit_id: str
    source_trace_id: str
    warnings: list[str] = Field(default_factory=list)


class V736CodexTrainingDryRunStatus(V736CodexTrainingDryRunSafetyBase):
    version: str = "v7.36"
    status: str = "codex_training_dryrun_ready"
    dryrun_engine_ready: bool = True
    dryrun_count: int = 0
    latest_run_id: str | None = None
    latest_run_status: str = "not_run"
    latest_gate_status: str = "not_run"
    log_count: int = 0
    warnings: list[str] = Field(default_factory=list)


class V737CodexTrainingRunSafetyBase(V736CodexTrainingDryRunSafetyBase):
    codex_skill_internal_training_run: bool = True
    internal_training_workspace_only: bool = True
    local_cpu_gpu_mode_allowed: bool = True
    internal_model_metadata_generated: bool = True
    training_metrics_generated: bool = True
    dryrun_log_compared: bool = True
    external_provider_training_triggered: bool = False
    provider_access_attempted: bool = False
    provider_call_executed: bool = False
    key_value_read: bool = False
    runtime_package_written: bool = False
    runtime_package_replaced: bool = False
    loaded_package_auto_mutated: bool = False
    lawyer_approved_package_auto_mutated: bool = False
    formal_training_set_written: bool = False
    real_training_output_exported: bool = False
    skill_updated: bool = False
    skill_published: bool = False


class CodexTrainingRunStartRequest(BaseModel):
    actor_id: str = "owner_lawyer"
    execution_mode: str = "internal_simulation"
    explicit_internal_training_confirmation: bool = True
    explicit_no_provider_confirmation: bool = True
    explicit_no_key_read_confirmation: bool = True
    explicit_no_runtime_package_replace_confirmation: bool = True
    explicit_no_skill_publish_confirmation: bool = True
    explicit_no_external_delivery_confirmation: bool = True


class CodexInternalTrainingMetrics(V737CodexTrainingRunSafetyBase):
    metrics_id: str
    run_id: str
    dataset_id: str | None = None
    dryrun_id: str | None = None
    candidate_count: int = 0
    example_count: int = 0
    log_alignment_score: float = 1.0
    metadata_safety_score: float = 1.0
    gate_pass_rate: float = 1.0
    provider_call_count: int = 0
    key_read_count: int = 0
    runtime_package_mutation_count: int = 0
    skill_publish_count: int = 0
    internal_model_artifact_id: str
    internal_model_artifact_status: str = "metadata_recorded_only"
    warnings: list[str] = Field(default_factory=list)


class CodexInternalTrainingLogEntry(V737CodexTrainingRunSafetyBase):
    log_id: str
    run_id: str
    step_name: str
    step_status: str
    message: str
    dryrun_log_ref: str | None = None
    dataset_id: str | None = None
    candidate_ids: list[str] = Field(default_factory=list)
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CodexInternalTrainingRun(V737CodexTrainingRunSafetyBase):
    run_id: str
    run_status: str
    execution_mode: str = "internal_simulation"
    dataset_id: str | None = None
    dryrun_id: str | None = None
    gate_report_id: str | None = None
    candidate_ids: list[str] = Field(default_factory=list)
    example_count: int = 0
    metrics: CodexInternalTrainingMetrics
    logs: list[CodexInternalTrainingLogEntry] = Field(default_factory=list)
    audit_id: str
    source_trace_id: str
    created_at: str
    warnings: list[str] = Field(default_factory=list)


class CodexInternalTrainingLogList(V737CodexTrainingRunSafetyBase):
    logs: list[CodexInternalTrainingLogEntry] = Field(default_factory=list)
    log_count: int = 0
    latest_run_id: str | None = None
    warnings: list[str] = Field(default_factory=list)


class CodexInternalTrainingGateReport(V737CodexTrainingRunSafetyBase):
    gate_report_id: str
    run_id: str | None = None
    gate_status: str
    passed_checks: list[str] = Field(default_factory=list)
    failed_checks: list[str] = Field(default_factory=list)
    metrics_summary: dict[str, float | int | str] = Field(default_factory=dict)
    gate_summary: str
    dryrun_log_comparison_status: str
    provider_boundary_safe: bool = True
    key_boundary_safe: bool = True
    runtime_package_boundary_safe: bool = True
    publication_boundary_safe: bool = True
    audit_source_trace_safe: bool = True
    created_at: str
    audit_id: str
    source_trace_id: str
    warnings: list[str] = Field(default_factory=list)


class V737CodexInternalTrainingStatus(V737CodexTrainingRunSafetyBase):
    version: str = "v7.37"
    status: str = "codex_internal_training_run_ready"
    training_run_engine_ready: bool = True
    training_run_count: int = 0
    latest_run_id: str | None = None
    latest_run_status: str = "not_started"
    latest_gate_status: str = "not_started"
    latest_metrics_id: str | None = None
    log_count: int = 0
    warnings: list[str] = Field(default_factory=list)
