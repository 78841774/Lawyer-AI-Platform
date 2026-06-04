from typing import Any

from fastapi import APIRouter

from personal_alpha_case_os.case_os_engine import (
    get_personal_alpha_case_os_audit_timeline,
    get_personal_alpha_case_os_case_detail,
    get_personal_alpha_case_os_next_action,
    get_personal_alpha_case_os_safety_checklist,
    get_personal_alpha_case_os_status,
    list_personal_alpha_case_os_cases,
)

router = APIRouter(prefix="/case-os", tags=["personal-alpha-case-os"])


@router.get("/status")
def personal_alpha_case_os_status() -> dict[str, Any]:
    return get_personal_alpha_case_os_status()


@router.get("")
def personal_alpha_case_os_cases() -> list[dict[str, Any]]:
    return list_personal_alpha_case_os_cases()


@router.get("/{case_id}")
def personal_alpha_case_os_case_detail(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_case_detail(case_id)


@router.get("/{case_id}/audit-timeline")
def personal_alpha_case_os_audit_timeline(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_audit_timeline(case_id)


@router.get("/{case_id}/next-action")
def personal_alpha_case_os_next_action(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_next_action(case_id)


@router.get("/{case_id}/safety-checklist")
def personal_alpha_case_os_safety_checklist(case_id: str) -> dict[str, Any]:
    return get_personal_alpha_case_os_safety_checklist(case_id)
