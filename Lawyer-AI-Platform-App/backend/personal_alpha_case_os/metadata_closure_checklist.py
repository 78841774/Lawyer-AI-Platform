from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSMetadataClosureChecklist,
    PersonalAlphaCaseOSMetadataClosureChecklistItem,
    PersonalAlphaCaseOSMetadataClosureSummary,
)


CHECK_DEFINITIONS = [
    ("workspace_run_ready", "Workspace Run Ready", "case_os_stage_orchestration"),
    ("source_review_completed", "Source Review Completed", "case_os_stage_orchestration"),
    ("source_decision_completed", "Source Decision Completed", "personal_alpha_source_review"),
    ("final_readiness_ready", "Final Readiness Ready", "personal_alpha_final_readiness"),
    ("final_gate_approved", "Final Gate Approved", "personal_alpha_final_gate"),
    ("final_packet_created", "Final Packet Created", "personal_alpha_final_packet"),
    ("lawyer_review_approved", "Lawyer Review Approved", "personal_alpha_lawyer_final_review"),
    ("final_lock_created", "Final Lock Created", "personal_alpha_final_lock"),
    ("audit_timeline_available", "Audit Timeline Available", "case_os_unified_audit_timeline"),
    ("redaction_check_passed", "Redaction Check Passed", "case_os_redaction_check"),
    ("no_raw_material_text", "No Raw Material Text", "safety_checklist"),
    ("no_raw_ocr_text", "No Raw OCR Text", "safety_checklist"),
    ("no_raw_legal_search_results", "No Raw Legal Search Results", "safety_checklist"),
    ("no_final_legal_opinion_generated", "No Final Legal Opinion Generated", "safety_checklist"),
    ("no_final_report_generated", "No Final Report Generated", "safety_checklist"),
    ("no_auto_skill_publish", "No Auto Skill Publish", "safety_checklist"),
    ("no_auto_workspace_runtime", "No Auto Workspace Runtime", "safety_checklist"),
]


def build_metadata_closure_summary(
    context: dict[str, Any],
    audit_summary: dict[str, Any],
    redaction_check: dict[str, Any],
) -> PersonalAlphaCaseOSMetadataClosureSummary:
    latest_lawyer_action = str(context.get("latest_lawyer_action") or "")
    audit_stats = audit_summary.get("summary", {}) if isinstance(audit_summary.get("summary", {}), dict) else {}
    redaction_stats = redaction_check.get("redaction_check", {}) if isinstance(redaction_check.get("redaction_check", {}), dict) else {}
    return PersonalAlphaCaseOSMetadataClosureSummary(
        workspace_run_ready=bool(context.get("latest_workspace_run_id")),
        source_review_completed=bool(context.get("latest_workspace_run_id")),
        source_decision_completed=bool(context.get("source_decisions", [])),
        final_readiness_ready=bool(context.get("source_decisions", [])),
        final_gate_approved=bool(context.get("gate_decisions", [])),
        final_packet_created=bool(context.get("latest_packet_id")),
        lawyer_review_approved=latest_lawyer_action == "approve_packet",
        final_lock_created=bool(context.get("latest_lock_id")),
        audit_timeline_available=int(audit_stats.get("total_events", 0) or 0) > 0,
        redaction_check_passed=bool(redaction_stats.get("passed", False)),
    )


def build_metadata_closure_checklist(
    case_id: str,
    context: dict[str, Any],
    audit_summary: dict[str, Any],
    redaction_check: dict[str, Any],
) -> dict[str, Any]:
    summary = build_metadata_closure_summary(context, audit_summary, redaction_check)
    summary_values = summary.model_dump()
    safety_values = _safety_values()
    checklist = []
    for check_id, label, source in CHECK_DEFINITIONS:
        passed = bool(summary_values.get(check_id, safety_values.get(check_id, False)))
        checklist.append(
            PersonalAlphaCaseOSMetadataClosureChecklistItem(
                check_id=check_id,
                label=label,
                passed=passed,
                required=True,
                source=source,
                mock_or_redacted_only=True,
            )
        )
    failed = [item for item in checklist if not item.passed]
    return PersonalAlphaCaseOSMetadataClosureChecklist(
        case_id=case_id,
        checklist=checklist,
        passed_count=len(checklist) - len(failed),
        failed_count=len(failed),
        required_failed_count=sum(1 for item in failed if item.required),
        closure_ready=not any(item.required and not item.passed for item in checklist),
        mock_or_redacted_only=True,
        raw_content_included=False,
        warnings=["Metadata closure checklist is derived from metadata only."],
    ).model_dump()


def _safety_values() -> dict[str, bool]:
    return {
        "no_raw_material_text": True,
        "no_raw_ocr_text": True,
        "no_raw_legal_search_results": True,
        "no_final_legal_opinion_generated": True,
        "no_final_report_generated": True,
        "no_auto_skill_publish": True,
        "no_auto_workspace_runtime": True,
    }
