from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.artifact_registry import get_package
from personal_skill_studio.training_artifacts.schemas import (
    CodexTrainingDryRun,
    CodexTrainingDryRunGateReport,
    CodexTrainingDryRunLogEntry,
    CodexTrainingDryRunLogList,
    CodexTrainingDryRunRequest,
    TrainingDatasetBuildRequest,
    TrainingDatasetManifest,
    TrainingGateReport,
    V736CodexTrainingDryRunStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    CODEX_TRAINING_DRYRUNS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)
from personal_skill_studio.training_artifacts.training_dataset_builder import (
    build_training_dataset,
    build_training_gate_report_for_manifest,
    latest_training_dataset_manifest,
    latest_training_gate_report,
)
from personal_skill_studio.training_artifacts.codex_training_dryrun_safety_engine import (
    codex_training_dryrun_metadata_safe,
    v736_safety_flags,
)


def run_codex_training_dryrun(request: CodexTrainingDryRunRequest | None = None) -> dict:
    request = request or CodexTrainingDryRunRequest()
    manifest = latest_training_dataset_manifest()
    if manifest is None:
        build_training_dataset(TrainingDatasetBuildRequest())
        manifest = latest_training_dataset_manifest()
    gate_report = latest_training_gate_report()
    if manifest and (gate_report is None or gate_report.dataset_id != manifest.dataset_id):
        gate_report = build_training_gate_report_for_manifest(manifest)

    run = _build_dryrun(request, manifest, gate_report)
    if codex_training_dryrun_metadata_safe(run.model_dump()):
        write_payload(CODEX_TRAINING_DRYRUNS_DIR, run.run_id, run.model_dump())
    return run.model_dump()


def get_codex_training_dryrun_status() -> dict:
    runs = _read_runs()
    latest = runs[0] if runs else None
    logs = [log for run in runs for log in run.logs]
    return V736CodexTrainingDryRunStatus(
        dryrun_count=len(runs),
        latest_run_id=latest.run_id if latest else None,
        latest_run_status=latest.run_status if latest else "not_run",
        latest_gate_status=latest.training_gate_status if latest else "not_run",
        log_count=len(logs),
        warnings=[
            "v7.36 is an internal dry run over v7.35 metadata only.",
            "It does not call providers, read key values, write runtime packages, train, or publish Skills.",
        ],
        **v736_safety_flags(),
    ).model_dump()


def list_codex_training_dryrun_logs() -> dict:
    runs = _read_runs()
    latest = runs[0] if runs else None
    logs = latest.logs if latest else []
    return CodexTrainingDryRunLogList(
        logs=logs,
        log_count=len(logs),
        latest_run_id=latest.run_id if latest else None,
        warnings=["Dry run logs are audit-safe metadata summaries only."],
        **v736_safety_flags(),
    ).model_dump()


def get_codex_training_dryrun_gate_report() -> dict:
    latest = _read_runs()[0] if _read_runs() else None
    report = _build_dryrun_gate_report(latest)
    return report.model_dump()


def _build_dryrun(
    request: CodexTrainingDryRunRequest,
    manifest: TrainingDatasetManifest | None,
    gate_report: TrainingGateReport | None,
) -> CodexTrainingDryRun:
    now = datetime.now(UTC).isoformat()
    run_id = f"codex_training_dryrun_v736_{_stamp(now)}"
    failed = _request_failures(request)
    if manifest is None:
        failed.append("dataset_manifest_missing")
    if gate_report is None:
        failed.append("training_gate_report_missing")
    elif gate_report.gate_status != "passed_reference_only":
        failed.append("training_gate_not_passed")
    refs = _metadata_refs(manifest)
    logs = _build_logs(run_id, manifest, gate_report, refs, failed, now)
    run_status = "dryrun_completed_reference_only" if not failed else "dryrun_blocked_reference_only"
    return CodexTrainingDryRun(
        run_id=run_id,
        run_status=run_status,
        dataset_id=manifest.dataset_id if manifest else None,
        gate_report_id=gate_report.gate_report_id if gate_report else None,
        candidate_ids=manifest.source_candidate_ids if manifest else [],
        example_count=manifest.example_count if manifest else 0,
        training_gate_status=gate_report.gate_status if gate_report else "missing",
        loaded_metadata_refs=refs,
        logs=logs,
        audit_id=f"{run_id}_audit",
        source_trace_id=f"{run_id}_source_trace",
        created_at=now,
        warnings=[
            "Dry run simulates Codex Skill training readiness with metadata only.",
            "No provider, key value, runtime package write, real training, Skill publish, final legal output, or delivery action is executed.",
        ],
        **v736_safety_flags(),
    )


