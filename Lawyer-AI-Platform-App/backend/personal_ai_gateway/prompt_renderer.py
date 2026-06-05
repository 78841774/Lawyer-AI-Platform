from personal_ai_gateway.approval_gate import validate_preview_confirmations
from personal_ai_gateway.prompt_registry import get_prompt_template
from personal_ai_gateway.schemas import PersonalAIPromptRenderPreviewRequest, PersonalAIPromptRenderPreviewResult


def render_prompt_preview(request: PersonalAIPromptRenderPreviewRequest) -> dict:
    template = get_prompt_template(request.template_id)
    if template is None:
        return PersonalAIPromptRenderPreviewResult(
            template_id=request.template_id,
            case_id=request.case_id,
            status="blocked",
            rendered_prompt_preview="",
            blocked_reasons=["template_id is not registered"],
            warnings=["Preview blocked before rendering. No provider call was attempted."],
        ).model_dump()

    blocked_reasons = validate_preview_confirmations(request)
    if blocked_reasons:
        return PersonalAIPromptRenderPreviewResult(
            template_id=request.template_id,
            case_id=request.case_id,
            status="blocked",
            rendered_prompt_preview="",
            blocked_reasons=blocked_reasons,
            warnings=["Preview blocked because required safety confirmations are incomplete."],
        ).model_dump()

    case_label = request.case_id or "mock_case_placeholder"
    variable_labels = ", ".join(sorted(request.variables.keys())) or "no variables"
    preview = (
        f"Mock-safe prompt preview for {template.name}. "
        f"Case reference: {case_label}. "
        f"Variable keys: {variable_labels}. "
        "Use redacted metadata only, produce an AI-assisted draft, require source tracing, "
        "and require lawyer review before any downstream use. Do not generate a final legal opinion or final report."
    )
    return PersonalAIPromptRenderPreviewResult(
        template_id=template.template_id,
        case_id=request.case_id,
        rendered_prompt_preview=preview,
        warnings=["No live provider call will be made from prompt preview."],
    ).model_dump()
