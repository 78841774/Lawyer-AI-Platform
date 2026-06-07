from typing import Any

from fastapi import APIRouter, HTTPException, Request

from personal_skill_studio.training_artifacts.artifact_registry import (
    build_scheme,
    get_package,
    get_skill,
    list_evaluations,
    list_gates,
    list_loading_manifests,
    list_packages,
    list_skills,
    list_test_cases,
)
from personal_skill_studio.training_artifacts.audit_engine import build_audit
from personal_skill_studio.training_artifacts.case_cause_matcher import match_case_cause
from personal_skill_studio.training_artifacts.case_cause_taxonomy import build_taxonomy_manifest, get_case_cause_node
from personal_skill_studio.training_artifacts.case_analysis_workbench_runtime import (
    build_v733_workbench_status,
    get_output_audit,
    get_output_source_trace,
    get_runtime_output,
    get_workbench_schema,
    get_workbench_view,
    list_output_feedback,
    list_output_risk_events,
    list_workbench_outputs,
    list_workbench_views,
    mark_output_reviewed,
    submit_output_feedback,
    submit_output_risk_event,
)
from personal_skill_studio.training_artifacts.case_analysis_improvement_candidate_registry import (
    archive_case_analysis_improvement_candidate,
    build_case_analysis_improvement_candidates,
    build_case_analysis_improvement_diff,
    build_v734_status,
    get_case_analysis_improvement_candidate,
    get_case_analysis_improvement_candidate_audit,
    get_case_analysis_improvement_candidate_readiness,
    get_case_analysis_improvement_candidate_source_trace,
    get_case_analysis_improvement_diff,
    get_case_analysis_output_to_experience_trace,
    list_case_analysis_improvement_candidates,
    list_case_analysis_improvement_diffs,
    list_case_analysis_output_to_experience_traces,
    mark_case_analysis_improvement_candidate_ready,
)
from personal_skill_studio.training_artifacts.codex_skill_draft_registry import (
    create_draft,
    get_draft,
    get_draft_audit,
    list_drafts,
    review_draft,
)
from personal_skill_studio.training_artifacts.codex_training_dryrun_registry import (
    get_codex_training_dryrun_gate_report,
    get_codex_training_dryrun_status,
    list_codex_training_dryrun_logs,
    run_codex_training_dryrun,
)
from personal_skill_studio.training_artifacts.codex_training_run_registry import (
    get_codex_internal_training_gate_report,
    get_codex_internal_training_status,
    list_codex_internal_training_logs,
    start_codex_internal_training_run,
)
from personal_skill_studio.training_artifacts.codex_training_skill_runtime import (
    build_v737_training_skill_status,
    build_v738_status,
    generate_training_skill,
    get_skill_training_artifact,
    get_skill_training_audit,
    get_skill_training_gate_report,
    get_skill_training_logs,
    get_skill_training_metrics,
    get_skill_training_run,
    get_skill_training_source_trace,
    get_training_skill,
    get_training_skill_audit,
    get_training_skill_gate_report,
    get_training_skill_interface_doc,
    get_training_skill_source_trace,
    list_skill_training_runs,
    list_training_skills,
    run_training_skill_gate,
    start_skill_training_run,
)
from personal_skill_studio.training_artifacts.experience_candidate_registry import (
    build_candidates,
    get_candidate,
    get_candidate_audit,
    list_candidates,
    redact_experience_candidate,
    review_experience_candidate,
)
from personal_skill_studio.training_artifacts.external_ocr_training_runtime import (
    build_external_ocr_redacted_summary,
    fetch_external_ocr_result,
    get_external_ocr_run,
    get_external_ocr_job_audit,
    get_external_ocr_job_source_trace,
    get_external_ocr_job_status,
    get_external_ocr_provider_status_diagnostics,
    list_external_ocr_runs,
    poll_external_ocr_job,
    record_external_ocr_job_submission,
    run_external_ocr_parse_quality_gate,
    start_external_ocr_parse,
)
from personal_skill_studio.training_artifacts.external_ocr_paddle_adapter import (
    ExternalOCRRequest,
    check_external_ocr_ready,
    external_ocr_diagnostics,
    redacted_file_ref,
    submit_paddle_ocr_job,
)
from personal_skill_studio.training_artifacts.experience_lifecycle_registry import (
    build_v732_status,
    get_lifecycle,
    get_lifecycle_audit_timeline,
    get_lifecycle_graph,
    get_lifecycle_integrity_check,
    get_lifecycle_safety_summary,
    get_lifecycle_source_trace_view,
    get_lifecycle_state,
    list_lifecycles,
    recompute_lifecycle,
)
from personal_skill_studio.training_artifacts.experience_candidate_safety_engine import build_v731b_status
from personal_skill_studio.training_artifacts.legal_retrieval_registry import (
    create_legal_retrieval_job,
    get_legal_retrieval_job,
    list_legal_retrieval_jobs,
)
from personal_skill_studio.training_artifacts.load_dry_run_engine import (
    create_load_dry_run,
    get_load_dry_run,
    get_skill_context,
    list_load_dry_runs,
    list_skill_contexts,
)
from personal_skill_studio.training_artifacts.ocr_job_registry import create_ocr_job, get_ocr_job, list_ocr_jobs
from personal_skill_studio.training_artifacts.next_experience_package_registry import (
    archive_next_package,
    build_v731j_status,
    get_next_experience_package,
    get_next_experience_package_audit,
    get_next_experience_package_lawyer_review_view,
    get_next_experience_package_manifest,
    get_next_experience_package_source_trace,
    list_next_experience_packages,
    mark_next_package_pending_load_review,
    rebuild_next_experience_package_record,
)
from personal_skill_studio.training_artifacts.practice_feedback_registry import build_feedback_summary, build_v731h_status
from personal_skill_studio.training_artifacts.practice_feedback_candidate_pack import (
    archive_candidate_pack,
    build_practice_feedback_candidate_pack,
    build_v731i_status,
    get_practice_feedback_candidate_pack,
    get_practice_feedback_candidate_pack_audit,
    get_practice_feedback_candidate_pack_diff,
    get_practice_feedback_candidate_pack_source_trace,
    list_practice_feedback_candidate_packs,
    mark_candidate_pack_ready,
)
from personal_skill_studio.training_artifacts.practice_lawyer_feedback import (
    create_lawyer_feedback,
    get_lawyer_feedback,
    list_lawyer_feedback,
    triage_lawyer_feedback,
)
from personal_skill_studio.training_artifacts.practice_load_review_gate import (
    approve_practice_load_package,
    build_v731f_status,
    edit_practice_load_package,
    get_practice_load_package,
    get_practice_load_package_audit,
    get_practice_load_package_source_trace,
    list_practice_load_packages,
    reject_practice_load_package,
    revalidate_practice_load_package,
    save_practice_load_package,
)
from personal_skill_studio.training_artifacts.practice_runtime_loader import load_practice_runtime_package
from personal_skill_studio.training_artifacts.practice_runtime_monitor import list_practice_runtime_usage
from personal_skill_studio.training_artifacts.practice_runtime_policy_engine import evaluate_practice_runtime_policy
from personal_skill_studio.training_artifacts.practice_runtime_registry import (
    build_v731g_status,
    get_runtime_load,
    get_runtime_load_audit,
    get_runtime_load_source_trace,
    list_runtime_loads,
)
from personal_skill_studio.training_artifacts.practice_runtime_rollback_engine import (
    disable_runtime_load,
    enable_runtime_load_active,
    enable_runtime_load_gray,
    rollback_runtime_load,
)
from personal_skill_studio.training_artifacts.practice_output_observation import (
    build_output_observation_status,
    create_output_observation,
    get_output_observation,
    list_output_observations,
)
from personal_skill_studio.training_artifacts.raw_work_product_boundary import build_raw_work_product_boundary_status
from personal_skill_studio.training_artifacts.real_closed_case_intake import (
    build_intake_status,
    create_intake,
    get_audit as get_intake_audit,
    get_classification,
    get_intake,
    get_redaction_report,
    get_review_queue,
    get_safety as get_intake_safety,
    get_segments,
    get_source_traces,
    list_intakes,
    run_classification,
    run_redaction,
    run_segmentation,
    submit_review_action,
)
from personal_skill_studio.training_artifacts.safety_engine import build_safety
from personal_skill_studio.training_artifacts.schemas import (
    ArtifactListResponse,
    CaseCauseMatchRequest,
    CaseAnalysisOutputFeedbackRequest,
    CaseAnalysisImprovementActionRequest,
    CaseAnalysisImprovementBuildRequest,
    CaseAnalysisOutputRiskEventRequest,
    CodexTrainingDryRunRequest,
    CodexTrainingRunStartRequest,
    CodexSkillDraftBuildRequest,
    CodexSkillDraftReviewRequest,
    CodexTrainingRunRequest,
    ExperienceCandidateBuildRequest,
    ExperienceCandidateReviewRequest,
    ExperiencePackageBuildRequest,
    LegalRetrievalJobRequest,
    LoadDryRunRequest,
    NextExperiencePackageActionRequest,
    NextExperiencePackageRebuildRequest,
    OcrJobRequest,
    PracticeLoadReviewDecisionRequest,
    PracticeLoadReviewEditRequest,
    PracticeLoadReviewSaveRequest,
    PracticeFeedbackCandidatePackActionRequest,
    PracticeFeedbackCandidatePackBuildRequest,
    PracticeFeedbackTriageRequest,
    PracticeLawyerFeedbackRequest,
    PracticeOutputObservationRequest,
    PracticeRiskEventRequest,
    PracticeRuntimeDisableRequest,
    PracticeRuntimeLoadRequest,
    PracticeRuntimePolicyEvaluateRequest,
    PracticeRuntimeRollbackRequest,
    PracticeRuntimeRolloutRequest,
    RealClosedCaseTrainingIntakeRequest,
    SkillPackageBuildRequest,
    SkillExperienceBindingRequest,
    SkillExperienceImportRequest,
    TrainingArtifactStatus,
    TrainingDatasetBuildRequest,
    TrainingTaskBuildRequest,
    TrainingIntakeReviewActionRequest,
)
from personal_skill_studio.training_artifacts.practice_risk_event_registry import (
    create_practice_risk_event,
    get_practice_risk_event,
    list_practice_risk_events,
)
from personal_skill_studio.training_artifacts.skill_experience_binding_engine import create_binding, get_binding, list_bindings
from personal_skill_studio.training_artifacts.skill_experience_pool import (
    get_pool_entry,
    import_approved_experience,
    list_pool_entries,
    pool_status,
)
from personal_skill_studio.training_artifacts.skill_experience_safety_engine import build_v731c_status
from personal_skill_studio.training_artifacts.skill_package_registry import (
    build_package_record,
    get_package_audit_record,
    get_package_manifest_record,
    get_package_record,
    get_package_source_trace_record,
    get_v731d_pipeline_status,
    list_package_records,
    validate_package_record,
)
from personal_skill_studio.training_artifacts.training_package_registry import (
    build_experience_package_record,
    build_training_task_record,
    build_v731e_status,
    get_experience_package_audit_record,
    get_experience_package_record,
    get_experience_package_source_trace_record,
    list_experience_package_records,
    list_training_task_records,
)
from personal_skill_studio.training_artifacts.training_dataset_builder import (
    build_training_dataset,
    get_training_dataset_status,
    get_training_gate_report,
    list_training_dataset_examples,
)
from personal_skill_studio.training_artifacts.training_run_engine import (
    build_training_run_audit,
    build_training_run_safety,
    create_training_run,
    create_training_run_load_dry_run,
    get_training_run,
    list_training_runs,
)
from personal_skill_studio.training_artifacts.training_material_runtime import (
    boundary_status as raw_training_material_boundary_status,
    build_experience_candidates as build_raw_based_experience_candidates,
    build_redacted_experience_package,
    build_v735a_status,
    build_v735b_status,
    get_document_parse_job as get_training_material_document_parse_job,
    get_experience_candidate as get_raw_based_experience_candidate,
    get_material as get_training_material,
    get_ocr_job as get_training_material_ocr_job,
    get_parse_quality_gate as get_training_material_parse_quality_gate,
    get_redacted_experience_package,
    list_document_parse_jobs as list_training_material_document_parse_jobs,
    list_evidence_indexes,
    list_experience_candidates as list_raw_based_experience_candidates,
    list_judgment_structures,
    list_legal_retrieval_jobs as list_training_material_legal_retrieval_jobs,
    list_materials as list_training_materials,
    list_ocr_jobs as list_training_material_ocr_jobs,
    list_redacted_experience_packages,
    list_rule_alignments as list_training_material_rule_alignments,
    list_work_product_structures,
    package_audit as get_redacted_experience_package_audit,
    package_source_trace as get_redacted_experience_package_source_trace,
    redaction_report as get_redacted_experience_package_redaction_report,
    register_material as register_training_material,
    run_document_parse_job,
    run_legal_retrieval as run_training_material_legal_retrieval,
    run_ocr_job as run_training_material_ocr,
    run_parse_quality_gate as run_training_material_parse_quality_gate,
    run_rule_alignment as run_training_material_rule_alignment,
    run_structure_jobs as run_training_material_structure_jobs,
)
from personal_skill_studio.training_artifacts.safe_provider_adapter_runtime import (
    call_provider_placeholder,
    list_provider_adapters,
    provider_adapter_status,
)


