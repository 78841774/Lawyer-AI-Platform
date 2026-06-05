from typing import Any

from personal_alpha_workspace.schemas import utc_now

VERSION_TRACE = [
    "v5_0_personal_alpha_workspace",
    "v5_1_personal_alpha_dashboard",
    "v5_2_personal_alpha_run_detail",
    "v5_3_personal_alpha_source_review",
    "v5_4_personal_alpha_source_review_decision",
    "v5_5_personal_alpha_final_readiness",
    "v5_6_personal_alpha_final_gate",
    "v5_7_personal_alpha_final_packet",
    "v5_8_personal_alpha_lawyer_final_review",
    "v5_9_personal_alpha_final_lock",
    "v6_0_personal_alpha_case_os",
    "v6_1_personal_alpha_case_os_stage_orchestrator",
    "v6_2_personal_alpha_case_os_unified_audit_timeline",
    "v6_3_personal_alpha_case_os_review_state_machine",
    "v6_4_personal_alpha_case_os_final_lock_consolidation",
    "v6_5_personal_alpha_case_os_export_package",
]


def build_export_package_content(
    *,
    package_id: str,
    case_id: str,
    package_format: str,
    reviewer_id: str,
    context: dict[str, Any],
    review_state: dict[str, Any],
    review_state_summary: dict[str, Any],
    final_lock_consolidation: dict[str, Any],
    metadata_closure: dict[str, Any],
    metadata_closure_checklist: dict[str, Any],
    audit_summary: dict[str, Any],
    redaction_check: dict[str, Any],
    created_at: str | None = None,
) -> dict[str, Any] | str:
    created = created_at or utc_now()
    sections = _sections(
        package_id,
        case_id,
        package_format,
        reviewer_id,
        context,
        review_state,
        review_state_summary,
        final_lock_consolidation,
        metadata_closure,
        metadata_closure_checklist,
        audit_summary,
        redaction_check,
        created,
    )
    if package_format == "markdown":
        return _render_markdown(package_id, case_id, sections, created)
    return {
        "package_id": package_id,
        "case_id": case_id,
        "package_type": "personal_alpha_case_os_metadata_export",
        "format": "json",
        "version": "v6_5",
        "metadata_only": True,
        "raw_content_included": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "sections": sections,
        "warnings": [
            "This is a metadata-only export package.",
            "No raw content is included.",
        ],
        "created_at": created,
    }


def _sections(
    package_id: str,
    case_id: str,
    package_format: str,
    reviewer_id: str,
    context: dict[str, Any],
    review_state: dict[str, Any],
    review_state_summary: dict[str, Any],
    final_lock_consolidation: dict[str, Any],
    metadata_closure: dict[str, Any],
    metadata_closure_checklist: dict[str, Any],
    audit_summary: dict[str, Any],
    redaction_check: dict[str, Any],
    created_at: str,
) -> dict[str, Any]:
    return {
        "package_header": {
            "package_id": package_id,
            "case_id": case_id,
            "format": package_format,
            "reviewer_id": reviewer_id,
            "created_at": created_at,
            "metadata_only": True,
            "raw_content_included": False,
        },
        "case_profile_metadata": {
            "case_id": case_id,
            "case_type": "personal_alpha_mock_or_redacted",
            "mock_or_redacted_only": True,
        },
        "stage_summary": {
            "workspace_run_ready": bool(context.get("latest_workspace_run_id")),
            "source_decision_count": len(context.get("source_decisions", [])),
            "final_gate_decision_count": len(context.get("gate_decisions", [])),
            "final_packet_created": bool(context.get("latest_packet_id")),
            "lawyer_review_action": context.get("latest_lawyer_action") or None,
            "final_lock_created": bool(context.get("latest_lock_id")),
            "raw_content_included": False,
        },
        "review_state_summary": {
            "review_state": review_state.get("review_state"),
            "completed_metadata_review": review_state.get("completed_metadata_review"),
            "terminal": review_state.get("terminal"),
            "summary": _without_keys(review_state_summary.get("summary", {}), ["target_route"]),
            "raw_content_included": False,
        },
        "final_lock_consolidation": _trim_payload(
            final_lock_consolidation,
            [
                "consolidation_status",
                "final_lock_created",
                "review_state",
                "completed_metadata_review",
                "final_lock_summary",
                "linked_metadata",
            ],
        ),
        "metadata_closure_summary": _trim_payload(
            metadata_closure,
            [
                "closure_status",
                "completed_metadata_review",
                "closure_ready",
                "review_state",
                "terminal",
                "blocked",
                "closure_summary",
                "next_action",
            ],
        ),
        "metadata_closure_checklist": metadata_closure_checklist.get("checklist", []),
        "audit_summary": audit_summary.get("summary", {}),
        "redaction_check_summary": _safe_redaction_summary(redaction_check.get("redaction_check", {})),
        "safety_checklist": {
            "local_only": True,
            "mock_first": True,
            "controlled_first": True,
            "metadata_only": True,
            "redacted_only": True,
            "advisory_only": True,
            "manual_review_required": True,
            "lawyer_review_required": True,
            "raw_content_included": False,
            "final_legal_opinion_generated": False,
            "final_report_generated": False,
            "auto_skill_publish_enabled": False,
            "auto_workspace_runtime_enabled": False,
        },
        "version_trace": VERSION_TRACE,
    }


