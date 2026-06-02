from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/cases", tags=["cases"])

_cases: dict[str, dict[str, Any]] = {}


class CaseCreate(BaseModel):
    case_id: str | None = None
    title: str = "MVP Demo Case"
    case_type: str = "contract_dispute"
    status: str = "draft"
    parties: list[dict[str, Any]] = Field(default_factory=list)
    objective: str | None = None


def _next_case_id() -> str:
    return f"case_{len(_cases) + 1:03d}"


@router.post("")
def create_case(payload: CaseCreate | None = None) -> dict[str, Any]:
    case_payload = payload or CaseCreate()
    case_id = case_payload.case_id or _next_case_id()

    if case_id in _cases:
        raise HTTPException(status_code=409, detail="case_id already exists")

    case_data = case_payload.model_dump()
    case_data["case_id"] = case_id
    _cases[case_id] = case_data
    return case_data


@router.get("/{case_id}")
def get_case(case_id: str) -> dict[str, Any]:
    case_data = _cases.get(case_id)
    if case_data is None:
        raise HTTPException(status_code=404, detail="case not found")
    return case_data
