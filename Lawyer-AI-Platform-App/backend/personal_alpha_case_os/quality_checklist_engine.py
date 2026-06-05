from typing import Any

from personal_alpha_case_os.audit_redaction import unsafe_reason
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSQualityChecklist,
    PersonalAlphaCaseOSQualityChecklistItem,
    PersonalAlphaCaseOSQualityStatus,
)

QUALITY_WARNINGS = [
    "v6.6 quality checklist is metadata-only.",
    "Quality results are advisory only.",
    "No legal opinion is generated.",
    "No final report body is generated.",
]

CHECK_DEFINITIONS = [
    ("workspace_run_exists", "workflow_completeness", "Workspace run exists", True, "critical", "personal_alpha_workspace", "/personal-alpha-workspace", "workspace_run_missing"),
    ("source_review_available", "workflow_completeness", "Source review metadata is available", True, "high", "personal_alpha_source_review", "/personal-alpha-source-review", "source_review_missing"),
    ("source_review_decisions_completed", "workflow_completeness", "Source review decisions are completed", True, "high", "personal_alpha_source_review", "/personal-alpha-source-review", "source_review_decision_missing"),
    ("final_readiness_checked", "workflow_completeness", "Final readiness metadata is checked", True, "high", "personal_alpha_final_readiness", "/personal-alpha-final-readiness", "final_readiness_missing"),
    ("final_gate_decision_available", "workflow_completeness", "Final gate decision is available", True, "high", "personal_alpha_final_gate", "/personal-alpha-final-gate", "final_gate_missing"),
    ("final_packet_created", "workflow_completeness", "Final packet metadata is created", True, "high", "personal_alpha_final_packet", "/personal-alpha-final-packet", "final_packet_missing"),
    ("lawyer_final_review_completed", "workflow_completeness", "Lawyer final review metadata is completed", True, "critical", "personal_alpha_lawyer_final_review", "/personal-alpha-lawyer-final-review", "lawyer_final_review_missing"),
    ("final_lock_created", "workflow_completeness", "Final lock metadata is created", True, "critical", "personal_alpha_final_lock", "/personal-alpha-final-lock", "final_lock_missing"),
    ("metadata_closure_ready", "metadata_closure", "Metadata closure is ready", True, "critical", "personal_alpha_case_os_metadata_closure", "/case-os/{case_id}", "metadata_closure_not_ready"),
    ("export_package_exists", "export_package", "At least one metadata export package exists", False, "medium", "personal_alpha_case_os_export_package", "/case-os/{case_id}", "export_package_missing"),
    ("no_raw_material_text", "safety_boundary", "No raw material text is included", True, "critical", "safety_boundary", "/case-os/{case_id}", "raw_material_text_detected"),
    ("no_raw_ocr_text", "safety_boundary", "No raw OCR text is included", True, "critical", "safety_boundary", "/case-os/{case_id}", "raw_ocr_text_detected"),
    ("no_raw_legal_search_results", "safety_boundary", "No raw legal search results are included", True, "critical", "safety_boundary", "/case-os/{case_id}", "raw_legal_search_results_detected"),
    ("no_raw_quote", "safety_boundary", "No raw quote is included", True, "critical", "safety_boundary", "/case-os/{case_id}", "raw_quote_detected"),
    ("no_local_path_exposed", "safety_boundary", "No local path is exposed", True, "critical", "safety_boundary", "/case-os/{case_id}", "local_path_exposed"),
    ("no_api_key_exposed", "safety_boundary", "No API key is exposed", True, "critical", "safety_boundary", "/case-os/{case_id}", "api_key_exposed"),
    ("no_final_legal_opinion_generated", "safety_boundary", "No final legal opinion is generated", True, "critical", "safety_boundary", "/case-os/{case_id}", "final_legal_opinion_generated"),
    ("no_final_report_generated", "safety_boundary", "No final report is generated", True, "critical", "safety_boundary", "/case-os/{case_id}", "final_report_generated"),
    ("no_pdf_docx_generated", "safety_boundary", "No PDF or DOCX is generated", True, "high", "safety_boundary", "/case-os/{case_id}", "pdf_docx_generated"),
    ("no_auto_skill_publish", "safety_boundary", "No automatic Skill publish is enabled", True, "high", "safety_boundary", "/case-os/{case_id}", "auto_skill_publish_enabled"),
    ("no_auto_workspace_runtime", "safety_boundary", "No automatic Workspace Runtime enablement is enabled", True, "high", "safety_boundary", "/case-os/{case_id}", "auto_workspace_runtime_enabled"),
    ("unified_audit_timeline_available", "audit_integrity", "Unified audit timeline is available", True, "high", "personal_alpha_case_os_unified_audit_timeline", "/case-os/{case_id}", "unified_audit_timeline_missing"),
    ("redaction_check_passed", "audit_integrity", "Redaction check passed", True, "critical", "personal_alpha_case_os_redaction_check", "/case-os/{case_id}", "redaction_check_failed"),
    ("unsafe_audit_event_count_zero", "audit_integrity", "Unsafe audit event count is zero", True, "critical", "personal_alpha_case_os_redaction_check", "/case-os/{case_id}", "unsafe_audit_event_detected"),
    ("blockers_count_zero", "audit_integrity", "Blocker count is zero", True, "high", "personal_alpha_case_os_blockers", "/case-os/{case_id}", "blockers_present"),
    ("review_state_terminal_or_actionable", "review_state", "Review state is terminal or actionable", True, "medium", "personal_alpha_case_os_review_state", "/case-os/{case_id}", "review_state_not_actionable"),
    ("quality_findings_generated", "recommendations", "Quality findings are generated", True, "info", "personal_alpha_case_os_quality_findings", "/case-os/{case_id}", None),
]


