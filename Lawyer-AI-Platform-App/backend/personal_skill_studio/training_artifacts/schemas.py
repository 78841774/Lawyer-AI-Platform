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
