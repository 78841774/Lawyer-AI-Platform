from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.artifact_registry import get_package, get_skill
from personal_skill_studio.training_artifacts.case_analysis_improvement_audit_engine import build_candidate_audit
from personal_skill_studio.training_artifacts.case_analysis_improvement_candidate_registry import (
    build_case_analysis_improvement_candidates,
    list_case_analysis_improvement_candidates,
)
from personal_skill_studio.training_artifacts.case_analysis_improvement_source_trace_engine import build_candidate_source_trace
from personal_skill_studio.training_artifacts.case_analysis_output_to_experience_trace import (
    get_output_to_experience_trace_by_output,
)
from personal_skill_studio.training_artifacts.case_analysis_workbench_runtime import get_workbench_schema
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisImprovementCandidate,
    TrainingDatasetBuildRequest,
    TrainingDatasetExample,
    TrainingDatasetExampleList,
    TrainingDatasetManifest,
    TrainingDatasetManifestList,
    TrainingGateReport,
    TrainingTaskPlan,
    V735TrainingDatasetStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    TRAINING_DATASETS_DIR,
    TRAINING_GATE_REPORTS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)
from personal_skill_studio.training_artifacts.training_dataset_safety_engine import (
    training_dataset_metadata_safe,
    v735_safety_flags,
)


def build_training_dataset(request: TrainingDatasetBuildRequest | None = None) -> dict:
    request = request or TrainingDatasetBuildRequest()
    candidates = _ready_candidates()
    if not _request_confirmed(request):
        manifest = _build_manifest([], "blocked_confirmation_missing")
        write_payload(TRAINING_DATASETS_DIR, manifest.dataset_id, manifest.model_dump())
        report = build_training_gate_report_for_manifest(manifest)
        write_payload(TRAINING_GATE_REPORTS_DIR, report.gate_report_id, report.model_dump())
        return manifest.model_dump()

    manifest = _build_manifest(candidates, "dataset_manifest_ready" if candidates else "blocked_no_ready_candidates")
    if training_dataset_metadata_safe(manifest.model_dump()):
        write_payload(TRAINING_DATASETS_DIR, manifest.dataset_id, manifest.model_dump())
        report = build_training_gate_report_for_manifest(manifest)
        write_payload(TRAINING_GATE_REPORTS_DIR, report.gate_report_id, report.model_dump())
    return manifest.model_dump()


def get_training_dataset_status() -> dict:
    manifests = _read_manifests()
    reports = _read_gate_reports()
    latest_manifest = _latest_manifest(manifests)
    latest_report = _latest_gate_report(reports)
    return V735TrainingDatasetStatus(
        ready_candidate_count=len(_ready_candidates(ensure_seed=False)),
        dataset_manifest_count=len(manifests),
        latest_dataset_id=latest_manifest.dataset_id if latest_manifest else None,
        latest_gate_status=latest_report.gate_status if latest_report else "not_built",
        example_count=latest_manifest.example_count if latest_manifest else 0,
        warnings=[
            "v7.35 builds training dataset metadata only from ready v7.34 improvement candidates.",
            "Training gate is reference-only and does not execute training or publish Skills.",
        ],
        **v735_safety_flags(),
    ).model_dump()


def list_training_dataset_manifests() -> dict:
    manifests = _read_manifests()
    latest = _latest_manifest(manifests)
    return TrainingDatasetManifestList(
        manifests=manifests,
        manifest_count=len(manifests),
        latest_dataset_id=latest.dataset_id if latest else None,
        warnings=["Dataset manifests are metadata-only and do not write formal training sets."],
        **v735_safety_flags(),
    ).model_dump()


def list_training_dataset_examples() -> dict:
    latest = _latest_manifest(_read_manifests())
    examples = latest.examples if latest else []
    return TrainingDatasetExampleList(
        dataset_id=latest.dataset_id if latest else None,
        examples=examples,
        example_count=len(examples),
        warnings=["Training examples are abstracted metadata pairs and are not provider prompts."],
        **v735_safety_flags(),
    ).model_dump()


def get_training_gate_report() -> dict:
    latest = _latest_gate_report(_read_gate_reports())
    if latest:
        return latest.model_dump()
    manifest = _latest_manifest(_read_manifests())
    if manifest:
        report = build_training_gate_report_for_manifest(manifest)
        write_payload(TRAINING_GATE_REPORTS_DIR, report.gate_report_id, report.model_dump())
        return report.model_dump()
    report = _build_gate_report(None, [], ["dataset_manifest_missing"])
    write_payload(TRAINING_GATE_REPORTS_DIR, report.gate_report_id, report.model_dump())
    return report.model_dump()


