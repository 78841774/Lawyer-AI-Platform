from typing import Any

STAGE_ROUTE_MAP = {
    "workspace_run": "/personal-alpha-workspace",
    "dashboard": "/personal-alpha-dashboard",
    "run_detail": "/personal-alpha-dashboard/runs/{workspace_run_id}",
    "source_review": "/personal-alpha-source-review",
    "source_review_decision": "/personal-alpha-source-review",
    "final_readiness": "/personal-alpha-final-readiness",
    "final_gate": "/personal-alpha-final-gate",
    "final_packet": "/personal-alpha-final-packet",
    "lawyer_final_review": "/personal-alpha-lawyer-final-review",
    "final_lock": "/personal-alpha-final-lock",
    "case_os": "/case-os/{case_id}",
}

ACTION_ROUTE_MAP = {
    "create_workspace_run": "workspace_run",
    "review_sources": "source_review",
    "submit_source_review_decision": "source_review_decision",
    "check_final_readiness": "final_readiness",
    "submit_final_gate_decision": "final_gate",
    "create_final_packet": "final_packet",
    "submit_lawyer_final_review": "lawyer_final_review",
    "create_final_lock": "final_lock",
    "view_completed_metadata_review": "final_lock",
    "resolve_blockers": "case_os",
}


def route_for_stage(stage_id: str, metadata: dict[str, Any] | None = None) -> str:
    route = STAGE_ROUTE_MAP.get(stage_id, "/case-os")
    return _format_route(route, metadata or {})


def route_for_action(action: str, metadata: dict[str, Any] | None = None) -> str:
    return route_for_stage(ACTION_ROUTE_MAP.get(action, "case_os"), metadata)


def _format_route(route: str, metadata: dict[str, Any]) -> str:
    safe_values = {
        "case_id": _safe_route_token(str(metadata.get("case_id", ""))),
        "workspace_run_id": _safe_route_token(str(metadata.get("workspace_run_id", ""))),
    }
    for key, value in safe_values.items():
        route = route.replace("{" + key + "}", value)
    return route


def _safe_route_token(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        return ""
    if "/" in text or "\\" in text or "." in text:
        return ""
    return "".join(char for char in text if char.isalnum() or char in {"_", "-"})
