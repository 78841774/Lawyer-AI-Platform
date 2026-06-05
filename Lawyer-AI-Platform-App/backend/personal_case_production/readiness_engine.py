from personal_case_production.audit_engine import record_audit_event
from personal_case_production.case_production_runtime import get_production_case, list_production_cases
from personal_case_production.schemas import ProductionReadiness, ProductionReadinessList
from personal_case_production.stage_orchestrator import list_stage_runs
from personal_case_production.workflow_registry import required_stage_ids


def build_readiness_list() -> dict:
    readiness = [build_case_readiness_record(case.production_case_id) for case in list_production_cases()]
    return ProductionReadinessList(
        readiness=readiness,
        readiness_count=len(readiness),
        warnings=["准备度检查仅返回生产流程 metadata，不触发交付。"],
    ).model_dump()


def build_case_readiness(production_case_id: str) -> dict | None:
    if get_production_case(production_case_id) is None:
        return None
    record = build_case_readiness_record(production_case_id)
    record_audit_event(
        action="readiness_checked",
        actor="system",
        object_type="production_case",
        object_id=production_case_id,
        timestamp=_latest_timestamp(record),
    )
    return record.model_dump()


def build_case_readiness_record(production_case_id: str) -> ProductionReadiness:
    required = required_stage_ids()
    completed = {
        stage.stage_id
        for stage in list_stage_runs()
        if _workflow_belongs_to_case(stage.workflow_run_id, production_case_id)
    }
    missing = [stage_id for stage_id in required if stage_id not in completed]
    completed_count = len(required) - len(missing)
    readiness_status = "not_ready"
    if completed_count:
        readiness_status = "in_progress"
    if completed_count >= len(required) - 1:
        readiness_status = "review_required"
    if completed_count == len(required):
        readiness_status = "ready_for_final_gate"
    return ProductionReadiness(
        production_case_id=production_case_id,
        readiness_status=readiness_status,
        completed_stage_count=completed_count,
        required_stage_count=len(required),
        missing_stage_ids=missing,
        risk_flags=[] if not missing else ["仍有阶段未完成或待复核"],
        lawyer_review_completed="lawyer_review_stage" in completed,
        source_trace_complete=completed_count > 0,
        final_gate_ready=readiness_status == "ready_for_final_gate",
        delivery_ready=False,
        checklist=[
            "律师复核必需",
            "最终门禁必需",
            "不生成最终法律意见",
            "不生成最终报告",
            "不自动对外交付",
        ],
    )


def _workflow_belongs_to_case(workflow_run_id: str, production_case_id: str) -> bool:
    from personal_case_production.stage_orchestrator import get_workflow_run

    workflow = get_workflow_run(workflow_run_id)
    return bool(workflow and workflow.production_case_id == production_case_id)


def _latest_timestamp(record: ProductionReadiness) -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()
