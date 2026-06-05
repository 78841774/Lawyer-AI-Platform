from typing import Any

from personal_alpha_case_os.safety_guard import safe_metadata_token

DEFAULT_SAFETY_FLAGS = {
    "mock_or_redacted_only": True,
    "raw_content_included": False,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
}


def safety_flags() -> dict[str, bool]:
    return dict(DEFAULT_SAFETY_FLAGS)


def safe_warnings(*items: str) -> list[str]:
    return list(dict.fromkeys(str(item) for item in items if item))


def build_safe_not_found_response(
    *,
    case_id: str | None = None,
    resource_type: str = "case",
    message: str = "Resource not found.",
) -> dict[str, Any]:
    return {
        "status": "not_found",
        "blocked": True,
        "reason": "safe_not_found",
        "resource_type": resource_type,
        "case_id": safe_metadata_token(case_id),
        "next_action": "resolve_blockers",
        **safety_flags(),
        "warnings": safe_warnings(message, "Safe not_found response does not expose local paths."),
    }


def build_blocked_response(
    *,
    reason: str,
    case_id: str | None = None,
    warnings: list[str] | None = None,
    next_action: str = "resolve_blockers",
) -> dict[str, Any]:
    return {
        "status": "blocked",
        "blocked": True,
        "reason": reason,
        "case_id": safe_metadata_token(case_id),
        "next_action": next_action,
        **safety_flags(),
        "warnings": safe_warnings("Request was blocked by metadata-only safety guard.", *(warnings or [])),
    }


def build_redacted_response(
    *,
    reason: str,
    case_id: str | None = None,
    warnings: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "status": "redacted",
        "blocked": True,
        "reason": reason,
        "case_id": safe_metadata_token(case_id),
        "next_action": "resolve_blockers",
        **safety_flags(),
        "warnings": safe_warnings("Unsafe metadata was redacted.", *(warnings or [])),
    }


def with_safety_metadata(payload: dict[str, Any], *warnings: str) -> dict[str, Any]:
    safe = dict(payload)
    safe.setdefault("mock_or_redacted_only", True)
    safe["raw_content_included"] = False
    safe.setdefault("final_legal_opinion_generated", False)
    safe.setdefault("final_report_generated", False)
    safe["warnings"] = safe_warnings(*(safe.get("warnings", []) if isinstance(safe.get("warnings"), list) else []), *warnings)
    return safe
