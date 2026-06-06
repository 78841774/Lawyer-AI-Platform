from personal_skill_studio.training_artifacts.next_experience_package_rebuilder import rebuild_next_experience_package
from personal_skill_studio.training_artifacts.next_package_audit_engine import build_next_package_audit_event
from personal_skill_studio.training_artifacts.next_package_safety_engine import (
    next_package_metadata_safe,
    v731j_safety_flags,
)
from personal_skill_studio.training_artifacts.practice_feedback_candidate_pack import list_candidate_pack_records
from personal_skill_studio.training_artifacts.schemas import (
    NextExperiencePackageActionRequest,
    NextExperiencePackageAudit,
    NextExperiencePackageDraft,
    NextExperiencePackageDraftList,
    NextExperiencePackageRebuildRequest,
    V731jNextExperiencePackageStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    NEXT_EXPERIENCE_PACKAGES_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


def rebuild_next_experience_package_record(request: NextExperiencePackageRebuildRequest) -> dict | None:
    draft = rebuild_next_experience_package(request)
    if draft is None:
        return None
    write_next_package(draft)
    return draft.model_dump()


def write_next_package(draft: NextExperiencePackageDraft) -> None:
    write_payload(NEXT_EXPERIENCE_PACKAGES_DIR, draft.next_package_id, draft.model_dump())


def get_next_package_record(next_package_id: str) -> NextExperiencePackageDraft | None:
    payload = read_payload(NEXT_EXPERIENCE_PACKAGES_DIR, next_package_id)
    return NextExperiencePackageDraft(**payload) if payload else None


def list_next_package_records() -> list[NextExperiencePackageDraft]:
    records = [
        NextExperiencePackageDraft(**payload)
        for payload in read_payloads(NEXT_EXPERIENCE_PACKAGES_DIR)
        if payload.get("next_package_id")
    ]
    return sorted(records, key=lambda item: item.created_at, reverse=True)


def list_next_experience_packages() -> dict:
    records = list_next_package_records()
    return NextExperiencePackageDraftList(
        next_packages=records,
        next_package_count=len(records),
        draft_rebuilt_count=_count_status(records, "draft_rebuilt"),
        pending_practice_load_review_count=_count_status(records, "pending_practice_load_review"),
        blocked_count=_count_status(records, "blocked"),
        archived_count=_count_status(records, "archived"),
        warnings=[
            "Next packages are draft metadata only.",
            "Pending load review status does not load the package into practice runtime.",
        ],
        **v731j_safety_flags(),
    ).model_dump()


def get_next_experience_package(next_package_id: str) -> dict | None:
    record = get_next_package_record(next_package_id)
    return record.model_dump() if record else None


def get_next_experience_package_lawyer_review_view(next_package_id: str) -> dict | None:
    record = get_next_package_record(next_package_id)
    return record.lawyer_review_view.model_dump() if record else None


def get_next_experience_package_manifest(next_package_id: str) -> dict | None:
    record = get_next_package_record(next_package_id)
    return record.manifest.model_dump() if record else None


def get_next_experience_package_audit(next_package_id: str) -> dict | None:
    record = get_next_package_record(next_package_id)
    if record is None:
        return None
    return NextExperiencePackageAudit(
        next_package_id=record.next_package_id,
        events=record.audit_events,
        event_count=len(record.audit_events),
        warnings=["Next package audit contains metadata events only."],
        **v731j_safety_flags(),
    ).model_dump()


def get_next_experience_package_source_trace(next_package_id: str) -> dict | None:
    record = get_next_package_record(next_package_id)
    return record.source_trace.model_dump() if record else None


def mark_next_package_pending_load_review(
    next_package_id: str,
    request: NextExperiencePackageActionRequest,
) -> dict | None:
    return _transition_next_package(
        next_package_id=next_package_id,
        request=request,
        status="pending_practice_load_review",
        action="next_package_marked_pending_practice_load_review",
    )


def archive_next_package(next_package_id: str, request: NextExperiencePackageActionRequest) -> dict | None:
    return _transition_next_package(
        next_package_id=next_package_id,
        request=request,
        status="archived",
        action="next_package_archived",
    )


def build_v731j_status() -> dict:
    records = list_next_package_records()
    candidate_packs = list_candidate_pack_records()
    return V731jNextExperiencePackageStatus(
        next_package_count=len(records),
        ready_candidate_pack_count=sum(
            1 for pack in candidate_packs if pack.candidate_status == "ready_for_next_experience_build"
        ),
        pending_practice_load_review_count=_count_status(records, "pending_practice_load_review"),
        warnings=[
            "v7.31j rebuilds next package draft metadata only from ready candidate packs.",
            "Drafts do not replace runtime packages and must be reviewed before future controlled loading.",
        ],
        **v731j_safety_flags(),
    ).model_dump()


def _transition_next_package(
    next_package_id: str,
    request: NextExperiencePackageActionRequest,
    status: str,
    action: str,
) -> dict | None:
    record = get_next_package_record(next_package_id)
    if record is None or not next_package_metadata_safe(request.model_dump()):
        return None
    updated = record.model_copy(deep=True)
    updated.draft_status = status
    updated.manifest.draft_status = status
    updated.audit_events.append(
        build_next_package_audit_event(
            next_package_id=next_package_id,
            action=action,
            actor_id=request.actor_id,
            actor_note=request.actor_note,
        )
    )
    updated.warnings = [
        "Next package status update is metadata-only.",
        "Status changes do not load or replace any practice runtime package.",
    ]
    write_next_package(updated)
    return updated.model_dump()


def _count_status(records: list[NextExperiencePackageDraft], status: str) -> int:
    return sum(1 for record in records if record.draft_status == status)
