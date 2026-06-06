import json

from personal_skill_studio.training_artifacts.codex_training_dryrun_safety_engine import (
    codex_training_dryrun_metadata_safe,
    v736_safety_flags,
)


def v737_safety_flags() -> dict[str, bool]:
    flags = v736_safety_flags()
    flags.update(
        {
            "codex_skill_internal_training_run": True,
            "internal_training_workspace_only": True,
            "local_cpu_gpu_mode_allowed": True,
            "internal_model_metadata_generated": True,
            "training_metrics_generated": True,
            "dryrun_log_compared": True,
            "external_provider_training_triggered": False,
            "provider_access_attempted": False,
            "provider_call_executed": False,
            "key_value_read": False,
            "runtime_package_written": False,
            "runtime_package_replaced": False,
            "loaded_package_auto_mutated": False,
            "lawyer_approved_package_auto_mutated": False,
            "formal_training_set_written": False,
            "real_training_output_exported": False,
            "training_triggered": False,
            "skill_updated": False,
            "skill_published": False,
        }
    )
    return flags


def codex_training_run_metadata_safe(payload: dict) -> bool:
    serialized = json.dumps(payload, ensure_ascii=False).lower()
    return (
        codex_training_dryrun_metadata_safe(payload)
        and "model_path" not in serialized
        and "checkpoint_path" not in serialized
        and "storage/runtime" not in serialized
    )
