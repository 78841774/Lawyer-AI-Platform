from typing import Any
from uuid import uuid4

from personal_alpha_case_os.export_package_renderers import build_export_package_content
from personal_alpha_case_os.export_package_safety import (
    build_export_package_safety_check,
    is_unsafe_export_value,
    sanitize_export_token,
)
from personal_alpha_case_os.export_package_storage import (
    get_export_package_record,
    list_export_package_records,
    load_export_package_content,
    public_record,
    store_export_package_record,
)
from personal_alpha_case_os.final_lock_consolidation import build_final_lock_consolidation
from personal_alpha_case_os.metadata_closure_checklist import build_metadata_closure_checklist
from personal_alpha_case_os.metadata_closure_engine import build_metadata_closure
from personal_alpha_case_os.review_state_machine import build_review_state, build_review_state_summary
from personal_alpha_case_os.schemas import (
    PersonalAlphaCaseOSExportPackageContent,
    PersonalAlphaCaseOSExportPackageContentSummary,
    PersonalAlphaCaseOSExportPackageCreateRequest,
    PersonalAlphaCaseOSExportPackageCreateResult,
    PersonalAlphaCaseOSExportPackageDetail,
    PersonalAlphaCaseOSExportPackageList,
    PersonalAlphaCaseOSExportPackageRecord,
    PersonalAlphaCaseOSExportPackageSafetyCheck,
    PersonalAlphaCaseOSExportPackageSafetyStats,
    PersonalAlphaCaseOSExportPackageStatus,
    PersonalAlphaCaseOSExportPackageSummary,
    PersonalAlphaCaseOSExportPackageSummaryStats,
    PersonalAlphaCaseOSExportPackageUnsafeItem,
)
from personal_alpha_case_os.unified_audit_engine import build_unified_audit_summary, build_unified_redaction_check
from personal_alpha_workspace.schemas import utc_now

SUPPORTED_FORMATS = {"json", "markdown"}
CONFIRMATION_FIELDS = [
    "manual_review_confirmed",
    "lawyer_review_confirmed",
    "metadata_only_confirmation",
    "redacted_only_confirmation",
    "no_raw_content_confirmation",
    "no_final_legal_opinion_confirmation",
    "no_final_report_generation_confirmation",
]


