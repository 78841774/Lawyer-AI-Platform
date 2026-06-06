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


def build_practice_runtime_audit_summary() -> dict:
    from personal_skill_studio.training_artifacts.practice_runtime_registry import list_runtime_load_records
    from personal_skill_studio.training_artifacts.practice_runtime_safety_engine import v731g_safety_flags

    records = list_runtime_load_records()
    events = [
        event.model_dump()
        for record in records
        for event in record.audit_events
    ]
    return {
        "events": events,
        "event_count": len(events),
        "runtime_load_count": len(records),
        **v731g_safety_flags(),
        "warnings": ["Practice runtime audit records are metadata-only and preserve source trace lineage."],
    }


def build_practice_feedback_audit_summary() -> dict:
    from personal_skill_studio.training_artifacts.practice_feedback_registry import (
        list_feedback_records,
        list_feedback_risk_event_records,
        list_observation_records,
    )
    from personal_skill_studio.training_artifacts.practice_feedback_safety_engine import v731h_safety_flags

    observations = list_observation_records()
    feedback_items = list_feedback_records()
    risk_events = list_feedback_risk_event_records()
    events = [
        event.model_dump()
        for record in [*observations, *feedback_items, *risk_events]
        for event in record.audit_events
    ]
    return {
        "events": events,
        "event_count": len(events),
        "observation_count": len(observations),
        "feedback_count": len(feedback_items),
        "risk_event_count": len(risk_events),
        **v731h_safety_flags(),
        "warnings": ["Practice feedback audit records are metadata-only and do not mutate runtime packages."],
    }


def build_iteration_candidate_audit_summary() -> dict:
    from personal_skill_studio.training_artifacts.iteration_candidate_safety_engine import v731i_safety_flags
    from personal_skill_studio.training_artifacts.practice_feedback_candidate_pack import list_candidate_pack_records

    records = list_candidate_pack_records()
    events = [
        event.model_dump()
        for record in records
        for event in record.audit_events
    ]
    return {
        "events": events,
        "event_count": len(events),
        "candidate_pack_count": len(records),
        **v731i_safety_flags(),
        "warnings": ["Iteration candidate audit records are metadata-only and do not mutate packages."],
    }


def build_next_package_audit_summary() -> dict:
    from personal_skill_studio.training_artifacts.next_experience_package_registry import list_next_package_records
    from personal_skill_studio.training_artifacts.next_package_safety_engine import v731j_safety_flags

    records = list_next_package_records()
    events = [
        event.model_dump()
        for record in records
        for event in record.audit_events
    ]
    return {
        "events": events,
        "event_count": len(events),
        "next_package_count": len(records),
        **v731j_safety_flags(),
        "warnings": ["Next package audit records are metadata-only and do not load runtime packages."],
    }


def build_case_analysis_workbench_audit_summary() -> dict:
    from personal_skill_studio.training_artifacts.case_analysis_output_safety_engine import v733_safety_flags
    from personal_skill_studio.training_artifacts.case_analysis_runtime_output_registry import list_workbench_views

    views = list_workbench_views().get("views", [])
    events = [
        {
            "event_id": f"{view.get('view_id')}_schema_rendered",
            "action": "schema_driven_workbench_view_rendered",
            "object_type": "case_analysis_workbench_view",
            "object_id": view.get("view_id"),
            "metadata_only": True,
            "schema_driven_output_only": True,
        }
        for view in views
    ]
    return {
        "events": events,
        "event_count": len(events),
        "view_count": len(views),
        **v733_safety_flags(),
        "warnings": ["Case analysis workbench audit records are metadata-only and schema-driven."],
    }


def build_case_analysis_improvement_audit_summary() -> dict:
    from personal_skill_studio.training_artifacts.case_analysis_improvement_candidate_registry import (
        list_case_analysis_improvement_candidates,
    )
    from personal_skill_studio.training_artifacts.case_analysis_improvement_safety_engine import v734_safety_flags

    candidates = list_case_analysis_improvement_candidates().get("candidates", [])
    events = [
        {
            "event_id": f"{candidate.get('candidate_id')}_improvement_mapped",
            "action": "case_analysis_feedback_mapped_to_improvement_candidate",
            "object_type": "case_analysis_improvement_candidate",
            "object_id": candidate.get("candidate_id"),
            "metadata_only": True,
            "training_triggered": False,
            "loaded_package_mutated": False,
        }
        for candidate in candidates
    ]
    return {
        "events": events,
        "event_count": len(events),
        "candidate_count": len(candidates),
        **v734_safety_flags(),
        "warnings": ["Case analysis improvement audit records are metadata-only and do not mutate packages."],
    }
