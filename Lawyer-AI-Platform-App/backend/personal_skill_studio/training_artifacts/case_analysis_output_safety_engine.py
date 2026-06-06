import json


FORBIDDEN_MARKERS = [
    "raw_text",
    "ocr_text",
    "original_text",
    "full_document_text",
    "raw_material",
    "raw_case_material",
    "local_path",
    "file_path",
    "absolute_path",
    "api_key",
    "secret",
    "private_key",
    "access_token",
    "refresh_token",
    "provider_response",
    "provider_raw_response",
    "unredacted",
]


def v733_safety_flags() -> dict[str, bool]:
    return {
        "owner_only": True,
        "metadata_only": True,
        "schema_driven_output_only": True,
        "redacted_abstracted_output_only": True,
        "frontend_output_definition_forbidden": True,
        "lawyer_review_required": True,
        "source_trace_required": True,
        "audit_required": True,
        "provider_call_executed": False,
        "key_value_read": False,
        "credential_value_returned": False,
        "provider_payload_returned": False,
        "source_content_returned": False,
        "case_material_returned": False,
        "loaded_package_mutated": False,
        "next_package_auto_generated": False,
        "training_triggered": False,
        "skill_published": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
    }


def case_analysis_output_metadata_safe(payload: dict) -> bool:
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    return not any(marker in serialized for marker in FORBIDDEN_MARKERS)
