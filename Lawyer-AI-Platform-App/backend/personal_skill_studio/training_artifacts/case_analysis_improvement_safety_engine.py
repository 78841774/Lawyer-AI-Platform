import json

from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import (
    FORBIDDEN_MARKERS,
    v733_safety_flags,
)


def v734_safety_flags() -> dict[str, bool]:
    flags = v733_safety_flags()
    flags.update(
        {
            "improvement_candidate_only": True,
            "redacted_abstracted_metadata_only": True,
            "output_feedback_input_only": True,
            "risk_event_input_only": True,
            "loaded_package_auto_mutated": False,
            "lawyer_approved_package_auto_mutated": False,
            "output_schema_auto_mutated": False,
            "runtime_package_auto_replaced": False,
            "training_dataset_auto_built": False,
            "training_gate_required": True,
            "package_disable_auto_executed": False,
            "package_rollback_auto_executed": False,
        }
    )
    return flags


def case_analysis_improvement_metadata_safe(payload: dict) -> bool:
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    return not any(marker in serialized for marker in FORBIDDEN_MARKERS)
