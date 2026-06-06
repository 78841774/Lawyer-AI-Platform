from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.codex_skill_draft_registry import list_drafts
from personal_skill_studio.training_artifacts.experience_candidate_registry import list_candidates
from personal_skill_studio.training_artifacts.experience_lifecycle_audit_aggregator import aggregate_lifecycle_audit
from personal_skill_studio.training_artifacts.experience_lifecycle_graph_builder import build_lifecycle_graph
from personal_skill_studio.training_artifacts.experience_lifecycle_integrity_engine import check_lifecycle_integrity
from personal_skill_studio.training_artifacts.experience_lifecycle_safety_engine import (
    lifecycle_metadata_safe,
    v732_safety_flags,
)
from personal_skill_studio.training_artifacts.experience_lifecycle_source_trace_aggregator import aggregate_lifecycle_source_trace
from personal_skill_studio.training_artifacts.experience_lifecycle_state_machine import build_stage_event
from personal_skill_studio.training_artifacts.next_experience_package_registry import list_next_package_records
from personal_skill_studio.training_artifacts.practice_feedback_candidate_pack import list_candidate_pack_records
from personal_skill_studio.training_artifacts.practice_feedback_registry import (
    list_feedback_records,
    list_feedback_risk_event_records,
    list_observation_records,
)
from personal_skill_studio.training_artifacts.practice_load_review_gate import list_practice_load_packages
from personal_skill_studio.training_artifacts.practice_runtime_registry import (
    list_runtime_load_records,
    list_usage_events,
)
from personal_skill_studio.training_artifacts.schemas import (
    ExperienceLifecycleList,
    ExperienceLifecycleRecord,
    ExperienceLifecycleSafetySummary,
    V732ExperienceLifecycleStatus,
)
from personal_skill_studio.training_artifacts.skill_experience_pool import list_pool_entries
from personal_skill_studio.training_artifacts.skill_package_registry import list_package_records
from personal_skill_studio.training_artifacts.storage import EXPERIENCE_LIFECYCLES_DIR, read_payload, read_payloads, write_payload
from personal_skill_studio.training_artifacts.training_package_registry import (
    list_experience_package_records,
    list_training_task_records,
)


DEFAULT_LIFECYCLE_ID = "experience_lifecycle_v732_owner"


def recompute_lifecycle(lifecycle_id: str = DEFAULT_LIFECYCLE_ID) -> dict | None:
    record, _context = build_lifecycle_record(lifecycle_id)
    if not lifecycle_metadata_safe(record.model_dump()):
        return None
    write_payload(EXPERIENCE_LIFECYCLES_DIR, lifecycle_id, record.model_dump())
    return record.model_dump()


def list_lifecycles() -> dict:
    records = _stored_or_computed_records()
    return ExperienceLifecycleList(
        lifecycles=records,
        lifecycle_count=len(records),
        warnings=["Experience lifecycles are consolidated metadata views only."],
        **v732_safety_flags(),
    ).model_dump()


def get_lifecycle(lifecycle_id: str) -> dict | None:
    record, _context = _read_or_compute(lifecycle_id)
    return record.model_dump() if record else None


def get_lifecycle_state(lifecycle_id: str) -> dict | None:
    record, _context = _read_or_compute(lifecycle_id)
    if record is None:
        return None
    return {"lifecycle_id": lifecycle_id, "stage_events": [event.model_dump() for event in record.stage_events], **v732_safety_flags()}


def get_lifecycle_graph(lifecycle_id: str) -> dict | None:
    record, context = _read_or_compute(lifecycle_id)
    if record is None:
        return None
    return build_lifecycle_graph(
        record,
        context["training_packages"],
        context["review_packages"],
        context["runtime_loads"],
        context["candidate_packs"],
        context["next_packages"],
    ).model_dump()


def get_lifecycle_audit_timeline(lifecycle_id: str) -> dict | None:
    record, _context = _read_or_compute(lifecycle_id)
    return aggregate_lifecycle_audit(record).model_dump() if record else None


