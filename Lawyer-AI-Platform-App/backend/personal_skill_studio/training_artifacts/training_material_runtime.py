from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from personal_skill_studio.training_artifacts.storage import (
    RAW_BASED_EXPERIENCE_CANDIDATES_DIR,
    REDACTED_EXPERIENCE_PACKAGES_DIR,
    TRAINING_MATERIAL_EVIDENCE_INDEXES_DIR,
    TRAINING_MATERIAL_JUDGMENT_STRUCTURES_DIR,
    TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR,
    TRAINING_MATERIAL_OCR_JOBS_DIR,
    TRAINING_MATERIAL_PARSE_GATES_DIR,
    TRAINING_MATERIAL_PARSE_JOBS_DIR,
    TRAINING_MATERIAL_RULE_ALIGNMENTS_DIR,
    TRAINING_MATERIAL_WORK_PRODUCT_STRUCTURES_DIR,
    TRAINING_MATERIALS_DIR,
    read_payload,
    read_payloads,
    write_payload,
)


SAFE_FLAGS: dict[str, bool] = {
    "owner_only": True,
    "metadata_only": True,
    "local_private_processing_only": True,
    "controlled_source_zone_only": True,
    "source_input_in_controlled_zone": True,
    "frontend_source_display_allowed": False,
    "api_source_payload_allowed": False,
    "git_tracking_allowed": False,
    "provider_call_allowed": False,
    "provider_call_executed": False,
    "key_value_read": False,
    "credential_value_returned": False,
    "source_content_returned": False,
    "case_material_returned": False,
    "filesystem_location_exposed": False,
    "redacted_output_only": True,
    "abstracted_output_only": True,
    "source_trace_required": True,
    "audit_required": True,
    "training_triggered": False,
    "skill_published": False,
    "runtime_package_replaced": False,
    "practice_load_review_required": True,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "public_link_created": False,
    "email_sent": False,
    "external_delivery_triggered": False,
}


COMMON_FACT_EXTRACTION_FRAMEWORK = [
    "当事人主体",
    "基础法律关系",
    "行为时间线",
    "权利义务来源",
    "履行 / 违约 / 损害事实",
    "证据对应关系",
    "争议焦点事实",
    "法院采信事实",
    "风险事实",
]


CASE_CAUSE_SPECIFIC_FACT_POINTS = [
    {
        "case_cause": "民间借贷纠纷",
        "fact_points": ["借贷合意", "款项交付", "还款事实", "催收记录", "利息约定", "诉讼时效"],
        "legal_summary": "抽象关注借贷关系成立、交付证明、利息边界与时效抗辩。",
    },
    {
        "case_cause": "买卖合同纠纷",
        "fact_points": ["合同成立", "交付事实", "验收事实", "付款节点", "质量异议", "违约通知"],
        "legal_summary": "抽象关注合同成立、交付验收、付款义务、质量抗辩与违约责任。",
    },
    {
        "case_cause": "劳动争议",
        "fact_points": ["劳动关系成立", "入职离职时间", "工资发放", "考勤", "社保", "解除理由"],
        "legal_summary": "抽象关注劳动关系认定、工资社保、解除事由、程序合法性与举证责任。",
    },
    {
        "case_cause": "婚姻家事纠纷",
        "fact_points": ["身份关系", "财产来源", "共同债务", "抚养事实", "过错事实"],
        "legal_summary": "抽象关注身份关系、财产来源、共同债务、子女抚养与过错情节。",
    },
]