router = APIRouter(prefix="/training-artifacts", tags=["personal-skill-studio-training-artifacts"])


def _ensure(payload):
    if payload is None:
        raise HTTPException(status_code=404, detail="metadata not found")
    return payload


def _safe_list(items: list[Any]) -> dict[str, Any]:
    return ArtifactListResponse(
        artifacts=[item.model_dump() if hasattr(item, "model_dump") else item for item in items],
        artifact_count=len(items),
        warnings=["Synthetic training artifact manifests only."],
    ).model_dump()


def _looks_like_local_path(value: str) -> bool:
    text = str(value or "")
    return text.startswith(("/Users/", "/Volumes/", "/", "./", "../", "file://")) or ":\\" in text


def _is_http_url(value: str) -> bool:
    text = str(value or "").strip().lower()
    return text.startswith("http://") or text.startswith("https://")


def _external_ocr_source_ref(payload: dict[str, Any]) -> tuple[str, str]:
    for key in ("file_url", "fileUrl", "file_path_or_url"):
        value = str(payload.get(key) or "").strip()
        if value:
            return value, "url" if _is_http_url(value) else "invalid_path"
    for key in ("fileRef", "file_ref", "controlled_file_ref"):
        value = str(payload.get(key) or "").strip()
        if value:
            return value, "file_ref"
    return "", "missing"


def _controlled_file_ref_exists(file_ref: str) -> bool:
    material = get_training_material(file_ref)
    if material:
        return True
    materials = list_training_materials().get("materials", [])
    for item in materials:
        if not isinstance(item, dict):
            continue
        allowed_values = {
            str(item.get("file_ref") or ""),
            str(item.get("fileRef") or ""),
            str(item.get("file_ref_id") or ""),
            str(item.get("controlled_file_ref") or ""),
            str(item.get("training_material_id") or ""),
        }
        if file_ref in allowed_values:
            return True
    return False


@router.get("/status")
def status() -> dict[str, Any]:
    taxonomy = build_taxonomy_manifest()
    packages = list_packages()
    skills = list_skills()
    return TrainingArtifactStatus(
        package_count=len(packages),
        skill_count=len(skills),
        taxonomy_node_count=taxonomy.node_count,
        warnings=["v7.30 is a metadata loader dry-run; no model fine-tuning or real training is executed."],
    ).model_dump()


@router.get("/scheme")
def scheme() -> dict[str, Any]:
    return build_scheme().model_dump()


@router.get("/case-cause-taxonomy")
def case_cause_taxonomy() -> dict[str, Any]:
    return build_taxonomy_manifest().model_dump()


@router.get("/case-cause-taxonomy/{case_cause_id}")
def case_cause_taxonomy_detail(case_cause_id: str) -> dict[str, Any]:
    node = get_case_cause_node(case_cause_id)
    if node is None:
        raise HTTPException(status_code=404, detail="case_cause_id 不存在")
    return node.model_dump()


@router.get("/packages")
def packages() -> dict[str, Any]:
    return _safe_list(list_packages())


@router.get("/packages/{package_id}")
def package_detail(package_id: str) -> dict[str, Any]:
    package = get_package(package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="package_id 不存在")
    return package.model_dump()


@router.get("/skills")
def skills() -> dict[str, Any]:
    return _safe_list(list_skills())


@router.get("/skills/{skill_id}")
def skill_detail(skill_id: str) -> dict[str, Any]:
    skill = get_skill(skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="skill_id 不存在")
    return skill.model_dump()


@router.get("/evaluations")
def evaluations() -> dict[str, Any]:
    return _safe_list(list_evaluations())


@router.get("/gates")
def gates() -> dict[str, Any]:
    return _safe_list(list_gates())


@router.get("/test-cases")
def test_cases() -> dict[str, Any]:
    return _safe_list(list_test_cases())


@router.get("/loading-manifests")
def loading_manifests() -> dict[str, Any]:
    return _safe_list(list_loading_manifests())


@router.post("/case-cause-match/mock")
def case_cause_match_mock(request: CaseCauseMatchRequest) -> dict[str, Any]:
    return match_case_cause(request).model_dump()


@router.post("/load-dry-run/mock")
def load_dry_run_mock(request: LoadDryRunRequest) -> dict[str, Any]:
    return create_load_dry_run(request)


@router.get("/load-dry-runs")
def load_dry_runs() -> dict[str, Any]:
    return list_load_dry_runs()


