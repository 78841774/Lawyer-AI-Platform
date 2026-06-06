from personal_skill_studio.training_artifacts.experience_iteration_candidate_builder import build_candidate_pack
from personal_skill_studio.training_artifacts.iteration_candidate_audit_engine import build_iteration_candidate_audit_event
from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import (
    iteration_candidate_metadata_safe,
    v731i_safety_flags,
)
from personal_skill_studio.training_artifacts.practice_feedback_registry import (
    list_feedback_records,
    list_feedback_risk_event_records,
)
from personal_skill_studio.training_artifacts.schemas import (
    PracticeFeedbackCandidatePack,
    PracticeFeedbackCandidatePackActionRequest,
    PracticeFeedbackCandidatePackAudit,
    PracticeFeedbackCandidatePackBuildRequest,
    PracticeFeedbackCandidatePackList,
    V731iPracticeFeedbackCandidatePackStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    PRACTICE_FEEDBACK_CANDIDATE_PACKS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def build_practice_feedback_candidate_pack(request: PracticeFeedbackCandidatePackBuildRequest) -> dict | None:
    pack = build_candidate_pack(request)
    if pack is None:
        return None
    write_candidate_pack(pack)
    return pack.model_dump()


def write_candidate_pack(pack: PracticeFeedbackCandidatePack) -> None:
    write_payload(PRACTICE_FEEDBACK_CANDIDATE_PACKS_DIR, pack.candidate_pack_id, pack.model_dump())


def get_candidate_pack_record(candidate_pack_id: str) -> PracticeFeedbackCandidatePack | None:
    payload = read_payload(PRACTICE_FEEDBACK_CANDIDATE_PACKS_DIR, candidate_pack_id)
    return PracticeFeedbackCandidatePack(**payload) if payload else None


def get_practice_feedback_candidate_pack(candidate_pack_id: str) -> dict | None:
    record = get_candidate_pack_record(candidate_pack_id)
    return record.model_dump() if record else None


def list_candidate_pack_records() -> list[PracticeFeedbackCandidatePack]:
    records = [
        PracticeFeedbackCandidatePack(**payload)
        for payload in read_payloads(PRACTICE_FEEDBACK_CANDIDATE_PACKS_DIR)
        if payload.get("candidate_pack_id")
    ]
    return sorted(records, key=lambda item: item.created_at, reverse=True)


def list_practice_feedback_candidate_packs() -> dict:
    records = list_candidate_pack_records()
    return PracticeFeedbackCandidatePackList(
        candidate_packs=records,
        candidate_pack_count=len(records),
        draft_count=_count_status(records, "draft_candidate_pack"),
        ready_count=_count_status(records, "ready_for_next_experience_build"),
        blocked_count=_count_status(records, "blocked"),
        archived_count=_count_status(records, "archived"),
        warnings=[
            "Candidate packs are metadata-only and do not alter current runtime packages.",
            "Ready status only prepares v7.31j rebuild; it does not load a package.",
        ],
        **v731i_safety_flags(),
    ).model_dump()


def get_practice_feedback_candidate_pack_diff(candidate_pack_id: str) -> dict | None:
    record = get_candidate_pack_record(candidate_pack_id)
    if record is None:
        return None
    return record.diff.model_dump()


def get_practice_feedback_candidate_pack_audit(candidate_pack_id: str) -> dict | None:
    record = get_candidate_pack_record(candidate_pack_id)
    if record is None:
        return None
    return PracticeFeedbackCandidatePackAudit(
        candidate_pack_id=candidate_pack_id,
        events=record.audit_events,
        event_count=len(record.audit_events),
        warnings=["Candidate pack audit contains metadata events only."],
        **v731i_safety_flags(),
    ).model_dump()


def get_practice_feedback_candidate_pack_source_trace(candidate_pack_id: str) -> dict | None:
    record = get_candidate_pack_record(candidate_pack_id)
    if record is None:
        return None
    return record.source_trace.model_dump()


def mark_candidate_pack_ready(candidate_pack_id: str, request: PracticeFeedbackCandidatePackActionRequest) -> dict | None:
    return _transition_candidate_pack(
        candidate_pack_id=candidate_pack_id,
        request=request,
        status="ready_for_next_experience_build",
        action="candidate_pack_marked_ready",
    )


def archive_candidate_pack(candidate_pack_id: str, request: PracticeFeedbackCandidatePackActionRequest) -> dict | None:
    return _transition_candidate_pack(
        candidate_pack_id=candidate_pack_id,
        request=request,
        status="archived",
        action="candidate_pack_archived",
    )


def build_v731i_status() -> dict:
    records = list_candidate_pack_records()
    feedback_items = list_feedback_records()
    risk_events = list_feedback_risk_event_records()
    return V731iPracticeFeedbackCandidatePackStatus(
        candidate_pack_count=len(records),
        ready_for_next_build_count=_count_status(records, "ready_for_next_experience_build"),
        triaged_feedback_count=sum(
            1
            for item in feedback_items
            if item.feedback_status in {"triaged", "accepted_as_candidate", "converted_to_iteration_candidate"}
        ),
        risk_event_count=len(risk_events),
        warnings=[
            "v7.31i builds next-iteration candidate pack metadata only.",
            "It does not modify loaded packages, lawyer-approved packages, runtime policy, Skills, training artifacts, or delivery state.",
        ],
        **v731i_safety_flags(),
    ).model_dump()


def _transition_candidate_pack(
    candidate_pack_id: str,
    request: PracticeFeedbackCandidatePackActionRequest,
    status: str,
    action: str,
) -> dict | None:
    record = get_candidate_pack_record(candidate_pack_id)
    if record is None or not iteration_candidate_metadata_safe(request.model_dump()):
        return None
    updated = record.model_copy(deep=True)
    updated.candidate_status = status
    updated.iteration_candidates = [
        candidate.model_copy(update={"status": "ready_for_next_build" if status == "ready_for_next_experience_build" else candidate.status})
        for candidate in updated.iteration_candidates
    ]
    updated.audit_events.append(
        build_iteration_candidate_audit_event(
            object_id=candidate_pack_id,
            object_type="practice_feedback_candidate_pack",
            action=action,
            actor_id=request.actor_id,
            actor_note=request.actor_note,
        )
    )
    updated.warnings = [
        "Candidate pack status update is metadata-only.",
        "Status changes do not mutate packages, runtime policy, Skills, training artifacts, or delivery state.",
    ]
    write_candidate_pack(updated)
    return updated.model_dump()


def _count_status(records: list[PracticeFeedbackCandidatePack], status: str) -> int:
    return sum(1 for record in records if record.candidate_status == status)