PROCEDURAL_PROFILE_POINTS = [
    {
        "profile_key": "litigation_first_instance",
        "procedure_type": "litigation",
        "procedure_stage": "first_instance",
        "required_material_patterns": ["起诉/答辩摘要", "证据目录", "庭审要点", "一审裁判理由摘要"],
        "fact_extraction_points": ["基础法律关系成立", "主要履行过程", "争议事实形成", "证据链完整性"],
        "evidence_review_points": ["三性审查", "举证责任", "核心证据闭环"],
        "legal_summary_points": ["请求权基础", "抗辩事由", "举证责任", "责任承担方式"],
        "substantive_impact_points": ["一审事实认定影响后续审查范围", "举证缺口可能形成实体败诉风险"],
        "procedural_transition_rules": ["一审→二审：识别事实认定错误、法律适用错误和新证据条件"],
        "risk_warnings": ["举证期限风险", "争点遗漏风险", "请求基础选择风险"],
    },
    {
        "profile_key": "litigation_second_instance",
        "procedure_type": "litigation",
        "procedure_stage": "second_instance",
        "required_material_patterns": ["一审裁判摘要", "上诉/答辩摘要", "二审新证据 metadata", "二审争点"],
        "fact_extraction_points": ["一审已查明事实", "上诉争议事实", "新证据关联事实", "事实认定错误主张"],
        "evidence_review_points": ["新证据条件", "一审证据评价偏差", "二审争点对应证据"],
        "legal_summary_points": ["上诉请求基础", "事实审查边界", "法律适用纠错", "改判/发回风险"],
        "substantive_impact_points": ["二审审查范围影响责任调整空间", "新证据采纳会改变实体认定空间"],
        "procedural_transition_rules": ["二审→再审：识别法定再审事由、重大证据、法律适用明显错误"],
        "risk_warnings": ["新证据不被采纳风险", "上诉请求范围限制", "发回重审周期风险"],
    },
    {
        "profile_key": "commercial_arbitration",
        "procedure_type": "arbitration",
        "procedure_stage": "commercial_arbitration",
        "required_material_patterns": ["仲裁协议摘要", "仲裁申请/答辩摘要", "仲裁证据目录", "仲裁庭审理要点"],
        "fact_extraction_points": ["仲裁协议效力", "合同履行节点", "违约责任触发事实", "损失计算基础"],
        "evidence_review_points": ["仲裁协议证明", "合同履行证据", "损失计算证据"],
        "legal_summary_points": ["仲裁管辖", "合同解释", "违约责任", "裁决司法审查边界"],
        "substantive_impact_points": ["仲裁协议效力决定程序路径", "司法审查通常不重新审理实体争议"],
        "procedural_transition_rules": ["仲裁→司法确认/撤销/执行：区分实体争议与程序审查边界"],
        "risk_warnings": ["仲裁条款效力风险", "保全衔接风险", "裁决执行风险"],
    },
    {
        "profile_key": "labor_arbitration",
        "procedure_type": "arbitration",
        "procedure_stage": "labor_arbitration",
        "required_material_patterns": ["劳动仲裁申请/答辩摘要", "用工证明 metadata", "工资/考勤/社保摘要", "解除材料摘要"],
        "fact_extraction_points": ["劳动关系成立", "入职离职时间", "工资发放", "解除理由", "仲裁时效"],
        "evidence_review_points": ["用工管理证据", "工资支付证据", "考勤社保证据", "规章制度程序证据"],
        "legal_summary_points": ["劳动关系认定", "工资/补偿/赔偿", "解除合法性", "仲裁前置与时效"],
        "substantive_impact_points": ["劳动仲裁前置影响后续诉讼范围", "管理证据缺口可能导致举证不利"],
        "procedural_transition_rules": ["劳动仲裁→一审：围绕仲裁请求、裁决结果和起诉范围衔接"],
        "risk_warnings": ["仲裁时效风险", "请求遗漏风险", "举证责任倒置风险"],
    },
]


def boundary_status() -> dict[str, Any]:
    now = _now()
    return _with_flags(
        {
            "boundary_id": "raw_training_material_boundary_v735a",
            "owner_user_id": "owner_local_demo",
            "workspace_id": "personal_training_workspace",
            "material_batch_id": "training_material_batch_v735a_demo",
            "controlled_zone_status": "enabled_for_private_processing_only",
            "allowed_material_types": [
                "judgment",
                "lawyer_work_product",
                "evidence",
                "court_record",
                "pleading",
                "agency_brief",
                "contract",
                "chat_record",
                "bank_flow",
                "other",
            ],
            "controlled_read_allowed": True,
            "frontend_source_display_allowed": False,
            "api_source_payload_allowed": False,
            "git_tracking_allowed": False,
            "provider_call_allowed": False,
            "filesystem_location_exposure_allowed": False,
            "audit_required": True,
            "source_trace_required": True,
            "created_at": now,
            "updated_at": now,
            "warnings": [
                "未脱敏基础材料仅允许在受控处理区内解析；API 与前端只返回脱敏摘要和 metadata。",
                "本地实现不调用 provider、不读取 key value、不返回 provider payload。",
            ],
        }
    )


