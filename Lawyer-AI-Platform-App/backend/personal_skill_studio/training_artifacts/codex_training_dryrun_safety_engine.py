import json

from personal_skill_studio.training_artifacts.training_dataset_safety_engine import (
    training_dataset_metadata_safe,
    v735_safety_flags,
)


def v736_safety_flags() -> dict[str, bool]:
    flags = v735_safety_flags()
    flags.update(
        {
            "codex_skill_dry_run": True,
            "internal_training_simulation_only": True,
            "provider_access_attempted": False,
            "provider_call_executed": False,
            "key_value_read": False,
            "runtime_package_written": False,
            "runtime_package_replaced": False,
            "loaded_package_auto_mutated": False,
            "lawyer_approved_package_auto_mutated": False,
            "real_training_triggered": False,
            "real_training_output_generated": False,
            "training_triggered": False,
            "skill_published": False,
        }
    )
    return flags


def codex_training_dryrun_metadata_safe(payload: dict) -> bool:
    serialized = json.dumps(payload, ensure_ascii=False)
    return training_dataset_metadata_safe(payload) and "provider_response" not in serialized.lower()
