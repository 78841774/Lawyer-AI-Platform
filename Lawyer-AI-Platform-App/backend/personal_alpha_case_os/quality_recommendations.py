from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSQualityRecommendation,
    PersonalAlphaCaseOSQualityRecommendations,
)

ACTION_LABELS = {
    "create_workspace_run": ("critical", "Create Workspace Run"),
    "review_sources": ("high", "Review Sources"),
    "submit_source_review_decision": ("high", "Submit Source Review Decision"),
    "check_final_readiness": ("high", "Check Final Readiness"),
    "submit_final_gate_decision": ("high", "Submit Final Gate Decision"),
    "create_final_packet": ("high", "Create Final Packet"),
    "submit_lawyer_final_review": ("critical", "Complete Lawyer Final Review"),
    "create_final_lock": ("critical", "Create Final Lock"),
    "resolve_metadata_closure": ("critical", "Resolve Metadata Closure"),
    "create_metadata_export_package": ("medium", "Create Metadata Export Package"),
    "review_safety_boundary": ("critical", "Review Safety Boundary"),
    "review_audit_timeline": ("high", "Review Audit Timeline"),
    "review_redaction_check": ("critical", "Review Redaction Check"),
    "resolve_blockers": ("high", "Resolve Blockers"),
    "review_state_machine": ("medium", "Review State Machine"),
}


def build_quality_recommendations(case_id: str, findings_payload: dict[str, Any]) -> dict[str, Any]:
    recommendations: list[PersonalAlphaCaseOSQualityRecommendation] = []
    seen_actions: set[str] = set()
    for finding in findings_payload.get("findings", []):
        if not isinstance(finding, dict):
            continue
        action = str(finding.get("recommended_action", "review_quality_checklist"))
        if action in seen_actions:
            continue
        seen_actions.add(action)
        default_priority = str(finding.get("severity", "medium"))
        priority, label = ACTION_LABELS.get(action, (default_priority, _label_from_action(action)))
        recommendations.append(
            PersonalAlphaCaseOSQualityRecommendation(
                recommendation_id=f"quality_recommendation_{len(recommendations) + 1:03d}",
                priority=priority,
                action=action,
                label=label,
                target_route=str(finding.get("target_route", "/case-os")),
                reason=str(finding.get("description", "Review metadata-only quality finding.")),
                would_execute_action=False,
                mock_or_redacted_only=True,
                raw_content_included=False,
            )
        )
    return PersonalAlphaCaseOSQualityRecommendations(
        case_id=case_id,
        recommendations=recommendations,
        recommendation_count=len(recommendations),
        warnings=["Recommendations are advisory only and do not execute workflow actions."],
    ).model_dump()


def _label_from_action(action: str) -> str:
    return " ".join(part.capitalize() for part in action.split("_") if part) or "Review Quality Checklist"
