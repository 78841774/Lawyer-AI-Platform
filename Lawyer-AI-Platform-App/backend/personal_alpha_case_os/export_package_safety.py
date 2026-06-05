import json
import re
from typing import Any

from personal_alpha_case_os.audit_redaction import unsafe_reason
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSExportPackageSafetyStats,
    PersonalAlphaCaseOSExportPackageUnsafeItem,
)

CHECKED_FIELDS = [
    "case_id",
    "package_id",
    "reviewer_id",
    "format",
    "file_name",
    "content",
    "section_id",
    "title",
    "warnings",
    "metadata_sections",
    "version_trace",
]


def is_unsafe_export_value(value: Any) -> bool:
    return bool(unsafe_reason(value))


def sanitize_export_token(value: str, fallback: str) -> str:
    if is_unsafe_export_value(value):
        return ""
    safe = re.sub(r"[^A-Za-z0-9_-]", "_", value or "")
    return safe[:120] or fallback


def build_export_package_safety_check(values: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, str]]]:
    unsafe_items: list[PersonalAlphaCaseOSExportPackageUnsafeItem] = []
    for field_name in CHECKED_FIELDS:
        value = values.get(field_name)
        if value is None:
            continue
        reason = unsafe_reason(_stringify(value))
        if reason:
            unsafe_items.append(PersonalAlphaCaseOSExportPackageUnsafeItem(field_name=field_name, reason=reason))
    path_like_count = sum(1 for item in unsafe_items if item.reason == "path_like_value")
    api_key_count = sum(1 for item in unsafe_items if item.reason == "api_key_like_value")
    pii_count = sum(1 for item in unsafe_items if item.reason == "personal_identifier_like_value")
    stats = PersonalAlphaCaseOSExportPackageSafetyStats(
        passed=not unsafe_items and not bool(values.get("raw_content_included", False)),
        raw_content_included=bool(values.get("raw_content_included", False)),
        path_like_value_count=path_like_count,
        api_key_like_value_count=api_key_count,
        personal_identifier_like_value_count=pii_count,
        unsafe_value_count=len(unsafe_items),
        checked_fields=CHECKED_FIELDS,
    )
    return stats.model_dump(), [item.model_dump() for item in unsafe_items]


def _stringify(value: Any) -> str:
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(value)
