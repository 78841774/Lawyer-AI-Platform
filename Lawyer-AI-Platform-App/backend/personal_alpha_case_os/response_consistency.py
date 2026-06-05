from typing import Any

REQUIRED_FIELDS = [
    "mock_or_redacted_only",
    "raw_content_included",
    "final_legal_opinion_generated",
    "final_report_generated",
    "warnings",
]


def normalize_response_metadata(payload: dict[str, Any], *, warning: str | None = None) -> dict[str, Any]:
    normalized = dict(payload)
    normalized.setdefault("mock_or_redacted_only", True)
    normalized["raw_content_included"] = False
    normalized.setdefault("final_legal_opinion_generated", False)
    normalized.setdefault("final_report_generated", False)
    warnings = normalized.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = [str(warnings)]
    if warning:
        warnings.append(warning)
    normalized["warnings"] = list(dict.fromkeys(str(item) for item in warnings if item))
    return normalized


def check_response_consistency(endpoint_payloads: dict[str, dict[str, Any]]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    for endpoint, payload in endpoint_payloads.items():
        for field in REQUIRED_FIELDS:
            if field not in payload:
                issues.append({"endpoint": endpoint, "field_name": field, "reason": "missing_required_field"})
        for field in ["raw_content_included", "final_legal_opinion_generated", "final_report_generated"]:
            if payload.get(field) is not False:
                issues.append({"endpoint": endpoint, "field_name": field, "reason": "inconsistent_safety_flag"})
        if payload.get("mock_or_redacted_only") is not True:
            issues.append({"endpoint": endpoint, "field_name": "mock_or_redacted_only", "reason": "inconsistent_safety_flag"})
        if not isinstance(payload.get("warnings", []), list):
            issues.append({"endpoint": endpoint, "field_name": "warnings", "reason": "warnings_not_list"})
    return {
        "passed": not issues,
        "checked_endpoints": list(endpoint_payloads.keys()),
        "missing_required_field_count": sum(1 for item in issues if item["reason"] == "missing_required_field"),
        "inconsistent_safety_flag_count": sum(1 for item in issues if item["reason"] != "missing_required_field"),
        "required_fields": REQUIRED_FIELDS,
        "issues": issues,
    }
