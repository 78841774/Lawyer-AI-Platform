import json

from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import (
    case_analysis_improvement_metadata_safe,
    v734_safety_flags,
)


def v735_safety_flags() -> dict[str, bool]:
    flags = v734_safety_flags()
    flags.update(
        {
            "training_dataset_manifest_generated": True,
            "training_examples_generated": True,
            "training_task_plan_generated": True,
            "training_gate_report_generated": True,
            "gate_reference_only": True,
            "quality_reference_only": True,
            "blocks_next_stage": False,
            "ready_candidate_only": True,
            "candidate_audit_checked": True,
            "source_trace_checked": True,
            "sensitive_metadata_scan_required": True,
            "sensitive_metadata_scan_passed": True,
            "experience_package_loaded_as_metadata": True,
            "skill_output_schema_loaded_as_metadata": True,
            "output_to_experience_trace_loaded_as_metadata": True,
            "loaded_package_auto_mutated": False,
            "lawyer_approved_package_auto_mutated": False,
            "runtime_package_auto_replaced": False,
            "formal_training_set_written": False,
            "real_training_triggered": False,
            "real_training_output_generated": False,
            "skill_updated": False,
            "skill_published": False,
            "training_triggered": False,
        }
    )
    return flags


def training_dataset_metadata_safe(payload: dict) -> bool:
    serialized = json.dumps(payload, ensure_ascii=False)
    return case_analysis_improvement_metadata_safe(payload) and "storage/runtime" not in serialized