@router.get("/load-dry-runs/{run_id}")
def load_dry_run_detail(run_id: str) -> dict[str, Any]:
    record = get_load_dry_run(run_id)
    if record is None:
        raise HTTPException(status_code=404, detail="run_id 不存在")
    return record


@router.get("/skill-contexts")
def skill_contexts() -> dict[str, Any]:
    return list_skill_contexts()


@router.get("/skill-contexts/{skill_context_id}")
def skill_context_detail(skill_context_id: str) -> dict[str, Any]:
    context = get_skill_context(skill_context_id)
    if context is None:
        raise HTTPException(status_code=404, detail="skill_context_id 不存在")
    return context.model_dump()


@router.get("/audit")
def audit() -> dict[str, Any]:
    return build_audit()


@router.get("/safety")
def safety() -> dict[str, Any]:
    return build_safety()


@router.get("/real-closed-case-intake/status")
def real_closed_case_intake_status() -> dict[str, Any]:
    return build_intake_status()


@router.post("/real-closed-case-intake/mock")
def real_closed_case_intake_mock(request: RealClosedCaseTrainingIntakeRequest) -> dict[str, Any]:
    return create_intake(request)


@router.get("/real-closed-case-intakes")
def real_closed_case_intakes() -> dict[str, Any]:
    return list_intakes()


@router.get("/real-closed-case-intakes/{intake_id}")
def real_closed_case_intake_detail(intake_id: str) -> dict[str, Any]:
    return _ensure(get_intake(intake_id))


@router.get("/real-closed-case-intakes/{intake_id}/redaction-report")
def real_closed_case_redaction_report(intake_id: str) -> dict[str, Any]:
    return _ensure(get_redaction_report(intake_id))


@router.post("/real-closed-case-intakes/{intake_id}/redaction/mock")
def real_closed_case_redaction_mock(intake_id: str) -> dict[str, Any]:
    return _ensure(run_redaction(intake_id))


@router.get("/real-closed-case-intakes/{intake_id}/case-cause-classification")
def real_closed_case_classification(intake_id: str) -> dict[str, Any]:
    return _ensure(get_classification(intake_id))


@router.post("/real-closed-case-intakes/{intake_id}/case-cause-classification/mock")
def real_closed_case_classification_mock(intake_id: str) -> dict[str, Any]:
    return _ensure(run_classification(intake_id))


@router.get("/real-closed-case-intakes/{intake_id}/segments")
def real_closed_case_segments(intake_id: str) -> dict[str, Any]:
    return _ensure(get_segments(intake_id))


@router.post("/real-closed-case-intakes/{intake_id}/segments/mock")
def real_closed_case_segments_mock(intake_id: str) -> dict[str, Any]:
    return _ensure(run_segmentation(intake_id))


@router.get("/real-closed-case-intakes/{intake_id}/review-queue")
def real_closed_case_review_queue(intake_id: str) -> dict[str, Any]:
    return _ensure(get_review_queue(intake_id))


@router.post("/real-closed-case-intakes/{intake_id}/review-queue/{review_item_id}/actions/mock")
def real_closed_case_review_action_mock(
    intake_id: str,
    review_item_id: str,
    request: TrainingIntakeReviewActionRequest,
) -> dict[str, Any]:
    return _ensure(submit_review_action(intake_id, review_item_id, request))


@router.get("/real-closed-case-intakes/{intake_id}/source-traces")
def real_closed_case_source_traces(intake_id: str) -> dict[str, Any]:
    return _ensure(get_source_traces(intake_id))


@router.get("/real-closed-case-intakes/{intake_id}/audit")
def real_closed_case_audit(intake_id: str) -> dict[str, Any]:
    return _ensure(get_intake_audit(intake_id))


@router.get("/real-closed-case-intakes/{intake_id}/safety")
def real_closed_case_safety(intake_id: str) -> dict[str, Any]:
    return _ensure(get_intake_safety(intake_id))


@router.get("/raw-work-product-boundary/status")
def raw_work_product_boundary_status() -> dict[str, Any]:
    return build_raw_work_product_boundary_status()


@router.post("/ocr-jobs")
def ocr_jobs_create(request: OcrJobRequest) -> dict[str, Any]:
    return create_ocr_job(request)


@router.get("/ocr-jobs")
def ocr_jobs() -> dict[str, Any]:
    return list_ocr_jobs()


@router.get("/ocr-jobs/{job_id}")
def ocr_job_detail(job_id: str) -> dict[str, Any]:
    return _ensure(get_ocr_job(job_id))


@router.post("/legal-retrieval-jobs")
def legal_retrieval_jobs_create(request: LegalRetrievalJobRequest) -> dict[str, Any]:
    return create_legal_retrieval_job(request)


@router.get("/legal-retrieval-jobs")
def legal_retrieval_jobs() -> dict[str, Any]:
    return list_legal_retrieval_jobs()


@router.get("/legal-retrieval-jobs/{job_id}")
def legal_retrieval_job_detail(job_id: str) -> dict[str, Any]:
    return _ensure(get_legal_retrieval_job(job_id))


@router.post("/experience-candidates/build")
def experience_candidates_build(request: ExperienceCandidateBuildRequest) -> dict[str, Any]:
    return build_candidates(request)


@router.get("/experience-candidates")
def experience_candidates() -> dict[str, Any]:
    return list_candidates()


@router.get("/experience-candidates/{candidate_id}")
def experience_candidate_detail(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_candidate(candidate_id))


@router.post("/experience-candidates/{candidate_id}/redact")
def experience_candidate_redact(candidate_id: str) -> dict[str, Any]:
    return _ensure(redact_experience_candidate(candidate_id))


@router.post("/experience-candidates/{candidate_id}/review")
def experience_candidate_review(candidate_id: str, request: ExperienceCandidateReviewRequest) -> dict[str, Any]:
    return _ensure(review_experience_candidate(candidate_id, request))


@router.get("/experience-candidates/{candidate_id}/audit")
def experience_candidate_audit(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_candidate_audit(candidate_id))


@router.get("/v7-31b/status")
def v731b_status() -> dict[str, Any]:
    return build_v731b_status()


@router.get("/skill-experience-pool/status")
def skill_experience_pool_status() -> dict[str, Any]:
    return pool_status()


@router.post("/skill-experience-pool/import-approved")
def skill_experience_pool_import_approved(request: SkillExperienceImportRequest) -> dict[str, Any]:
    return import_approved_experience(request)


@router.get("/skill-experience-pool")
def skill_experience_pool() -> dict[str, Any]:
    return list_pool_entries()


@router.get("/skill-experience-pool/{experience_id}")
def skill_experience_pool_detail(experience_id: str) -> dict[str, Any]:
    return _ensure(get_pool_entry(experience_id))


@router.post("/skill-experience-bindings")
def skill_experience_bindings_create(request: SkillExperienceBindingRequest) -> dict[str, Any]:
    return create_binding(request)


@router.get("/skill-experience-bindings")
def skill_experience_bindings() -> dict[str, Any]:
    return list_bindings()


@router.get("/skill-experience-bindings/{binding_id}")
def skill_experience_binding_detail(binding_id: str) -> dict[str, Any]:
    return _ensure(get_binding(binding_id))


@router.post("/codex-skill-drafts/build")
def codex_skill_drafts_build(request: CodexSkillDraftBuildRequest) -> dict[str, Any]:
    return create_draft(request)


@router.get("/codex-skill-drafts")
def codex_skill_drafts() -> dict[str, Any]:
    return list_drafts()


@router.get("/codex-skill-drafts/{draft_id}")
def codex_skill_draft_detail(draft_id: str) -> dict[str, Any]:
    return _ensure(get_draft(draft_id))


@router.post("/codex-skill-drafts/{draft_id}/review")
def codex_skill_draft_review(draft_id: str, request: CodexSkillDraftReviewRequest) -> dict[str, Any]:
    return _ensure(review_draft(draft_id, request))


@router.get("/codex-skill-drafts/{draft_id}/audit")
def codex_skill_draft_audit(draft_id: str) -> dict[str, Any]:
    return _ensure(get_draft_audit(draft_id))


@router.get("/v7-31c/status")
def v731c_status() -> dict[str, Any]:
    return build_v731c_status()


@router.get("/skill-packages")
def skill_packages() -> dict[str, Any]:
    return list_package_records()


@router.get("/skill-packages/{package_id}")
def skill_package_detail(package_id: str) -> dict[str, Any]:
    return _ensure(get_package_record(package_id))


@router.post("/skill-packages/build")
def skill_packages_build(request: SkillPackageBuildRequest) -> dict[str, Any]:
    return _ensure(build_package_record(request))


@router.post("/skill-packages/{package_id}/validate")
def skill_package_validate(package_id: str) -> dict[str, Any]:
    return _ensure(validate_package_record(package_id))


