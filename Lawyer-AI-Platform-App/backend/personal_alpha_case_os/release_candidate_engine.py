from typing import Any

from personal_alpha_case_os.case_os_engine import (
    get_personal_alpha_case_os_export_package_status,
    get_personal_alpha_case_os_hardening_response_consistency,
    get_personal_alpha_case_os_hardening_runtime_storage_check,
    get_personal_alpha_case_os_hardening_safety_check,
    get_personal_alpha_case_os_metadata_closure,
    get_personal_alpha_case_os_quality_summary,
)
from personal_alpha_case_os.release_candidate_audit import build_release_candidate_audit
from personal_alpha_case_os.release_candidate_checklist import (
    build_release_candidate_checklist,
    release_candidate_summary_flags,
)
from personal_alpha_case_os.release_candidate_notes import build_release_notes_preview
from personal_alpha_case_os.safety_guard import safe_metadata_token, scan_scoped_payloads
from personal_alpha_case_os.safety_response import build_safe_not_found_response
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSReleaseCandidateAudit,
    PersonalAlphaCaseOSReleaseCandidateCaseReadiness,
    PersonalAlphaCaseOSReleaseCandidateChecklist,
    PersonalAlphaCaseOSReleaseCandidateReadiness,
    PersonalAlphaCaseOSReleaseCandidateStatus,
    PersonalAlphaCaseOSReleaseCandidateSummary,
    PersonalAlphaCaseOSReleaseCandidateUnsafeItem,
)

NEXT_MAJOR_VERSION = "v7.0 Personal Production Workspace Foundation"
NEXT_MAJOR_DIRECTION = "Controlled personal production delivery validation before external client delivery."


def get_release_candidate_status() -> dict[str, Any]:
    return PersonalAlphaCaseOSReleaseCandidateStatus(
        next_major_version=NEXT_MAJOR_VERSION,
        next_major_direction=NEXT_MAJOR_DIRECTION,
        warnings=[
            "v6.9 is a release candidate metadata review.",
            "No production provider is called.",
            "No legal opinion or final report is generated.",
            "Next stage is personal production validation, not external client delivery.",
        ],
    ).model_dump()


def get_release_candidate_summary() -> dict[str, Any]:
    summary = release_candidate_summary_flags()
    capability_keys = [
        "case_os_foundation",
        "stage_orchestration",
        "unified_audit_timeline",
        "review_state_machine",
        "final_lock_consolidation",
        "export_package",
        "quality_checklist",
        "regression_suite",
        "hardening_layer",
        "personal_production_next_step_defined",
    ]
    missing_capabilities = [key for key in capability_keys if not summary.get(key, False)]
    return PersonalAlphaCaseOSReleaseCandidateSummary(
        summary=summary,
        capability_count=len(capability_keys),
        ready_capability_count=len(capability_keys) - len(missing_capabilities),
        missing_capabilities=missing_capabilities,
        next_major_version=NEXT_MAJOR_VERSION,
        warnings=[] if not missing_capabilities else ["Release candidate has missing required metadata capabilities."],
    ).model_dump()


def get_release_candidate_checklist() -> dict[str, Any]:
    checklist = build_release_candidate_checklist()
    return PersonalAlphaCaseOSReleaseCandidateChecklist(
        checklist=checklist["checklist"],
        passed_count=int(checklist["passed_count"]),
        failed_count=int(checklist["failed_count"]),
        required_failed_count=int(checklist["required_failed_count"]),
        release_candidate_ready=bool(checklist["release_candidate_ready"]),
        warnings=[] if checklist["release_candidate_ready"] else ["Release candidate checklist has required failures."],
    ).model_dump()


def get_release_candidate_readiness() -> dict[str, Any]:
    checklist = get_release_candidate_checklist()
    summary = get_release_candidate_summary()
    required_failed_count = int(checklist.get("required_failed_count", 0) or 0)
    readiness = {
        "required_failed_count": required_failed_count,
        "critical_failed_count": required_failed_count,
        "regression_suite_available": _summary_flag(summary, "regression_suite"),
        "hardening_layer_available": _summary_flag(summary, "hardening_layer"),
        "docs_complete": _summary_flag(summary, "docs_available"),
        "changelogs_complete": _summary_flag(summary, "changelogs_available"),
        "safety_boundary_passed": required_failed_count == 0,
        "no_raw_content": True,
        "no_final_legal_opinion": True,
        "no_final_report": True,
        "no_production_provider": True,
        "personal_production_next_step_defined": _summary_flag(summary, "personal_production_next_step_defined"),
    }
    release_candidate_ready = (
        required_failed_count == 0
        and int(readiness["critical_failed_count"]) == 0
        and bool(readiness["regression_suite_available"])
        and bool(readiness["hardening_layer_available"])
        and bool(readiness["docs_complete"])
        and bool(readiness["changelogs_complete"])
        and bool(readiness["safety_boundary_passed"])
        and bool(readiness["no_raw_content"])
        and bool(readiness["no_final_legal_opinion"])
        and bool(readiness["no_final_report"])
        and bool(readiness["no_production_provider"])
        and bool(readiness["personal_production_next_step_defined"])
    )
    return PersonalAlphaCaseOSReleaseCandidateReadiness(
        release_candidate_ready=release_candidate_ready,
        readiness=readiness,
        next_action="prepare_v6_9_release" if release_candidate_ready else "resolve_release_candidate_blockers",
        next_major_version=NEXT_MAJOR_VERSION,
        warnings=[] if release_candidate_ready else ["Release candidate readiness has blockers."],
    ).model_dump()


