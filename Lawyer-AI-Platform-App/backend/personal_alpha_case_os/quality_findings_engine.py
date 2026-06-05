from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSQualityFinding,
    PersonalAlphaCaseOSQualityFindings,
)

FINDING_COPY = {
    "workspace_run_missing": ("Workspace run metadata is missing", "Create or review the local workspace run metadata before continuing.", "create_workspace_run"),
    "source_review_missing": ("Source review metadata is missing", "Review source metadata before downstream readiness checks.", "review_sources"),
    "source_review_decision_missing": ("Source review decision metadata is missing", "Complete the source review decision metadata.", "submit_source_review_decision"),
    "final_readiness_missing": ("Final readiness metadata is missing", "Run the metadata-only final readiness check.", "check_final_readiness"),
    "final_gate_missing": ("Final gate decision metadata is missing", "Submit the controlled final gate decision metadata.", "submit_final_gate_decision"),
    "final_packet_missing": ("Final packet metadata is missing", "Create the final packet metadata after gate approval.", "create_final_packet"),
    "lawyer_final_review_missing": ("Lawyer final review metadata is missing", "Complete lawyer final review metadata before final lock.", "submit_lawyer_final_review"),
    "final_lock_missing": ("Final lock metadata is missing", "Create final lock metadata after lawyer approval.", "create_final_lock"),
    "metadata_closure_not_ready": ("Metadata closure is not ready", "Resolve required metadata closure checks before review portability.", "resolve_metadata_closure"),
    "export_package_missing": ("Metadata export package is missing", "Create a metadata-only export package after metadata closure is ready.", "create_metadata_export_package"),
    "raw_material_text_detected": ("Raw material text risk detected", "Review metadata-only safety guards before exposing quality results.", "review_safety_boundary"),
    "raw_ocr_text_detected": ("Raw OCR text risk detected", "Review metadata-only safety guards before exposing quality results.", "review_safety_boundary"),
    "raw_legal_search_results_detected": ("Raw legal search result risk detected", "Review metadata-only safety guards before exposing quality results.", "review_safety_boundary"),
    "raw_quote_detected": ("Raw quote risk detected", "Remove raw quotes from metadata-only quality surfaces.", "review_safety_boundary"),
    "local_path_exposed": ("Local path exposure risk detected", "Redact path-like values before showing quality metadata.", "review_safety_boundary"),
    "api_key_exposed": ("API key exposure risk detected", "Redact key-like values before showing quality metadata.", "review_safety_boundary"),
    "final_legal_opinion_generated": ("Final legal opinion generation risk detected", "Disable final legal opinion generation for v6.6 quality checks.", "review_safety_boundary"),
    "final_report_generated": ("Final report generation risk detected", "Disable final report generation for v6.6 quality checks.", "review_safety_boundary"),
    "pdf_docx_generated": ("PDF or DOCX generation risk detected", "Keep quality report preview as metadata-only and fileless.", "review_safety_boundary"),
    "auto_skill_publish_enabled": ("Automatic Skill publish risk detected", "Keep Skill publishing disabled for v6.6.", "review_safety_boundary"),
    "auto_workspace_runtime_enabled": ("Automatic Workspace Runtime enablement risk detected", "Keep Workspace Runtime enablement disabled for v6.6.", "review_safety_boundary"),
    "unified_audit_timeline_missing": ("Unified audit timeline is missing", "Review audit metadata before quality scoring.", "review_audit_timeline"),
    "redaction_check_failed": ("Redaction check failed", "Resolve redaction check issues before treating quality results as ready.", "review_redaction_check"),
    "unsafe_audit_event_detected": ("Unsafe audit event metadata detected", "Review redacted audit metadata and keep raw content out of quality surfaces.", "review_redaction_check"),
    "blockers_present": ("Workflow blockers are present", "Resolve workflow blockers before personal alpha review.", "resolve_blockers"),
    "review_state_not_actionable": ("Review state is not actionable", "Move review metadata to a terminal or actionable state.", "review_state_machine"),
}


def build_quality_findings(case_id: str, checklist_payload: dict[str, Any]) -> dict[str, Any]:
    findings: list[PersonalAlphaCaseOSQualityFinding] = []
    for item in checklist_payload.get("checklist", []):
        if not isinstance(item, dict) or item.get("passed", False) or not item.get("finding_code"):
            continue
        finding_code = str(item.get("finding_code", "quality_check_failed"))
        title, description, action = FINDING_COPY.get(
            finding_code,
            ("Quality check failed", "Review the failed metadata-only quality check.", "review_quality_checklist"),
        )
        severity = str(item.get("severity", "medium"))
        findings.append(
            PersonalAlphaCaseOSQualityFinding(
                finding_id=f"quality_finding_{len(findings) + 1:03d}",
                finding_code=finding_code,
                category=str(item.get("category", "workflow_completeness")),
                severity=severity,
                title=title,
                description=description,
                blocking=bool(item.get("required", True)) and severity in {"critical", "high"},
                target_route=str(item.get("target_route", "/case-os")),
                recommended_action=action,
                mock_or_redacted_only=True,
                raw_content_included=False,
            )
        )
    return PersonalAlphaCaseOSQualityFindings(
        case_id=case_id,
        findings=findings,
        finding_count=len(findings),
        blocking_finding_count=sum(1 for item in findings if item.blocking),
        critical_finding_count=sum(1 for item in findings if item.severity == "critical"),
        high_finding_count=sum(1 for item in findings if item.severity == "high"),
        medium_finding_count=sum(1 for item in findings if item.severity == "medium"),
        low_finding_count=sum(1 for item in findings if item.severity == "low"),
        warnings=["Quality findings are metadata-only and do not include raw source content."],
    ).model_dump()
