FORBIDDEN_LIFECYCLE_MARKERS = [
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


def v732_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "metadata_only": True,
        "lifecycle_view_only": True,
        "redacted_abstracted_experience_only": True,
        "lawyer_approval_required_for_runtime_load": True,
        "source_trace_required": True,
        "audit_required": True,
        "feedback_does_not_mutate_loaded_package": True,
        "candidate_pack_does_not_mutate_loaded_package": True,
        "next_package_requires_load_review": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_result_payload_returned": False,
        "source_content_returned": False,
        "source_material_returned": False,
        "full_output_returned": False,
        "case_material_returned": False,
        "loaded_package_mutated": False,
        "next_package_draft_auto_loaded": False,
        "automatic_training_triggered": False,
        "skill_updated": False,
        "skill_published": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def lifecycle_metadata_safe(payload: dict) -> bool:
    scan_text = str(payload).lower()
    return not any(marker in scan_text for marker in FORBIDDEN_LIFECYCLE_MARKERS)
