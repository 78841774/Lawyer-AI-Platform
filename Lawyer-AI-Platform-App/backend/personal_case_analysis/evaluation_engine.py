from datetime import datetime, timezone
from uuid import uuid4

from personal_case_analysis.schemas import (
    CaseAnalysisEvaluation,
    CaseAnalysisEvaluationList,
    CaseAnalysisGate,
    CaseAnalysisGateList,
)
from personal_case_analysis.storage import EVALUATIONS_DIR, GATES_DIR, read_payload, read_payloads, write_payload


def create_evaluation_and_gate(
    *,
    run_id: str | None,
    fact_draft_id: str | None,
    legal_draft_id: str | None,
    created_at: str | None = None,
) -> tuple[CaseAnalysisEvaluation, CaseAnalysisGate]:
    timestamp = created_at or datetime.now(timezone.utc).isoformat()
    evaluation_id = f"case_analysis_evaluation_{uuid4().hex[:12]}"
    gate_id = f"case_analysis_gate_{uuid4().hex[:12]}"
    evaluation = CaseAnalysisEvaluation(
        evaluation_id=evaluation_id,
        run_id=run_id,
        fact_draft_id=fact_draft_id,
        legal_draft_id=legal_draft_id,
        fact_scores={
            "fact_draft_readability": 74,
            "reviewability": 72,
            "evidence_mapping_reviewability": 68,
            "missing_information_value": 80,
            "confidence_flag_quality": 76,
            "source_trace_runtime_completeness": 60,
        },
        legal_scores={
            "legal_relationship_draft_quality": 72,
            "issue_spotting_helpfulness": 76,
            "claim_basis_coverage": 68,
            "defense_path_coverage": 66,
            "burden_of_proof_clarity": 75,
            "risk_warning_value": 82,
            "next_action_checklist_value": 78,
        },
        optimization_notes=[
            "补齐律师确认后的事实链再进入下一阶段。",
            "来源追踪完整前不得作为最终引用。",
            "低置信度项仅用于修订方向，不进入训练集。",
        ],
        created_at=timestamp,
        warnings=["Evaluation 仅作为本案 draft 质量评分和优化方向，不阻断下一步，不产生训练数据。"],
    )
    gate = CaseAnalysisGate(
        gate_id=gate_id,
        run_id=run_id,
        fact_draft_id=fact_draft_id,
        legal_draft_id=legal_draft_id,
        readiness={
            "fact_review_required": True,
            "legal_review_required": True,
            "source_trace_complete": False,
            "delivery_packet_ready": False,
            "blocks_next_stage": False,
        },
        low_confidence_flags=["source_trace_incomplete", "lawyer_review_pending"],
        missing_information_checklist=["补充证据链 metadata", "确认法律检索候选来源", "律师复核事实争议点"],
        source_trace_complete=False,
        created_at=timestamp,
        warnings=["Gate 为 reference-only，不阻断下一步流程，不触发交付包或最终报告。"],
    )
    write_payload(EVALUATIONS_DIR, evaluation_id, evaluation.model_dump())
    write_payload(GATES_DIR, gate_id, gate.model_dump())
    return evaluation, gate


def get_evaluation(evaluation_id: str) -> CaseAnalysisEvaluation | None:
    payload = read_payload(EVALUATIONS_DIR, evaluation_id)
    return CaseAnalysisEvaluation(**payload) if payload else None


def list_evaluations() -> list[CaseAnalysisEvaluation]:
    return [CaseAnalysisEvaluation(**payload) for payload in read_payloads(EVALUATIONS_DIR)]


def build_evaluation_list() -> dict:
    records = sorted(list_evaluations(), key=lambda record: record.created_at, reverse=True)
    return CaseAnalysisEvaluationList(
        evaluations=records,
        evaluation_count=len(records),
        warnings=["评价结果仅用于本案 draft 质量评分，不写入 v7.15 训练评价。"],
    ).model_dump()


def get_gate(gate_id: str) -> CaseAnalysisGate | None:
    payload = read_payload(GATES_DIR, gate_id)
    return CaseAnalysisGate(**payload) if payload else None


def list_gates() -> list[CaseAnalysisGate]:
    return [CaseAnalysisGate(**payload) for payload in read_payloads(GATES_DIR)]


def build_gate_list() -> dict:
    records = sorted(list_gates(), key=lambda record: record.created_at, reverse=True)
    return CaseAnalysisGateList(
        gates=records,
        gate_count=len(records),
        warnings=["Gate 仅作为质量参考，不阻断下一步，不生成最终交付。"],
    ).model_dump()
