from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.lawyer_experience_editor import (
    build_review_package,
    save_edits,
    start_edit,
    v731f_safety_flags,
)
from personal_skill_studio.training_artifacts.schemas import (
    ExperiencePackage,
    PracticeLoadReviewAuditEvent,
    PracticeLoadReviewDecisionRequest,
    PracticeLoadReviewEditRequest,
    PracticeLoadReviewPackage,
    PracticeLoadReviewPackageAudit,
    PracticeLoadReviewPackageList,
    PracticeLoadReviewSaveRequest,
    PracticeLoadRevalidationResult,
    V731fPracticeLoadPipelineStatus,
)
from personal_skill_studio.training_artifacts.storage import (
    PRACTICE_LOAD_REVIEW_PACKAGES_DIR,
    TRAINING_PACKAGES_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


FORBIDDEN_MARKERS = [
    "api_key",
    "provider_response",
    "provider_raw_response",
    "raw_text",
    "ocr_text",
    "original_text",
    "full_document_text",
    "raw_material",
    "private_key",
    "access_token",
    "refresh_token",
    "unredacted_payload",
    "unredacted_material",
]


def list_practice_load_packages() -> dict:
    packages = _all_review_packages()
    return PracticeLoadReviewPackageList(
        packages=packages,
        package_count=len(packages),
        pending_practice_load_review_count=sum(
            1 for package in packages if package.review_status == "pending_practice_load_review"
        ),
        approved_for_practice_load_count=sum(
            1 for package in packages if package.review_status == "approved_for_practice_load"
        ),
        warnings=["Practice load review packages are metadata-only and not loaded into practice runtime by this API."],
        **v731f_safety_flags(),
    ).model_dump()


def get_practice_load_package(package_id: str) -> dict | None:
    package = _read_or_build_review_package(package_id)
    return package.model_dump() if package else None


def edit_practice_load_package(package_id: str, request: PracticeLoadReviewEditRequest) -> dict | None:
    package = _read_or_build_review_package(package_id)
    if package is None:
        return None
    updated = start_edit(package, request)
    _write_review_package(updated)
    return updated.model_dump()


def save_practice_load_package(package_id: str, request: PracticeLoadReviewSaveRequest) -> dict | None:
    package = _read_or_build_review_package(package_id)
    if package is None:
        return None
    updated = save_edits(package, request)
    _write_review_package(updated)
    return updated.model_dump()


def revalidate_practice_load_package(package_id: str) -> dict | None:
    package = _read_or_build_review_package(package_id)
    if package is None:
        return None
    errors = _revalidation_errors(package)
    updated = package.model_copy(deep=True)
    passed = not errors
    updated.revalidation_result = PracticeLoadRevalidationResult(
        package_id=package.package_id,
        validation_status="system_revalidated" if passed else "changes_requested",
        revalidation_passed=passed,
        all_cards_metadata_safe=passed,
        source_trace_complete=bool(package.source_trace_bundle.source_trace_ids),
        audit_complete=bool(package.audit_events),
        sensitive_field_scan_passed=passed,
        generated_package_preserved=bool(package.generated_experience_package.get("generated_package_preserved", False)),
        lawyer_approved_package_ready=bool(package.lawyer_approved_experience_package),
        validation_errors=errors,
        warnings=["System revalidation scans review metadata only."],
        **v731f_safety_flags(),
    )
    updated.validation_status = updated.revalidation_result.validation_status
    updated.review_status = "system_revalidated" if passed else "changes_requested"
    updated.load_gate_status = updated.review_status
    updated.can_load_to_practice_runtime = False
    updated.updated_at = datetime.now(UTC).isoformat()
    updated.audit_events.append(_audit_event(package_id, updated.review_status))
    _write_review_package(updated)
    return updated.model_dump()


def approve_practice_load_package(package_id: str, request: PracticeLoadReviewDecisionRequest) -> dict | None:
    package = _read_or_build_review_package(package_id)
    if package is None or package.validation_status != "system_revalidated":
        return None
    updated = package.model_copy(deep=True)
    updated.review_status = "approved_for_practice_load"
    updated.load_gate_status = "approved_for_practice_load"
    updated.can_load_to_practice_runtime = True
    updated.gray_load_enabled = request.gray_load_enabled
    if updated.lawyer_approved_experience_package is None:
        updated.lawyer_approved_experience_package = {
            "source_training_package_id": updated.source_training_package_id,
            "approved_card_count": len(updated.experience_cards),
            "review_status": "approved_for_practice_load",
            "validation_status": "system_revalidated",
            "gray_load_enabled": updated.gray_load_enabled,
            "practice_runtime_load_status": "not_loaded",
            "metadata_only": True,
            "card_ids": [card.card_id for card in updated.experience_cards],
        }
    else:
        updated.lawyer_approved_experience_package["review_status"] = "approved_for_practice_load"
        updated.lawyer_approved_experience_package["gray_load_enabled"] = updated.gray_load_enabled
    updated.updated_at = datetime.now(UTC).isoformat()
    updated.audit_events.append(_audit_event(package_id, "approved_for_practice_load", request.reviewer_id, request.reviewer_note))
    _write_review_package(updated)
    return updated.model_dump()


def reject_practice_load_package(package_id: str, request: PracticeLoadReviewDecisionRequest) -> dict | None:
    package = _read_or_build_review_package(package_id)
    if package is None:
        return None
    updated = package.model_copy(deep=True)
    updated.review_status = "rejected_for_practice_load"
    updated.load_gate_status = "rejected_for_practice_load"
    updated.can_load_to_practice_runtime = False
    updated.updated_at = datetime.now(UTC).isoformat()
    updated.audit_events.append(_audit_event(package_id, "rejected_for_practice_load", request.reviewer_id, request.reviewer_note))
    _write_review_package(updated)
    return updated.model_dump()


def get_practice_load_package_audit(package_id: str) -> dict | None:
    package = _read_or_build_review_package(package_id)
    if package is None:
        return None
    return PracticeLoadReviewPackageAudit(
        package_id=package.package_id,
        events=package.audit_events,
        event_count=len(package.audit_events),
        warnings=["Practice load review audit contains metadata events only."],
        **v731f_safety_flags(),
    ).model_dump()


def get_practice_load_package_source_trace(package_id: str) -> dict | None:
    package = _read_or_build_review_package(package_id)
    return package.source_trace_bundle.model_dump() if package else None


def build_v731f_status() -> dict:
    packages = _all_review_packages()
    return V731fPracticeLoadPipelineStatus(
        package_count=len(packages),
        pending_practice_load_review_count=sum(
            1 for package in packages if package.review_status == "pending_practice_load_review"
        ),
        system_revalidated_count=sum(
            1 for package in packages if package.validation_status == "system_revalidated"
        ),
        approved_for_practice_load_count=sum(
            1 for package in packages if package.review_status == "approved_for_practice_load"
        ),
        rejected_for_practice_load_count=sum(
            1 for package in packages if package.review_status == "rejected_for_practice_load"
        ),
        warnings=[
            "v7.31f is the lawyer review gate before practice runtime loading.",
            "This stage approves metadata for future loading only; it does not load runtime packages.",
        ],
        **v731f_safety_flags(),
    ).model_dump()


def _read_or_build_review_package(package_id: str) -> PracticeLoadReviewPackage | None:
    existing = read_payload(PRACTICE_LOAD_REVIEW_PACKAGES_DIR, package_id)
    if existing:
        return PracticeLoadReviewPackage(**existing)
    source_payload = read_payload(TRAINING_PACKAGES_DIR, package_id)
    if not source_payload:
        return None
    source_package = ExperiencePackage(**source_payload)
    if source_package.package_status != "pending_practice_load_review":
        return None
    package = build_review_package(source_package)
    _write_review_package(package)
    return package


def _all_review_packages() -> list[PracticeLoadReviewPackage]:
    packages_by_id = {
        payload.get("package_id"): PracticeLoadReviewPackage(**payload)
        for payload in read_payloads(PRACTICE_LOAD_REVIEW_PACKAGES_DIR)
        if payload.get("package_id")
    }
    for payload in read_payloads(TRAINING_PACKAGES_DIR):
        source_package = ExperiencePackage(**payload)
        if source_package.package_status == "pending_practice_load_review" and source_package.package_id not in packages_by_id:
            packages_by_id[source_package.package_id] = build_review_package(source_package)
    return sorted(packages_by_id.values(), key=lambda item: item.updated_at, reverse=True)


def _write_review_package(package: PracticeLoadReviewPackage) -> None:
    write_payload(PRACTICE_LOAD_REVIEW_PACKAGES_DIR, package.package_id, package.model_dump())


def _revalidation_errors(package: PracticeLoadReviewPackage) -> list[str]:
    errors: list[str] = []
    if not package.generated_experience_package.get("generated_package_preserved", False):
        errors.append("generated_experience_package_not_preserved")
    if not package.experience_cards:
        errors.append("missing_experience_cards")
    if not package.source_trace_bundle.source_trace_ids:
        errors.append("missing_source_trace")
    if not package.audit_events:
        errors.append("missing_audit")
    if package.lawyer_approved_experience_package is None:
        errors.append("missing_lawyer_approved_experience_package")
    scan_target = package.model_dump()
    scan_text = str(scan_target).lower()
    for marker in FORBIDDEN_MARKERS:
        if marker in scan_text:
            errors.append(f"forbidden_marker_detected:{marker}")
    return errors


def _audit_event(package_id: str, action: str, reviewer_id: str | None = None, reviewer_note: str | None = None) -> PracticeLoadReviewAuditEvent:
    return PracticeLoadReviewAuditEvent(
        event_id=f"{package_id}_practice_load_audit_{action}_{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}",
        package_id=package_id,
        action=action,
        reviewer_id=reviewer_id,
        reviewer_note=reviewer_note,
        timestamp=datetime.now(UTC).isoformat(),
    )