def build_export_package_status(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    closure_bundle = _closure_bundle(case_id, context)
    closure = closure_bundle["metadata_closure"]
    can_create = bool(closure.get("closure_ready", False)) and not bool(context.get("blocked", False))
    warnings = [
        "v6.5 export package is metadata-only.",
        "No raw content is exported.",
        "No final legal opinion is generated.",
        "No final report body is generated.",
    ]
    if context.get("blocked"):
        warnings.extend(str(item) for item in context.get("blocked_reasons", []) if item)
    if not can_create:
        warnings.append("Metadata closure is not ready; export package creation is blocked.")
    return PersonalAlphaCaseOSExportPackageStatus(
        case_id=case_id,
        can_create_export_package=can_create,
        warnings=list(dict.fromkeys(warnings)),
    ).model_dump()


def create_export_package(case_id: str, context: dict[str, Any], payload: PersonalAlphaCaseOSExportPackageCreateRequest) -> dict[str, Any]:
    package_format = str(payload.format or "").strip().lower()
    reviewer_id = str(payload.reviewer_id or "local_demo_lawyer").strip()
    created_at = utc_now()
    if context.get("blocked") or not case_id:
        return _blocked_create_result(case_id, package_format or "json", reviewer_id, payload, "Case is blocked or unsafe.")
    if package_format not in SUPPORTED_FORMATS:
        return _blocked_create_result(case_id, package_format or "invalid", reviewer_id, payload, "invalid_format", status="invalid_format")
    if is_unsafe_export_value(reviewer_id):
        return _blocked_create_result(case_id, package_format, "", payload, "reviewer_id contains unsafe raw content or path-like value.")
    missing = [field for field in CONFIRMATION_FIELDS if not bool(getattr(payload, field))]
    if missing:
        return _blocked_create_result(case_id, package_format, reviewer_id, payload, f"Missing required confirmations: {', '.join(missing)}.")
    closure_bundle = _closure_bundle(case_id, context)
    closure = closure_bundle["metadata_closure"]
    if not bool(closure.get("closure_ready", False)):
        return _blocked_create_result(case_id, package_format, reviewer_id, payload, "Metadata closure is not ready.")
    package_id = f"case_os_export_package_{uuid4().hex[:16]}"
    content = build_export_package_content(
        package_id=package_id,
        case_id=case_id,
        package_format=package_format,
        reviewer_id=reviewer_id,
        context=context,
        review_state=closure_bundle["review_state"],
        review_state_summary=closure_bundle["review_state_summary"],
        final_lock_consolidation=closure_bundle["final_lock_consolidation"],
        metadata_closure=closure,
        metadata_closure_checklist=closure_bundle["metadata_closure_checklist"],
        audit_summary=closure_bundle["audit_summary"],
        redaction_check=closure_bundle["redaction_check"],
        created_at=created_at,
    )
    content_summary = _content_summary(content)
    public_file_name = f"redacted_or_safe_metadata_filename_{'md' if package_format == 'markdown' else 'json'}"
    content_file_name = f"package_{sanitize_export_token(case_id, 'case')}_{package_id}_{'md' if package_format == 'markdown' else 'json'}"
    safety_check, unsafe_items = build_export_package_safety_check(
        {
            "case_id": case_id,
            "package_id": package_id,
            "reviewer_id": reviewer_id,
            "format": package_format,
            "file_name": public_file_name,
            "content": content,
            "metadata_sections": _metadata_sections(content),
            "version_trace": _version_trace(content),
            "raw_content_included": False,
        }
    )
    if unsafe_items or not safety_check.get("passed", False):
        return _blocked_create_result(case_id, package_format, reviewer_id, payload, "Export package safety check failed.")
    record = {
        "package_id": package_id,
        "case_id": case_id,
        "format": package_format,
        "status": "export_package_created",
        "reviewer_id": reviewer_id,
        "file_name": public_file_name,
        "content_file_name": content_file_name,
        "content_summary": content_summary,
        "safety_check": safety_check,
        "unsafe_items": unsafe_items,
        "manual_review_confirmed": payload.manual_review_confirmed,
        "lawyer_review_confirmed": payload.lawyer_review_confirmed,
        "metadata_only_confirmation": payload.metadata_only_confirmation,
        "redacted_only_confirmation": payload.redacted_only_confirmation,
        "no_raw_content_confirmation": payload.no_raw_content_confirmation,
        "no_final_legal_opinion_confirmation": payload.no_final_legal_opinion_confirmation,
        "no_final_report_generation_confirmation": payload.no_final_report_generation_confirmation,
        "warnings": [],
        "created_at": created_at,
    }
    store_result = store_export_package_record(record, content)
    return PersonalAlphaCaseOSExportPackageCreateResult(
        package_id=package_id,
        case_id=case_id,
        format=package_format,
        status="export_package_created",
        reviewer_id=reviewer_id,
        stored=bool(store_result.get("stored", False)),
        file_created=bool(store_result.get("file_created", False)),
        file_path_redacted=True,
        file_name=public_file_name,
        content_summary=PersonalAlphaCaseOSExportPackageContentSummary(**content_summary),
        safety_check=PersonalAlphaCaseOSExportPackageSafetyStats(**safety_check),
        mock_or_redacted_only=True,
        raw_content_included=False,
        final_legal_opinion_generated=False,
        final_report_generated=False,
        manual_review_confirmed=payload.manual_review_confirmed,
        lawyer_review_confirmed=payload.lawyer_review_confirmed,
        metadata_only_confirmation=payload.metadata_only_confirmation,
        redacted_only_confirmation=payload.redacted_only_confirmation,
        no_raw_content_confirmation=payload.no_raw_content_confirmation,
        no_final_legal_opinion_confirmation=payload.no_final_legal_opinion_confirmation,
        no_final_report_generation_confirmation=payload.no_final_report_generation_confirmation,
        warnings=[],
        created_at=created_at,
    ).model_dump()


def list_export_packages(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    if context.get("blocked") or not case_id:
        return PersonalAlphaCaseOSExportPackageList(
            case_id=case_id,
            packages=[],
            package_count=0,
            warnings=[str(item) for item in context.get("blocked_reasons", ["Case not found."])],
        ).model_dump()
    records = [PersonalAlphaCaseOSExportPackageRecord(**public_record(record)) for record in list_export_package_records(case_id)]
    return PersonalAlphaCaseOSExportPackageList(
        case_id=case_id,
        packages=records,
        package_count=len(records),
        warnings=[],
    ).model_dump()


def get_export_package_detail(case_id: str, context: dict[str, Any], package_id: str) -> dict[str, Any]:
    record = _safe_existing_record(case_id, context, package_id)
    if not record:
        return _not_found_detail()
    return PersonalAlphaCaseOSExportPackageDetail(
        package=PersonalAlphaCaseOSExportPackageRecord(**public_record(record)),
        content_summary=PersonalAlphaCaseOSExportPackageContentSummary(**record.get("content_summary", {})),
        safety_check=PersonalAlphaCaseOSExportPackageSafetyStats(**record.get("safety_check", {})),
        warnings=[],
    ).model_dump()


def get_export_package_content(case_id: str, context: dict[str, Any], package_id: str) -> dict[str, Any]:
    record = _safe_existing_record(case_id, context, package_id)
    if not record:
        return PersonalAlphaCaseOSExportPackageContent(
            package_id="",
            case_id=case_id,
            format="",
            content_type="metadata_only_not_found",
            content={},
            warnings=["Export package not found."],
        ).model_dump()
    content = load_export_package_content(record)
    safety_check, unsafe_items = build_export_package_safety_check(
        {
            "case_id": case_id,
            "package_id": record.get("package_id", ""),
            "format": record.get("format", ""),
            "content": content,
            "warnings": record.get("warnings", []),
            "raw_content_included": False,
        }
    )
    if unsafe_items or not safety_check.get("passed", False):
        content = {} if record.get("format") == "json" else ""
    return PersonalAlphaCaseOSExportPackageContent(
        package_id=record.get("package_id", ""),
        case_id=case_id,
        format=record.get("format", ""),
        content_type="metadata_only_markdown" if record.get("format") == "markdown" else "metadata_only_json",
        content=content if content is not None else {},
        warnings=[
            "This is a metadata-only export package.",
            "No raw content is included.",
        ],
    ).model_dump()


def get_export_package_safety_check(case_id: str, context: dict[str, Any], package_id: str) -> dict[str, Any]:
    record = _safe_existing_record(case_id, context, package_id)
    if not record:
        return PersonalAlphaCaseOSExportPackageSafetyCheck(
            package_id="",
            case_id=case_id,
            safety_check=PersonalAlphaCaseOSExportPackageSafetyStats(passed=False, unsafe_value_count=0),
            unsafe_items=[],
            warnings=["Export package not found."],
        ).model_dump()
    content = load_export_package_content(record)
    safety_check, unsafe_items = build_export_package_safety_check(
        {
            "case_id": case_id,
            "package_id": record.get("package_id", ""),
            "format": record.get("format", ""),
            "file_name": record.get("file_name", ""),
            "content": content,
            "warnings": record.get("warnings", []),
            "metadata_sections": _metadata_sections(content),
            "version_trace": _version_trace(content),
            "raw_content_included": False,
        }
    )
    return PersonalAlphaCaseOSExportPackageSafetyCheck(
        package_id=record.get("package_id", ""),
        case_id=case_id,
        safety_check=PersonalAlphaCaseOSExportPackageSafetyStats(**safety_check),
        unsafe_items=[PersonalAlphaCaseOSExportPackageUnsafeItem(**item) for item in unsafe_items],
        warnings=[],
    ).model_dump()


def get_export_package_summary(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    records = [] if context.get("blocked") or not case_id else list_export_package_records(case_id)
    latest = records[-1] if records else {}
    unsafe_count = sum(1 for record in records if not record.get("safety_check", {}).get("passed", True))
    raw_count = sum(1 for record in records if record.get("safety_check", {}).get("raw_content_included", False))
    return PersonalAlphaCaseOSExportPackageSummary(
        case_id=case_id,
        summary=PersonalAlphaCaseOSExportPackageSummaryStats(
            package_count=len(records),
            json_package_count=sum(1 for item in records if item.get("format") == "json"),
            markdown_package_count=sum(1 for item in records if item.get("format") == "markdown"),
            latest_package_id=latest.get("package_id") or None,
            latest_package_created_at=latest.get("created_at") or None,
            all_packages_metadata_only=raw_count == 0,
            unsafe_package_count=unsafe_count,
            raw_content_package_count=raw_count,
        ),
        warnings=[] if not context.get("blocked") else [str(item) for item in context.get("blocked_reasons", [])],
    ).model_dump()


def _closure_bundle(case_id: str, context: dict[str, Any]) -> dict[str, Any]:
    review_state = build_review_state(case_id, context)
    review_state_summary = build_review_state_summary(case_id, context)
    audit_summary = build_unified_audit_summary(case_id, context)
    redaction_check = build_unified_redaction_check(case_id, context)
    checklist = build_metadata_closure_checklist(case_id, context, audit_summary, redaction_check)
    closure = build_metadata_closure(case_id, context, review_state, audit_summary, redaction_check, checklist)
    final_lock = build_final_lock_consolidation(case_id, context, review_state)
    return {
        "review_state": review_state,
        "review_state_summary": review_state_summary,
        "audit_summary": audit_summary,
        "redaction_check": redaction_check,
        "metadata_closure_checklist": checklist,
        "metadata_closure": closure,
        "final_lock_consolidation": final_lock,
    }


def _blocked_create_result(
    case_id: str,
    package_format: str,
    reviewer_id: str,
    payload: PersonalAlphaCaseOSExportPackageCreateRequest,
    reason: str,
    *,
    status: str = "blocked",
) -> dict[str, Any]:
    return PersonalAlphaCaseOSExportPackageCreateResult(
        package_id="",
        case_id=case_id,
        format=package_format,
        status=status,
        reviewer_id=reviewer_id if not is_unsafe_export_value(reviewer_id) else "",
        stored=False,
        file_created=False,
        file_path_redacted=True,
        file_name="redacted_or_safe_metadata_filename",
        content_summary=PersonalAlphaCaseOSExportPackageContentSummary(),
        safety_check=PersonalAlphaCaseOSExportPackageSafetyStats(passed=False),
        manual_review_confirmed=payload.manual_review_confirmed,
        lawyer_review_confirmed=payload.lawyer_review_confirmed,
        metadata_only_confirmation=payload.metadata_only_confirmation,
        redacted_only_confirmation=payload.redacted_only_confirmation,
        no_raw_content_confirmation=payload.no_raw_content_confirmation,
        no_final_legal_opinion_confirmation=payload.no_final_legal_opinion_confirmation,
        no_final_report_generation_confirmation=payload.no_final_report_generation_confirmation,
        warnings=[reason],
        created_at=utc_now(),
    ).model_dump()


def _safe_existing_record(case_id: str, context: dict[str, Any], package_id: str) -> dict[str, Any] | None:
    if context.get("blocked") or not case_id or is_unsafe_export_value(package_id):
        return None
    return get_export_package_record(case_id, package_id)


def _not_found_detail() -> dict[str, Any]:
    return PersonalAlphaCaseOSExportPackageDetail(
        package=None,
        content_summary=PersonalAlphaCaseOSExportPackageContentSummary(),
        safety_check=PersonalAlphaCaseOSExportPackageSafetyStats(passed=False),
        warnings=["Export package not found."],
    ).model_dump()


def _content_summary(content: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(content, dict):
        sections = content.get("sections", {}) if isinstance(content.get("sections", {}), dict) else {}
        item_count = _count_items(sections)
        section_count = len(sections)
    else:
        section_count = content.count("\n## ")
        item_count = content.count("\n- ")
    return PersonalAlphaCaseOSExportPackageContentSummary(
        section_count=section_count,
        item_count=item_count,
        includes_raw_content=False,
    ).model_dump()


def _count_items(value: Any) -> int:
    if isinstance(value, dict):
        return sum(_count_items(item) for item in value.values()) or len(value)
    if isinstance(value, list):
        return len(value)
    return 1 if value is not None else 0


def _metadata_sections(content: Any) -> Any:
    if isinstance(content, dict):
        return list((content.get("sections") or {}).keys())
    if isinstance(content, str):
        return [line.replace("## ", "") for line in content.splitlines() if line.startswith("## ")]
    return []


def _version_trace(content: Any) -> Any:
    if isinstance(content, dict):
        sections = content.get("sections", {}) if isinstance(content.get("sections", {}), dict) else {}
        return sections.get("version_trace", [])
    if isinstance(content, str):
        return [line[2:] for line in content.splitlines() if line.startswith("- v")]
    return []
