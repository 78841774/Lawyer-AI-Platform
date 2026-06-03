from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from app.llm.llm_service import generate_text, get_llm_status

router = APIRouter(prefix="/llm", tags=["llm"])


class LLMTestRequest(BaseModel):
    prompt: str
    context: dict[str, Any] | None = None


@router.get("/status")
def llm_status() -> dict[str, object]:
    return get_llm_status()


@router.post("/test")
def test_llm(payload: LLMTestRequest) -> dict[str, object]:
    return generate_text(prompt=payload.prompt, context=payload.context)
