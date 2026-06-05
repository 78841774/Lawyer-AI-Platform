from personal_material_runtime.schemas import PersonalMaterialSafetyStatus


SAFETY_FLAGS = {
    "mock_first_enabled": True,
    "live_provider_disabled_by_default": True,
    "provider_secret_hidden": True,
    "manual_approval_required": True,
    "lawyer_review_required": True,
    "raw_ocr_controlled": True,
    "no_uncontrolled_raw_content_exposure": True,
    "source_trace_required": True,
    "audit_log_enabled": True,
    "no_final_legal_opinion": True,
    "no_final_report": True,
    "no_external_delivery": True,
}


def build_safety_status() -> dict:
    return PersonalMaterialSafetyStatus(
        safety=SAFETY_FLAGS,
        all_safety_checks_passed=all(SAFETY_FLAGS.values()),
        warnings=["v7.2 is mock-first, controlled-preview-only, and lawyer-review required."],
    ).model_dump()
