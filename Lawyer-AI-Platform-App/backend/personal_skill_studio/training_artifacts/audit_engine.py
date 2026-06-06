from personal_skill_studio.training_artifacts.load_dry_run_engine import list_load_dry_runs
from personal_skill_studio.training_artifacts.schemas import safety_flags


def build_audit() -> dict:
    runs = list_load_dry_runs().get("load_dry_runs", [])
    return {
        "events": [
            {
                "event_id": "training_artifact_loader_registered",
                "action": "register_metadata_loader",
                "object_type": "codex_training_scheme",
                "object_id": "codex_training_scheme_v7_30",
                "metadata_only": True,
                "load_executed": False,
            },
            *[
                {
                    "event_id": run.get("run_id"),
                    "action": "load_dry_run",
                    "object_type": "skill_context_manifest",
                    "object_id": run.get("skill_context", {}).get("skill_context_id"),
                    "metadata_only": True,
                    "load_executed": False,
                }
                for run in runs
            ],
        ],
        "event_count": len(runs) + 1,
        **safety_flags(),
        "warnings": ["Audit records are metadata-only and do not include raw content."],
    }

