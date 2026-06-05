from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_production.audit_engine import record_audit_event
from personal_case_production.case_production_runtime import get_production_case
from personal_case_production.schemas import StageRunList, StageRunMockRequest, StageRunRecord, WorkflowRunList, WorkflowRunMockRequest, WorkflowRunRecord
from personal_case_production.source_trace_engine import create_source_trace
from personal_case_production.storage import STAGE_RUNS_DIR, WORKFLOW_RUNS_DIR, read_payload, read_payloads, write_payload
from personal_case_production.workflow_registry import get_stage, required_stage_ids


def create_mock_workflow_run(request: WorkflowRunMockRequest) -> dict:
    if get_production_case(request.production_case_id) is None:
        raise HTTPException(status_code=404, detail="production_case_id 不存在")
    invalid = [stage_id for stage_id in request.selected_stage_ids if get_stage(stage_id) is None]
    if invalid:
        raise HTTPException(status_code=404, detail={"message": "stage_id 不存在", "stage_ids": invalid})
    if not request.explicit_mock_confirmation or not request.explicit_lawyer_review_confirmation or not request.explicit_no_final_opinion_confirmation or not request.explicit_no_external_delivery_confirmation:
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    workflow_run_id = f"personal_workflow_run_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    trace = create_source_trace(
        source_trace_id=f"case_production_source_trace_{workflow_run_id}_1",
        source_type="final_readiness_metadata",
        source_label="工作流运行 metadata placeholder",
        linked_object_type="workflow_run",
        linked_object_id=workflow_run_id,
        production_case_id=request.production_case_id,
        workflow_run_id=workflow_run_id,
        created_at=created_at,
    )
    selected = request.selected_stage_ids or required_stage_ids()
    record = WorkflowRunRecord(
        workflow_run_id=workflow_run_id,
        production_case_id=request.production_case_id,
        workflow_scope=request.workflow_scope,
        selected_stage_ids=selected,
        stage_summary={"selected_stage_count": len(selected), "mode": "mock"},
        readiness_summary={"readiness_status": "in_progress", "delivery_ready": False},
        source_trace_ids=[trace.source_trace_id],
        created_at=created_at,
        warnings=["模拟工作流不调用真实 provider，不生成最终法律意见或报告。"],
    )
    write_payload(WORKFLOW_RUNS_DIR, workflow_run_id, record.model_dump())
    record_audit_event(action="workflow_run_mock_created", actor="system", object_type="workflow_run", object_id=workflow_run_id, timestamp=created_at)
    return record.model_dump()


def get_workflow_run(workflow_run_id: str) -> WorkflowRunRecord | None:
    payload = read_payload(WORKFLOW_RUNS_DIR, workflow_run_id)
    return WorkflowRunRecord(**payload) if payload else None


def list_workflow_runs() -> list[WorkflowRunRecord]:
    return [WorkflowRunRecord(**payload) for payload in read_payloads(WORKFLOW_RUNS_DIR)]


def build_workflow_run_list() -> dict:
    records = sorted(list_workflow_runs(), key=lambda record: record.created_at, reverse=True)
    return WorkflowRunList(workflow_runs=records, run_count=len(records), warnings=["工作流列表仅包含 metadata。"]).model_dump()


def create_mock_stage_run(request: StageRunMockRequest) -> dict:
    workflow = get_workflow_run(request.workflow_run_id)
    if workflow is None:
        raise HTTPException(status_code=404, detail="workflow_run_id 不存在")
    if get_stage(request.stage_id) is None:
        raise HTTPException(status_code=404, detail="stage_id 不存在")
    if not request.explicit_mock_confirmation or not request.explicit_no_live_provider_confirmation or not request.explicit_no_final_opinion_confirmation:
        raise HTTPException(status_code=400, detail="confirmation 不完整")
    stage_run_id = f"personal_stage_run_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    trace = create_source_trace(
        source_trace_id=f"case_production_source_trace_{stage_run_id}_1",
        source_type=_source_type_for_stage(request.stage_id),
        source_label="阶段运行 metadata placeholder",
        linked_object_type="stage_run",
        linked_object_id=stage_run_id,
        production_case_id=workflow.production_case_id,
        workflow_run_id=workflow.workflow_run_id,
        stage_run_id=stage_run_id,
        created_at=created_at,
    )
    record = StageRunRecord(
        stage_run_id=stage_run_id,
        workflow_run_id=request.workflow_run_id,
        stage_id=request.stage_id,
        linked_runtime_object_ids=request.linked_runtime_object_ids,
        stage_result_metadata={"stage_note": request.stage_note or "模拟阶段已记录", "mode": "mock"},
        source_trace_ids=[trace.source_trace_id],
        created_at=created_at,
        warnings=["模拟阶段运行不调用真实 provider，不生成最终法律意见或报告。"],
    )
    write_payload(STAGE_RUNS_DIR, stage_run_id, record.model_dump())
    record_audit_event(action="stage_run_mock_created", actor="system", object_type="stage_run", object_id=stage_run_id, timestamp=created_at)
    return record.model_dump()


def get_stage_run(stage_run_id: str) -> StageRunRecord | None:
    payload = read_payload(STAGE_RUNS_DIR, stage_run_id)
    return StageRunRecord(**payload) if payload else None


def list_stage_runs() -> list[StageRunRecord]:
    return [StageRunRecord(**payload) for payload in read_payloads(STAGE_RUNS_DIR)]


def build_stage_run_list() -> dict:
    records = sorted(list_stage_runs(), key=lambda record: record.created_at, reverse=True)
    return StageRunList(stage_runs=records, stage_run_count=len(records), warnings=["阶段运行列表仅包含 metadata。"]).model_dump()


def _source_type_for_stage(stage_id: str) -> str:
    mapping = {
        "case_intake_stage": "case_metadata",
        "material_processing_stage": "material_runtime_metadata",
        "ai_draft_stage": "ai_gateway_metadata",
        "intelligence_check_stage": "personal_intelligence_metadata",
        "skill_studio_stage": "skill_studio_metadata",
        "lawyer_review_stage": "lawyer_review_metadata",
        "final_readiness_stage": "final_readiness_metadata",
    }
    return mapping.get(stage_id, "final_readiness_metadata")
