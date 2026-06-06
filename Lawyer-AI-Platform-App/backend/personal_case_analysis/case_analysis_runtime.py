from datetime import datetime, timezone
from uuid import uuid4

from fastapi import HTTPException

from personal_case_analysis.audit_engine import record_audit_event
from personal_case_analysis.evaluation_engine import create_evaluation_and_gate
from personal_case_analysis.fact_analysis_engine import create_mock_fact_draft
from personal_case_analysis.legal_analysis_engine import create_mock_legal_draft
from personal_case_analysis.schemas import (
    CaseAnalysisRunList,
    CaseAnalysisRunMockRequest,
    CaseAnalysisRunRecord,
    FactDraftMockRequest,
    LegalDraftMockRequest,
)
from personal_case_analysis.skill_loader import build_skill_baseline_report
from personal_case_analysis.source_trace_engine import create_source_trace
from personal_case_analysis.storage import RUNS_DIR, read_payload, read_payloads, write_payload


def _validate_request(request: CaseAnalysisRunMockRequest) -> list[str]:
    blocked: list[str] = []
    for field in [
        "explicit_mock_confirmation",
        "explicit_open_case_confirmation",
        "explicit_no_training_data_confirmation",
        "explicit_no_raw_content_confirmation",
        "explicit_lawyer_review_confirmation",
        "explicit_no_final_opinion_confirmation",
    ]:
        if not getattr(request, field):
            blocked.append(f"{field} 必须为 true")
    if not request.case_id.strip():
        blocked.append("case_id 不能为空")
    return blocked


def create_mock_run(request: CaseAnalysisRunMockRequest) -> dict:
    blocked = _validate_request(request)
    if blocked:
        raise HTTPException(status_code=400, detail={"message": "受控案件分析 run 请求被阻断。", "blocked_reasons": blocked})
    run_id = f"case_analysis_run_{uuid4().hex[:12]}"
    created_at = datetime.now(timezone.utc).isoformat()
    baseline_report = build_skill_baseline_report()
    baseline_ids = [baseline["source_skill_id"] for baseline in baseline_report["baselines"]]
    trace = create_source_trace(
        source_trace_id=f"case_analysis_source_trace_{run_id}_1",
        source_type="case_analysis_run_metadata",
        source_label="受控案件分析 run metadata",
        linked_object_type="case_analysis_run",
        linked_object_id=run_id,
        case_id=request.case_id,
        run_id=run_id,
        created_at=created_at,
    )
    fact_payload = create_mock_fact_draft(
        FactDraftMockRequest(
            case_id=request.case_id,
            run_id=run_id,
            source_trace_ids=[*request.source_trace_ids, trace.source_trace_id],
            material_metadata_ids=request.material_metadata_ids,
            explicit_mock_confirmation=True,
            explicit_no_training_data_confirmation=True,
            explicit_no_raw_content_confirmation=True,
            explicit_lawyer_review_confirmation=True,
        )
    )
    legal_payload = create_mock_legal_draft(
        LegalDraftMockRequest(
            case_id=request.case_id,
            fact_draft_id=fact_payload["fact_draft_id"],
            source_trace_ids=fact_payload["source_trace_ids"],
            explicit_mock_confirmation=True,
            explicit_no_training_data_confirmation=True,
            explicit_no_raw_content_confirmation=True,
            explicit_lawyer_review_confirmation=True,
            explicit_no_final_opinion_confirmation=True,
        )
    )
    evaluation, gate = create_evaluation_and_gate(
        run_id=run_id,
        fact_draft_id=fact_payload["fact_draft_id"],
        legal_draft_id=legal_payload["legal_draft_id"],
        created_at=created_at,
    )
    record = CaseAnalysisRunRecord(
        run_id=run_id,
        case_id=request.case_id,
        case_alias=request.case_alias,
        analysis_scope=request.analysis_scope,
        stage_status={
            "fact_analysis": "draft_created",
            "legal_analysis": "draft_created",
            "review_readiness": "pending_lawyer_review",
        },
        selected_skill_ids=request.selected_skill_ids or ["case_fact_extraction_skill", "case_legal_analysis_skill"],
        skill_baseline_ids=baseline_ids,
        fact_draft_id=fact_payload["fact_draft_id"],
        legal_draft_id=legal_payload["legal_draft_id"],
        evaluation_id=evaluation.evaluation_id,
        gate_id=gate.gate_id,
        review_item_ids=[*fact_payload.get("review_item_ids", []), *legal_payload.get("review_item_ids", [])],
        source_trace_ids=list(dict.fromkeys([trace.source_trace_id, *fact_payload["source_trace_ids"], *legal_payload["source_trace_ids"]])),
        created_at=created_at,
        warnings=[
            "v7.16 run 仅为未结案件实战分析 draft metadata。",
            "不会写入训练集、不会更新 Skill、不会发布 Skill。",
            "不会生成最终法律意见、最终报告或真实交付文件。",
        ],
    )
    write_payload(RUNS_DIR, run_id, record.model_dump())
    record_audit_event(action="case_analysis_run_mock_created", actor="system", object_type="case_analysis_run", object_id=run_id, timestamp=created_at)
    payload = record.model_dump()
    payload["skill_baseline_report"] = baseline_report
    payload["fact_draft"] = fact_payload
    payload["legal_draft"] = legal_payload
    payload["evaluation"] = evaluation.model_dump()
    payload["gate"] = gate.model_dump()
    return payload


def get_run(run_id: str) -> CaseAnalysisRunRecord | None:
    payload = read_payload(RUNS_DIR, run_id)
    return CaseAnalysisRunRecord(**payload) if payload else None


def list_runs() -> list[CaseAnalysisRunRecord]:
    return [CaseAnalysisRunRecord(**payload) for payload in read_payloads(RUNS_DIR)]


def build_run_list() -> dict:
    runs = sorted(list_runs(), key=lambda run: run.created_at, reverse=True)
    return CaseAnalysisRunList(
        runs=runs,
        run_count=len(runs),
        warnings=["受控案件分析 run 列表仅包含 draft metadata，不包含 raw content 或训练样本。"],
    ).model_dump()


build_runtime = build_run_list
