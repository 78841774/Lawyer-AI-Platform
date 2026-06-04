import re
from typing import Any

from controlled_material_processing.schemas import RedactedPreviewResult

MAX_REDACTED_PREVIEW_CHARS = 8000

REDACTION_PATTERNS: list[tuple[str, str, str]] = [
    ("phone", r"(?<!\d)1[3-9]\d{9}(?!\d)", "<PHONE_REDACTED>"),
    ("id_number", r"(?<!\d)\d{6}(?:19|20)\d{2}\d{2}\d{2}\d{3}[\dXx](?!\d)", "<ID_NUMBER_REDACTED>"),
    ("bank_card", r"(?<!\d)(?:\d[ -]?){16,19}(?!\d)", "<BANK_CARD_REDACTED>"),
    ("email", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<EMAIL_REDACTED>"),
    ("case_number", r"[（(]\d{4}[）)][\u4e00-\u9fa5A-Za-z0-9第初终再执民商行刑破知号字\-]{4,40}号", "<CASE_NUMBER_REDACTED>"),
    ("address", r"(?:地址|住址|住所地|联系地址|户籍地|现住址)[:：]?[^\n\r，。；;]{0,80}", "<ADDRESS_REDACTED>"),
    ("long_number", r"(?<!\d)\d{8,}(?!\d)", "<LONG_NUMBER_REDACTED>"),
]


def build_redacted_preview(raw_text: str) -> dict[str, Any]:
    redacted = raw_text
    detected: list[str] = []
    for pattern_name, pattern, replacement in REDACTION_PATTERNS:
        redacted, count = re.subn(pattern, replacement, redacted)
        if count:
            detected.append(pattern_name)

    truncated = False
    if len(redacted) > MAX_REDACTED_PREVIEW_CHARS:
        redacted = redacted[:MAX_REDACTED_PREVIEW_CHARS]
        truncated = True

    warnings = ["Redaction is best-effort and requires manual lawyer review."]
    if truncated:
        warnings.append("Redacted preview was truncated to 8000 characters.")

    return RedactedPreviewResult(
        redacted_preview=redacted,
        redaction_applied=bool(detected),
        sensitive_patterns_detected=detected,
        warnings=warnings,
    ).model_dump()
