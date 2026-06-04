from typing import Any

from fastapi import APIRouter

from personal_alpha_final_lock.lock_engine import (
    create_personal_alpha_final_lock,
    get_personal_alpha_final_lock,
    get_personal_alpha_final_lock_readiness,
    get_personal_alpha_final_lock_status,
    list_personal_alpha_final_locks,
    list_personal_alpha_final_locks_for_packet,
)
from personal_alpha_final_lock.schemas import PersonalAlphaFinalLockCreateRequest

router = APIRouter(prefix="/personal-alpha-final-lock", tags=["personal-alpha-final-lock"])


@router.get("/status")
def personal_alpha_final_lock_status() -> dict[str, Any]:
    return get_personal_alpha_final_lock_status()


@router.get("/packets/{packet_id}/readiness")
def personal_alpha_final_lock_readiness(packet_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_lock_readiness(packet_id)


@router.post("/packets/{packet_id}/create")
def personal_alpha_final_lock_create(packet_id: str, request: PersonalAlphaFinalLockCreateRequest) -> dict[str, Any]:
    return create_personal_alpha_final_lock(packet_id, request)


@router.get("/locks")
def personal_alpha_final_lock_list() -> dict[str, Any]:
    return list_personal_alpha_final_locks()


@router.get("/locks/{lock_id}")
def personal_alpha_final_lock_detail(lock_id: str) -> dict[str, Any]:
    return get_personal_alpha_final_lock(lock_id)


@router.get("/packets/{packet_id}/locks")
def personal_alpha_final_lock_packet_locks(packet_id: str) -> dict[str, Any]:
    return list_personal_alpha_final_locks_for_packet(packet_id)
