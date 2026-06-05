from typing import Any

from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSMetadataClosureExportPreview,
    PersonalAlphaCaseOSMetadataClosureExportPreviewPayload,
    PersonalAlphaCaseOSMetadataClosureExportSection,
)


def build_metadata_closure_export_preview(
    case_id: str,
    context: dict[str, Any],
    closure_payload: dict[str, Any],
    checklist_payload: dict[str, Any],
    audit_summary: dict[str, Any],
) -> dict[str, Any]:
    audit_stats = audit_summary.get("summary", {}) if isinstance(audit_summary.get("summary", {}), dict) else {}
    sections = [
        _section("case_profile", "Case Profile Metadata", True, 1),
        _section("stage_summary", "Stage Summary", True, 8),
        _section("final_lock_summary", "Final Lock Summary", bool(context.get("latest_lock_id")), 1 if context.get("latest_lock_id") else 0),
        _section("metadata_closure_summary", "Metadata Closure Summary", True, 1),
        _section("metadata_closure_checklist", "Metadata Closure Checklist", True, len(checklist_payload.get("checklist", []))),
        _section("audit_timeline_summary", "Audit Timeline Summary", True, int(audit_stats.get("total_events", 0) or 0)),
        _section("safety_checklist", "Safety Checklist", True, 1),
    ]
    warnings = [
        "v6.4 export preview does not create files.",
        "v6.4 export preview does not include raw content.",
    ]
    if closure_payload.get("blocked"):
        warnings.append("Metadata closure is not ready; preview remains metadata-only.")
    return PersonalAlphaCaseOSMetadataClosureExportPreview(
        case_id=case_id,
        export_preview=PersonalAlphaCaseOSMetadataClosureExportPreviewPayload(sections=sections),
        can_export_metadata_preview=bool(case_id) and not bool(context.get("blocked")),
        would_create_file=False,
        would_include_raw_content=False,
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        warnings=warnings,
    ).model_dump()


def _section(section_id: str, title: str, included: bool, item_count: int) -> PersonalAlphaCaseOSMetadataClosureExportSection:
    return PersonalAlphaCaseOSMetadataClosureExportSection(
        section_id=section_id,
        title=title,
        included=included,
        raw_content_included=False,
        item_count=item_count,
    )