@router.get("/skill-packages/{package_id}/manifest")
def skill_package_manifest(package_id: str) -> dict[str, Any]:
    return _ensure(get_package_manifest_record(package_id))


@router.get("/skill-packages/{package_id}/audit")
def skill_package_audit(package_id: str) -> dict[str, Any]:
    return _ensure(get_package_audit_record(package_id))


@router.get("/skill-packages/{package_id}/source-trace")
def skill_package_source_trace(package_id: str) -> dict[str, Any]:
    return _ensure(get_package_source_trace_record(package_id))


@router.get("/v7-31d/status")
def v731d_status() -> dict[str, Any]:
    return get_v731d_pipeline_status()


@router.get("/training-tasks")
def training_tasks() -> dict[str, Any]:
    return list_training_task_records()


@router.post("/training-tasks/build")
def training_tasks_build(request: TrainingTaskBuildRequest) -> dict[str, Any]:
    return _ensure(build_training_task_record(request))


@router.get("/training-packages")
def training_packages() -> dict[str, Any]:
    return list_experience_package_records()


@router.post("/training-packages/build")
def training_packages_build(request: ExperiencePackageBuildRequest) -> dict[str, Any]:
    return _ensure(build_experience_package_record(request))


@router.get("/training-packages/{package_id}")
def training_package_detail(package_id: str) -> dict[str, Any]:
    return _ensure(get_experience_package_record(package_id))


@router.get("/training-packages/{package_id}/audit")
def training_package_audit(package_id: str) -> dict[str, Any]:
    return _ensure(get_experience_package_audit_record(package_id))


@router.get("/training-packages/{package_id}/source-trace")
def training_package_source_trace(package_id: str) -> dict[str, Any]:
    return _ensure(get_experience_package_source_trace_record(package_id))


@router.get("/v7-31e/status")
def v731e_status() -> dict[str, Any]:
    return build_v731e_status()


@router.get("/practice-load-review/packages")
def practice_load_review_packages() -> dict[str, Any]:
    return list_practice_load_packages()


@router.get("/practice-load-review/packages/{package_id}")
def practice_load_review_package_detail(package_id: str) -> dict[str, Any]:
    return _ensure(get_practice_load_package(package_id))


@router.post("/practice-load-review/packages/{package_id}/edit")
def practice_load_review_package_edit(package_id: str, request: PracticeLoadReviewEditRequest) -> dict[str, Any]:
    return _ensure(edit_practice_load_package(package_id, request))


@router.post("/practice-load-review/packages/{package_id}/save")
def practice_load_review_package_save(package_id: str, request: PracticeLoadReviewSaveRequest) -> dict[str, Any]:
    return _ensure(save_practice_load_package(package_id, request))


@router.post("/practice-load-review/packages/{package_id}/revalidate")
def practice_load_review_package_revalidate(package_id: str) -> dict[str, Any]:
    return _ensure(revalidate_practice_load_package(package_id))


@router.post("/practice-load-review/packages/{package_id}/approve")
def practice_load_review_package_approve(package_id: str, request: PracticeLoadReviewDecisionRequest) -> dict[str, Any]:
    return _ensure(approve_practice_load_package(package_id, request))


@router.post("/practice-load-review/packages/{package_id}/reject")
def practice_load_review_package_reject(package_id: str, request: PracticeLoadReviewDecisionRequest) -> dict[str, Any]:
    return _ensure(reject_practice_load_package(package_id, request))


@router.get("/practice-load-review/packages/{package_id}/audit")
def practice_load_review_package_audit(package_id: str) -> dict[str, Any]:
    return _ensure(get_practice_load_package_audit(package_id))


@router.get("/practice-load-review/packages/{package_id}/source-trace")
def practice_load_review_package_source_trace(package_id: str) -> dict[str, Any]:
    return _ensure(get_practice_load_package_source_trace(package_id))


@router.get("/v7-31f/status")
def v731f_status() -> dict[str, Any]:
    return build_v731f_status()


@router.get("/practice-runtime-loads/status")
def practice_runtime_loads_status() -> dict[str, Any]:
    return build_v731g_status()


@router.post("/practice-runtime-loads/load")
def practice_runtime_loads_load(request: PracticeRuntimeLoadRequest) -> dict[str, Any]:
    return _ensure(load_practice_runtime_package(request))


@router.get("/practice-runtime-loads")
def practice_runtime_loads() -> dict[str, Any]:
    return list_runtime_loads()


@router.get("/practice-runtime-loads/{runtime_load_id}")
def practice_runtime_load_detail(runtime_load_id: str) -> dict[str, Any]:
    return _ensure(get_runtime_load(runtime_load_id))


@router.post("/practice-runtime-loads/{runtime_load_id}/enable-gray")
def practice_runtime_load_enable_gray(runtime_load_id: str, request: PracticeRuntimeRolloutRequest) -> dict[str, Any]:
    return _ensure(enable_runtime_load_gray(runtime_load_id, request))


@router.post("/practice-runtime-loads/{runtime_load_id}/enable-active")
def practice_runtime_load_enable_active(runtime_load_id: str, request: PracticeRuntimeRolloutRequest) -> dict[str, Any]:
    return _ensure(enable_runtime_load_active(runtime_load_id, request))


@router.post("/practice-runtime-loads/{runtime_load_id}/disable")
def practice_runtime_load_disable(runtime_load_id: str, request: PracticeRuntimeDisableRequest) -> dict[str, Any]:
    return _ensure(disable_runtime_load(runtime_load_id, request))


@router.post("/practice-runtime-loads/{runtime_load_id}/rollback")
def practice_runtime_load_rollback(runtime_load_id: str, request: PracticeRuntimeRollbackRequest) -> dict[str, Any]:
    return _ensure(rollback_runtime_load(runtime_load_id, request))


@router.post("/practice-runtime-policy/evaluate")
def practice_runtime_policy_evaluate(request: PracticeRuntimePolicyEvaluateRequest) -> dict[str, Any]:
    return evaluate_practice_runtime_policy(request)


@router.get("/practice-runtime-usage")
def practice_runtime_usage() -> dict[str, Any]:
    return list_practice_runtime_usage()


@router.get("/practice-runtime-loads/{runtime_load_id}/audit")
def practice_runtime_load_audit(runtime_load_id: str) -> dict[str, Any]:
    return _ensure(get_runtime_load_audit(runtime_load_id))


@router.get("/practice-runtime-loads/{runtime_load_id}/source-trace")
def practice_runtime_load_source_trace(runtime_load_id: str) -> dict[str, Any]:
    return _ensure(get_runtime_load_source_trace(runtime_load_id))


@router.get("/v7-31g/status")
def v731g_status() -> dict[str, Any]:
    return build_v731g_status()


@router.get("/practice-output-observations/status")
def practice_output_observations_status() -> dict[str, Any]:
    return build_output_observation_status()


@router.post("/practice-output-observations")
def practice_output_observations_create(request: PracticeOutputObservationRequest) -> dict[str, Any]:
    return _ensure(create_output_observation(request))


@router.get("/practice-output-observations")
def practice_output_observations() -> dict[str, Any]:
    return list_output_observations()


@router.get("/practice-output-observations/{observation_id}")
def practice_output_observation_detail(observation_id: str) -> dict[str, Any]:
    return _ensure(get_output_observation(observation_id))


@router.post("/practice-lawyer-feedback")
def practice_lawyer_feedback_create(request: PracticeLawyerFeedbackRequest) -> dict[str, Any]:
    return _ensure(create_lawyer_feedback(request))


@router.get("/practice-lawyer-feedback")
def practice_lawyer_feedback_list() -> dict[str, Any]:
    return list_lawyer_feedback()


@router.get("/practice-lawyer-feedback/{feedback_id}")
def practice_lawyer_feedback_detail(feedback_id: str) -> dict[str, Any]:
    return _ensure(get_lawyer_feedback(feedback_id))


@router.post("/practice-lawyer-feedback/{feedback_id}/triage")
def practice_lawyer_feedback_triage(feedback_id: str, request: PracticeFeedbackTriageRequest) -> dict[str, Any]:
    return _ensure(triage_lawyer_feedback(feedback_id, request))


@router.post("/practice-risk-events")
def practice_risk_events_create(request: PracticeRiskEventRequest) -> dict[str, Any]:
    return _ensure(create_practice_risk_event(request))


@router.get("/practice-risk-events")
def practice_risk_events() -> dict[str, Any]:
    return list_practice_risk_events()


@router.get("/practice-risk-events/{risk_event_id}")
def practice_risk_event_detail(risk_event_id: str) -> dict[str, Any]:
    return _ensure(get_practice_risk_event(risk_event_id))


@router.get("/practice-feedback-summary")
def practice_feedback_summary() -> dict[str, Any]:
    return build_feedback_summary()


@router.get("/v7-31h/status")
def v731h_status() -> dict[str, Any]:
    return build_v731h_status()


