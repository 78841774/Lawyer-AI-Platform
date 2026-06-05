import json
import re
from typing import Any

SENSITIVE_MARKERS = (
    "/Users",
    "/Volumes",
    "local.db",
    ".env",
    "storage/runtime",
    "real_cases",
    "sandbox_cases",
)

UNSAFE_PATTERNS = {
    "api_key_like_value": (
        r"sk-[A-Za-z0-9_-]{12,}",
        r"api[_-]?key",
    ),
    "personal_identifier_like_value": (
        r"(?<!\d)1[3-9]\d{9}(?!\d)",
        r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)",
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号",
    ),
    "path_like_value": (
        r"C:\\",
        r"\\[^\\]+\\",
        r"\.(pdf|docx|xlsx|zip|png|jpg|jpeg|txt)$",
    ),
    "raw_content_like_value": (
        r"raw material",
        r"raw OCR",
        r"raw legal search",
    ),
}


def unsafe_reason(value: Any) -> str:
    text = _stringify(value)
    if not text:
        return ""
    if _is_safe_metadata_string(text):
        return ""
    lowered = text.lower()
    if any(marker.lower() in lowered for marker in SENSITIVE_MARKERS):
        return "path_like_value"
    for reason, patterns in UNSAFE_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in patterns):
            return reason
    return ""


def contains_unsafe_value(value: Any) -> bool:
    return bool(unsafe_reason(value))


def redact_unsafe_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): redact_unsafe_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [redact_unsafe_value(item) for item in value]
    return "" if contains_unsafe_value(value) else value


def assert_safe_metadata_value(value: Any) -> bool:
    return not contains_unsafe_value(value)


def scan_response_for_unsafe_values(payload: Any) -> dict[str, Any]:
    unsafe_items: list[dict[str, str]] = []
    _scan(payload, scope="response", field_name="root", unsafe_items=unsafe_items)
    return {
        "passed": not unsafe_items,
        "unsafe_value_count": len(unsafe_items),
        "path_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "path_like_value"),
        "api_key_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "api_key_like_value"),
        "raw_content_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "raw_content_like_value"),
        "personal_identifier_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "personal_identifier_like_value"),
        "unsafe_items": unsafe_items,
    }


def scan_scoped_payloads(scoped_payloads: dict[str, Any]) -> dict[str, Any]:
    unsafe_items: list[dict[str, str]] = []
    for scope, payload in scoped_payloads.items():
        _scan(payload, scope=scope, field_name=scope, unsafe_items=unsafe_items)
    return {
        "passed": not unsafe_items,
        "unsafe_value_count": len(unsafe_items),
        "path_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "path_like_value"),
        "api_key_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "api_key_like_value"),
        "raw_content_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "raw_content_like_value"),
        "personal_identifier_like_value_count": sum(1 for item in unsafe_items if item["reason"] == "personal_identifier_like_value"),
        "unsafe_items": unsafe_items,
    }


def safe_metadata_token(value: str | None) -> str:
    text = str(value or "").strip()
    return "" if contains_unsafe_value(text) else text


def _scan(payload: Any, *, scope: str, field_name: str, unsafe_items: list[dict[str, str]]) -> None:
    if isinstance(payload, dict):
        for key, value in payload.items():
            _scan(value, scope=scope, field_name=f"{field_name}.{key}", unsafe_items=unsafe_items)
        return
    if isinstance(payload, list):
        for index, value in enumerate(payload):
            _scan(value, scope=scope, field_name=f"{field_name}[{index}]", unsafe_items=unsafe_items)
        return
    reason = unsafe_reason(payload)
    if reason:
        unsafe_items.append({"scope": scope, "field_name": field_name, "reason": reason})


def _is_safe_metadata_string(text: str) -> bool:
    if text in {"json", "markdown", "metadata_only_json", "metadata_only_markdown"}:
        return True
    if text.startswith(("/case-os", "/personal-alpha")):
        return True
    return False


def _stringify(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)
