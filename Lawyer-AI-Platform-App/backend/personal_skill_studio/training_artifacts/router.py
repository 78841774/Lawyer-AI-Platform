from typing import Any

from fastapi import APIRouter, HTTPException

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
from personal_skill_studio.training_artifacts.codex_skill_draft_registry import (
    create_draft,
    get_draft,
    get_draft_audit,
    list_drafts,
    review_draft,
)
from personal_skill_studio.training_artifacts.experience_candidate_registry import (
    build_candidates,
    get_candidate,
    get_candidate_audit,
    list_candidates,
    redact_experience_candidate,
    review_experience_candidate,
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
    CodexSkillDraftBuildRequest,
    CodexSkillDraftReviewRequest,
    CodexTrainingRunRequest,
    ExperienceCandidateBuildRequest,
    ExperienceCandidateReviewRequest,
    LegalRetrievalJobRequest,
    LoadDryRunRequest,
    OcrJobRequest,
    RealClosedCaseTrainingIntakeRequest,
    SkillExperienceBindingRequest,
    SkillExperienceImportRequest,
    TrainingArtifactStatus,
    TrainingIntakeReviewActionRequest,
)
from personal_skill_studio.training_artifacts.skill_experience_binding_engine import create_binding, get_binding, list_bindings
from personal_skill_studio.training_artifacts.skill_experience_pool import (
    get_pool_entry,
    import_approved_experience,
    list_pool_entries,
    pool_status,
)
from personal_skill_studio.training_artifacts.skill_experience_safety_engine import build_v731c_status
from personal_skill_studio.training_artifacts.training_run_engine import (
    build_training_run_audit,
    build_training_run_safety,
    create_training_run,
    create_training_run_load_dry_run,
    get_training_run,
    list_training_runs,
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