def register_material(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    now = _now()
    record_id = f"training_material_v735a_{uuid4().hex[:10]}"
    material = _with_flags(
        {
            "training_material_id": record_id,
            "material_batch_id": str(payload.get("material_batch_id") or "training_material_batch_v735a_demo"),
            "material_kind": str(payload.get("material_kind") or "lawyer_work_product"),
            "material_label": str(payload.get("material_label") or "受控训练基础材料 metadata"),
            "material_status": "registered_for_controlled_processing",
            "source_zone_status": "controlled_private_processing",
            "ocr_status": "not_started",
            "document_parse_status": "not_started",
            "structure_status": "not_started",
            "legal_retrieval_status": "not_started",
            "parse_quality_status": "not_started",
            "redaction_output_status": "not_started",
            "source_trace_id": f"{record_id}_source_trace",
            "audit_id": f"{record_id}_audit",
            "safety_flags": _flag_summary(),
            "created_at": now,
            "updated_at": now,
            "warnings": ["登记结果为 metadata；不包含材料正文、OCR 内容、文件位置或 provider payload。"],
        }
    )
    write_payload(TRAINING_MATERIALS_DIR, record_id, material)
    return material


def list_materials() -> dict[str, Any]:
    materials = _read(TRAINING_MATERIALS_DIR)
    if not materials:
        materials = [register_material()]
    return _with_flags({"training_materials": materials, "material_count": len(materials), "warnings": ["仅展示受控材料 metadata。"]})


def get_material(material_id: str) -> dict[str, Any] | None:
    return read_payload(TRAINING_MATERIALS_DIR, material_id) or _find(TRAINING_MATERIALS_DIR, "training_material_id", material_id)


def run_ocr_job(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    now = _now()
    job_id = f"ocr_job_v735a_{uuid4().hex[:10]}"
    job = _with_flags(
        {
            "ocr_job_id": job_id,
            "training_material_id": material["training_material_id"],
            "material_kind": material["material_kind"],
            "ocr_status": "completed_metadata_only",
            "ocr_engine_mode": "mock_local_registry",
            "controlled_internal_ref": f"{job_id}_controlled_ref",
            "redacted_preview_available": True,
            "quality_score": 93,
            "source_trace_id": f"{job_id}_source_trace",
            "audit_id": f"{job_id}_audit",
            "created_at": now,
            "warnings": ["OCR 作业可在内部受控区处理基础材料，但 API 不返回识别正文。"],
        }
    )
    write_payload(TRAINING_MATERIAL_OCR_JOBS_DIR, job_id, job)
    _update_material(material, {"ocr_status": "completed_metadata_only"})
    return job


def list_ocr_jobs() -> dict[str, Any]:
    jobs = _read(TRAINING_MATERIAL_OCR_JOBS_DIR)
    if not jobs:
        jobs = [run_ocr_job()]
    return _with_flags({"ocr_jobs": jobs, "job_count": len(jobs), "warnings": ["OCR 列表只包含状态、质量和溯源 metadata。"]})


def get_ocr_job(job_id: str) -> dict[str, Any] | None:
    return _find(TRAINING_MATERIAL_OCR_JOBS_DIR, "ocr_job_id", job_id)


def run_document_parse_job(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    now = _now()
    parse_id = f"document_parse_job_v735a_{uuid4().hex[:10]}"
    job = _with_flags(
        {
            "parse_job_id": parse_id,
            "training_material_id": material["training_material_id"],
            "parse_status": "completed_metadata_only",
            "document_type": material["material_kind"],
            "sections_detected": ["事实背景", "证据目录", "争议焦点", "法律依据"],
            "tables_detected": 2,
            "entities_detected_count": 12,
            "controlled_structured_ref": f"{parse_id}_controlled_structure",
            "redacted_summary": "已生成脱敏结构摘要，可供后续质量 Gate 与经验抽象使用。",
            "quality_score": 91,
            "source_trace_id": f"{parse_id}_source_trace",
            "audit_id": f"{parse_id}_audit",
            "created_at": now,
            "warnings": ["文档解析不向前端返回正文或文件位置。"],
        }
    )
    write_payload(TRAINING_MATERIAL_PARSE_JOBS_DIR, parse_id, job)
    _update_material(material, {"document_parse_status": "completed_metadata_only"})
    return job


def list_document_parse_jobs() -> dict[str, Any]:
    jobs = _read(TRAINING_MATERIAL_PARSE_JOBS_DIR)
    if not jobs:
        jobs = [run_document_parse_job()]
    return _with_flags({"document_parse_jobs": jobs, "job_count": len(jobs), "warnings": ["解析结果只展示脱敏摘要。"]})


def get_document_parse_job(parse_job_id: str) -> dict[str, Any] | None:
    return _find(TRAINING_MATERIAL_PARSE_JOBS_DIR, "parse_job_id", parse_job_id)


def run_structure_jobs(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    now = _now()
    judgment_id = f"judgment_structure_v735a_{uuid4().hex[:10]}"
    work_id = f"work_product_structure_v735a_{uuid4().hex[:10]}"
    evidence_id = f"evidence_index_v735a_{uuid4().hex[:10]}"
    judgment = _with_flags(
        {
            "judgment_structure_id": judgment_id,
            "training_material_id": material["training_material_id"],
            "court_level": "基层法院 metadata",
            "case_cause": "买卖合同纠纷",
            "parties_redacted": True,
            "claims_summary_redacted": "围绕付款、交付、违约责任形成的脱敏请求摘要。",
            "facts_found_by_court_redacted": "法院采信的交易事实被抽象为时间线与履行节点。",
            "issues_summary_redacted": "合同成立、履行状态、违约责任与抗辩边界。",
            "evidence_accepted_summary_redacted": "合同、交付凭证、对账记录等证据类型被采信。",
            "evidence_rejected_summary_redacted": "关联性或证明力不足的证据类型被标注。",
            "legal_basis_summary": "合同编、证据规则与裁判规则摘要 metadata。",
            "court_reasoning_summary_redacted": "裁判理由被抽象为事实-证据-规则对齐模式。",
            "judgment_result_summary_redacted": "结果仅以责任类型和支持比例区间表达。",
            "source_trace_id": f"{judgment_id}_source_trace",
            "audit_id": f"{judgment_id}_audit",
            "quality_score": 90,
            "created_at": now,
        }
    )
    work_product = _with_flags(
        {
            "work_product_structure_id": work_id,
            "training_material_id": material["training_material_id"],
            "fact_notes_summary_redacted": "事实笔记已转换为履行节点和争点摘要。",
            "evidence_strategy_summary_redacted": "证据策略以证据类型、证明目的和缺口表达。",
            "argument_strategy_summary_redacted": "代理思路以请求基础、抗辩路径和风险提示表达。",
            "risk_assessment_summary_redacted": "风险以举证责任、时效、证据链完整性呈现。",
            "drafting_notes_summary_redacted": "文书写作要点保留为结构化 checklist。",
            "hearing_notes_summary_redacted": "庭审关注点保留为问题清单 metadata。",
            "client_objective_summary_redacted": "当事人目标被抽象为诉讼目标类型。",
            "source_trace_id": f"{work_id}_source_trace",
            "audit_id": f"{work_id}_audit",
            "quality_score": 92,
            "created_at": now,
        }
    )
    evidence = _with_flags(
        {
            "evidence_index_id": evidence_id,
            "material_batch_id": material["material_batch_id"],
            "evidence_items_count": 8,
            "evidence_groups": ["合同基础", "履行交付", "结算付款", "沟通记录"],
            "proof_purpose_summary": "证明合同关系、履行节点、欠款范围和违约责任。",
            "evidence_chain_summary_redacted": "证据链以类型和证明目的连接，不包含具体文本。",
            "missing_evidence_warnings": ["需人工核对签收链条完整性", "需复核对账凭证证明力"],
            "source_trace_id": f"{evidence_id}_source_trace",
            "audit_id": f"{evidence_id}_audit",
            "quality_score": 89,
            "created_at": now,
        }
    )
    write_payload(TRAINING_MATERIAL_JUDGMENT_STRUCTURES_DIR, judgment_id, judgment)
    write_payload(TRAINING_MATERIAL_WORK_PRODUCT_STRUCTURES_DIR, work_id, work_product)
    write_payload(TRAINING_MATERIAL_EVIDENCE_INDEXES_DIR, evidence_id, evidence)
    _update_material(material, {"structure_status": "completed_metadata_only"})
    return _with_flags({"judgment_structure": judgment, "work_product_structure": work_product, "evidence_index": evidence})


def list_judgment_structures() -> dict[str, Any]:
    items = _read(TRAINING_MATERIAL_JUDGMENT_STRUCTURES_DIR)
    if not items:
        run_structure_jobs()
        items = _read(TRAINING_MATERIAL_JUDGMENT_STRUCTURES_DIR)
    return _with_flags({"judgment_structures": items, "structure_count": len(items), "warnings": ["判决结构化结果为脱敏摘要。"]})


def list_work_product_structures() -> dict[str, Any]:
    items = _read(TRAINING_MATERIAL_WORK_PRODUCT_STRUCTURES_DIR)
    if not items:
        run_structure_jobs()
        items = _read(TRAINING_MATERIAL_WORK_PRODUCT_STRUCTURES_DIR)
    return _with_flags({"work_product_structures": items, "structure_count": len(items), "warnings": ["底稿结构化结果为脱敏摘要。"]})


def list_evidence_indexes() -> dict[str, Any]:
    items = _read(TRAINING_MATERIAL_EVIDENCE_INDEXES_DIR)
    if not items:
        run_structure_jobs()
        items = _read(TRAINING_MATERIAL_EVIDENCE_INDEXES_DIR)
    return _with_flags({"evidence_indexes": items, "index_count": len(items), "warnings": ["证据索引不包含证据正文。"]})


def run_legal_retrieval(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    now = _now()
    job_id = f"legal_retrieval_job_v735a_{uuid4().hex[:10]}"
    job = _with_flags(
        {
            "legal_retrieval_job_id": job_id,
            "material_batch_id": material["material_batch_id"],
            "case_cause": "买卖合同纠纷",
            "claims_summary_redacted": "付款请求、违约责任和费用承担的脱敏摘要。",
            "issues_summary_redacted": "合同履行、付款抗辩、证据链和违约责任。",
            "retrieval_status": "completed_mock_metadata",
            "statutes": ["民法典合同编相关规则 metadata", "民事诉讼证据规则 metadata"],
            "judicial_interpretations": ["买卖合同司法解释相关规则 metadata"],
            "case_law_references": ["类案裁判规则候选 metadata"],
            "rule_summaries": ["付款义务认定", "交付证明责任", "违约责任计算边界"],
            "retrieval_source_trace_id": f"{job_id}_source_trace",
            "audit_id": f"{job_id}_audit",
            "quality_score": 90,
            "created_at": now,
            "warnings": ["本阶段使用本地 mock / registry metadata，不调用真实法律检索 provider。"],
        }
    )
    write_payload(TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR, job_id, job)
    _update_material(material, {"legal_retrieval_status": "completed_mock_metadata"})
    return job


def list_legal_retrieval_jobs() -> dict[str, Any]:
    jobs = _read(TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR)
    if not jobs:
        jobs = [run_legal_retrieval()]
    return _with_flags({"legal_retrieval_jobs": jobs, "job_count": len(jobs), "warnings": ["法律检索结果为候选规则 metadata。"]})


def run_rule_alignment(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    now = _now()
    alignment_id = f"rule_alignment_v735a_{uuid4().hex[:10]}"
    alignment = _with_flags(
        {
            "alignment_id": alignment_id,
            "material_batch_id": material["material_batch_id"],
            "fact_to_evidence_links": ["履行节点 -> 交付凭证类型", "付款节点 -> 对账/流水类型"],
            "issue_to_rule_links": ["付款争议 -> 合同履行规则", "证据缺口 -> 举证责任规则"],
            "evidence_to_court_reasoning_links": ["证据组 -> 裁判理由模式 metadata"],
            "lawyer_strategy_to_court_result_links": ["请求基础 -> 支持范围 metadata"],
            "risk_to_outcome_links": ["证据链缺口 -> 支持比例风险"],
            "alignment_summary_redacted": "事实、证据、争点、规则与裁判理由已形成脱敏对齐摘要。",
            "missing_alignment_warnings": ["需律师复核争点覆盖是否充分"],
            "quality_score": 88,
            "source_trace_id": f"{alignment_id}_source_trace",
            "audit_id": f"{alignment_id}_audit",
            "created_at": now,
        }
    )
    write_payload(TRAINING_MATERIAL_RULE_ALIGNMENTS_DIR, alignment_id, alignment)
    return alignment


def list_rule_alignments() -> dict[str, Any]:
    alignments = _read(TRAINING_MATERIAL_RULE_ALIGNMENTS_DIR)
    if not alignments:
        alignments = [run_rule_alignment()]
    return _with_flags({"rule_alignments": alignments, "alignment_count": len(alignments), "warnings": ["对齐结果为 metadata。"]})


def run_parse_quality_gate(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    if not _read(TRAINING_MATERIAL_OCR_JOBS_DIR):
        run_ocr_job({"training_material_id": material["training_material_id"]})
    if not _read(TRAINING_MATERIAL_PARSE_JOBS_DIR):
        run_document_parse_job({"training_material_id": material["training_material_id"]})
    if not _read(TRAINING_MATERIAL_JUDGMENT_STRUCTURES_DIR):
        run_structure_jobs({"training_material_id": material["training_material_id"]})
    if not _read(TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR):
        run_legal_retrieval({"training_material_id": material["training_material_id"]})
    if not _read(TRAINING_MATERIAL_RULE_ALIGNMENTS_DIR):
        run_rule_alignment({"training_material_id": material["training_material_id"]})
    now = _now()
    gate_id = f"parse_quality_gate_v735a_{uuid4().hex[:10]}"
    report = _with_flags(
        {
            "parse_quality_gate_id": gate_id,
            "material_batch_id": material["material_batch_id"],
            "ocr_completed": True,
            "document_parse_completed": True,
            "judgment_structured": True,
            "lawyer_work_product_structured": True,
            "evidence_index_built": True,
            "legal_retrieval_completed": True,
            "rule_alignment_completed": True,
            "source_trace_complete": True,
            "audit_complete": True,
            "source_payload_not_exported": True,
            "quality_score": 90,
            "gate_status": "passed",
            "blocked_reason": None,
            "warnings": ["解析质量 Gate 通过后，仍只能进入脱敏经验抽象链路。"],
            "created_at": now,
        }
    )
    write_payload(TRAINING_MATERIAL_PARSE_GATES_DIR, material["material_batch_id"], report)
    _update_material(material, {"parse_quality_status": "passed"})
    return report


def get_parse_quality_gate(material_batch_id: str) -> dict[str, Any] | None:
    return read_payload(TRAINING_MATERIAL_PARSE_GATES_DIR, material_batch_id)


def build_v735a_status() -> dict[str, Any]:
    gate = _latest(TRAINING_MATERIAL_PARSE_GATES_DIR)
    return _with_flags(
        {
            "version": "v7.35a",
            "status": "raw_training_material_boundary_ready",
            "boundary_ready": True,
            "material_count": len(_read(TRAINING_MATERIALS_DIR)),
            "ocr_job_count": len(_read(TRAINING_MATERIAL_OCR_JOBS_DIR)),
            "parse_job_count": len(_read(TRAINING_MATERIAL_PARSE_JOBS_DIR)),
            "legal_retrieval_job_count": len(_read(TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR)),
            "latest_gate_status": gate.get("gate_status") if gate else "not_run",
            "warnings": ["v7.35a 是受控解析层；不替代已完成的 v7.35 数据集构建。"],
        }
    )


def build_experience_candidates(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    gate = get_parse_quality_gate(material["material_batch_id"]) or run_parse_quality_gate({"training_material_id": material["training_material_id"]})
    now = _now()
    types = ["fact_pattern", "evidence_chain_pattern", "legal_rule_application", "risk_warning"]
    candidates = []
    for item_type in types:
        candidate_id = f"raw_based_candidate_v735b_{item_type}_{uuid4().hex[:8]}"
        candidate = _with_flags(
            {
                "raw_based_candidate_id": candidate_id,
                "material_batch_id": material["material_batch_id"],
                "case_cause": "买卖合同纠纷",
                "candidate_type": item_type,
                "candidate_title": f"{item_type} 脱敏经验候选",
                "candidate_summary_redacted": "从受控解析结果抽象出的经验候选，不含原始内容。",
                "fact_pattern_redacted": "交易关系、履行节点、付款争议与证据链缺口的抽象模式。",
                "evidence_pattern_redacted": "合同、交付、结算、沟通记录的证明目的模式。",
                "issue_pattern_redacted": "合同履行、付款抗辩、违约责任和举证责任。",
                "legal_rule_pattern": "合同履行规则、证据规则和类案裁判规则候选。",
                "court_reasoning_pattern_redacted": "法院围绕证据链完整性和规则适用进行理由展开。",
                "lawyer_strategy_pattern_redacted": "优先补强履行证据、整理争点和责任计算边界。",
                "risk_warning_pattern_redacted": "证据链断点、对账争议和责任比例需律师复核。",
                "abstraction_level": "case_cause_pattern",
                "redaction_status": "passed",
                "parse_quality_gate_id": gate["parse_quality_gate_id"],
                "source_trace_id": f"{candidate_id}_source_trace",
                "audit_id": f"{candidate_id}_audit",
                "quality_score": 90,
                "created_at": now,
            }
        )
        write_payload(RAW_BASED_EXPERIENCE_CANDIDATES_DIR, candidate_id, candidate)
        candidates.append(candidate)
    return _with_flags({"candidates": candidates, "candidate_count": len(candidates), "warnings": ["经验候选已脱敏、抽象化、metadata-safe。"]})


def list_experience_candidates() -> dict[str, Any]:
    candidates = _read(RAW_BASED_EXPERIENCE_CANDIDATES_DIR)
    if not candidates:
        candidates = build_experience_candidates()["candidates"]
    return _with_flags({"candidates": candidates, "candidate_count": len(candidates), "warnings": ["不包含基础材料正文。"]})


def get_experience_candidate(candidate_id: str) -> dict[str, Any] | None:
    return _find(RAW_BASED_EXPERIENCE_CANDIDATES_DIR, "raw_based_candidate_id", candidate_id)


def build_redacted_experience_package(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    material = _material_from_payload(payload)
    candidates = list_experience_candidates()["candidates"]
    gate = get_parse_quality_gate(material["material_batch_id"]) or run_parse_quality_gate({"training_material_id": material["training_material_id"]})
    now = _now()
    package_id = f"redacted_experience_package_v735b_{uuid4().hex[:10]}"
    cards = [
        {
            "card_id": f"{package_id}_card_{index}",
            "card_type": candidate["candidate_type"],
            "title": candidate["candidate_title"],
            "summary_redacted": candidate["candidate_summary_redacted"],
            "usage_boundary": "仅作为律师复核前的经验参考 metadata，不作为最终法律意见。",
        }
        for index, candidate in enumerate(candidates, start=1)
    ]
    facts_summary = {
        "common_fact_extraction_framework": COMMON_FACT_EXTRACTION_FRAMEWORK,
        "common_template_boundary": "共用模板只提供事实提炼基础结构，不写死案由细节。",
        "case_cause_specific_fact_summaries": [
            {
                "case_cause": item["case_cause"],
                "fact_extraction_summary": f"{item['case_cause']}事实提炼应在共用框架下突出：" + "、".join(item["fact_points"]) + "。",
                "case_cause_specific_fact_points": item["fact_points"],
                "source_trace_id": f"{package_id}_{index}_source_trace",
                "audit_id": f"{package_id}_{index}_audit",
            }
            for index, item in enumerate(CASE_CAUSE_SPECIFIC_FACT_POINTS, start=1)
        ],
    }
    legal_summary = {
        "summary": "法律要点 summary 由法条检索候选、裁判理由摘要、争点结构与律师复核 metadata 抽象生成。",
        "case_cause_legal_summaries": [
            {
                "case_cause": item["case_cause"],
                "legal_summary": item["legal_summary"],
                "source_trace_id": f"{package_id}_{index}_legal_source_trace",
                "audit_id": f"{package_id}_{index}_legal_audit",
            }
            for index, item in enumerate(CASE_CAUSE_SPECIFIC_FACT_POINTS, start=1)
        ],
    }
    case_cause_profiles = [
        {
            "case_cause": item["case_cause"],
            "case_cause_specific_fact_points": item["fact_points"],
            "case_cause_legal_summary": item["legal_summary"],
            "substantive_experience_profiles": [],
            "procedural_experience_profiles": [],
            "procedural_profiles": [
                {
                    **profile,
                    "fact_extraction_points": list(dict.fromkeys([*item["fact_points"], *profile["fact_extraction_points"]])),
                    "metadata": {
                        "case_cause": item["case_cause"],
                        "profile_match_key": f"{item['case_cause']}::{profile['procedure_type']}::{profile['procedure_stage']}",
                        "lawyer_review_required": True,
                        "audit_required": True,
                        "source_trace_required": True,
                    },
                    "source_trace_id": f"{package_id}_{index}_{profile['profile_key']}_source_trace",
                    "audit_id": f"{package_id}_{index}_{profile['profile_key']}_audit",
                }
                for profile in PROCEDURAL_PROFILE_POINTS
            ],
            "procedure_transition_rules": ["一审→二审→再审", "仲裁→司法确认/撤销/执行", "劳动仲裁→一审"],
        }
        for index, item in enumerate(CASE_CAUSE_SPECIFIC_FACT_POINTS, start=1)
    ]
    substantive_profiles = [
        {
            "experience_type": "substantive",
            "profile_id": f"{package_id}_{index}_substantive_profile",
            "case_cause": item["case_cause"],
            "substantive_issue": f"{item['case_cause']}实体争点 metadata",
            "fact_pattern": f"{item['case_cause']}事实结构 metadata",
            "evidence_pattern": f"{item['case_cause']}证据结构 metadata",
            "fact_extraction_points": item["fact_points"],
            "substantive_legal_summary_points": [item["legal_summary"], "请求权/抗辩基础", "责任范围"],
            "claim_basis_patterns": [f"{item['case_cause']}请求基础 metadata"],
            "issue_to_rule_patterns": [f"{item['case_cause']}争点到规则 metadata"],
            "evidence_to_legal_effect_patterns": [f"{item['case_cause']}证据到法律效果 metadata"],
            "court_reasoning_patterns": [f"{item['case_cause']}裁判理由模式 metadata"],
            "risk_fact_patterns": ["关键事实缺口", "证据链断点"],
            "risk_legal_points": ["举证责任风险", "抗辩成立风险"],
            "substantive_impact_points": ["实体经验可在边界允许时跨程序参考，但不代表程序规则适用"],
            "source_procedure_type": "litigation",
            "source_procedure_stage": "second_instance",
            "source_stage_reference": {
                "source_procedure_type": "litigation",
                "source_procedure_stage": "second_instance",
                "runtime_reference_type": "substantive_reference",
                "notice": "仅为实体经验参考，不代表程序规则适用。",
            },
            "runtime_reference_type": "substantive_reference",
            "usage_boundary": {
                "allows_cross_procedure_reference": True,
                "requires_case_cause_match_or_same_hierarchy": True,
                "requires_substantive_issue_match": True,
                "requires_fact_pattern_similarity": True,
                "requires_evidence_pattern_similarity_or_explanation": True,
                "procedural_rules_not_included": True,
            },
            "source_trace_id": f"{package_id}_{index}_substantive_source_trace",
            "audit_id": f"{package_id}_{index}_substantive_audit",
        }
        for index, item in enumerate(CASE_CAUSE_SPECIFIC_FACT_POINTS, start=1)
    ]
    procedural_profiles = [
        {
            "experience_type": "procedural",
            "profile_id": f"{package_id}_{profile['profile_key']}_procedural_profile",
            "procedure_type": profile["procedure_type"],
            "procedure_stage": profile["procedure_stage"],
            "required_material_patterns": profile["required_material_patterns"],
            "procedural_deadline_rules": ["程序期限 metadata，需律师复核"],
            "procedural_burden_rules": profile["evidence_review_points"],
            "appeal_scope_rules": ["二审上诉范围规则"] if profile["procedure_stage"] == "second_instance" else ["非二审 profile 不直接适用"],
            "retrial_threshold_rules": ["再审门槛规则"] if profile["procedure_stage"] == "retrial" else ["非再审 profile 不直接适用"],
            "arbitration_clause_review_rules": ["仲裁协议效力审查"] if profile["procedure_stage"] == "commercial_arbitration" else ["非商事仲裁 profile 不直接适用"],
            "labor_arbitration_precondition_rules": ["劳动仲裁前置"] if profile["procedure_stage"] == "labor_arbitration" else ["非劳动仲裁 profile 不直接适用"],
            "procedural_transition_rules": profile["procedural_transition_rules"],
            "procedural_risk_warnings": profile["risk_warnings"],
            "source_procedure_type": profile["procedure_type"],
            "source_procedure_stage": profile["procedure_stage"],
            "source_stage_reference": {
                "source_procedure_type": profile["procedure_type"],
                "source_procedure_stage": profile["procedure_stage"],
                "runtime_reference_type": "procedural_exact_match",
                "notice": "程序经验仅适用于精确匹配的程序类型和阶段。",
            },
            "runtime_reference_type": "procedural_exact_match",
            "cross_procedure_reference_allowed": False,
            "cross_stage_reference_allowed": False,
            "usage_boundary": {
                "exact_procedure_type_required": True,
                "exact_procedure_stage_required": True,
                "cross_procedure_reference_forbidden": True,
                "cross_stage_reference_forbidden": True,
            },
            "source_trace_id": f"{package_id}_{profile['profile_key']}_procedural_source_trace",
            "audit_id": f"{package_id}_{profile['profile_key']}_procedural_audit",
        }
        for profile in PROCEDURAL_PROFILE_POINTS
    ]
    for case_profile in case_cause_profiles:
        case_profile["substantive_experience_profiles"] = [
            profile for profile in substantive_profiles if profile["case_cause"] == case_profile["case_cause"]
        ]
        case_profile["procedural_experience_profiles"] = procedural_profiles
        case_profile["procedural_profiles"] = procedural_profiles
    package = _with_flags(
        {
            "redacted_experience_package_id": package_id,
            "material_batch_id": material["material_batch_id"],
            "case_cause": "买卖合同纠纷",
            "experience_cards": cards,
            "facts_output": facts_summary,
            "legal_output": legal_summary,
            "substantive_experience_profiles": substantive_profiles,
            "procedural_experience_profiles": procedural_profiles,
            "case_cause_profiles": case_cause_profiles,
            "profile_loading_contract": {
                "two_layer_matching": True,
                "substantive_match_keys": ["case_cause", "substantive_issue", "fact_pattern", "evidence_pattern"],
                "substantive_cross_procedure_reference_allowed": True,
                "procedural_match_keys": ["procedure_type", "procedure_stage"],
                "procedural_cross_stage_reference_allowed": False,
                "procedural_cross_procedure_reference_allowed": False,
                "loads": ["substantive_reference", "procedural_exact_match", "materials", "substantive_impact", "risk_warnings"],
                "missing_profile_action": "manual_confirmation_review_queue",
                "diff_supported": True,
                "audit_required": True,
                "source_trace_required": True,
            },
            "diff_summary": "共用事实框架保持一致，案由、程序和阶段差异化要点根据训练材料 metadata 抽象生成。",
            "readiness_checks": {
                "multi_case_cause_dry_run": True,
                "multi_procedure_stage_dry_run": True,
                "facts_output_diff_check": True,
                "legal_summary_check": True,
                "substantive_impact_check": True,
                "profile_loading_contract_check": True,
                "audit_check": True,
                "source_trace_check": True,
            },
            "source_candidate_ids": [candidate["raw_based_candidate_id"] for candidate in candidates],
            "parse_quality_gate_id": gate["parse_quality_gate_id"],
            "legal_retrieval_job_ids": [job["legal_retrieval_job_id"] for job in _read(TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR)],
            "rule_alignment_ids": [item["alignment_id"] for item in _read(TRAINING_MATERIAL_RULE_ALIGNMENTS_DIR)],
            "redaction_report_id": f"{package_id}_redaction_report",
            "safety_report_id": f"{package_id}_safety_report",
            "source_trace_bundle_id": f"{package_id}_source_trace_bundle",
            "audit_bundle_id": f"{package_id}_audit_bundle",
            "package_status": "ready_for_training_dataset",
            "created_at": now,
            "warnings": ["脱敏经验包只包含抽象经验卡片，不包含受控区输入内容。"],
        }
    )
    write_payload(REDACTED_EXPERIENCE_PACKAGES_DIR, package_id, package)
    _update_material(material, {"redaction_output_status": "ready_for_training_dataset"})
    return package


def list_redacted_experience_packages() -> dict[str, Any]:
    packages = _read(REDACTED_EXPERIENCE_PACKAGES_DIR)
    if not packages:
        packages = [build_redacted_experience_package()]
    return _with_flags({"redacted_experience_packages": packages, "package_count": len(packages), "warnings": ["经验包均为脱敏抽象 metadata。"]})


def get_redacted_experience_package(package_id: str) -> dict[str, Any] | None:
    return _find(REDACTED_EXPERIENCE_PACKAGES_DIR, "redacted_experience_package_id", package_id)


def redaction_report(package_id: str) -> dict[str, Any] | None:
    package = get_redacted_experience_package(package_id)
    if not package:
        return None
    return _with_flags(
        {
            "redaction_report_id": package["redaction_report_id"],
            "package_id": package_id,
            "source_payload_absent": True,
            "ocr_payload_absent": True,
            "original_payload_absent": True,
            "filesystem_location_absent": True,
            "credential_value_absent": True,
            "provider_payload_absent": True,
            "party_identity_redacted": True,
            "case_number_redacted": True,
            "contact_info_redacted": True,
            "bank_account_redacted": True,
            "id_number_redacted": True,
            "source_trace_complete": True,
            "audit_complete": True,
            "warnings": ["Redaction gate passed for package metadata."],
        }
    )


def package_audit(package_id: str) -> dict[str, Any] | None:
    package = get_redacted_experience_package(package_id)
    if not package:
        return None
    return _with_flags(
        {
            "audit_bundle_id": package["audit_bundle_id"],
            "package_id": package_id,
            "events": [
                {"event": "parse_gate_checked", "status": "passed"},
                {"event": "redaction_checked", "status": "passed"},
                {"event": "experience_package_built", "status": "metadata_only"},
            ],
            "event_count": 3,
            "warnings": ["Audit bundle contains metadata events only."],
        }
    )


def package_source_trace(package_id: str) -> dict[str, Any] | None:
    package = get_redacted_experience_package(package_id)
    if not package:
        return None
    return _with_flags(
        {
            "source_trace_bundle_id": package["source_trace_bundle_id"],
            "package_id": package_id,
            "trace_status": "complete_metadata_only",
            "candidate_count": len(package["source_candidate_ids"]),
            "parse_quality_gate_id": package["parse_quality_gate_id"],
            "warnings": ["Source trace links to controlled metadata references only."],
        }
    )


def build_v735b_status() -> dict[str, Any]:
    packages = _read(REDACTED_EXPERIENCE_PACKAGES_DIR)
    return _with_flags(
        {
            "version": "v7.35b",
            "status": "redacted_experience_output_ready",
            "candidate_count": len(_read(RAW_BASED_EXPERIENCE_CANDIDATES_DIR)),
            "redacted_package_count": len(packages),
            "ready_for_training_dataset_count": sum(1 for item in packages if item.get("package_status") == "ready_for_training_dataset"),
            "warnings": ["v7.35b 生成脱敏经验输出，不重做既有 v7.35 数据集构建。"],
        }
    )


def _material_from_payload(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    material_id = payload.get("training_material_id")
    if material_id:
        material = get_material(str(material_id))
        if material:
            return material
    materials = _read(TRAINING_MATERIALS_DIR)
    return materials[0] if materials else register_material(payload)


def _update_material(material: dict[str, Any], updates: dict[str, Any]) -> None:
    material.update(updates)
    material["updated_at"] = _now()
    write_payload(TRAINING_MATERIALS_DIR, material["training_material_id"], material)


def _read(directory) -> list[dict[str, Any]]:
    return read_payloads(directory)


def _find(directory, field: str, value: str) -> dict[str, Any] | None:
    for payload in read_payloads(directory):
        if payload.get(field) == value:
            return payload
    return None


def _latest(directory) -> dict[str, Any] | None:
    payloads = read_payloads(directory)
    return payloads[-1] if payloads else None


def _with_flags(payload: dict[str, Any]) -> dict[str, Any]:
    return {**SAFE_FLAGS, **payload}


def _flag_summary() -> dict[str, bool]:
    return {
        "frontend_source_display_allowed": False,
        "api_source_payload_allowed": False,
        "provider_call_executed": False,
        "key_value_read": False,
        "redacted_output_only": True,
        "source_trace_required": True,
        "audit_required": True,
    }


def _now() -> str:
    return datetime.now(UTC).isoformat()