@router.get("/practice-feedback-candidate-packs/status")
def practice_feedback_candidate_packs_status() -> dict[str, Any]:
    return build_v731i_status()


@router.post("/practice-feedback-candidate-packs/build")
def practice_feedback_candidate_packs_build(request: PracticeFeedbackCandidatePackBuildRequest) -> dict[str, Any]:
    return _ensure(build_practice_feedback_candidate_pack(request))


@router.get("/practice-feedback-candidate-packs")
def practice_feedback_candidate_packs() -> dict[str, Any]:
    return list_practice_feedback_candidate_packs()


@router.get("/practice-feedback-candidate-packs/{candidate_pack_id}")
def practice_feedback_candidate_pack_detail(candidate_pack_id: str) -> dict[str, Any]:
    return _ensure(get_practice_feedback_candidate_pack(candidate_pack_id))


@router.get("/practice-feedback-candidate-packs/{candidate_pack_id}/diff")
def practice_feedback_candidate_pack_diff(candidate_pack_id: str) -> dict[str, Any]:
    return _ensure(get_practice_feedback_candidate_pack_diff(candidate_pack_id))


@router.get("/practice-feedback-candidate-packs/{candidate_pack_id}/audit")
def practice_feedback_candidate_pack_audit(candidate_pack_id: str) -> dict[str, Any]:
    return _ensure(get_practice_feedback_candidate_pack_audit(candidate_pack_id))


@router.get("/practice-feedback-candidate-packs/{candidate_pack_id}/source-trace")
def practice_feedback_candidate_pack_source_trace(candidate_pack_id: str) -> dict[str, Any]:
    return _ensure(get_practice_feedback_candidate_pack_source_trace(candidate_pack_id))


@router.post("/practice-feedback-candidate-packs/{candidate_pack_id}/mark-ready")
def practice_feedback_candidate_pack_mark_ready(
    candidate_pack_id: str,
    request: PracticeFeedbackCandidatePackActionRequest,
) -> dict[str, Any]:
    return _ensure(mark_candidate_pack_ready(candidate_pack_id, request))


@router.post("/practice-feedback-candidate-packs/{candidate_pack_id}/archive")
def practice_feedback_candidate_pack_archive(
    candidate_pack_id: str,
    request: PracticeFeedbackCandidatePackActionRequest,
) -> dict[str, Any]:
    return _ensure(archive_candidate_pack(candidate_pack_id, request))


@router.get("/v7-31i/status")
def v731i_status() -> dict[str, Any]:
    return build_v731i_status()


@router.get("/next-experience-packages/status")
def next_experience_packages_status() -> dict[str, Any]:
    return build_v731j_status()


@router.post("/next-experience-packages/rebuild")
def next_experience_packages_rebuild(request: NextExperiencePackageRebuildRequest) -> dict[str, Any]:
    return _ensure(rebuild_next_experience_package_record(request))


@router.get("/next-experience-packages")
def next_experience_packages() -> dict[str, Any]:
    return list_next_experience_packages()


@router.get("/next-experience-packages/{next_package_id}")
def next_experience_package_detail(next_package_id: str) -> dict[str, Any]:
    return _ensure(get_next_experience_package(next_package_id))


@router.get("/next-experience-packages/{next_package_id}/lawyer-review-view")
def next_experience_package_lawyer_review_view(next_package_id: str) -> dict[str, Any]:
    return _ensure(get_next_experience_package_lawyer_review_view(next_package_id))


@router.get("/next-experience-packages/{next_package_id}/manifest")
def next_experience_package_manifest(next_package_id: str) -> dict[str, Any]:
    return _ensure(get_next_experience_package_manifest(next_package_id))


@router.get("/next-experience-packages/{next_package_id}/audit")
def next_experience_package_audit(next_package_id: str) -> dict[str, Any]:
    return _ensure(get_next_experience_package_audit(next_package_id))


@router.get("/next-experience-packages/{next_package_id}/source-trace")
def next_experience_package_source_trace(next_package_id: str) -> dict[str, Any]:
    return _ensure(get_next_experience_package_source_trace(next_package_id))


@router.post("/next-experience-packages/{next_package_id}/mark-pending-load-review")
def next_experience_package_mark_pending_load_review(
    next_package_id: str,
    request: NextExperiencePackageActionRequest,
) -> dict[str, Any]:
    return _ensure(mark_next_package_pending_load_review(next_package_id, request))


@router.post("/next-experience-packages/{next_package_id}/archive")
def next_experience_package_archive(
    next_package_id: str,
    request: NextExperiencePackageActionRequest,
) -> dict[str, Any]:
    return _ensure(archive_next_package(next_package_id, request))


@router.get("/v7-31j/status")
def v731j_status() -> dict[str, Any]:
    return build_v731j_status()


@router.get("/experience-lifecycle/status")
def experience_lifecycle_status() -> dict[str, Any]:
    return build_v732_status()


@router.get("/experience-lifecycles")
def experience_lifecycles() -> dict[str, Any]:
    return list_lifecycles()


@router.get("/experience-lifecycles/{lifecycle_id}")
def experience_lifecycle_detail(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle(lifecycle_id))


@router.get("/experience-lifecycles/{lifecycle_id}/state")
def experience_lifecycle_state(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle_state(lifecycle_id))


@router.get("/experience-lifecycles/{lifecycle_id}/graph")
def experience_lifecycle_graph(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle_graph(lifecycle_id))


@router.get("/experience-lifecycles/{lifecycle_id}/audit-timeline")
def experience_lifecycle_audit_timeline(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle_audit_timeline(lifecycle_id))


@router.get("/experience-lifecycles/{lifecycle_id}/source-trace-view")
def experience_lifecycle_source_trace_view(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle_source_trace_view(lifecycle_id))


@router.get("/experience-lifecycles/{lifecycle_id}/integrity-check")
def experience_lifecycle_integrity_check(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle_integrity_check(lifecycle_id))


