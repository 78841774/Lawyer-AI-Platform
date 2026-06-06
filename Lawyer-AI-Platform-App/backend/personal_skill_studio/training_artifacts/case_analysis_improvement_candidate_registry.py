from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.case_analysis_feedback_to_improvement_mapper import (
    choose_mapping,
    classify_risk_type,
)
from personal_skill_studio.training_artifacts.case_analysis_improvement_audit_engine import build_candidate_audit
from personal_skill_studio.training_artifacts.case_analysis_improvement_diff_engine import build_improvement_diff
from personal_skill_studio.training_artifacts.case_analysis_improvement_readiness_engine import (
    build_readiness_report,
    can_mark_ready,
)
from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import (
    case_analysis_improvement_metadata_safe,
    v734_safety_flags,
)
from personal_skill_studio.training_artifacts.case_analysis_improvement_source_trace_engine import build_candidate_source_trace
from personal_skill_studio.training_artifacts.case_analysis_output_to_experience_trace import (
    build_output_to_experience_traces,
    get_output_to_experience_trace,
    list_output_to_experience_traces,
)
from personal_skill_studio.training_artifacts.case_analysis_runtime_output_registry import list_workbench_views
from personal_skill_studio.training_artifacts.schemas import (
    CaseAnalysisImprovementActionRequest,
    CaseAnalysisImprovementBuildRequest,
    CaseAnalysisImprovementCandidate,
    CaseAnalysisImprovementCandidateList,
    CaseAnalysisImprovementDiff,
    CaseAnalysisImprovementDiffList,
    V734CaseAnalysisImprovementStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR,
    CASE_ANALYSIS_IMPROVEMENT_DIFFS_DIR,
    CASE_ANALYSIS_IMPROVEMENT_TRACES_DIR,
    CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR,
    CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def build_case_analysis_improvement_candidates(
    request: CaseAnalysisImprovementBuildRequest | None = None,
) -> dict:
    request = request or CaseAnalysisImprovementBuildRequest()
    if not (
        request.explicit_metadata_only_confirmation
        and request.explicit_no_package_mutation_confirmation
        and request.explicit_no_training_confirmation
        and request.explicit_no_schema_mutation_confirmation
    ):
        return _candidate_list([])

    traces = build_output_to_experience_traces()
    for trace in traces:
        write_payload(CASE_ANALYSIS_IMPROVEMENT_TRACES_DIR, trace.trace_id, trace.model_dump())

    built: list[CaseAnalysisImprovementCandidate] = []
    feedback_by_output = _records_by_output(read_payloads(CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR))
    risk_by_output = _records_by_output(read_payloads(CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR))
    for view in _views():
        for group in view.get("output_groups", []):
            for output in group.get("outputs", []):
                output_id = output.get("output_id")
                feedback_records = feedback_by_output.get(output_id, [])
                risk_records = risk_by_output.get(output_id, [])
                if not feedback_records and not risk_records:
                    continue
                candidate = _build_candidate(view, group, output, feedback_records, risk_records)
                if case_analysis_improvement_metadata_safe(candidate.model_dump()):
                    write_payload(CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR, candidate.candidate_id, candidate.model_dump())
                    built.append(candidate)
    return _candidate_list(built)


def list_case_analysis_improvement_candidates() -> dict:
    candidates = _read_candidates()
    return _candidate_list(candidates)


def get_case_analysis_improvement_candidate(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    return candidate.model_dump() if candidate else None


def get_case_analysis_improvement_candidate_readiness(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    return build_readiness_report(candidate).model_dump() if candidate else None


def mark_case_analysis_improvement_candidate_ready(
    candidate_id: str,
    request: CaseAnalysisImprovementActionRequest | None = None,
) -> dict | None:
    candidate = _read_candidate(candidate_id)
    if candidate is None:
        return None
    request = request or CaseAnalysisImprovementActionRequest()
    if not (
        request.explicit_metadata_only_confirmation
        and request.explicit_no_training_confirmation
        and request.explicit_no_package_mutation_confirmation
        and can_mark_ready(candidate)
    ):
        updated = candidate.model_copy(
            update={
                "candidate_status": "blocked",
                "readiness_status": "blocked",
                "blocked_reason": "Readiness metadata is incomplete or confirmation is missing.",
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
    else:
        updated = candidate.model_copy(
            update={
                "candidate_status": "ready_for_training_dataset_build",
                "readiness_status": "ready_for_training_dataset_build",
                "blocked_reason": None,
                "updated_at": datetime.now(UTC).isoformat(),
            }
        )
    write_payload(CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR, updated.candidate_id, updated.model_dump())
    return updated.model_dump()


def archive_case_analysis_improvement_candidate(
    candidate_id: str,
    request: CaseAnalysisImprovementActionRequest | None = None,
) -> dict | None:
    candidate = _read_candidate(candidate_id)
    if candidate is None:
        return None
    request = request or CaseAnalysisImprovementActionRequest()
    if not request.explicit_metadata_only_confirmation:
        return candidate.model_dump()
    updated = candidate.model_copy(
        update={
            "candidate_status": "archived",
            "readiness_status": "not_ready",
            "blocked_reason": "Archived by owner lawyer metadata action.",
            "updated_at": datetime.now(UTC).isoformat(),
        }
    )
    write_payload(CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR, updated.candidate_id, updated.model_dump())
    return updated.model_dump()


def build_case_analysis_improvement_diff() -> dict:
    candidates = _read_candidates()
    if not candidates:
        build_case_analysis_improvement_candidates()
        candidates = _read_candidates()
    diff = build_improvement_diff(candidates)
    write_payload(CASE_ANALYSIS_IMPROVEMENT_DIFFS_DIR, diff.diff_id, diff.model_dump())
    return diff.model_dump()


def list_case_analysis_improvement_diffs() -> dict:
    diffs = [
        CaseAnalysisImprovementDiff(**payload)
        for payload in read_payloads(CASE_ANALYSIS_IMPROVEMENT_DIFFS_DIR)
        if payload.get("diff_id")
    ]
    return CaseAnalysisImprovementDiffList(
        diffs=sorted(diffs, key=lambda item: item.created_at, reverse=True),
        diff_count=len(diffs),
        warnings=["Improvement diffs are summaries only and are never auto-applied."],
        **v734_safety_flags(),
    ).model_dump()


def get_case_analysis_improvement_diff(diff_id: str) -> dict | None:
    payload = read_payload(CASE_ANALYSIS_IMPROVEMENT_DIFFS_DIR, diff_id)
    return CaseAnalysisImprovementDiff(**payload).model_dump() if payload else None


def get_case_analysis_improvement_candidate_audit(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    return build_candidate_audit(candidate).model_dump() if candidate else None


def get_case_analysis_improvement_candidate_source_trace(candidate_id: str) -> dict | None:
    candidate = _read_candidate(candidate_id)
    return build_candidate_source_trace(candidate).model_dump() if candidate else None


def list_case_analysis_output_to_experience_traces() -> dict:
    traces = build_output_to_experience_traces()
    for trace in traces:
        write_payload(CASE_ANALYSIS_IMPROVEMENT_TRACES_DIR, trace.trace_id, trace.model_dump())
    return list_output_to_experience_traces()


def get_case_analysis_output_to_experience_trace(trace_id: str) -> dict | None:
    payload = read_payload(CASE_ANALYSIS_IMPROVEMENT_TRACES_DIR, trace_id)
    if payload:
        return payload
    trace = get_output_to_experience_trace(trace_id)
    if trace:
        write_payload(CASE_ANALYSIS_IMPROVEMENT_TRACES_DIR, trace_id, trace)
    return trace


def build_v734_status() -> dict:
    candidates = _read_candidates()
    traces = build_output_to_experience_traces()
    diffs = read_payloads(CASE_ANALYSIS_IMPROVEMENT_DIFFS_DIR)
    feedback = read_payloads(CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR)
    risks = read_payloads(CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR)
    return V734CaseAnalysisImprovementStatus(
        candidate_count=len(candidates),
        ready_for_training_dataset_build_count=sum(
            1 for candidate in candidates if candidate.readiness_status == "ready_for_training_dataset_build"
        ),
        trace_count=len(traces),
        diff_count=len(diffs),
        feedback_count=len(feedback),
        risk_event_count=len(risks),
        warnings=[
            "v7.34 maps case-analysis output feedback and risk events into improvement candidate metadata only.",
            "Candidates do not update packages, schemas, Skills, runtime loads, training artifacts, or external delivery state.",
        ],
        **v734_safety_flags(),
    ).model_dump()


def _build_candidate(
    view: dict,
    group: dict,
    output: dict,
    feedback_records: list[dict],
    risk_records: list[dict],
) -> CaseAnalysisImprovementCandidate:
    now = datetime.now(UTC).isoformat()
    output_group = group.get("group_type") or group.get("group_id", "unknown_group")
    candidate_type, change_type, target_type, severity, reasons = choose_mapping(output_group, feedback_records, risk_records)
    feedback_ids = [item.get("feedback_id") for item in feedback_records if item.get("feedback_id")]
    risk_event_ids = [item.get("risk_event_id") for item in risk_records if item.get("risk_event_id")]
    feedback_types = sorted({str(item.get("feedback_type", "improvement_suggestion")) for item in feedback_records})
    risk_types = sorted({classify_risk_type(item) for item in risk_records})
    output_id = output.get("output_id", "unknown_output")
    experience_card_ids = list(output.get("source_experience_ids") or [])
    target_id = experience_card_ids[0] if target_type == "experience_card" and experience_card_ids else output_id
    return CaseAnalysisImprovementCandidate(
        candidate_id=f"{output_id}_improvement_candidate_v734",
        source_output_id=output_id,
        source_output_group=output_group,
        source_output_type=output.get("output_type", "unknown_output_type"),
        source_output_title=output.get("output_title", "Schema output"),
        source_output_order=int(output.get("output_order", 0)),
        source_output_summary_redacted=output.get("output_summary_redacted", "Redacted metadata summary only."),
        source_case_analysis_view_id=view.get("view_id", "case_analysis_view_pending"),
        source_runtime_load_id=output.get("source_runtime_load_id") or view.get("runtime_load_id", "runtime_load_pending"),
        source_usage_event_id=output.get("source_usage_event_id"),
        source_package_id=view.get("package_id", "package_pending"),
        source_package_version=view.get("package_version", "version_pending"),
        source_experience_card_ids=experience_card_ids,
        source_feedback_ids=feedback_ids,
        source_risk_event_ids=risk_event_ids,
        source_audit_ids=[output.get("audit_id", f"{output_id}_audit")]
        + [item.get("audit_id") for item in feedback_records + risk_records if item.get("audit_id")],
        source_trace_ids=[output.get("source_trace_id", f"{output_id}_source_trace")]
        + [item.get("source_trace_id") for item in feedback_records + risk_records if item.get("source_trace_id")],
        source_feedback_types=feedback_types,
        source_risk_types=risk_types,
        candidate_type=candidate_type,
        candidate_status="mapped",
        candidate_severity=severity,
        candidate_title=f"{output.get('output_title', 'Schema output')} 改进候选",
        candidate_summary="根据律师反馈与风险事件生成的经验改进候选 metadata。",
        candidate_reason=f"Mapping basis: {', '.join(reasons)}.",
        proposed_change_type=change_type,
        proposed_change_summary="建议进入后续人工复核与 v7.35 dataset gate；本阶段不应用改动。",
        target_object_type=target_type,
        target_object_id=target_id,
        affected_output_schema_group=group.get("group_id", output_group),
        affected_output_schema_type=output.get("output_type", "unknown_output_type"),
        affected_usage_boundary="review_later_metadata_only",
        affected_risk_warning="review_later_metadata_only",
        affected_experience_card_id=experience_card_ids[0] if experience_card_ids else None,
        training_relevance="requires_dataset_gate" if candidate_type != "mark_output_as_high_risk" else "training_candidate",
        practice_relevance="requires_lawyer_load_review_later",
        safety_flags=v734_safety_flags(),
        readiness_status="ready_for_candidate_pack",
        created_at=now,
        updated_at=now,
        audit_id=f"{output_id}_improvement_candidate_audit_v734",
        source_trace_id=f"{output_id}_improvement_candidate_source_trace_v734",
        warnings=[
            "Candidate is reference metadata only.",
            "No package, schema, Skill, training, runtime, report, or delivery action is executed.",
        ],
        **v734_safety_flags(),
    )


def _candidate_list(candidates: list[CaseAnalysisImprovementCandidate]) -> dict:
    ordered = sorted(candidates, key=lambda item: item.updated_at, reverse=True)
    return CaseAnalysisImprovementCandidateList(
        candidates=ordered,
        candidate_count=len(ordered),
        warnings=["Improvement candidates are metadata-only and require later gate review before any training dataset use."],
        **v734_safety_flags(),
    ).model_dump()


def _read_candidates() -> list[CaseAnalysisImprovementCandidate]:
    return [
        CaseAnalysisImprovementCandidate(**payload)
        for payload in read_payloads(CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR)
        if payload.get("candidate_id")
    ]


def _read_candidate(candidate_id: str) -> CaseAnalysisImprovementCandidate | None:
    payload = read_payload(CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR, candidate_id)
    return CaseAnalysisImprovementCandidate(**payload) if payload else None


def _records_by_output(records: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = {}
    for record in records:
        output_id = record.get("output_id")
        if output_id:
            grouped.setdefault(output_id, []).append(record)
    return grouped


def _views() -> list[dict]:
    return list_workbench_views().get("views", []) or []
