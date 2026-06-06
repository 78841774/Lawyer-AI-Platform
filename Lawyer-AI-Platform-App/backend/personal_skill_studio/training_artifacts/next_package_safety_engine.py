FORBIDDEN_NEXT_PACKAGE_MARKERS = [
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


def v731j_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "metadata_only": True,
        "local_private_processing_only": True,
        "next_experience_package_draft_only": True,
        "candidate_pack_required": True,
        "ready_candidate_pack_required": True,
        "practice_load_review_required": True,
        "redacted_abstracted_experience_only": True,
        "source_trace_required": True,
        "audit_required": True,
        "loaded_package_mutated": False,
        "lawyer_approved_package_mutated": False,
        "runtime_package_replaced": False,
        "runtime_policy_changed": False,
        "next_package_draft_auto_loaded": False,
        "package_auto_disabled": False,
        "package_auto_rolled_back": False,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "full_output_returned": False,
        "case_material_returned": False,
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


def next_package_metadata_safe(payload: dict) -> bool:
    scan_text = str(payload).lower()
    return not any(marker in scan_text for marker in FORBIDDEN_NEXT_PACKAGE_MARKERS)