def get_lifecycle_source_trace_view(lifecycle_id: str) -> dict | None:
    record, _context = _read_or_compute(lifecycle_id)
    return aggregate_lifecycle_source_trace(record).model_dump() if record else None


def get_lifecycle_integrity_check(lifecycle_id: str) -> dict | None:
    record, _context = _read_or_compute(lifecycle_id)
    return check_lifecycle_integrity(record).model_dump() if record else None


def get_lifecycle_safety_summary(lifecycle_id: str) -> dict | None:
    record, _context = _read_or_compute(lifecycle_id)
    if record is None:
        return None
    return ExperienceLifecycleSafetySummary(
        lifecycle_id=lifecycle_id,
        loaded_package_is_lawyer_approved=bool(record.latest_lawyer_approved_package_id) or not record.runtime_load_ids,
        warnings=["Safety summary is metadata-only and contains no source content, credential values, or provider payload."],
        **v732_safety_flags(),
    ).model_dump()


def build_v732_status() -> dict:
    records = _stored_or_computed_records()
    return V732ExperienceLifecycleStatus(
        lifecycle_count=len(records),
        stage_event_count=sum(len(record.stage_events) for record in records),
        warnings=[
            "v7.32 consolidates v7.31b-v7.31j lifecycle metadata only.",
            "It does not auto-advance lawyer review, mutate loaded packages, load next drafts, train, publish, or deliver externally.",
        ],
        **v732_safety_flags(),
    ).model_dump()


def build_lifecycle_record(lifecycle_id: str = DEFAULT_LIFECYCLE_ID):
    context = _collect_context()
    now = datetime.now(UTC).isoformat()
    stage_specs = _stage_specs(lifecycle_id, context)
    events = []
    previous_id = None
    for spec in stage_specs:
        event = build_stage_event(
            lifecycle_id=lifecycle_id,
            previous_stage_event_id=previous_id,
            **spec,
        )
        events.append(event)
        previous_id = event.stage_event_id

    current_event = next((event for event in reversed(events) if event.stage_status not in {"not_started"}), events[-1])
    latest_runtime_load = context["runtime_loads"][0] if context["runtime_loads"] else None
    latest_review_package = context["review_packages"][0] if context["review_packages"] else None
    latest_next_package = context["next_packages"][0] if context["next_packages"] else None
    record = ExperienceLifecycleRecord(
        lifecycle_id=lifecycle_id,
        root_material_batch_id=(_get(context["experience_candidates"][0], "source_ocr_job_id") if context["experience_candidates"] else None),
        current_stage=current_event.stage_name,
        current_status=current_event.stage_status,
        case_cause_scope=["personal_production", "practice_runtime_experience"],
        source_candidate_ids=_ids(context["experience_candidates"], "candidate_id"),
        experience_ids=_ids(context["pool_entries"], "experience_id"),
        skill_draft_ids=_ids(context["skill_drafts"], "draft_id"),
        skill_package_ids=_ids(context["skill_packages"], "package_id"),
        training_task_ids=_ids(context["training_tasks"], "training_task_id"),
        experience_package_ids=_ids(context["training_packages"], "package_id"),
        practice_load_review_ids=[_get(item, "package_id") for item in context["review_packages"] if _get(item, "package_id", None)],
        runtime_load_ids=[item.runtime_load_id for item in context["runtime_loads"]],
        usage_event_ids=[item.usage_event_id for item in context["usage_events"]],
        observation_ids=[item.observation_id for item in context["observations"]],
        feedback_ids=[item.feedback_id for item in context["feedback_items"]],
        risk_event_ids=[item.risk_event_id for item in context["risk_events"]],
        candidate_pack_ids=[item.candidate_pack_id for item in context["candidate_packs"]],
        next_package_ids=[item.next_package_id for item in context["next_packages"]],
        latest_loaded_package_id=latest_runtime_load.experience_package_id if latest_runtime_load else None,
        latest_lawyer_approved_package_id=_get(latest_review_package, "package_id") if latest_review_package and _get(latest_review_package, "review_status") == "approved_for_practice_load" else None,
        latest_next_package_draft_id=latest_next_package.next_package_id if latest_next_package else None,
        blocked_reason=None,
        safety_flags=["metadata_only", "lawyer_review_required", "source_trace_required", "audit_required"],
        source_trace_root_id=f"{lifecycle_id}_source_trace_root",
        audit_timeline_id=f"{lifecycle_id}_audit_timeline",
        stage_events=events,
        next_allowed_actions=_next_allowed_actions(current_event.stage_name),
        created_at=now,
        updated_at=now,
        warnings=["Lifecycle record is a consolidated metadata view; it does not mutate or advance package state."],
        **v732_safety_flags(),
    )
    return record, context


