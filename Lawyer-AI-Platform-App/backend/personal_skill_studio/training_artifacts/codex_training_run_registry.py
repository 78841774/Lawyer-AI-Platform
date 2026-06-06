from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.codex_training_dryrun_registry import (
    run_codex_training_dryrun,
)
from personal_skill_studio.training_artifacts.schemas import (
    CodexInternalTrainingGateReport,
    CodexInternalTrainingLogEntry,
    CodexInternalTrainingLogList,
    CodexInternalTrainingMetrics,
    CodexInternalTrainingRun,
    CodexTrainingDryRun,
    CodexTrainingDryRunRequest,
    CodexTrainingRunStartRequest,
    TrainingDatasetBuildRequest,
    TrainingDatasetManifest,
    TrainingGateReport,
    V737CodexInternalTrainingStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    CODEX_INTERNAL_TRAINING_RUNS_DIR,
    read_payloads,
    write_payload,
)
from personal_skill_studio.training_artifacts.training_dataset_builder import (
    build_training_dataset,
    latest_training_dataset_manifest,
    latest_training_gate_report,
)
from personal_skill_studio.training_artifacts.training_dataset_safety_engine import training_dataset_metadata_safe
from personal_skill_studio.training_artifacts.codex_training_run_safety_engine import (
    codex_training_run_metadata_safe,
    v737_safety_flags,
)


def start_codex_internal_training_run(request: CodexTrainingRunStartRequest | None = None) -> dict:
    request = request or CodexTrainingRunStartRequest()
    manifest = latest_training_dataset_manifest()
    if manifest is None:
        build_training_dataset(TrainingDatasetBuildRequest())
        manifest = latest_training_dataset_manifest()
    gate_report = latest_training_gate_report()
    dryrun = _latest_dryrun()
    if dryrun is None or (manifest and dryrun.dataset_id != manifest.dataset_id):
        run_codex_training_dryrun(CodexTrainingDryRunRequest())
        dryrun = _latest_dryrun()

    run = _build_training_run(request, manifest, gate_report, dryrun)
    if codex_training_run_metadata_safe(run.model_dump()):
        write_payload(CODEX_INTERNAL_TRAINING_RUNS_DIR, run.run_id, run.model_dump())
    return run.model_dump()


def get_codex_internal_training_status() -> dict:
    runs = _read_runs()
    latest = runs[0] if runs else None
    logs = [log for run in runs for log in run.logs]
    report = _build_gate_report(latest)
    return V737CodexInternalTrainingStatus(
        training_run_count=len(runs),
        latest_run_id=latest.run_id if latest else None,
        latest_run_status=latest.run_status if latest else "not_started",
        latest_gate_status=report.gate_status,
        latest_metrics_id=latest.metrics.metrics_id if latest else None,
        log_count=len(logs),
        warnings=[
            "v7.37 starts an internal training run metadata record only.",
            "It does not call providers, read key values, replace runtime packages, publish Skills, or export model files.",
        ],
        **v737_safety_flags(),
    ).model_dump()


def list_codex_internal_training_logs() -> dict:
    runs = _read_runs()
    latest = runs[0] if runs else None
    logs = latest.logs if latest else []
    return CodexInternalTrainingLogList(
        logs=logs,
        log_count=len(logs),
        latest_run_id=latest.run_id if latest else None,
        warnings=["Internal training logs are redacted metadata and comparable with dry-run logs."],
        **v737_safety_flags(),
    ).model_dump()


def get_codex_internal_training_gate_report() -> dict:
    latest = _read_runs()[0] if _read_runs() else None
    return _build_gate_report(latest).model_dump()


