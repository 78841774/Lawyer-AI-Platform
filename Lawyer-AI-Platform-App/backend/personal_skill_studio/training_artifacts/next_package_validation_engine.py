from personal_skill_studio.training_artifacts.next_package_safety_engine import (
    next_package_metadata_safe,
    v731j_safety_flags,
)
from personal_skill_studio.training_artifacts.schemas import NextPackageValidationResult, PracticeFeedbackCandidatePack


def validate_next_package_metadata(next_package_id: str, candidate_pack: PracticeFeedbackCandidatePack) -> NextPackageValidationResult:
    errors: list[str] = []
    if candidate_pack.candidate_status != "ready_for_next_experience_build":
        errors.append("candidate_pack_not_ready")
    if not candidate_pack.source_trace_id:
        errors.append("missing_candidate_pack_source_trace")
    if not candidate_pack.audit_events:
        errors.append("missing_candidate_pack_audit")
    if not next_package_metadata_safe(candidate_pack.model_dump()):
        errors.append("sensitive_marker_detected")
    passed = not errors
    return NextPackageValidationResult(
        validation_id=f"{next_package_id}_validation",
        next_package_id=next_package_id,
        validation_status="metadata_validated" if passed else "blocked",
        ready_for_practice_load_review=passed,
        candidate_pack_ready=candidate_pack.candidate_status == "ready_for_next_experience_build",
        source_trace_complete=bool(candidate_pack.source_trace_id),
        audit_complete=bool(candidate_pack.audit_events),
        sensitive_scan_passed=next_package_metadata_safe(candidate_pack.model_dump()),
        loaded_package_preserved=True,
        validation_errors=errors,
        warnings=["Validation scans draft metadata only and does not load runtime packages."],
        **v731j_safety_flags(),
    )