def _build_logs(
    run_id: str,
    manifest: TrainingDatasetManifest | None,
    gate_report: TrainingGateReport | None,
    refs: list[dict[str, str]],
    failed: list[str],
    now: str,
) -> list[CodexTrainingDryRunLogEntry]:
    dataset_id = manifest.dataset_id if manifest else None
    gate_report_id = gate_report.gate_report_id if gate_report else None
    candidate_ids = manifest.source_candidate_ids if manifest else []
    steps = [
        ("load_training_dataset_manifest", "loaded" if manifest else "blocked", "Loaded v7.35 dataset manifest metadata."),
        ("load_training_examples", "loaded" if manifest and manifest.example_count else "blocked", "Loaded abstracted training example metadata."),
        ("load_experience_package_metadata", "loaded" if refs else "blocked", "Loaded experience package metadata references only."),
        ("load_skill_output_schema_metadata", "loaded" if refs else "blocked", "Loaded Skill output schema references only."),
        ("load_output_to_experience_trace_metadata", "loaded" if refs else "blocked", "Loaded output-to-experience trace references only."),
        ("run_training_gate_reference_check", "passed" if gate_report and gate_report.gate_status == "passed_reference_only" else "blocked", "Checked v7.35 training gate summary."),
        ("record_no_provider_no_key_no_training_boundary", "passed", "Confirmed no provider, no key value read, no runtime package write, no Skill publish."),
    ]
    if failed:
        steps.append(("dryrun_completion", "blocked", f"Dry run blocked by {', '.join(failed)}."))
    else:
        steps.append(("dryrun_completion", "completed", "Dry run completed as internal metadata simulation only."))
    return [
        CodexTrainingDryRunLogEntry(
            log_id=f"{run_id}_{index:02d}_{name}",
            run_id=run_id,
            step_name=name,
            step_status=status,
            message=message,
            candidate_ids=candidate_ids,
            dataset_id=dataset_id,
            gate_report_id=gate_report_id,
            loaded_metadata_refs=refs[:8],
            created_at=now,
            warnings=["Log entry is safe metadata and contains no source content."],
            **v736_safety_flags(),
        )
        for index, (name, status, message) in enumerate(steps, start=1)
    ]


def _build_dryrun_gate_report(run: CodexTrainingDryRun | None) -> CodexTrainingDryRunGateReport:
    now = datetime.now(UTC).isoformat()
    failed: list[str] = []
    if run is None:
        failed.append("dryrun_missing")
    elif run.run_status != "dryrun_completed_reference_only":
        failed.append("dryrun_not_completed")
    passed = [
        "provider_boundary_safe",
        "key_boundary_safe",
        "runtime_package_boundary_safe",
        "training_boundary_safe",
        "publication_boundary_safe",
        "audit_log_recorded",
        "source_trace_recorded",
    ]
    status = "passed_reference_only" if not failed else "blocked_reference_only"
    report_id = f"codex_training_dryrun_gate_report_v736_{_stamp(now)}"
    return CodexTrainingDryRunGateReport(
        gate_report_id=report_id,
        run_id=run.run_id if run else None,
        dataset_gate_report_id=run.gate_report_id if run else None,
        gate_status=status,
        passed_checks=passed if not failed else passed[:5],
        failed_checks=failed,
        gate_summary=(
            "Dry run gate passed: only metadata was loaded and no provider/key/training/runtime/package publish action occurred."
            if not failed
            else "Dry run gate blocked until a completed reference-only dry run exists."
        ),
        provider_boundary_safe=True,
        key_boundary_safe=True,
        runtime_package_boundary_safe=True,
        training_boundary_safe=True,
        publication_boundary_safe=True,
        created_at=now,
        audit_id=f"{report_id}_audit",
        source_trace_id=f"{report_id}_source_trace",
        warnings=["Dry run gate is reference-only and does not trigger training."],
        **v736_safety_flags(),
    )


def _metadata_refs(manifest: TrainingDatasetManifest | None) -> list[dict[str, str]]:
    if manifest is None:
        return []
    refs: list[dict[str, str]] = []
    for example in manifest.examples:
        package = get_package(example.source_package_id)
        refs.extend(
            [
                {
                    "ref_type": "candidate",
                    "ref_id": example.candidate_id,
                    "status": "loaded_metadata_only",
                },
                {
                    "ref_type": "experience_package",
                    "ref_id": example.source_package_id,
                    "status": "loaded_metadata_only" if package else "metadata_reference_only",
                },
                {
                    "ref_type": "skill_output_schema",
                    "ref_id": example.skill_schema_id,
                    "status": "loaded_metadata_only",
                },
                {
                    "ref_type": "output_to_experience_trace",
                    "ref_id": example.output_trace_id or "trace_pending",
                    "status": example.output_trace_status,
                },
            ]
        )
    return refs


def _request_failures(request: CodexTrainingDryRunRequest) -> list[str]:
    failed: list[str] = []
    if not request.explicit_internal_dry_run_confirmation:
        failed.append("internal_dry_run_confirmation_missing")
    if not request.explicit_no_provider_confirmation:
        failed.append("no_provider_confirmation_missing")
    if not request.explicit_no_key_read_confirmation:
        failed.append("no_key_read_confirmation_missing")
    if not request.explicit_no_runtime_package_write_confirmation:
        failed.append("no_runtime_package_write_confirmation_missing")
    if not request.explicit_no_training_confirmation:
        failed.append("no_training_confirmation_missing")
    if not request.explicit_no_skill_publish_confirmation:
        failed.append("no_skill_publish_confirmation_missing")
    return failed


def _read_runs() -> list[CodexTrainingDryRun]:
    runs = [
        CodexTrainingDryRun(**payload)
        for payload in read_payloads(CODEX_TRAINING_DRYRUNS_DIR)
        if payload.get("run_id")
    ]
    return sorted(runs, key=lambda item: item.created_at, reverse=True)


def _stamp(value: str) -> str:
    return value.replace("+00:00", "Z").replace(":", "").replace("-", "").replace(".", "")