def get_release_candidate_audit() -> dict[str, Any]:
    status = get_release_candidate_status()
    summary = get_release_candidate_summary()
    checklist = get_release_candidate_checklist()
    readiness = get_release_candidate_readiness()
    release_notes_preview = build_release_notes_preview()
    audit = build_release_candidate_audit(
        status=status,
        summary=summary,
        checklist=checklist,
        readiness=readiness,
        release_notes_preview=release_notes_preview,
    )
    unsafe_items = [
        PersonalAlphaCaseOSReleaseCandidateUnsafeItem(**item)
        for item in audit.pop("unsafe_items", [])
    ]
    return PersonalAlphaCaseOSReleaseCandidateAudit(
        audit=audit,
        unsafe_items=unsafe_items,
        warnings=[] if audit.get("passed") else ["Release candidate audit detected metadata issues."],
    ).model_dump()


def get_release_notes_preview() -> dict[str, Any]:
    return build_release_notes_preview()


def get_release_candidate_case_readiness(case_id: str) -> dict[str, Any]:
    safe_case_id = safe_metadata_token(case_id)
    if not safe_case_id:
        payload = build_safe_not_found_response(case_id="", resource_type="case", message="Case not found.")
        payload.update(
            PersonalAlphaCaseOSReleaseCandidateCaseReadiness(
                case_id="",
                release_candidate_case_ready=False,
                case_readiness=_empty_case_readiness(),
                next_action="resolve_blockers",
                warnings=payload.get("warnings", []),
            ).model_dump()
        )
        return payload

    quality_summary = get_personal_alpha_case_os_quality_summary(case_id)
    metadata_closure = get_personal_alpha_case_os_metadata_closure(case_id)
    export_package_status = get_personal_alpha_case_os_export_package_status(case_id)
    hardening_safety = get_personal_alpha_case_os_hardening_safety_check(case_id)
    response_consistency = get_personal_alpha_case_os_hardening_response_consistency(case_id)
    runtime_storage_check = get_personal_alpha_case_os_hardening_runtime_storage_check(case_id)
    scan = scan_scoped_payloads(
        {
            "quality_summary": quality_summary,
            "metadata_closure": metadata_closure,
            "export_package_status": export_package_status,
            "hardening_safety": hardening_safety,
            "response_consistency": response_consistency,
            "runtime_storage_check": runtime_storage_check,
        }
    )
    if not scan.get("passed", False):
        payload = build_safe_not_found_response(case_id=safe_case_id, resource_type="case", message="Case metadata is unavailable.")
        payload.update(
            PersonalAlphaCaseOSReleaseCandidateCaseReadiness(
                case_id=safe_case_id,
                release_candidate_case_ready=False,
                case_readiness=_empty_case_readiness(),
                next_action="resolve_blockers",
                warnings=payload.get("warnings", []),
            ).model_dump()
        )
        return payload

    quality = quality_summary.get("summary", {}) if isinstance(quality_summary.get("summary"), dict) else {}
    closure = metadata_closure.get("closure_summary", {}) if isinstance(metadata_closure.get("closure_summary"), dict) else {}
    package_summary = export_package_status.get("package_summary", {}) if isinstance(export_package_status.get("package_summary"), dict) else {}
    case_readiness = {
        "quality_summary_available": bool(quality_summary),
        "metadata_closure_ready": bool(closure.get("metadata_closure_ready", False)),
        "export_package_available": bool(package_summary.get("package_count", 0) or export_package_status.get("latest_package_id")),
        "hardening_safety_check_passed": bool(hardening_safety.get("safety_check", {}).get("passed", False)),
        "response_consistency_passed": bool(response_consistency.get("response_consistency", {}).get("passed", False)),
        "runtime_storage_check_passed": bool(runtime_storage_check.get("runtime_storage_check", {}).get("passed", False)),
        "ready_for_personal_alpha_review": bool(quality.get("ready_for_personal_alpha_review", False)),
    }
    release_candidate_case_ready = all(case_readiness.values())
    return PersonalAlphaCaseOSReleaseCandidateCaseReadiness(
        case_id=safe_case_id,
        release_candidate_case_ready=release_candidate_case_ready,
        case_readiness=case_readiness,
        next_action="prepare_personal_alpha_review" if release_candidate_case_ready else "resolve_quality_findings",
        warnings=[] if release_candidate_case_ready else ["Case remains in metadata-only release candidate review."],
    ).model_dump()


def _summary_flag(summary: dict[str, Any], field_name: str) -> bool:
    values = summary.get("summary", {})
    return bool(values.get(field_name, False)) if isinstance(values, dict) else False


def _empty_case_readiness() -> dict[str, bool]:
    return {
        "quality_summary_available": False,
        "metadata_closure_ready": False,
        "export_package_available": False,
        "hardening_safety_check_passed": False,
        "response_consistency_passed": False,
        "runtime_storage_check_passed": False,
        "ready_for_personal_alpha_review": False,
    }
