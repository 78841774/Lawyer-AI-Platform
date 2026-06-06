import json
from datetime import UTC, datetime

from personal_skill_studio.training_artifacts.schemas import (
    SkillPackage,
    SkillPackageValidationResult,
)
from personal_skill_studio.training_artifacts.skill_package_audit_engine import build_audit_event
from personal_skill_studio.training_artifacts.skill_package_safety_engine import v731d_safety_flags
from personal_skill_studio.training_artifacts.storage import SKILL_EXPERIENCE_POOL_DIR, read_payload


FORBIDDEN_TERMS = [
    "raw_text",
    "ocr_text",
    "original_text",
    "full_document_text",
    "local_path",
    "file_path",
    "absolute_path",
    "api_key",
    "secret",
    "provider_response",
    "private_key",
    "access_token",
    "refresh_token",
]


def validate_package(package: SkillPackage) -> SkillPackage:
    package.pre_publish_gate_status = "system_validating"
    package.package_status = "system_validating"
    validation = _build_validation_result(package)
    package.validation_result = validation
    package.pre_publish_gate_status = validation.pre_publish_gate_status
    package.package_status = validation.package_status
    package.updated_at = datetime.now(UTC).isoformat()
    package.audit_events.append(build_audit_event(package.package_id, "system_validation_gate"))
    return package


def _build_validation_result(package: SkillPackage) -> SkillPackageValidationResult:
    errors: list[str] = []
    experiences = [read_payload(SKILL_EXPERIENCE_POOL_DIR, experience_id) for experience_id in package.experience_ids]
    experiences = [experience for experience in experiences if experience]

    all_experiences_redacted = all(experience.get("redacted_output_only") is True for experience in experiences)
    all_experiences_approved = (
        len(experiences) == len(package.experience_ids)
        and all(experience.get("reviewer_confirmation") == "approved_for_skill_experience" for experience in experiences)
    )
    all_source_traces_present = bool(package.source_trace_bundle.source_trace_ids) and all(
        bool(experience.get("source_trace_id")) for experience in experiences
    )
    audit_complete = bool(package.audit_events) and bool(package.audit_bundle_id)
    draft_structure_confirmed = bool(package.source_draft_id) and package.manifest.section_count > 0
    manifest_generated = package.manifest.manifest_status == "generated"
    sensitive_field_scan_passed = not _contains_forbidden_terms(package)
    package_status_valid = package.package_status in {"draft_package", "system_validating"}

    checks = {
        "all_experiences_redacted": all_experiences_redacted,
        "all_experiences_approved": all_experiences_approved,
        "all_source_traces_present": all_source_traces_present,
        "audit_complete": audit_complete,
        "draft_structure_confirmed": draft_structure_confirmed,
        "manifest_generated": manifest_generated,
        "sensitive_field_scan_passed": sensitive_field_scan_passed,
        "package_status_valid": package_status_valid,
    }
    for field, passed in checks.items():
        if not passed:
            errors.append(field)

    gate_passed = not errors
    return SkillPackageValidationResult(
        package_id=package.package_id,
        pre_publish_gate_status="system_validated" if gate_passed else "validation_failed",
        package_status="ready_for_training_package_build" if gate_passed else "validation_failed",
        gate_passed=gate_passed,
        ready_for_training_package_build=gate_passed,
        validation_errors=errors,
        warnings=["System validation gate does not perform manual review or publish a Skill."],
        **checks,
        **v731d_safety_flags(),
    )


def _contains_forbidden_terms(package: SkillPackage) -> bool:
    payload = json.dumps(package.model_dump(mode="json"), ensure_ascii=False).lower()
    return any(term in payload for term in FORBIDDEN_TERMS)
