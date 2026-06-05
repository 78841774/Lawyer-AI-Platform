from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSQualityScore,
    PersonalAlphaCaseOSQualityScoreDetail,
)

SCORE_LOGIC = {
    "base_score": 100,
    "critical_penalty": 25,
    "high_penalty": 15,
    "medium_penalty": 7,
    "low_penalty": 3,
    "minimum_score": 0,
}


def build_quality_score(case_id: str, checklist_payload: dict[str, Any], findings_payload: dict[str, Any]) -> dict[str, Any]:
    failed_items = [
        item
        for item in checklist_payload.get("checklist", [])
        if isinstance(item, dict) and not bool(item.get("passed", False))
    ]
    counts = {
        "critical": _count_severity(failed_items, "critical"),
        "high": _count_severity(failed_items, "high"),
        "medium": _count_severity(failed_items, "medium"),
        "low": _count_severity(failed_items, "low"),
    }
    penalty = (
        counts["critical"] * SCORE_LOGIC["critical_penalty"]
        + counts["high"] * SCORE_LOGIC["high_penalty"]
        + counts["medium"] * SCORE_LOGIC["medium_penalty"]
        + counts["low"] * SCORE_LOGIC["low_penalty"]
    )
    quality_score = max(SCORE_LOGIC["minimum_score"], min(100, SCORE_LOGIC["base_score"] - penalty))
    required_failed_count = int(checklist_payload.get("required_failed_count", 0) or 0)
    critical_failed_count = int(checklist_payload.get("critical_failed_count", 0) or 0)
    ready = (
        required_failed_count == 0
        and critical_failed_count == 0
        and not bool(checklist_payload.get("raw_content_included", False))
    )
    score = PersonalAlphaCaseOSQualityScoreDetail(
        quality_score=quality_score,
        quality_grade=_grade(quality_score),
        max_score=100,
        passed_count=int(checklist_payload.get("passed_count", 0) or 0),
        failed_count=int(checklist_payload.get("failed_count", 0) or 0),
        required_failed_count=required_failed_count,
        critical_failed_count=critical_failed_count,
        high_failed_count=counts["high"],
        medium_failed_count=counts["medium"],
        low_failed_count=counts["low"],
        blocking_issue_count=int(findings_payload.get("blocking_finding_count", 0) or 0),
        advisory_warning_count=int(checklist_payload.get("warning_count", 0) or 0),
        ready_for_personal_alpha_review=ready,
    )
    return PersonalAlphaCaseOSQualityScore(
        case_id=case_id,
        score=score,
        score_logic=SCORE_LOGIC,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Quality score is advisory metadata only."],
    ).model_dump()


def _count_severity(items: list[dict[str, Any]], severity: str) -> int:
    return sum(1 for item in items if str(item.get("severity", "")) == severity)


def _grade(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
