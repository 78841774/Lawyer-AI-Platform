from typing import Any

from fastapi import APIRouter

from controlled_final_review_lock.audit import list_controlled_final_review_lock_audit_logs
from controlled_final_review_lock.lock_engine import (
    create_mock_final_review_lock,
    get_controlled_final_review_lock_status,
    load_controlled_final_review_lock,
)
from controlled_final_review_lock.schemas import ControlledFinalReviewLockRequest

router = APIRouter(prefix="/controlled-final-review", tags=["controlled-final-review"])


@router.get("/status")
def controlled_final_review_lock_status() -> dict[str, Any]:
    return get_controlled_final_review_lock_status()


@router.post("/lock")
def controlled_final_review_lock(request: ControlledFinalReviewLockRequest) -> dict[str, Any]:
    return create_mock_final_review_lock(request)


@router.get("/audit-logs")
def controlled_final_review_lock_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_controlled_final_review_lock_audit_logs()}


@router.get("/{final_lock_id}")
def controlled_final_review_lock_record(final_lock_id: str) -> dict[str, Any]:
    return load_controlled_final_review_lock(final_lock_id)
