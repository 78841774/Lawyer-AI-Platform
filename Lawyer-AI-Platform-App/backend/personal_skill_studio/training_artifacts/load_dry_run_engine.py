from uuid import uuid4

from personal_skill_studio.training_artifacts.case_cause_matcher import match_case_cause
from personal_skill_studio.training_artifacts.schemas import (
    LoadDryRunRecord,
    LoadDryRunRequest,
    SkillContextManifest,
)
from personal_skill_studio.training_artifacts.skill_context_builder import build_skill_context
from personal_skill_studio.training_artifacts.storage import LOAD_DRY_RUNS_DIR, read_payload, read_payloads, write_payload


def create_load_dry_run(request: LoadDryRunRequest) -> dict:
    match_result = match_case_cause(request)
    skill_context = build_skill_context(match_result, request.target_skill_ids)
    run_id = f"training_artifact_load_dry_run_{uuid4().hex[:12]}"
    record = LoadDryRunRecord(
        run_id=run_id,
        match_result=match_result,
        skill_context=skill_context,
        warnings=[
            "Dry-run only: no training, no Skill update, no Skill publish, no provider call.",
            "Open-case data is not used for training artifacts.",
        ],
    )
    write_payload(LOAD_DRY_RUNS_DIR, run_id, record.model_dump())
    return record.model_dump()


def list_load_dry_runs() -> dict:
    runs = [LoadDryRunRecord(**payload).model_dump() for payload in read_payloads(LOAD_DRY_RUNS_DIR)]
    return {
        "load_dry_runs": runs,
        "run_count": len(runs),
        "owner_only": True,
        "metadata_only": True,
        "training_artifact_only": True,
        "codex_training_scheme": True,
        "fine_tune_model_training": False,
        "closed_case_only": True,
        "open_case_data_used": False,
        "raw_content_included": False,
        "raw_ocr_content_included": False,
        "api_key_exposed": False,
        "secret_value_returned": False,
        "local_path_exposed": False,
        "training_data_generated": False,
        "writes_to_training_set": False,
        "skill_updated": False,
        "skill_published": False,
        "skill_auto_published": False,
        "case_cause_taxonomy_required": True,
        "multi_level_case_cause_enabled": True,
        "case_cause_match_required": True,
        "fallback_supported": True,
        "load_dry_run": True,
        "load_executed": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
        "gate_reference_only": True,
        "blocks_next_stage": False,
        "audit_required": True,
    }


def get_load_dry_run(run_id: str) -> dict | None:
    payload = read_payload(LOAD_DRY_RUNS_DIR, run_id)
    return LoadDryRunRecord(**payload).model_dump() if payload else None


def list_skill_contexts() -> dict:
    contexts = [
        LoadDryRunRecord(**payload).skill_context.model_dump()
        for payload in read_payloads(LOAD_DRY_RUNS_DIR)
    ]
    if not contexts:
        contexts = [
            build_skill_context(
                match_case_cause(LoadDryRunRequest()),
                ["case_fact_extraction_skill", "case_legal_analysis_skill"],
            ).model_dump()
        ]
    return {
        "skill_contexts": contexts,
        "skill_context_count": len(contexts),
        "owner_only": True,
        "metadata_only": True,
        "training_artifact_only": True,
        "codex_training_scheme": True,
        "fine_tune_model_training": False,
        "closed_case_only": True,
        "open_case_data_used": False,
        "raw_content_included": False,
        "raw_ocr_content_included": False,
        "api_key_exposed": False,
        "secret_value_returned": False,
        "local_path_exposed": False,
        "training_data_generated": False,
        "writes_to_training_set": False,
        "skill_updated": False,
        "skill_published": False,
        "skill_auto_published": False,
        "case_cause_taxonomy_required": True,
        "multi_level_case_cause_enabled": True,
        "case_cause_match_required": True,
        "fallback_supported": True,
        "load_dry_run": True,
        "load_executed": False,
        "final_legal_opinion_generated": False,
        "final_report_generated": False,
        "public_link_created": False,
        "email_sent": False,
        "external_delivery_triggered": False,
        "gate_reference_only": True,
        "blocks_next_stage": False,
        "audit_required": True,
    }


def get_skill_context(skill_context_id: str) -> SkillContextManifest | None:
    for payload in read_payloads(LOAD_DRY_RUNS_DIR):
        context = LoadDryRunRecord(**payload).skill_context
        if context.skill_context_id == skill_context_id:
            return context
    default_context = build_skill_context(match_case_cause(LoadDryRunRequest()), ["case_fact_extraction_skill", "case_legal_analysis_skill"])
    if default_context.skill_context_id == skill_context_id:
        return default_context
    return None

