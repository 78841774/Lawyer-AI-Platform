from personal_skill_studio.training_artifacts.practice_load_review_gate import FORBIDDEN_MARKERS
from personal_skill_studio.training_artifacts.schemas import PracticeLoadReviewPackage, PracticeRuntimeSafetyReport


def v731g_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "local_private_processing_only": True,
        "lawyer_approved_package_only": True,
        "metadata_safe": True,
        "redacted_abstracted_experience_only": True,
        "source_trace_required": True,
        "audit_required": True,
        "runtime_monitoring_required": True,
        "rollback_available": True,
        "controlled_runtime_loading_only": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "unreviewed_package_loaded": False,
        "system_revalidation_failed_package_loaded": False,
        "generated_only_package_loaded": False,
        "unredacted_content_loaded": False,
        "automatic_training_triggered": False,
        "formal_training_set_written": False,
        "skill_updated": False,
        "skill_published": False,
        "feedback_auto_mutates_loaded_package": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def build_runtime_safety_report(runtime_load_id: str, package: PracticeLoadReviewPackage) -> PracticeRuntimeSafetyReport:
    blocked_reasons = validate_runtime_load_candidate(package)
    return PracticeRuntimeSafetyReport(
        safety_report_id=f"{runtime_load_id}_safety_report",
        runtime_load_id=runtime_load_id,
        load_allowed=not blocked_reasons,
        safety_status="passed" if not blocked_reasons else "blocked",
        approval_status_valid=package.review_status == "approved_for_practice_load" and package.can_load_to_practice_runtime,
        lawyer_approved_package_exists=bool(package.lawyer_approved_experience_package),
        system_revalidated=package.validation_status == "system_revalidated"
        and bool(package.revalidation_result and package.revalidation_result.revalidation_passed),
        source_trace_exists=bool(package.source_trace_bundle.source_trace_ids),
        audit_exists=bool(package.audit_events),
        sensitive_scan_passed=bool(
            package.revalidation_result and package.revalidation_result.sensitive_field_scan_passed
        ),
        generated_package_preserved=bool(
            package.revalidation_result and package.revalidation_result.generated_package_preserved
        ),
        blocked_reasons=blocked_reasons,
        warnings=[
            "Runtime loading validates lawyer-approved metadata only.",
            "No provider call, source content return, final legal opinion, or external delivery is triggered.",
        ],
        **v731g_safety_flags(),
    )


def validate_runtime_load_candidate(package: PracticeLoadReviewPackage) -> list[str]:
    blocked_reasons: list[str] = []
    if package.review_status != "approved_for_practice_load" or not package.can_load_to_practice_runtime:
        blocked_reasons.append("package_not_approved_for_practice_load")
    if not package.lawyer_approved_experience_package:
        blocked_reasons.append("missing_lawyer_approved_package")
    if package.validation_status != "system_revalidated":
        blocked_reasons.append("package_not_system_revalidated")
    if not package.revalidation_result or not package.revalidation_result.revalidation_passed:
        blocked_reasons.append("missing_passed_revalidation_result")
    if not package.source_trace_bundle.source_trace_ids:
        blocked_reasons.append("missing_source_trace")
    if not package.audit_events:
        blocked_reasons.append("missing_audit")
    if package.revalidation_result and not package.revalidation_result.sensitive_field_scan_passed:
        blocked_reasons.append("sensitive_scan_not_passed")
    if package.revalidation_result and not package.revalidation_result.generated_package_preserved:
        blocked_reasons.append("generated_package_not_preserved")
    if _contains_forbidden_marker(package):
        blocked_reasons.append("forbidden_metadata_marker_detected")
    return blocked_reasons


def _contains_forbidden_marker(package: PracticeLoadReviewPackage) -> bool:
    scan_text = str(package.model_dump()).lower()
    return any(marker in scan_text for marker in FORBIDDEN_MARKERS)