def build_training_gate_report_for_manifest(manifest: TrainingDatasetManifest) -> TrainingGateReport:
    failed: list[str] = []
    if manifest.candidate_count == 0:
        failed.append("ready_candidate_missing")
    if manifest.example_count == 0:
        failed.append("training_example_missing")
    if not manifest.source_trace_ids:
        failed.append("source_trace_missing")
    if not manifest.source_audit_ids:
        failed.append("audit_missing")
    if not training_dataset_metadata_safe(manifest.model_dump()):
        failed.append("sensitive_metadata_scan_failed")
    return _build_gate_report(manifest, failed)


def latest_training_dataset_manifest() -> TrainingDatasetManifest | None:
    return _latest_manifest(_read_manifests())


def latest_training_gate_report() -> TrainingGateReport | None:
    return _latest_gate_report(_read_gate_reports())


def _build_manifest(candidates: list[CaseAnalysisImprovementCandidate], status: str) -> TrainingDatasetManifest:
    now = datetime.now(UTC).isoformat()
    dataset_id = f"training_dataset_v735_{_stamp(now)}"
    examples = [_build_example(candidate, index, now) for index, candidate in enumerate(candidates, start=1)]
    source_skill_ids = sorted({_skill_id_for(candidate) for candidate in candidates})
    source_package_ids = sorted({candidate.source_package_id for candidate in candidates})
    task_plan = TrainingTaskPlan(
        task_plan_id=f"{dataset_id}_task_plan",
        dataset_id=dataset_id,
        target_skill_ids=source_skill_ids,
        source_package_ids=source_package_ids,
        source_candidate_ids=[candidate.candidate_id for candidate in candidates],
        example_count=len(examples),
        planned_steps=[
            "review_ready_improvement_candidates",
            "load_experience_package_metadata",
            "load_skill_output_schema_metadata",
            "load_output_to_experience_trace_metadata",
            "run_reference_training_gate",
            "keep_for_v7_36_internal_dry_run_only",
        ],
        blocked_actions=[
            "provider_call",
            "key_value_read",
            "real_training",
            "formal_training_set_write",
            "runtime_package_replace",
            "skill_publish",
            "external_delivery",
        ],
        created_at=now,
        warnings=["Task plan is metadata-only and does not execute training."],
        **v735_safety_flags(),
    )
    return TrainingDatasetManifest(
        dataset_id=dataset_id,
        dataset_status=status,
        source_candidate_ids=[candidate.candidate_id for candidate in candidates],
        source_package_ids=source_package_ids,
        source_skill_ids=source_skill_ids,
        source_output_ids=[candidate.source_output_id for candidate in candidates],
        source_trace_ids=sorted({trace_id for candidate in candidates for trace_id in candidate.source_trace_ids + [candidate.source_trace_id] if trace_id}),
        source_audit_ids=sorted({audit_id for candidate in candidates for audit_id in candidate.source_audit_ids + [candidate.audit_id] if audit_id}),
        candidate_count=len(candidates),
        example_count=len(examples),
        examples=examples,
        task_plan=task_plan,
        audit_id=f"{dataset_id}_audit",
        source_trace_id=f"{dataset_id}_source_trace",
        created_at=now,
        updated_at=now,
        warnings=[
            "Dataset manifest is built from redacted and abstracted candidate metadata only.",
            "No provider call, key read, real training, Skill publish, package mutation, or delivery action is executed.",
        ],
        **v735_safety_flags(),
    )


def _build_example(candidate: CaseAnalysisImprovementCandidate, index: int, now: str) -> TrainingDatasetExample:
    trace = get_output_to_experience_trace_by_output(candidate.source_output_id)
    schema = get_workbench_schema(candidate.source_case_analysis_view_id) or {}
    skill_id = _skill_id_for(candidate)
    skill = get_skill(skill_id)
    package = get_package(candidate.source_package_id)
    package_version = getattr(package, "package_version", None) or candidate.source_package_version
    return TrainingDatasetExample(
        example_id=f"{candidate.candidate_id}_example_v735_{index}",
        candidate_id=candidate.candidate_id,
        source_output_id=candidate.source_output_id,
        source_output_group=candidate.source_output_group,
        source_output_type=candidate.source_output_type,
        source_package_id=candidate.source_package_id,
        source_package_version=package_version,
        source_experience_card_ids=candidate.source_experience_card_ids,
        source_feedback_ids=candidate.source_feedback_ids,
        source_risk_event_ids=candidate.source_risk_event_ids,
        source_audit_ids=candidate.source_audit_ids + [candidate.audit_id],
        source_trace_ids=candidate.source_trace_ids + [candidate.source_trace_id],
        output_trace_id=trace.trace_id if trace else None,
        output_trace_status=trace.trace_status if trace else "missing",
        skill_schema_id=f"{skill_id}_output_schema_v735",
        skill_schema_version=str(schema.get("schema_version") or "v7.35"),
        training_input_summary=(
            f"{candidate.source_output_group}/{candidate.source_output_type} feedback metadata with "
            f"{len(candidate.source_feedback_ids)} feedback refs and {len(candidate.source_risk_event_ids)} risk refs."
        ),
        training_target_summary=(
            f"{candidate.proposed_change_type} for {candidate.target_object_type}; "
            "abstracted experience update candidate only."
        ),
        training_task_type=getattr(skill, "skill_type", None) or _task_type_for(candidate),
        gate_input_status="ready_for_reference_gate",
        metadata_safety_status="passed",
        created_at=now,
        warnings=["Example contains no source content and is not sent to a provider."],
        **v735_safety_flags(),
    )