def _render_markdown(package_id: str, case_id: str, sections: dict[str, Any], created_at: str) -> str:
    closure = sections["metadata_closure_summary"]
    audit = sections["audit_summary"]
    redaction = sections["redaction_check_summary"]
    checklist = sections["metadata_closure_checklist"]
    lines = [
        "# Personal Alpha Case OS Metadata Export Package",
        "",
        "## Safety Notice",
        "- Metadata-only",
        "- No raw content",
        "- No final legal opinion",
        "- No final report generated",
        "- Local-only personal alpha package",
        "",
        "## Package Header",
        f"- package_id: {package_id}",
        f"- case_id: {case_id}",
        f"- created_at: {created_at}",
        "",
        "## Case Profile Metadata",
        f"- case_id: {case_id}",
        "- case_type: personal_alpha_mock_or_redacted",
        "",
        "## Stage Summary",
        *_dict_lines(sections["stage_summary"]),
        "",
        "## Review State Summary",
        *_dict_lines(sections["review_state_summary"]),
        "",
        "## Final Lock Consolidation",
        *_dict_lines(sections["final_lock_consolidation"]),
        "",
        "## Metadata Closure Summary",
        *_dict_lines(closure),
        "",
        "## Metadata Closure Checklist",
        *[f"- {item.get('check_id')}: passed={item.get('passed')} required={item.get('required')}" for item in checklist],
        "",
        "## Audit Summary",
        *_dict_lines(audit),
        "",
        "## Redaction Check Summary",
        *_dict_lines(redaction),
        "",
        "## Safety Checklist",
        *_dict_lines(sections["safety_checklist"]),
        "",
        "## Version Trace",
        *[f"- {item}" for item in sections["version_trace"]],
        "",
    ]
    return "\n".join(lines)


def _trim_payload(payload: dict[str, Any], keys: list[str]) -> dict[str, Any]:
    return {key: payload.get(key) for key in keys}


def _without_keys(payload: Any, blocked_keys: list[str]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {key: value for key, value in payload.items() if key not in blocked_keys}


def _safe_redaction_summary(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    return {
        "passed": bool(payload.get("passed", False)),
        "unsafe_event_count": int(payload.get("unsafe_event_count", 0) or 0),
        "raw_content_event_count": int(payload.get("raw_content_event_count", 0) or 0),
        "path_like_value_count": int(payload.get("path_like_value_count", 0) or 0),
        "key_like_value_count": int(payload.get("api_key_like_value_count", 0) or 0),
        "personal_identifier_like_value_count": int(payload.get("personal_identifier_like_value_count", 0) or 0),
        "redacted_event_count": int(payload.get("redacted_event_count", 0) or 0),
    }


def _dict_lines(payload: dict[str, Any]) -> list[str]:
    lines = []
    for key, value in payload.items():
        if isinstance(value, dict):
            lines.append(f"- {key}: metadata object")
        elif isinstance(value, list):
            lines.append(f"- {key}: {len(value)} metadata items")
        else:
            lines.append(f"- {key}: {value}")
    return lines
