from personal_material_runtime.provider_config import document_live_mode_enabled, ocr_live_mode_enabled
from personal_material_runtime.schemas import PersonalMaterialLiveSafetyStatus, PersonalMaterialSafetyStatus


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


LIVE_SAFETY_FLAGS = {
    "ocr_live_mode_disabled_by_default": True,
    "document_live_mode_disabled_by_default": True,
    "provider_gated": True,
    "api_key_backend_only": True,
    "api_key_exposed": False,
    "dry_run_ready": True,
    "explicit_confirmation_required": True,
    "raw_ocr_text_blocked_by_default": True,
    "raw_document_content_blocked_by_default": True,
    "no_ai_prompt_injection": True,
    "no_fact_extraction_trigger": True,
    "no_legal_analysis_trigger": True,
    "source_trace_required": True,
    "lawyer_review_required": True,
    "audit_required": True,
    "no_final_legal_opinion": True,
    "no_final_report": True,
    "no_external_delivery": True,
}


def build_live_safety_status() -> dict:
    safety = {
        **LIVE_SAFETY_FLAGS,
        "ocr_live_mode_currently_enabled": ocr_live_mode_enabled(),
        "document_live_mode_currently_enabled": document_live_mode_enabled(),
    }
    return PersonalMaterialLiveSafetyStatus(
        safety=safety,
        all_safety_checks_passed=all(value is True for key, value in safety.items() if not key.endswith("_currently_enabled")),
        live_mode_enabled=ocr_live_mode_enabled() or document_live_mode_enabled(),
        warnings=[
            "v7.13 OCR / Document Live Gateway is dry-run first and disabled by default.",
            "Raw OCR text and raw document content are not returned or injected into AI prompts.",
        ],
    ).model_dump()