def _build_gate_report(
    manifest: TrainingDatasetManifest | None,
    failed: list[str],
    extra_failed: list[str] | None = None,
) -> TrainingGateReport:
    now = datetime.now(UTC).isoformat()
    failed_checks = list(failed) + list(extra_failed or [])
    passed_checks = [
        "ready_candidate_only",
        "candidate_audit_checked",
        "source_trace_checked",
        "provider_boundary_safe",
        "key_boundary_safe",
        "package_mutation_boundary_safe",
        "training_boundary_safe",
        "skill_publish_boundary_safe",
        "external_delivery_boundary_safe",
    ]
    if failed_checks:
        passed_checks = [check for check in passed_checks if check not in {"ready_candidate_only", "source_trace_checked"}]
    gate_status = "passed_reference_only" if not failed_checks else "blocked_reference_only"
    gate_report_id = f"training_gate_report_v735_{_stamp(now)}"
    return TrainingGateReport(
        gate_report_id=gate_report_id,
        dataset_id=manifest.dataset_id if manifest else None,
        gate_status=gate_status,
        candidate_count=manifest.candidate_count if manifest else 0,
        example_count=manifest.example_count if manifest else 0,
        passed_checks=passed_checks,
        failed_checks=failed_checks,
        gate_summary=(
            "Training gate reference passed for metadata-only dry run input."
            if not failed_checks
            else "Training gate reference is blocked until ready candidate metadata, audit, and source trace are complete."
        ),
        candidate_metadata_safe=not failed_checks,
        audit_source_trace_safe=not any(check in failed_checks for check in {"source_trace_missing", "audit_missing"}),
        provider_boundary_safe=True,
        package_mutation_safe=True,
        training_boundary_safe=True,
        recommended_next_action="Proceed to v7.36 internal dry run only." if not failed_checks else "Review v7.34 candidate readiness metadata.",
        created_at=now,
        audit_id=f"{gate_report_id}_audit",
        source_trace_id=f"{gate_report_id}_source_trace",
        warnings=["Gate is reference-only and does not block by side effect or trigger training."],
        **v735_safety_flags(),
    )


def _ready_candidates(ensure_seed: bool = True) -> list[CaseAnalysisImprovementCandidate]:
    payload = list_case_analysis_improvement_candidates()
    candidates = payload.get("candidates", [])
    if ensure_seed and not candidates:
        payload = build_case_analysis_improvement_candidates()
        candidates = payload.get("candidates", [])
    return [
        CaseAnalysisImprovementCandidate(**candidate)
        for candidate in candidates
        if candidate.get("readiness_status") == "ready_for_training_dataset_build"
        and candidate.get("candidate_status") != "archived"
    ]


def _read_manifests() -> list[TrainingDatasetManifest]:
    manifests = [
        TrainingDatasetManifest(**payload)
        for payload in read_payloads(TRAINING_DATASETS_DIR)
        if payload.get("dataset_id")
    ]
    return sorted(manifests, key=lambda item: item.created_at, reverse=True)


def _read_gate_reports() -> list[TrainingGateReport]:
    reports = [
        TrainingGateReport(**payload)
        for payload in read_payloads(TRAINING_GATE_REPORTS_DIR)
        if payload.get("gate_report_id")
    ]
    return sorted(reports, key=lambda item: item.created_at, reverse=True)


def _latest_manifest(manifests: list[TrainingDatasetManifest]) -> TrainingDatasetManifest | None:
    return manifests[0] if manifests else None


def _latest_gate_report(reports: list[TrainingGateReport]) -> TrainingGateReport | None:
    return reports[0] if reports else None


def _request_confirmed(request: TrainingDatasetBuildRequest) -> bool:
    return (
        request.explicit_metadata_only_confirmation
        and request.explicit_ready_candidate_only_confirmation
        and request.explicit_no_training_confirmation
        and request.explicit_no_package_mutation_confirmation
        and request.explicit_no_skill_publish_confirmation
    )


def _skill_id_for(candidate: CaseAnalysisImprovementCandidate) -> str:
    if candidate.source_output_group == "fact_extraction":
        return "case_fact_extraction_skill"
    return "case_legal_analysis_skill"


def _task_type_for(candidate: CaseAnalysisImprovementCandidate) -> str:
    return "fact_extraction" if candidate.source_output_group == "fact_extraction" else "legal_analysis"


def _stamp(value: str) -> str:
    return value.replace("+00:00", "Z").replace(":", "").replace("-", "").replace(".", "")