def _build_training_run(
    request: CodexTrainingRunStartRequest,
    manifest: TrainingDatasetManifest | None,
    gate_report: TrainingGateReport | None,
    dryrun: CodexTrainingDryRun | None,
) -> CodexInternalTrainingRun:
    now = datetime.now(UTC).isoformat()
    run_id = f"codex_internal_training_run_v737_{_stamp(now)}"
    failed = _request_failures(request)
    if manifest is None:
        failed.append("dataset_manifest_missing")
    elif not training_dataset_metadata_safe(manifest.model_dump()):
        failed.append("dataset_metadata_safety_failed")
    if gate_report is None or gate_report.gate_status != "passed_reference_only":
        failed.append("training_dataset_gate_not_passed")
    if dryrun is None or dryrun.run_status != "dryrun_completed_reference_only":
        failed.append("dryrun_not_completed")
    metrics = _build_metrics(run_id, manifest, dryrun, failed)
    logs = _build_logs(run_id, manifest, dryrun, failed, now)
    return CodexInternalTrainingRun(
        run_id=run_id,
        run_status="internal_training_completed_metadata_only" if not failed else "internal_training_blocked_metadata_only",
        execution_mode=request.execution_mode,
        dataset_id=manifest.dataset_id if manifest else None,
        dryrun_id=dryrun.run_id if dryrun else None,
        gate_report_id=gate_report.gate_report_id if gate_report else None,
        candidate_ids=manifest.source_candidate_ids if manifest else [],
        example_count=manifest.example_count if manifest else 0,
        metrics=metrics,
        logs=logs,
        audit_id=f"{run_id}_audit",
        source_trace_id=f"{run_id}_source_trace",
        created_at=now,
        warnings=[
            "Internal training run records metadata, metrics, and logs only.",
            "No external provider training, key read, runtime package replacement, Skill publication, final legal output, or delivery action is executed.",
        ],
        **v737_safety_flags(),
    )


def _build_metrics(
    run_id: str,
    manifest: TrainingDatasetManifest | None,
    dryrun: CodexTrainingDryRun | None,
    failed: list[str],
) -> CodexInternalTrainingMetrics:
    dryrun_step_count = len(dryrun.logs) if dryrun else 0
    training_step_count = 7
    alignment = 1.0 if dryrun_step_count else 0.0
    if failed:
        alignment = min(alignment, 0.5)
    return CodexInternalTrainingMetrics(
        metrics_id=f"{run_id}_metrics",
        run_id=run_id,
        dataset_id=manifest.dataset_id if manifest else None,
        dryrun_id=dryrun.run_id if dryrun else None,
        candidate_count=len(manifest.source_candidate_ids) if manifest else 0,
        example_count=manifest.example_count if manifest else 0,
        log_alignment_score=alignment,
        metadata_safety_score=1.0 if not failed else 0.5,
        gate_pass_rate=1.0 if not failed else 0.0,
        provider_call_count=0,
        key_read_count=0,
        runtime_package_mutation_count=0,
        skill_publish_count=0,
        internal_model_artifact_id=f"{run_id}_internal_model_metadata",
        internal_model_artifact_status="metadata_recorded_only",
        warnings=[
            f"Compared {dryrun_step_count} dry-run log steps with {training_step_count} internal training log steps.",
            "Internal model artifact is metadata only; no file path or model checkpoint is returned.",
        ],
        **v737_safety_flags(),
    )


def _build_logs(
    run_id: str,
    manifest: TrainingDatasetManifest | None,
    dryrun: CodexTrainingDryRun | None,
    failed: list[str],
    now: str,
) -> list[CodexInternalTrainingLogEntry]:
    dataset_id = manifest.dataset_id if manifest else None
    candidate_ids = manifest.source_candidate_ids if manifest else []
    dryrun_refs = [log.log_id for log in (dryrun.logs if dryrun else [])]
    steps = [
        ("load_v735_dataset_manifest", "loaded" if manifest else "blocked", "Loaded v7.35 dataset manifest metadata."),
        ("verify_v735_training_gate", "passed" if manifest and not failed else "blocked", "Checked dataset gate and safety metadata."),
        ("compare_v736_dryrun_logs", "passed" if dryrun_refs else "blocked", "Compared dry-run logs with internal training plan."),
        ("execute_internal_training_simulation", "completed" if not failed else "blocked", "Recorded internal training simulation metrics only."),
        ("record_internal_model_metadata", "completed" if not failed else "blocked", "Recorded internal model artifact metadata without path or checkpoint export."),
        ("record_audit_and_source_trace", "completed", "Recorded audit and source trace metadata."),
        ("confirm_no_provider_key_runtime_publish", "passed", "Confirmed no provider call, key read, runtime package replacement, or Skill publish."),
    ]
    if failed:
        steps.append(("internal_training_completion", "blocked", f"Internal training run blocked by {', '.join(failed)}."))
    else:
        steps.append(("internal_training_completion", "completed", "Internal training run completed as owner-only metadata simulation."))
    return [
        CodexInternalTrainingLogEntry(
            log_id=f"{run_id}_{index:02d}_{name}",
            run_id=run_id,
            step_name=name,
            step_status=status,
            message=message,
            dryrun_log_ref=dryrun_refs[index - 1] if index - 1 < len(dryrun_refs) else None,
            dataset_id=dataset_id,
            candidate_ids=candidate_ids,
            created_at=now,
            warnings=["Training log entry is safe metadata and contains no raw source material."],
            **v737_safety_flags(),
        )
        for index, (name, status, message) in enumerate(steps, start=1)
    ]


