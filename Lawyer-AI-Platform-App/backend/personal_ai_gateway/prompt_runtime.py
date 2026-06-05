from datetime import datetime, timezone
from uuid import uuid4

from personal_ai_gateway.approval_gate import validate_mock_run_confirmations
from personal_ai_gateway.audit_engine import persist_run
from personal_ai_gateway.prompt_registry import get_prompt_template
from personal_ai_gateway.provider_gateway import validate_provider_for_mock_run
from personal_ai_gateway.schemas import (
    PersonalAIDraftOutput,
    PersonalAIMockRunRequest,
    PersonalAIMockRunResult,
    PersonalAIRunRecord,
)
from personal_ai_gateway.token_usage_engine import estimate_token_usage


def create_mock_run(request: PersonalAIMockRunRequest) -> dict:
    blocked_reasons = [
        *validate_provider_for_mock_run(request.provider_id),
        *validate_template_for_mock_run(request.template_id),
        *validate_mock_run_confirmations(request),
    ]
    if blocked_reasons:
        return PersonalAIMockRunResult(
            provider_id=request.provider_id,
            template_id=request.template_id,
            case_id=request.case_id,
            status="blocked",
            blocked_reasons=blocked_reasons,
            warnings=["Mock AI run blocked. No run was created and no provider call was attempted."],
        ).model_dump()

    template = get_prompt_template(request.template_id)
    assert template is not None

    ai_run_id = f"personal_ai_run_{uuid4().hex[:12]}"
    token_usage = estimate_token_usage(request.template_id, request.provider_id)
    draft_output = PersonalAIDraftOutput(
        title=f"Mock {template.name}",
        content="This is a mock-safe draft output for workflow validation.",
    )
    created_at = datetime.now(timezone.utc).isoformat()
    record = PersonalAIRunRecord(
        ai_run_id=ai_run_id,
        provider_id=request.provider_id,
        template_id=request.template_id,
        case_id=request.case_id,
        purpose=template.purpose,
        token_usage=token_usage,
        created_at=created_at,
        warnings=["Mock AI run metadata only. No live provider call was executed."],
    )
    persist_run(record)

    return PersonalAIMockRunResult(
        ai_run_id=ai_run_id,
        provider_id=request.provider_id,
        template_id=request.template_id,
        case_id=request.case_id,
        draft_output=draft_output,
        token_usage=token_usage,
        warnings=[],
    ).model_dump()


def validate_template_for_mock_run(template_id: str) -> list[str]:
    template = get_prompt_template(template_id)
    if template is None:
        return ["template_id is not registered"]
    if not template.enabled:
        return ["template is disabled"]
    if not template.draft_only:
        return ["template must be draft_only"]
    if not template.requires_lawyer_review:
        return ["template must require lawyer review"]
    if not template.source_trace_required:
        return ["template must require source trace"]
    return []