def _collect_context() -> dict:
    return {
        "experience_candidates": list_candidates().get("candidates", []),
        "pool_entries": list_pool_entries().get("experiences", []),
        "skill_drafts": list_drafts().get("drafts", []),
        "skill_packages": list_package_records().get("skill_packages", []),
        "training_tasks": list_training_task_records().get("training_tasks", []),
        "training_packages": list_experience_package_records().get("training_packages", []),
        "review_packages": list_practice_load_packages().get("packages", []),
        "runtime_loads": list_runtime_load_records(),
        "usage_events": list_usage_events(),
        "observations": list_observation_records(),
        "feedback_items": list_feedback_records(),
        "risk_events": list_feedback_risk_event_records(),
        "candidate_packs": list_candidate_pack_records(),
        "next_packages": list_next_package_records(),
    }


def _stage_specs(lifecycle_id: str, context: dict) -> list[dict]:
    return [
        _stage("raw_work_product_controlled_processing", context["experience_candidates"], "raw_work_product_batch", "ready_for_next_stage"),
        _stage("ocr_document_parse", context["experience_candidates"], "ocr_job", "ready_for_next_stage"),
        _stage("legal_retrieval", context["experience_candidates"], "legal_retrieval_job", "ready_for_next_stage"),
        _stage("experience_candidate_generation", context["experience_candidates"], "experience_candidate", "ready_for_next_stage"),
        _stage("experience_redaction_abstraction", context["experience_candidates"], "experience_candidate", "ready_for_next_stage"),
        _stage("skill_experience_pool", context["pool_entries"], "skill_experience_pool_entry", "ready_for_next_stage"),
        _stage("skill_draft_build", context["skill_drafts"], "codex_skill_draft", "ready_for_next_stage"),
        _stage("skill_package_versioning", context["skill_packages"], "skill_package", "ready_for_next_stage"),
        _stage("system_validation_gate", context["skill_packages"], "skill_package", "system_validated"),
        _stage("internal_training_task_build", context["training_tasks"], "training_task", "ready_for_next_stage"),
        _stage("experience_package_build", context["training_packages"], "experience_package", "pending_lawyer_load_review"),
        _stage("practice_load_review", context["review_packages"], "practice_load_review_package", "pending_lawyer_load_review"),
        _stage("lawyer_experience_editing", context["review_packages"], "practice_load_review_package", "ready_for_next_stage"),
        _stage("lawyer_approved_package", [item for item in context["review_packages"] if _get(item, "review_status") == "approved_for_practice_load"], "lawyer_approved_package", "lawyer_approved"),
        _stage("practice_runtime_loading", context["runtime_loads"], "runtime_load", _runtime_status(context["runtime_loads"])),
        _stage("runtime_policy_evaluation", context["usage_events"], "usage_event", "ready_for_next_stage"),
        _stage("runtime_usage_monitoring", context["usage_events"], "usage_event", "ready_for_next_stage"),
        _stage("output_observation", context["observations"], "practice_output_observation", "feedback_collected"),
        _stage("lawyer_feedback", context["feedback_items"], "practice_lawyer_feedback", "feedback_collected"),
        _stage("risk_event", context["risk_events"], "practice_feedback_risk_event", "feedback_collected"),
        _stage("feedback_candidate_pack", context["candidate_packs"], "practice_feedback_candidate_pack", _candidate_pack_status(context["candidate_packs"])),
        _stage("next_experience_package_draft", context["next_packages"], "next_experience_package_draft", _next_package_status(context["next_packages"])),
        _stage("pending_next_practice_load_review", [item for item in context["next_packages"] if item.draft_status == "pending_practice_load_review"], "next_experience_package_draft", "pending_next_load_review"),
    ]


