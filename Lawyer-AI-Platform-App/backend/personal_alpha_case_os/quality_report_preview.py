from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSQualityReportPreview,
    PersonalAlphaCaseOSQualityReportPreviewPayload,
    PersonalAlphaCaseOSQualityReportSection,
    PersonalAlphaCaseOSQualitySummary,
    PersonalAlphaCaseOSQualitySummaryDetail,
)


def build_quality_report_preview(
    case_id: str,
    checklist_payload: dict[str, Any],
    findings_payload: dict[str, Any],
    recommendations_payload: dict[str, Any],
) -> dict[str, Any]:
    sections = [
        _section("quality_score", "Quality Score", 1),
        _section("quality_checklist", "Quality Checklist", int(checklist_payload.get("passed_count", 0) or 0) + int(checklist_payload.get("failed_count", 0) or 0)),
        _section("quality_findings", "Quality Findings", int(findings_payload.get("finding_count", 0) or 0)),
        _section("recommendations", "Recommendations", int(recommendations_payload.get("recommendation_count", 0) or 0)),
        _section("safety_boundary", "Safety Boundary", 1),
    ]
    return PersonalAlphaCaseOSQualityReportPreview(
        case_id=case_id,
        report_preview=PersonalAlphaCaseOSQualityReportPreviewPayload(sections=sections),
        would_create_file=False,
        would_generate_final_report=False,
        would_generate_legal_opinion=False,
        would_include_raw_content=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=[
            "v6.6 quality report preview does not create files.",
            "v6.6 quality report preview is not a legal opinion.",
            "v6.6 quality report preview is not a final case report.",
        ],
    ).model_dump()


def build_quality_summary(
    case_id: str,
    score_payload: dict[str, Any],
    findings_payload: dict[str, Any],
    recommendations_payload: dict[str, Any],
    metadata_closure: dict[str, Any],
    export_summary: dict[str, Any],
    redaction_check: dict[str, Any],
) -> dict[str, Any]:
    score = score_payload.get("score", {}) if isinstance(score_payload.get("score", {}), dict) else {}
    export_stats = export_summary.get("summary", {}) if isinstance(export_summary.get("summary", {}), dict) else {}
    redaction_stats = redaction_check.get("redaction_check", {}) if isinstance(redaction_check.get("redaction_check", {}), dict) else {}
    top_findings = [
        _compact_finding(item)
        for item in findings_payload.get("findings", [])[:3]
        if isinstance(item, dict)
    ]
    top_recommendations = [
        _compact_recommendation(item)
        for item in recommendations_payload.get("recommendations", [])[:3]
        if isinstance(item, dict)
    ]
    summary = PersonalAlphaCaseOSQualitySummaryDetail(
        quality_score=int(score.get("quality_score", 0) or 0),
        quality_grade=str(score.get("quality_grade", "F")),
        ready_for_personal_alpha_review=bool(score.get("ready_for_personal_alpha_review", False)),
        required_failed_count=int(score.get("required_failed_count", 0) or 0),
        critical_failed_count=int(score.get("critical_failed_count", 0) or 0),
        blocking_finding_count=int(findings_payload.get("blocking_finding_count", 0) or 0),
        advisory_warning_count=int(score.get("advisory_warning_count", 0) or 0),
        top_findings=top_findings,
        top_recommendations=top_recommendations,
        metadata_closure_ready=bool(metadata_closure.get("closure_ready", False)),
        export_package_available=int(export_stats.get("package_count", 0) or 0) > 0,
        redaction_check_passed=bool(redaction_stats.get("passed", False)),
    )
    return PersonalAlphaCaseOSQualitySummary(
        case_id=case_id,
        summary=summary,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=["Quality summary is advisory metadata only."],
    ).model_dump()


def _section(section_id: str, title: str, item_count: int) -> PersonalAlphaCaseOSQualityReportSection:
    return PersonalAlphaCaseOSQualityReportSection(
        section_id=section_id,
        title=title,
        included=True,
        raw_content_included=False,
        item_count=item_count,
    )


def _compact_finding(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "finding_code": str(item.get("finding_code", "")),
        "severity": str(item.get("severity", "")),
        "title": str(item.get("title", "")),
        "blocking": bool(item.get("blocking", False)),
        "target_route": str(item.get("target_route", "")),
    }


def _compact_recommendation(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "priority": str(item.get("priority", "")),
        "action": str(item.get("action", "")),
        "label": str(item.get("label", "")),
        "target_route": str(item.get("target_route", "")),
        "would_execute_action": False,
    }
