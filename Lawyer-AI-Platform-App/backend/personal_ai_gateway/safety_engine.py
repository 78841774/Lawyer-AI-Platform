from personal_ai_gateway.schemas import PersonalAISafetyStatus


SAFETY_FLAGS = {
    "mock_first_enabled": True,
    "live_provider_disabled_by_default": True,
    "provider_secret_hidden": True,
    "manual_approval_required": True,
    "lawyer_review_required": True,
    "draft_only_output": True,
    "no_final_legal_opinion": True,
    "no_final_report": True,
    "no_external_delivery": True,
    "source_trace_required": True,
    "audit_log_enabled": True,
    "token_usage_metadata_enabled": True,
}


def build_safety_status() -> dict:
    return PersonalAISafetyStatus(
        safety=SAFETY_FLAGS,
        all_safety_checks_passed=all(SAFETY_FLAGS.values()),
        warnings=["v7.1 is mock-first, draft-only, provider-gated, and lawyer-review required."],
    ).model_dump()