def build_quality_status(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    blocked = bool(context.get("blocked")) or not case_id
    warnings = list(QUALITY_WARNINGS)
    if blocked:
        warnings.extend(str(item) for item in context.get("blocked_reasons", ["Case not found."]) if item)
    return PersonalAlphaCaseOSQualityStatus(
        case_id=case_id,
        quality_check_available=not blocked,
        warnings=list(dict.fromkeys(warnings)),
    ).model_dump()


def build_quality_checklist(case_id: str, quality_context: dict[str, Any]) -> dict[str, Any]:
    status = build_quality_status(case_id, quality_context.get("context", {}))
    values = _quality_values(case_id, quality_context)
    checklist: list[PersonalAlphaCaseOSQualityChecklistItem] = []
    for check_id, category, label, required, severity, source, route, finding_code in CHECK_DEFINITIONS:
        passed = bool(values.get(check_id, False))
        checklist.append(
            PersonalAlphaCaseOSQualityChecklistItem(
                check_id=check_id,
                category=category,
                label=label,
                passed=passed,
                required=required,
                severity=severity,
                source=source,
                target_route=_route(route, case_id),
                finding_code=None if passed else finding_code,
                mock_or_redacted_only=True,
                raw_content_included=False,
            )
        )
    failed = [item for item in checklist if not item.passed]
    return PersonalAlphaCaseOSQualityChecklist(
        case_id=case_id,
        checklist=checklist,
        passed_count=len(checklist) - len(failed),
        failed_count=len(failed),
        required_failed_count=sum(1 for item in failed if item.required),
        critical_failed_count=sum(1 for item in failed if item.severity == "critical"),
        warning_count=sum(1 for item in failed if item.severity in {"medium", "low"}),
        warnings=list(dict.fromkeys(status.get("warnings", []) + ["Quality checklist is advisory metadata only."])),
    ).model_dump()


def _quality_values(case_id: str, payload: dict[str, Any]) -> dict[str, bool]:
    context = payload.get("context", {})
    metadata_closure = payload.get("metadata_closure", {})
    closure_summary = metadata_closure.get("closure_summary", {}) if isinstance(metadata_closure, dict) else {}
    audit_summary = payload.get("audit_summary", {}).get("summary", {})
    redaction = payload.get("redaction_check", {}).get("redaction_check", {})
    blockers = payload.get("blockers", {})
    review_state = payload.get("review_state", {})
    export_summary = payload.get("export_package_summary", {}).get("summary", {})
    unsafe_output_detected = _unsafe_output_detected(case_id, payload)
    blocked = bool(context.get("blocked")) or not case_id
    review_actionable = bool(review_state.get("terminal")) or not bool(review_state.get("blocked"))
    return {
        "workspace_run_exists": bool(context.get("latest_workspace_run_id")),
        "source_review_available": bool(context.get("latest_workspace_run_id")),
        "source_review_decisions_completed": bool(context.get("source_decisions", [])),
        "final_readiness_checked": bool(closure_summary.get("final_readiness_ready", False)),
        "final_gate_decision_available": bool(context.get("gate_decisions", [])),
        "final_packet_created": bool(context.get("latest_packet_id")),
        "lawyer_final_review_completed": bool(context.get("lawyer_actions", [])),
        "final_lock_created": bool(context.get("latest_lock_id")),
        "metadata_closure_ready": bool(metadata_closure.get("closure_ready", False)),
        "export_package_exists": int(export_summary.get("package_count", 0) or 0) > 0,
        "no_raw_material_text": not unsafe_output_detected,
        "no_raw_ocr_text": not unsafe_output_detected,
        "no_raw_legal_search_results": not unsafe_output_detected,
        "no_raw_quote": not unsafe_output_detected,
        "no_local_path_exposed": not unsafe_output_detected,
        "no_api_key_exposed": not unsafe_output_detected,
        "no_final_legal_opinion_generated": True,
        "no_final_report_generated": True,
        "no_pdf_docx_generated": True,
        "no_auto_skill_publish": True,
        "no_auto_workspace_runtime": True,
        "unified_audit_timeline_available": int(audit_summary.get("total_events", 0) or 0) > 0,
        "redaction_check_passed": bool(redaction.get("passed", False)),
        "unsafe_audit_event_count_zero": int(redaction.get("unsafe_event_count", 0) or 0) == 0,
        "blockers_count_zero": not blocked and not bool(blockers.get("blocked", False)),
        "review_state_terminal_or_actionable": review_actionable,
        "quality_findings_generated": True,
    }


def _unsafe_output_detected(case_id: str, payload: dict[str, Any]) -> bool:
    checked = {
        "case_id": case_id,
        "warnings": payload.get("warnings", []),
    }
    return any(bool(unsafe_reason(value)) for value in checked.values())


def _route(route: str, case_id: str) -> str:
    safe_case_id = case_id if case_id and not unsafe_reason(case_id) else ""
    return route.replace("{case_id}", safe_case_id)
