FORBIDDEN_FEEDBACK_MARKERS = [
    "api_key",
    "provider_response",
    "provider_raw_response",
    "raw_text",
    "ocr_text",
    "original_text",
    "full_document_text",
    "raw_material",
    "raw_case_material",
    "local_path",
    "file_path",
    "absolute_path",
    "private_key",
    "access_token",
    "refresh_token",
    "unredacted",
]


def v731h_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "metadata_only": True,
        "local_private_processing_only": True,
        "lawyer_approved_package_only": True,
        "redacted_abstracted_experience_only": True,
        "output_observation_metadata_only": True,
        "lawyer_feedback_metadata_only": True,
        "source_trace_required": True,
        "audit_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "full_output_returned": False,
        "case_material_returned": False,
        "feedback_auto_mutates_loaded_package": False,
        "candidate_pack_auto_mutates_loaded_package": False,
        "package_auto_disabled_by_feedback": False,
        "package_auto_rolled_back_by_feedback": False,
        "practice_runtime_package_auto_replaced": False,
        "automatic_training_triggered": False,
        "formal_training_set_written": False,
        "skill_updated": False,
        "skill_published": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def feedback_metadata_safe(payload: dict) -> bool:
    scan_text = str(payload).lower()
    return not any(marker in scan_text for marker in FORBIDDEN_FEEDBACK_MARKERS)
