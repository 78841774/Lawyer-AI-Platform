from typing import Any
from uuid import uuid4

from local_sandbox.guards import check_material_safety_guard
from personal_alpha.schemas import (
    PersonalCaseManifestPreview,
    PersonalCaseManifestPreviewRequest,
    RedactionChecklist,
    utc_now,
)


def preview_case_manifest(request: PersonalCaseManifestPreviewRequest) -> dict[str, Any]:
    material_guard = check_material_safety_guard(request.local_case_root)
    warnings = [
        "Case manifest preview only.",
        "File content was not read.",
        "Local case root is redacted.",
        "Redaction checklist requires manual confirmation.",
    ]
    warnings.extend(str(item) for item in material_guard.get("warnings", []))
    if not request.case_title_redacted.strip():
        warnings.append("case_title_redacted is empty; provide a non-sensitive redacted title.")
    if not request.dry_run_only:
        warnings.append("dry_run_only=false is blocked; v4.1 supports dry-run only.")
    if not request.manual_review_confirmed:
        warnings.append("Manual review confirmation is required.")

    allowed_to_continue = (
        bool(material_guard.get("allowed"))
        and request.dry_run_only
        and request.manual_review_confirmed
        and bool(request.case_title_redacted.strip())
    )
    return PersonalCaseManifestPreview(
        manifest_id=f"personal_alpha_manifest_{uuid4().hex[:12]}",
        case_id=request.case_id,
        workspace_id=request.workspace_id,
        case_title_redacted=request.case_title_redacted,
        case_cause_code=request.case_cause_code,
        jurisdiction=request.jurisdiction,
        dry_run_only=request.dry_run_only,
        manual_review_confirmed=request.manual_review_confirmed,
        allowed_to_continue=allowed_to_continue,
        redaction_checklist=RedactionChecklist(),
        warnings=list(dict.fromkeys(warnings)),
        created_at=utc_now(),
    ).model_dump()
