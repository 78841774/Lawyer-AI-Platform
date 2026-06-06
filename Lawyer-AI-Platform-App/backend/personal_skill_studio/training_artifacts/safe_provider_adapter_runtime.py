import os
from datetime import UTC, datetime
from typing import Any


PROVIDER_SPECS: list[dict[str, Any]] = [
    {
        "provider_type": "OCR_API",
        "provider_category": "ocr_document",
        "credential_alias": "PADDLEOCR_AISTUDIO_CREDENTIAL",
        "credential_loaded": False,
        "gate_requirements": [
            "credential_loaded=True",
            "provider_gate=True",
            "manual_approval=True",
            "source_trace_required=True",
            "audit_required=True",
        ],
        "allowed_methods": ["submit_ocr_job", "get_ocr_job_status"],
        "output_schema": {
            "job_status": "string",
            "quality_score": "number",
            "redacted_preview_available": "boolean",
            "source_trace_id": "string",
            "audit_id": "string",
        },
    },
    {
        "provider_type": "Legal_API",
        "provider_category": "legal_retrieval",
        "credential_alias": "FAZHI_LAW_CREDENTIAL",
        "credential_loaded": False,
        "gate_requirements": [
            "credential_loaded=True",
            "provider_gate=True",
            "lawyer_review_required=True",
            "source_trace_required=True",
            "audit_required=True",
        ],
        "allowed_methods": ["search_statutes", "search_case_law", "summarize_rule_candidates"],
        "output_schema": {
            "retrieval_status": "string",
            "statute_candidates": "metadata[]",
            "case_law_candidates": "metadata[]",
            "review_required": "boolean",
            "source_trace_id": "string",
            "audit_id": "string",
        },
    },
    {
        "provider_type": "Enterprise_API",
        "provider_category": "enterprise_lookup",
        "credential_alias": "TIANYANCHA_AI_CREDENTIAL",
        "credential_loaded": False,
        "gate_requirements": [
            "credential_loaded=True",
            "provider_gate=True",
            "verification_only=True",
            "source_trace_required=True",
            "audit_required=True",
        ],
        "allowed_methods": ["lookup_enterprise_profile", "verify_enterprise_status"],
        "output_schema": {
            "lookup_status": "string",
            "verification_candidates": "metadata[]",
            "not_final_fact_finding": "boolean",
            "source_trace_id": "string",
            "audit_id": "string",
        },
    },
]


def provider_specs_with_loaded_state() -> list[dict[str, Any]]:
    return [_with_loaded_state(spec) for spec in PROVIDER_SPECS]


def list_provider_adapters() -> dict[str, Any]:
    specs = provider_specs_with_loaded_state()
    return _safe_response(
        {
            "provider_specs": specs,
            "provider_count": len(specs),
            "all_credentials_loaded": all(spec["credential_loaded"] for spec in specs),
            "warnings": [
                "Adapter status checks only credential presence by alias and never returns credential values.",
                "Current stage keeps live provider execution disabled by default.",
            ],
        }
    )


def provider_adapter_status(provider_type: str) -> dict[str, Any] | None:
    spec = next((item for item in provider_specs_with_loaded_state() if item["provider_type"] == provider_type), None)
    if spec is None:
        return None
    return _safe_response(
        {
            "provider_type": spec["provider_type"],
            "credential_alias": spec["credential_alias"],
            "credential_loaded": spec["credential_loaded"],
            "adapter_status": "credential_ready_provider_gated" if spec["credential_loaded"] else "credential_not_loaded",
            "client_initialized": bool(spec["credential_loaded"]),
            "gate_requirements": spec["gate_requirements"],
            "allowed_methods": spec["allowed_methods"],
            "live_call_executed": False,
            "audit_id": f"{spec['provider_type'].lower()}_adapter_audit",
            "source_trace_id": f"{spec['provider_type'].lower()}_adapter_source_trace",
            "warnings": ["No credential value is returned to Skill, frontend, logs, docs, or regression output."],
        }
    )


def call_provider_placeholder(provider_type: str, method_name: str | None = None) -> dict[str, Any] | None:
    spec = next((item for item in provider_specs_with_loaded_state() if item["provider_type"] == provider_type), None)
    if spec is None:
        return None
    method = method_name or spec["allowed_methods"][0]
    gate_passed = spec["credential_loaded"]
    return _safe_response(
        {
            "provider_type": spec["provider_type"],
            "credential_alias": spec["credential_alias"],
            "credential_loaded": spec["credential_loaded"],
            "method_name": method,
            "gate_status": "ready_provider_gated" if gate_passed else "blocked_credential_not_loaded",
            "live_call_allowed": False,
            "live_call_executed": False,
            "result_status": "placeholder_only_current_stage",
            "result_metadata": {
                "status": "not_executed",
                "reason": "current_training_skill_stage_keeps_provider_calls_disabled",
            },
            "audit": {
                "audit_id": f"{spec['provider_type'].lower()}_{method}_audit",
                "events": [{"event": "adapter_placeholder_checked", "status": "metadata_only"}],
                "event_count": 1,
            },
            "source_trace": {
                "source_trace_id": f"{spec['provider_type'].lower()}_{method}_source_trace",
                "trace_status": "placeholder_metadata_only",
            },
            "warnings": [
                "Skill may receive status/result metadata only; it never receives credential values.",
                "Real provider execution requires a later explicitly enabled provider-gated adapter path.",
            ],
        }
    )


def _with_loaded_state(spec: dict[str, Any]) -> dict[str, Any]:
    loaded = spec["credential_alias"] in os.environ
    return {**spec, "credential_loaded": loaded}


def _safe_response(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "owner_only": True,
        "metadata_only": True,
        "provider_gated": True,
        "credential_value_returned": False,
        "key_value_read": False,
        "provider_call_executed": False,
        "source_content_returned": False,
        "case_material_returned": False,
        "filesystem_location_exposed": False,
        "skill_published": False,
        "runtime_package_replaced": False,
        "source_trace_required": True,
        "audit_required": True,
        "created_at": datetime.now(UTC).isoformat(),
        **payload,
    }