def _stage(stage_name: str, items: list, linked_object_type: str, present_status: str) -> dict:
    first = items[0] if items else None
    return {
        "stage_name": stage_name,
        "stage_status": present_status if items else "not_started",
        "linked_object_type": linked_object_type,
        "linked_object_id": _object_id(first),
        "allowed_actions": _next_allowed_actions(stage_name),
        "source_trace_id": f"{stage_name}_source_trace_ready" if items else None,
        "blocked_reason": None if items else "stage metadata not created yet",
    }


def _object_id(item) -> str | None:
    if item is None:
        return None
    if isinstance(item, dict):
        for key in ("candidate_id", "experience_id", "draft_id", "package_id", "training_task_id"):
            if item.get(key):
                return item[key]
        return None
    for key in ("runtime_load_id", "usage_event_id", "observation_id", "feedback_id", "risk_event_id", "candidate_pack_id", "next_package_id", "package_id"):
        value = getattr(item, key, None)
        if value:
            return value
    return None


def _get(item, key: str, default=None):
    if item is None:
        return default
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def _ids(items: list[dict], key: str) -> list[str]:
    return [str(item.get(key)) for item in items if item.get(key)]


def _runtime_status(loads: list) -> str:
    if not loads:
        return "not_started"
    status = loads[0].load_status
    return "loaded_active" if status == "loaded_active" else "loaded_gray" if status == "loaded_gray" else status


def _candidate_pack_status(packs: list) -> str:
    if any(pack.candidate_status == "ready_for_next_experience_build" for pack in packs):
        return "candidate_pack_ready"
    return packs[0].candidate_status if packs else "not_started"


def _next_package_status(drafts: list) -> str:
    if any(draft.draft_status == "pending_practice_load_review" for draft in drafts):
        return "pending_next_load_review"
    if drafts:
        return "next_package_draft_ready"
    return "not_started"


def _next_allowed_actions(stage_name: str) -> list[str]:
    actions = {
        "practice_load_review": ["lawyer_edit", "system_revalidate", "approve_for_practice_load", "reject_for_practice_load"],
        "practice_runtime_loading": ["manual_disable_via_runtime_control", "manual_rollback_via_runtime_control"],
        "lawyer_feedback": ["triage_feedback", "build_candidate_pack"],
        "feedback_candidate_pack": ["mark_ready_for_next_build", "archive_candidate_pack"],
        "next_experience_package_draft": ["mark_pending_practice_load_review", "archive_next_package"],
        "pending_next_practice_load_review": ["restart_practice_load_review_gate"],
    }
    return actions.get(stage_name, ["continue_when_metadata_ready"])


def _stored_or_computed_records() -> list[ExperienceLifecycleRecord]:
    records = [
        ExperienceLifecycleRecord(**payload)
        for payload in read_payloads(EXPERIENCE_LIFECYCLES_DIR)
        if payload.get("lifecycle_id")
    ]
    if records:
        return sorted(records, key=lambda item: item.updated_at, reverse=True)
    record, _context = build_lifecycle_record(DEFAULT_LIFECYCLE_ID)
    return [record]


def _read_or_compute(lifecycle_id: str):
    payload = read_payload(EXPERIENCE_LIFECYCLES_DIR, lifecycle_id)
    if payload:
        return ExperienceLifecycleRecord(**payload), _collect_context()
    if lifecycle_id == DEFAULT_LIFECYCLE_ID:
        return build_lifecycle_record(lifecycle_id)
    return None, {}