def _build_gate_report(run: CodexInternalTrainingRun | None) -> CodexInternalTrainingGateReport:
    now = datetime.now(UTC).isoformat()
    failed: list[str] = []
    if run is None:
        failed.append("training_run_missing")
    elif run.run_status != "internal_training_completed_metadata_only":
        failed.append("training_run_not_completed")
    status = "passed_reference_only" if not failed else "blocked_reference_only"
    report_id = f"codex_internal_training_gate_report_v737_{_stamp(now)}"
    metrics = run.metrics if run else None
    return CodexInternalTrainingGateReport(
        gate_report_id=report_id,
        run_id=run.run_id if run else None,
        gate_status=status,
        passed_checks=[
            "dataset_gate_passed",
            "dryrun_log_compared",
            "training_metrics_generated",
            "provider_boundary_safe",
            "key_boundary_safe",
            "runtime_package_boundary_safe",
            "skill_publish_boundary_safe",
            "audit_source_trace_safe",
        ]
        if not failed
        else ["provider_boundary_safe", "key_boundary_safe", "runtime_package_boundary_safe", "skill_publish_boundary_safe"],
        failed_checks=failed,
        metrics_summary={
            "candidate_count": metrics.candidate_count if metrics else 0,
            "example_count": metrics.example_count if metrics else 0,
            "log_alignment_score": metrics.log_alignment_score if metrics else 0.0,
            "metadata_safety_score": metrics.metadata_safety_score if metrics else 0.0,
            "gate_pass_rate": metrics.gate_pass_rate if metrics else 0.0,
        },
        gate_summary=(
            "Internal training run gate passed with metrics/log/audit/source trace metadata only."
            if not failed
            else "Internal training run gate is blocked until a completed metadata-only training run exists."
        ),
        dryrun_log_comparison_status="compared" if run and run.metrics.log_alignment_score > 0 else "missing",
        provider_boundary_safe=True,
        key_boundary_safe=True,
        runtime_package_boundary_safe=True,
        publication_boundary_safe=True,
        audit_source_trace_safe=True,
        created_at=now,
        audit_id=f"{report_id}_audit",
        source_trace_id=f"{report_id}_source_trace",
        warnings=["Gate report is reference-only and does not publish or load any artifact."],
        **v737_safety_flags(),
    )


def _latest_dryrun() -> CodexTrainingDryRun | None:
    from personal_skill_studio.training_artifacts.storage import CODEX_TRAINING_DRYRUNS_DIR

    runs = [
        CodexTrainingDryRun(**payload)
        for payload in read_payloads(CODEX_TRAINING_DRYRUNS_DIR)
        if payload.get("run_id")
    ]
    runs = sorted(runs, key=lambda item: item.created_at, reverse=True)
    return runs[0] if runs else None


def _read_runs() -> list[CodexInternalTrainingRun]:
    runs = [
        CodexInternalTrainingRun(**payload)
        for payload in read_payloads(CODEX_INTERNAL_TRAINING_RUNS_DIR)
        if payload.get("run_id")
    ]
    return sorted(runs, key=lambda item: item.created_at, reverse=True)


def _request_failures(request: CodexTrainingRunStartRequest) -> list[str]:
    failed: list[str] = []
    if not request.explicit_internal_training_confirmation:
        failed.append("internal_training_confirmation_missing")
    if not request.explicit_no_provider_confirmation:
        failed.append("no_provider_confirmation_missing")
    if not request.explicit_no_key_read_confirmation:
        failed.append("no_key_read_confirmation_missing")
    if not request.explicit_no_runtime_package_replace_confirmation:
        failed.append("no_runtime_package_replace_confirmation_missing")
    if not request.explicit_no_skill_publish_confirmation:
        failed.append("no_skill_publish_confirmation_missing")
    if not request.explicit_no_external_delivery_confirmation:
        failed.append("no_external_delivery_confirmation_missing")
    if request.execution_mode not in {"internal_simulation", "local_cpu", "local_gpu"}:
        failed.append("unsupported_execution_mode")
    return failed


def _stamp(value: str) -> str:
    return value.replace("+00:00", "Z").replace(":", "").replace("-", "").replace(".", "")