@router.get("/experience-lifecycles/{lifecycle_id}/safety-summary")
def experience_lifecycle_safety_summary(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(get_lifecycle_safety_summary(lifecycle_id))


@router.post("/experience-lifecycles/{lifecycle_id}/recompute")
def experience_lifecycle_recompute(lifecycle_id: str) -> dict[str, Any]:
    return _ensure(recompute_lifecycle(lifecycle_id))


@router.get("/v7-32/status")
def v732_status() -> dict[str, Any]:
    return build_v732_status()


@router.get("/case-analysis-workbench/status")
def case_analysis_workbench_status() -> dict[str, Any]:
    return build_v733_workbench_status()


@router.get("/case-analysis-workbench/views")
def case_analysis_workbench_views() -> dict[str, Any]:
    return list_workbench_views()


@router.get("/case-analysis-workbench/views/{view_id}")
def case_analysis_workbench_view_detail(view_id: str) -> dict[str, Any]:
    return _ensure(get_workbench_view(view_id))


@router.get("/case-analysis-workbench/views/{view_id}/schema")
def case_analysis_workbench_schema(view_id: str) -> dict[str, Any]:
    return _ensure(get_workbench_schema(view_id))


@router.get("/case-analysis-workbench/views/{view_id}/outputs")
def case_analysis_workbench_outputs(view_id: str) -> dict[str, Any]:
    return _ensure(list_workbench_outputs(view_id))


@router.get("/case-analysis-workbench/outputs/{output_id}")
def case_analysis_workbench_output_detail(output_id: str) -> dict[str, Any]:
    return _ensure(get_runtime_output(output_id))


@router.post("/case-analysis-workbench/outputs/{output_id}/mark-reviewed")
def case_analysis_workbench_output_mark_reviewed(output_id: str) -> dict[str, Any]:
    return _ensure(mark_output_reviewed(output_id))


@router.post("/case-analysis-workbench/outputs/{output_id}/feedback")
async def case_analysis_workbench_output_feedback(
    output_id: str,
    request: Request,
) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CaseAnalysisOutputFeedbackRequest(**payload)
    return _ensure(submit_output_feedback(output_id, action))


@router.post("/case-analysis-workbench/outputs/{output_id}/risk-event")
async def case_analysis_workbench_output_risk_event(
    output_id: str,
    request: Request,
) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CaseAnalysisOutputRiskEventRequest(**payload)
    return _ensure(submit_output_risk_event(output_id, action))


@router.get("/case-analysis-workbench/outputs/{output_id}/feedback")
def case_analysis_workbench_output_feedback_list(output_id: str) -> dict[str, Any]:
    return list_output_feedback(output_id)


@router.get("/case-analysis-workbench/outputs/{output_id}/risk-events")
def case_analysis_workbench_output_risk_event_list(output_id: str) -> dict[str, Any]:
    return list_output_risk_events(output_id)


@router.get("/case-analysis-workbench/outputs/{output_id}/audit")
def case_analysis_workbench_output_audit(output_id: str) -> dict[str, Any]:
    return _ensure(get_output_audit(output_id))


@router.get("/case-analysis-workbench/outputs/{output_id}/source-trace")
def case_analysis_workbench_output_source_trace(output_id: str) -> dict[str, Any]:
    return _ensure(get_output_source_trace(output_id))


@router.get("/v7-33/status")
def v733_status() -> dict[str, Any]:
    return build_v733_workbench_status()


@router.get("/case-analysis-improvement/status")
def case_analysis_improvement_status() -> dict[str, Any]:
    return build_v734_status()


@router.post("/case-analysis-improvement/candidates/build")
async def case_analysis_improvement_candidates_build(request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CaseAnalysisImprovementBuildRequest(**payload)
    return build_case_analysis_improvement_candidates(action)


@router.get("/case-analysis-improvement/candidates")
def case_analysis_improvement_candidates() -> dict[str, Any]:
    return list_case_analysis_improvement_candidates()


@router.get("/case-analysis-improvement/candidates/{candidate_id}")
def case_analysis_improvement_candidate_detail(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_case_analysis_improvement_candidate(candidate_id))


@router.get("/case-analysis-improvement/candidates/{candidate_id}/readiness")
def case_analysis_improvement_candidate_readiness(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_case_analysis_improvement_candidate_readiness(candidate_id))


@router.post("/case-analysis-improvement/candidates/{candidate_id}/mark-ready")
async def case_analysis_improvement_candidate_mark_ready(candidate_id: str, request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CaseAnalysisImprovementActionRequest(**payload)
    return _ensure(mark_case_analysis_improvement_candidate_ready(candidate_id, action))


@router.post("/case-analysis-improvement/candidates/{candidate_id}/archive")
async def case_analysis_improvement_candidate_archive(candidate_id: str, request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CaseAnalysisImprovementActionRequest(**payload)
    return _ensure(archive_case_analysis_improvement_candidate(candidate_id, action))


@router.get("/case-analysis-improvement/output-traces")
def case_analysis_improvement_output_traces() -> dict[str, Any]:
    return list_case_analysis_output_to_experience_traces()


@router.get("/case-analysis-improvement/output-traces/{trace_id}")
def case_analysis_improvement_output_trace_detail(trace_id: str) -> dict[str, Any]:
    return _ensure(get_case_analysis_output_to_experience_trace(trace_id))


@router.post("/case-analysis-improvement/diff/build")
def case_analysis_improvement_diff_build() -> dict[str, Any]:
    return build_case_analysis_improvement_diff()


@router.get("/case-analysis-improvement/diffs")
def case_analysis_improvement_diffs() -> dict[str, Any]:
    return list_case_analysis_improvement_diffs()


@router.get("/case-analysis-improvement/diffs/{diff_id}")
def case_analysis_improvement_diff_detail(diff_id: str) -> dict[str, Any]:
    return _ensure(get_case_analysis_improvement_diff(diff_id))


@router.get("/case-analysis-improvement/candidates/{candidate_id}/audit")
def case_analysis_improvement_candidate_audit(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_case_analysis_improvement_candidate_audit(candidate_id))


@router.get("/case-analysis-improvement/candidates/{candidate_id}/source-trace")
def case_analysis_improvement_candidate_source_trace(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_case_analysis_improvement_candidate_source_trace(candidate_id))


@router.get("/v7-34/status")
def v734_status() -> dict[str, Any]:
    return build_v734_status()


@router.get("/training-dataset/status")
def training_dataset_status() -> dict[str, Any]:
    return get_training_dataset_status()


@router.post("/training-dataset/build")
async def training_dataset_build(request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = TrainingDatasetBuildRequest(**payload)
    return build_training_dataset(action)


@router.get("/training-dataset/examples")
def training_dataset_examples() -> dict[str, Any]:
    return list_training_dataset_examples()


@router.get("/training-dataset/gate-report")
def training_dataset_gate_report() -> dict[str, Any]:
    return get_training_gate_report()


@router.get("/training-dryrun/status")
def training_dryrun_status() -> dict[str, Any]:
    return get_codex_training_dryrun_status()


@router.post("/training-dryrun/run")
async def training_dryrun_run(request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CodexTrainingDryRunRequest(**payload)
    return run_codex_training_dryrun(action)


@router.get("/training-dryrun/logs")
def training_dryrun_logs() -> dict[str, Any]:
    return list_codex_training_dryrun_logs()


@router.get("/training-dryrun/gate-report")
def training_dryrun_gate_report() -> dict[str, Any]:
    return get_codex_training_dryrun_gate_report()


@router.post("/training-run/start")
async def training_run_start(request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = CodexTrainingRunStartRequest(**payload)
    return start_codex_internal_training_run(action)


@router.get("/training-run/status")
def training_run_status() -> dict[str, Any]:
    return get_codex_internal_training_status()


@router.get("/training-run/logs")
def training_run_logs() -> dict[str, Any]:
    return list_codex_internal_training_logs()


@router.get("/training-run/gate-report")
def training_run_gate_report() -> dict[str, Any]:
    return get_codex_internal_training_gate_report()


@router.get("/training-materials/raw-boundary/status")
def training_materials_raw_boundary_status() -> dict[str, Any]:
    return raw_training_material_boundary_status()


@router.post("/training-materials/register")
async def training_materials_register(request: Request) -> dict[str, Any]:
    return register_training_material(await _safe_request_payload(request))


@router.get("/training-materials")
def training_materials() -> dict[str, Any]:
    return list_training_materials()


@router.post("/training-materials/ocr-jobs/run")
async def training_material_ocr_jobs_run(request: Request) -> dict[str, Any]:
    return run_training_material_ocr(await _safe_request_payload(request))


@router.get("/training-materials/ocr-jobs")
def training_material_ocr_jobs() -> dict[str, Any]:
    return list_training_material_ocr_jobs()


@router.get("/training-materials/ocr-jobs/{ocr_job_id}")
def training_material_ocr_job_detail(ocr_job_id: str) -> dict[str, Any]:
    return _ensure(get_training_material_ocr_job(ocr_job_id))


@router.post("/training-materials/document-parse-jobs/run")
async def training_material_document_parse_jobs_run(request: Request) -> dict[str, Any]:
    return run_document_parse_job(await _safe_request_payload(request))


@router.get("/training-materials/document-parse-jobs")
def training_material_document_parse_jobs() -> dict[str, Any]:
    return list_training_material_document_parse_jobs()


@router.get("/training-materials/document-parse-jobs/{parse_job_id}")
def training_material_document_parse_job_detail(parse_job_id: str) -> dict[str, Any]:
    return _ensure(get_training_material_document_parse_job(parse_job_id))


@router.post("/training-materials/structure-jobs/run")
async def training_material_structure_jobs_run(request: Request) -> dict[str, Any]:
    return run_training_material_structure_jobs(await _safe_request_payload(request))


@router.get("/training-materials/judgment-structures")
def training_material_judgment_structures() -> dict[str, Any]:
    return list_judgment_structures()


@router.get("/training-materials/work-product-structures")
def training_material_work_product_structures() -> dict[str, Any]:
    return list_work_product_structures()


@router.get("/training-materials/evidence-indexes")
def training_material_evidence_indexes() -> dict[str, Any]:
    return list_evidence_indexes()


@router.post("/training-materials/legal-retrieval-jobs/run")
async def training_material_legal_retrieval_jobs_run(request: Request) -> dict[str, Any]:
    return run_training_material_legal_retrieval(await _safe_request_payload(request))


@router.get("/training-materials/legal-retrieval-jobs")
def training_material_legal_retrieval_jobs() -> dict[str, Any]:
    return list_training_material_legal_retrieval_jobs()


@router.post("/training-materials/rule-alignment/run")
async def training_material_rule_alignment_run(request: Request) -> dict[str, Any]:
    return run_training_material_rule_alignment(await _safe_request_payload(request))


@router.get("/training-materials/rule-alignments")
def training_material_rule_alignments() -> dict[str, Any]:
    return list_training_material_rule_alignments()


@router.post("/training-materials/parse-quality-gate/run")
async def training_material_parse_quality_gate_run(request: Request) -> dict[str, Any]:
    return run_training_material_parse_quality_gate(await _safe_request_payload(request))


@router.get("/training-materials/parse-quality-gate/{material_batch_id}")
def training_material_parse_quality_gate_detail(material_batch_id: str) -> dict[str, Any]:
    return _ensure(get_training_material_parse_quality_gate(material_batch_id))


@router.get("/v7-35a/status")
def v735a_status() -> dict[str, Any]:
    return build_v735a_status()


@router.post("/training-materials/experience-candidates/build")
async def training_material_experience_candidates_build(request: Request) -> dict[str, Any]:
    return build_raw_based_experience_candidates(await _safe_request_payload(request))


@router.get("/training-materials/experience-candidates")
def training_material_experience_candidates() -> dict[str, Any]:
    return list_raw_based_experience_candidates()


@router.get("/training-materials/experience-candidates/{candidate_id}")
def training_material_experience_candidate_detail(candidate_id: str) -> dict[str, Any]:
    return _ensure(get_raw_based_experience_candidate(candidate_id))


@router.post("/training-materials/redacted-experience-packages/build")
async def training_material_redacted_experience_package_build(request: Request) -> dict[str, Any]:
    return build_redacted_experience_package(await _safe_request_payload(request))


@router.get("/training-materials/redacted-experience-packages")
def training_material_redacted_experience_packages() -> dict[str, Any]:
    return list_redacted_experience_packages()


@router.get("/training-materials/redacted-experience-packages/{package_id}")
def training_material_redacted_experience_package_detail(package_id: str) -> dict[str, Any]:
    return _ensure(get_redacted_experience_package(package_id))


@router.get("/training-materials/redacted-experience-packages/{package_id}/redaction-report")
def training_material_redacted_experience_package_redaction_report(package_id: str) -> dict[str, Any]:
    return _ensure(get_redacted_experience_package_redaction_report(package_id))


@router.get("/training-materials/redacted-experience-packages/{package_id}/audit")
def training_material_redacted_experience_package_audit(package_id: str) -> dict[str, Any]:
    return _ensure(get_redacted_experience_package_audit(package_id))


@router.get("/training-materials/redacted-experience-packages/{package_id}/source-trace")
def training_material_redacted_experience_package_source_trace(package_id: str) -> dict[str, Any]:
    return _ensure(get_redacted_experience_package_source_trace(package_id))


@router.get("/v7-35b/status")
def v735b_status() -> dict[str, Any]:
    return build_v735b_status()


@router.get("/training-materials/{training_material_id}")
def training_material_detail(training_material_id: str) -> dict[str, Any]:
    return _ensure(get_training_material(training_material_id))


@router.post("/training-materials/external-ocr/parse")
async def training_material_external_ocr_parse(request: Request) -> dict[str, Any]:
    return start_external_ocr_parse(await _safe_request_payload(request))


@router.get("/external-ocr/status")
def external_ocr_status() -> dict[str, Any]:
    return check_external_ocr_ready()


@router.get("/external-ocr/diagnostics")
def external_ocr_provider_diagnostics() -> dict[str, Any]:
    return external_ocr_diagnostics()


@router.post("/external-ocr/jobs/submit")
async def external_ocr_job_submit(request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    material_id = str(payload.get("material_id") or "").strip()
    source_ref, source_mode = _external_ocr_source_ref(payload)
    if not source_ref:
        status = check_external_ocr_ready()
        return record_external_ocr_job_submission(
            {
                "ocr_mode": "external_ocr_failed",
                "parse_status": "failed",
                "provider_job_id": None,
                "file_ref": "file_ref_missing",
                "credential_loaded": bool(status.get("credential_loaded")),
                "provider_call_allowed": bool(status.get("provider_call_allowed")),
                "external_ocr_completed": False,
                "real_material_training_allowed": False,
                "training_status": "blocked_for_external_ocr",
                "redacted_error_summary": "material_id and controlled file reference are required.",
            },
            material_id=material_id or "controlled_file_ref",
            file_ref="file_ref_missing",
        )
    if source_mode == "invalid_path" or _looks_like_local_path(source_ref):
        status = check_external_ocr_ready()
        return record_external_ocr_job_submission(
            {
                "ocr_mode": "external_ocr_failed",
                "parse_status": "failed",
                "provider_job_id": None,
                "file_ref": redacted_file_ref(source_ref),
                "credential_loaded": bool(status.get("credential_loaded")),
                "provider_call_allowed": False,
                "external_ocr_completed": False,
                "real_material_training_allowed": False,
                "training_status": "blocked_for_external_ocr",
                "redacted_error_summary": "Invalid file reference. Raw path was not exposed.",
            },
            material_id=material_id or "controlled_file_ref",
            file_ref=redacted_file_ref(source_ref),
        )
    if source_mode == "file_ref" and not _controlled_file_ref_exists(source_ref):
        status = check_external_ocr_ready()
        return record_external_ocr_job_submission(
            {
                "ocr_mode": "external_ocr_failed",
                "parse_status": "failed",
                "provider_job_id": None,
                "file_ref": redacted_file_ref(source_ref),
                "credential_loaded": bool(status.get("credential_loaded")),
                "provider_call_allowed": bool(status.get("provider_call_allowed")),
                "external_ocr_completed": False,
                "real_material_training_allowed": False,
                "training_status": "blocked_for_external_ocr",
                "redacted_error_summary": "Controlled file reference not found.",
            },
            material_id=material_id or "controlled_file_ref",
            file_ref=redacted_file_ref(source_ref),
        )
    response = submit_paddle_ocr_job(
        ExternalOCRRequest(
            material_id=material_id or "controlled_file_ref",
            file_path_or_url=source_ref,
            use_doc_orientation_classify=bool(payload.get("use_doc_orientation_classify")),
            use_doc_unwarping=bool(payload.get("use_doc_unwarping")),
            use_chart_recognition=bool(payload.get("use_chart_recognition")),
        )
    )
    return record_external_ocr_job_submission(response, material_id=material_id or "controlled_file_ref", file_ref=source_ref)


@router.get("/external-ocr/jobs/{job_id}/status")
def external_ocr_job_status(job_id: str) -> dict[str, Any]:
    return _ensure(get_external_ocr_job_status(job_id))


@router.post("/external-ocr/jobs/{job_id}/poll")
async def external_ocr_job_poll(job_id: str, request: Request) -> dict[str, Any]:
    return _ensure(poll_external_ocr_job(job_id, await _safe_request_payload(request)))


@router.post("/external-ocr/jobs/{job_id}/fetch-result")
async def external_ocr_job_fetch_result(job_id: str, request: Request) -> dict[str, Any]:
    return _ensure(fetch_external_ocr_result(job_id, await _safe_request_payload(request)))


@router.post("/external-ocr/jobs/{job_id}/build-redacted-summary")
async def external_ocr_job_build_redacted_summary(job_id: str, request: Request) -> dict[str, Any]:
    return _ensure(build_external_ocr_redacted_summary(job_id, await _safe_request_payload(request)))


@router.post("/external-ocr/jobs/{job_id}/parse-quality-gate")
def external_ocr_job_parse_quality_gate(job_id: str) -> dict[str, Any]:
    return _ensure(run_external_ocr_parse_quality_gate(job_id))


@router.get("/external-ocr/jobs/{job_id}/audit")
def external_ocr_job_audit(job_id: str) -> dict[str, Any]:
    return _ensure(get_external_ocr_job_audit(job_id))


@router.get("/external-ocr/jobs/{job_id}/source-trace")
def external_ocr_job_source_trace(job_id: str) -> dict[str, Any]:
    return _ensure(get_external_ocr_job_source_trace(job_id))


@router.get("/external-ocr/jobs/{job_id}/provider-status-diagnostics")
def external_ocr_job_provider_status_diagnostics(job_id: str) -> dict[str, Any]:
    return _ensure(get_external_ocr_provider_status_diagnostics(job_id))


@router.get("/training-materials/external-ocr/runs")
def training_material_external_ocr_runs() -> dict[str, Any]:
    return list_external_ocr_runs()


@router.get("/training-materials/external-ocr/runs/{external_ocr_run_id}")
def training_material_external_ocr_run_detail(external_ocr_run_id: str) -> dict[str, Any]:
    return _ensure(get_external_ocr_run(external_ocr_run_id))


@router.post("/training-datasets/build")
async def training_datasets_build_alias(request: Request) -> dict[str, Any]:
    payload = await _safe_request_payload(request)
    action = TrainingDatasetBuildRequest(**payload)
    return build_training_dataset(action)


@router.get("/training-datasets")
def training_datasets_alias() -> dict[str, Any]:
    from personal_skill_studio.training_artifacts.training_dataset_builder import list_training_dataset_manifests

    return list_training_dataset_manifests()


@router.get("/training-datasets/{training_dataset_id}")
def training_dataset_detail_alias(training_dataset_id: str) -> dict[str, Any]:
    from personal_skill_studio.training_artifacts.training_dataset_builder import list_training_dataset_manifests

    manifests = list_training_dataset_manifests().get("manifests", [])
    return _ensure(next((item for item in manifests if item.get("dataset_id") == training_dataset_id), None))


@router.get("/training-datasets/{training_dataset_id}/examples")
def training_dataset_examples_alias(training_dataset_id: str) -> dict[str, Any]:
    return list_training_dataset_examples()


@router.get("/training-datasets/{training_dataset_id}/task-plan")
def training_dataset_task_plan_alias(training_dataset_id: str) -> dict[str, Any]:
    dataset = training_dataset_detail_alias(training_dataset_id)
    return _ensure(dataset.get("task_plan"))


@router.post("/training-datasets/{training_dataset_id}/gate/run")
def training_dataset_gate_run_alias(training_dataset_id: str) -> dict[str, Any]:
    return get_training_gate_report()


@router.get("/training-datasets/{training_dataset_id}/gate-report")
def training_dataset_gate_report_alias(training_dataset_id: str) -> dict[str, Any]:
    return get_training_gate_report()


@router.get("/training-datasets/{training_dataset_id}/audit")
def training_dataset_audit_alias(training_dataset_id: str) -> dict[str, Any]:
    return {"dataset_id": training_dataset_id, "audit_id": f"{training_dataset_id}_audit", "events": [{"event": "dataset_metadata_built", "status": "metadata_only"}], "event_count": 1}


@router.get("/training-datasets/{training_dataset_id}/source-trace")
def training_dataset_source_trace_alias(training_dataset_id: str) -> dict[str, Any]:
    return {"dataset_id": training_dataset_id, "source_trace_id": f"{training_dataset_id}_source_trace", "trace_status": "complete_metadata_only"}


@router.get("/v7-36/status")
def v736_dataset_status_alias() -> dict[str, Any]:
    return get_training_dataset_status()


@router.get("/codex-training-skills/interface-doc")
def codex_training_skill_interface_doc() -> dict[str, Any]:
    return get_training_skill_interface_doc()


@router.get("/codex-training-skills/provider-adapters")
def codex_training_skill_provider_adapters() -> dict[str, Any]:
    return list_provider_adapters()


@router.get("/codex-training-skills/provider-adapters/{provider_type}")
def codex_training_skill_provider_adapter_status(provider_type: str) -> dict[str, Any]:
    return _ensure(provider_adapter_status(provider_type))


@router.post("/codex-training-skills/generate")
async def codex_training_skills_generate(request: Request) -> dict[str, Any]:
    return generate_training_skill(await _safe_request_payload(request))


@router.get("/codex-training-skills")
def codex_training_skills() -> dict[str, Any]:
    return list_training_skills()


@router.get("/codex-training-skills/{training_skill_id}")
def codex_training_skill_detail(training_skill_id: str) -> dict[str, Any]:
    return _ensure(get_training_skill(training_skill_id))


@router.post("/codex-training-skills/{training_skill_id}/gate/run")
def codex_training_skill_gate_run(training_skill_id: str) -> dict[str, Any]:
    return _ensure(run_training_skill_gate(training_skill_id))


@router.get("/codex-training-skills/{training_skill_id}/gate-report")
def codex_training_skill_gate_report(training_skill_id: str) -> dict[str, Any]:
    return _ensure(get_training_skill_gate_report(training_skill_id))


@router.get("/codex-training-skills/{training_skill_id}/audit")
def codex_training_skill_audit(training_skill_id: str) -> dict[str, Any]:
    return _ensure(get_training_skill_audit(training_skill_id))


@router.get("/codex-training-skills/{training_skill_id}/source-trace")
def codex_training_skill_source_trace(training_skill_id: str) -> dict[str, Any]:
    return _ensure(get_training_skill_source_trace(training_skill_id))


@router.post("/codex-training-skills/{training_skill_id}/provider-call/mock")
async def codex_training_skill_provider_call_mock(training_skill_id: str, request: Request) -> dict[str, Any]:
    _ensure(get_training_skill(training_skill_id))
    payload = await _safe_request_payload(request)
    provider_type = str(payload.get("provider_type") or "OCR_API")
    method_name = payload.get("method_name")
    return _ensure(call_provider_placeholder(provider_type, str(method_name) if method_name else None))


@router.get("/v7-37/status")
def v737_training_skill_status_alias() -> dict[str, Any]:
    return build_v737_training_skill_status()


@router.post("/codex-skill-training-runs/start")
async def codex_skill_training_runs_start(request: Request) -> dict[str, Any]:
    return start_skill_training_run(await _safe_request_payload(request))


@router.get("/codex-skill-training-runs")
def codex_skill_training_runs() -> dict[str, Any]:
    return list_skill_training_runs()


@router.get("/codex-skill-training-runs/{training_run_id}")
def codex_skill_training_run_detail(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_run(training_run_id))


@router.get("/codex-skill-training-runs/{training_run_id}/logs")
def codex_skill_training_run_logs(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_logs(training_run_id))


@router.get("/codex-skill-training-runs/{training_run_id}/metrics")
def codex_skill_training_run_metrics(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_metrics(training_run_id))


@router.get("/codex-skill-training-runs/{training_run_id}/gate-report")
def codex_skill_training_run_gate_report(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_gate_report(training_run_id))


@router.get("/codex-skill-training-runs/{training_run_id}/artifact")
def codex_skill_training_run_artifact(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_artifact(training_run_id))


@router.get("/codex-skill-training-runs/{training_run_id}/audit")
def codex_skill_training_run_audit(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_audit(training_run_id))


@router.get("/codex-skill-training-runs/{training_run_id}/source-trace")
def codex_skill_training_run_source_trace(training_run_id: str) -> dict[str, Any]:
    return _ensure(get_skill_training_source_trace(training_run_id))


@router.get("/v7-38/status")
def v738_status() -> dict[str, Any]:
    return build_v738_status()


async def _safe_request_payload(request: Request) -> dict[str, Any]:
    try:
        payload = await request.json()
    except Exception:
        return {}
    return payload if isinstance(payload, dict) else {}


@router.get("/training-runs")
def training_runs() -> dict[str, Any]:
    return list_training_runs()


@router.post("/training-runs/mock")
def training_runs_mock(request: CodexTrainingRunRequest) -> dict[str, Any]:
    return create_training_run(request)


@router.get("/training-runs/{run_id}")
def training_run_detail(run_id: str) -> dict[str, Any]:
    return _ensure(get_training_run(run_id)).model_dump()


@router.get("/training-runs/{run_id}/summary")
def training_run_summary(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return {
        "training_run_id": run_id,
        "summary": {
            "source_case_mode": record.manifest.source_case_mode,
            "source_case_count": record.manifest.source_case_count,
            "synthetic_case_count": record.manifest.synthetic_case_count,
            "package_count": len(record.experience_packages),
            "skill_count": len(record.generated_skills),
            "test_case_count": len(record.test_cases),
            "loading_manifest_id": record.loading_manifest.loading_manifest_id,
        },
        **record.model_dump(exclude={"training_samples", "experience_packages", "generated_skills", "evaluations", "gates", "test_cases", "loading_manifest", "manifest"}) ,
    }


@router.get("/training-runs/{run_id}/case-cause-packages")
def training_run_case_cause_packages(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return ArtifactListResponse(
        artifacts=[package.model_dump() for package in record.experience_packages],
        artifact_count=len(record.experience_packages),
        warnings=["Generated packages are synthetic closed-case metadata."],
    ).model_dump() | {"codex_training": True, "training_run_generated": True}


@router.get("/training-runs/{run_id}/generated-skills")
def training_run_generated_skills(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return ArtifactListResponse(
        artifacts=[skill.model_dump() for skill in record.generated_skills],
        artifact_count=len(record.generated_skills),
        warnings=["Generated skills are metadata-only and not published."],
    ).model_dump() | {"codex_training": True, "training_run_generated": True}


@router.get("/training-runs/{run_id}/evaluations")
def training_run_evaluations(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return ArtifactListResponse(
        artifacts=[evaluation.model_dump() for evaluation in record.evaluations],
        artifact_count=len(record.evaluations),
        warnings=["Evaluation manifests are reference-only."],
    ).model_dump() | {"codex_training": True, "training_run_generated": True}


@router.get("/training-runs/{run_id}/gates")
def training_run_gates(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return ArtifactListResponse(
        artifacts=[gate.model_dump() for gate in record.gates],
        artifact_count=len(record.gates),
        warnings=["Gate manifests are reference-only and do not block next stage."],
    ).model_dump() | {"codex_training": True, "training_run_generated": True}


@router.get("/training-runs/{run_id}/test-cases")
def training_run_test_cases(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return ArtifactListResponse(
        artifacts=[test_case.model_dump() for test_case in record.test_cases],
        artifact_count=len(record.test_cases),
        warnings=["Test cases use metadata schemas only."],
    ).model_dump() | {"codex_training": True, "training_run_generated": True}


@router.get("/training-runs/{run_id}/loading-manifest")
def training_run_loading_manifest(run_id: str) -> dict[str, Any]:
    record = _ensure(get_training_run(run_id))
    return record.loading_manifest.model_dump()


@router.post("/training-runs/{run_id}/load-dry-run/mock")
def training_run_load_dry_run(run_id: str) -> dict[str, Any]:
    return _ensure(create_training_run_load_dry_run(run_id))


@router.get("/training-runs/{run_id}/audit")
def training_run_audit(run_id: str) -> dict[str, Any]:
    return _ensure(build_training_run_audit(run_id))


@router.get("/training-runs/{run_id}/safety")
def training_run_safety(run_id: str) -> dict[str, Any]:
    return _ensure(build_training_run_safety(run_id))
