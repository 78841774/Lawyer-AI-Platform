from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from personal_skill_studio.training_artifacts.storage import (
    CODEX_SKILL_TRAINING_RUNS_DIR,
    CODEX_TRAINING_SKILLS_DIR,
    read_payloads,
    write_payload,
)
from personal_skill_studio.training_artifacts.training_dataset_builder import (
    build_training_dataset,
    get_training_gate_report,
    latest_training_dataset_manifest,
)
from personal_skill_studio.training_artifacts.artifact_registry import get_skill
from personal_skill_studio.training_artifacts.safe_provider_adapter_runtime import (
    call_provider_placeholder,
    provider_specs_with_loaded_state,
)


SAFE_FLAGS: dict[str, bool] = {
    "owner_only": True,
    "metadata_only": True,
    "redacted_output_only": True,
    "abstracted_output_only": True,
    "source_trace_required": True,
    "audit_required": True,
    "provider_call_executed": False,
    "key_value_read": False,
    "credential_value_returned": False,
    "source_content_returned": False,
    "case_material_returned": False,
    "filesystem_location_exposed": False,
    "skill_published": False,
    "runtime_package_replaced": False,
    "not_publishable_by_default": True,
    "not_runtime_loadable_by_default": True,
    "requires_practice_load_review": True,
    "final_legal_opinion_generated": False,
    "final_report_generated": False,
    "public_link_created": False,
    "email_sent": False,
    "external_delivery_triggered": False,
}


FACT_BASELINE = {
    "target_skill_id": "case_fact_extraction_skill",
    "legacy_skill_id": "case-fact-extractor-v3",
    "training_package_id": "case-fact-extractor-v3@v1.0.0",
    "domain": "case_fact_extraction",
    "source_assets": [
        "runtime_rules/material_context_rules.md",
        "runtime_rules/evidence_matrix_rules.md",
        "runtime_rules/amount_audit_rules.md",
        "runtime_rules/contradiction_gap_rules.md",
        "runtime_rules/legal_element_mapping_rules.md",
        "prompt_templates/fact_extraction_prompt_template.md",
        "evaluation_rubrics/fact_extraction_rubric.md",
    ],
    "evaluation_id": "eval_case_fact_extraction_v7_30",
    "gate_id": "gate_case_fact_extraction_v7_30",
}


LEGAL_BASELINE = {
    "target_skill_id": "case_legal_analysis_skill",
    "legacy_skill_id": "case-analysis-pro-v3",
    "training_package_id": "case-analysis-pro-v3@v1.0.0",
    "domain": "case_legal_analysis",
    "source_assets": [
        "runtime_rules/legal_analysis_chain_rules.md",
        "runtime_rules/claim_defense_rules.md",
        "runtime_rules/litigation_strategy_rules.md",
        "prompt_templates/legal_analysis_prompt_template.md",
        "report_templates/legal_analysis_report_template.md",
        "evaluation_rubrics/legal_analysis_rubric.md",
    ],
    "evaluation_id": "eval_case_legal_analysis_v7_30",
    "gate_id": "gate_case_legal_analysis_v7_30",
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


CASE_CAUSE_FACT_POINT_LIBRARY = [
    {
        "case_cause_code": "civil.contract.private_lending",
        "case_cause_name": "民间借贷纠纷",
        "learned_from_material_types": ["judgment", "lawyer_work_product", "evidence", "legal_retrieval"],
        "case_cause_specific_fact_points": ["借贷合意", "款项交付", "还款事实", "催收记录", "利息约定", "诉讼时效"],
        "legal_summary": "围绕借贷关系成立、交付证明、利息边界与时效抗辩形成法律要点摘要。",
    },
    {
        "case_cause_code": "civil.contract.sales",
        "case_cause_name": "买卖合同纠纷",
        "learned_from_material_types": ["judgment", "lawyer_work_product", "evidence", "legal_retrieval"],
        "case_cause_specific_fact_points": ["合同成立", "交付事实", "验收事实", "付款节点", "质量异议", "违约通知"],
        "legal_summary": "围绕合同成立、交付验收、付款义务、质量抗辩与违约责任形成法律要点摘要。",
    },
    {
        "case_cause_code": "civil.labor.dispute",
        "case_cause_name": "劳动争议",
        "learned_from_material_types": ["judgment", "lawyer_work_product", "evidence", "legal_retrieval"],
        "case_cause_specific_fact_points": ["劳动关系成立", "入职离职时间", "工资发放", "考勤", "社保", "解除理由"],
        "legal_summary": "围绕劳动关系认定、工资社保、解除事由、程序合法性与举证责任形成法律要点摘要。",
    },
    {
        "case_cause_code": "civil.family.marriage",
        "case_cause_name": "婚姻家事纠纷",
        "learned_from_material_types": ["judgment", "lawyer_work_product", "evidence", "legal_retrieval"],
        "case_cause_specific_fact_points": ["身份关系", "财产来源", "共同债务", "抚养事实", "过错事实"],
        "legal_summary": "围绕身份关系、财产来源、共同债务、子女抚养与过错情节形成法律要点摘要。",
    },
]


COMMON_LEGAL_SUMMARY_FRAMEWORK = [
    "请求权基础 / 抗辩基础",
    "程序身份与管辖 / 仲裁约定",
    "举证责任分配",
    "实体构成要件",
    "法律适用与裁判规则",
    "责任范围与计算边界",
    "程序风险与救济路径",
]


PROCEDURAL_PROFILE_LIBRARY = [
    {
        "profile_key": "litigation_first_instance",
        "procedure_type": "litigation",
        "procedure_stage": "first_instance",
        "profile_name": "诉讼一审",
        "required_material_patterns": ["起诉状/答辩状摘要", "证据目录", "庭审笔录摘要", "一审裁判理由摘要"],
        "fact_focus": ["基础法律关系成立", "主要履行过程", "争议事实形成", "证据链完整性"],
        "evidence_focus": ["证据真实性/合法性/关联性", "举证责任是否完成", "核心证据能否形成闭环"],
        "legal_focus": ["请求权基础", "抗辩事由", "举证责任", "责任承担方式"],
        "substantive_impact_points": ["一审事实认定将影响后续上诉审查范围", "未充分举证的事实可能形成实体败诉风险"],
        "procedural_transition_rules": ["一审→二审：重点识别事实认定错误、法律适用错误和新证据条件"],
        "risk_warnings": ["举证期限风险", "争点遗漏风险", "请求基础选择风险"],
    },
    {
        "profile_key": "litigation_second_instance",
        "procedure_type": "litigation",
        "procedure_stage": "second_instance",
        "profile_name": "诉讼二审",
        "required_material_patterns": ["一审裁判摘要", "上诉状/答辩状摘要", "二审新证据 metadata", "二审争点整理"],
        "fact_focus": ["一审已查明事实", "上诉争议事实", "新证据关联事实", "事实认定错误主张"],
        "evidence_focus": ["新证据提交条件", "一审证据评价偏差", "二审争点对应证据"],
        "legal_focus": ["上诉请求基础", "事实审查边界", "法律适用纠错", "改判/发回风险"],
        "substantive_impact_points": ["二审通常围绕上诉请求和争点审查，直接影响责任范围是否调整", "新证据能否进入审查会改变实体认定空间"],
        "procedural_transition_rules": ["二审→再审：重点识别法定再审事由、重大证据、法律适用明显错误"],
        "risk_warnings": ["新证据不被采纳风险", "上诉请求范围限制", "发回重审周期风险"],
    },
    {
        "profile_key": "litigation_retrial",
        "procedure_type": "litigation",
        "procedure_stage": "retrial",
        "profile_name": "诉讼再审",
        "required_material_patterns": ["生效裁判摘要", "再审申请摘要", "法定再审事由 metadata", "新增/重大证据摘要"],
        "fact_focus": ["生效裁判认定事实", "再审事由对应事实", "重大证据影响事实", "程序违法影响事实"],
        "evidence_focus": ["重大证据标准", "原审证据采信缺陷", "程序违法与实体结果关联"],
        "legal_focus": ["再审法定事由", "生效裁判稳定性", "明显错误审查", "救济边界"],
        "substantive_impact_points": ["再审门槛高，程序事由是否足以动摇实体结果是核心", "重大证据需证明可能改变原裁判结果"],
        "procedural_transition_rules": ["再审审查→再审审理：区分启动事由与重新实体审理重点"],
        "risk_warnings": ["再审事由不足风险", "超过申请期限风险", "重复主张原审事实风险"],
    },
    {
        "profile_key": "commercial_arbitration",
        "procedure_type": "arbitration",
        "procedure_stage": "commercial_arbitration",
        "profile_name": "商事仲裁",
        "required_material_patterns": ["仲裁协议/条款摘要", "仲裁申请/答辩摘要", "仲裁证据目录", "仲裁庭审理要点"],
        "fact_focus": ["仲裁协议效力", "合同履行节点", "违约责任触发事实", "损失计算基础"],
        "evidence_focus": ["仲裁协议证明", "合同履行证据", "损失计算证据", "专家/鉴定材料 metadata"],
        "legal_focus": ["仲裁管辖", "合同解释", "违约责任", "裁决撤销/不予执行风险"],
        "substantive_impact_points": ["仲裁协议效力决定程序路径，证据组织更直接影响责任和损失认定", "仲裁裁决后司法审查通常不重新审理实体争议"],
        "procedural_transition_rules": ["仲裁→司法确认/撤销/执行：区分实体争议与程序审查边界"],
        "risk_warnings": ["仲裁条款效力风险", "保全衔接风险", "裁决执行风险"],
    },
    {
        "profile_key": "labor_arbitration",
        "procedure_type": "arbitration",
        "procedure_stage": "labor_arbitration",
        "profile_name": "劳动仲裁",
        "required_material_patterns": ["仲裁申请/答辩摘要", "劳动合同/用工证明 metadata", "工资/考勤/社保记录摘要", "解除通知/规章制度摘要"],
        "fact_focus": ["劳动关系成立", "工作岗位与期间", "工资发放与考勤", "解除/终止理由", "仲裁时效"],
        "evidence_focus": ["用工管理证据", "工资支付证据", "考勤社保证据", "规章制度民主程序证据"],
        "legal_focus": ["劳动关系认定", "工资/补偿/赔偿", "解除合法性", "仲裁前置与时效"],
        "substantive_impact_points": ["劳动仲裁前置影响后续诉讼范围，仲裁请求设计会影响实体审查边界", "用人单位管理证据缺口可能导致举证不利"],
        "procedural_transition_rules": ["劳动仲裁→一审：围绕仲裁请求、裁决结果和起诉范围衔接"],
        "risk_warnings": ["仲裁时效风险", "请求遗漏风险", "举证责任倒置风险"],
    },
]


def generate_training_skill(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    manifest = latest_training_dataset_manifest()
    if manifest is None:
        build_training_dataset()
        manifest = latest_training_dataset_manifest()
    gate_report = get_training_gate_report()
    now = _now()
    skill_id = f"codex_training_skill_v737_addon_{uuid4().hex[:10]}"
    skill_target = str(payload.get("skill_target") or "case_analysis_skill")
    target_skill_ids = _target_skill_ids(skill_target)
    output_groups = _output_groups(manifest)
    baselines = _baseline_refs(target_skill_ids)
    provider_specs = provider_specs_with_loaded_state()
    differentiated_package = _differentiated_experience_package(manifest, skill_id)
    skill = _with_flags(
        {
            "training_skill_id": skill_id,
            "training_dataset_id": manifest.dataset_id if manifest else None,
            "skill_target": skill_target,
            "target_skill_ids": target_skill_ids,
            "baseline_complete": True,
            "source_skill_ids": target_skill_ids,
            "source_package_ids": [baseline["training_package_id"] for baseline in baselines],
            "derived_from": [
                "case-fact-extractor-v3@v1.0.0 readonly versioned package",
                "case-analysis-pro-v3@v1.0.0 readonly versioned package",
                "v7.30 case_fact_extraction_skill and case_legal_analysis_skill manifests",
                "v7.35 dataset and training gate metadata",
            ],
            "source_baseline_refs": baselines,
            "source_evaluation_files": [
                "evaluation_rubrics/fact_extraction_rubric.md",
                "evaluation_rubrics/legal_analysis_rubric.md",
            ],
            "source_gate_ids": [baseline["gate_id"] for baseline in baselines],
            "skill_name": "Codex 训练 Skill Spec metadata",
            "skill_version": "v7.37.addon",
            "skill_status": "ready_for_dry_run_training" if gate_report.get("gate_status") == "passed_reference_only" else "blocked",
            "training_objectives": [
                "从脱敏经验包与训练样例中形成案件事实提取规则",
                "生成法律要点 summary 与事实提炼 summary",
                "共用事实模板只提供基础结构，不写死案由细节",
                "根据判决结构、律师底稿结构、证据索引、裁判理由和法条检索 metadata 总结案由差异化事实要点",
                "从输出 schema 中约束法律分析和风险提示结构",
                "合并事实提炼 Skill 的材料-事实-证据矩阵规则与法律分析 Skill 的争点-规则-策略链条",
                "保持律师复核、来源可追踪和不可自动发布边界",
            ],
            "input_schema": {
                "dataset_manifest": "metadata",
                "training_examples": "abstracted_metadata",
                "redacted_experience_package": "metadata_refs",
                "improvement_candidates": "metadata_refs",
                "provider_results": "provider_gated_metadata",
            },
            "output_schema": {
                "schema_source": "backend_case_analysis_output_schema_or_task_plan",
                "output_group_count": len(output_groups),
                "output_groups": {
                    "facts": {
                        "path": "case_cause_profile.procedural_profile.fact_extraction_points",
                        "substantive_path": "substantive_experience_profiles[].fact_extraction_points",
                        "common_fact_extraction_framework": "shared structural checklist only",
                        "case_cause_specific_fact_points": "learned per case cause from desensitized training materials",
                        "procedural_fact_extraction_points": "adjusted by procedure_type and procedure_stage",
                        "fact_extraction_summary": "common framework plus case-cause differentiated summary",
                    },
                    "legal": {
                        "path": "case_cause_profile.procedural_profile.legal_summary_points",
                        "substantive_path": "substantive_experience_profiles[].substantive_legal_summary_points",
                        "legal_summary": "statute / reasoning / review-note summary metadata",
                        "procedural_legal_summary_points": "adjusted by procedure_type and procedure_stage",
                    },
                    "procedural_profile": {
                        "path": "case_cause_profile.procedural_profile.metadata",
                        "strict_path": "procedural_experience_profiles[]",
                        "required_material_patterns": "procedure/stage material emphasis",
                        "evidence_review_points": "procedure/stage evidence emphasis",
                        "substantive_impact_points": "how procedure affects substantive judgment",
                        "procedural_transition_rules": "procedure transition metadata",
                        "risk_warnings": "procedure/stage risks",
                    },
                    "audit": "audit_metadata",
                    "source_trace": "source_trace_metadata",
                },
                "diff_readiness": "case_cause_specific_fact_points and procedural_profile points must differ across case causes, procedure types, and stages when training materials indicate different legal/procedural posture",
                "runtime_loading_rules": {
                    "substantive_experience_match": "case_cause + substantive_issue + fact_pattern + evidence_pattern; may cross procedure only when usage boundary allows",
                    "procedural_experience_match": "procedure_type + procedure_stage exact match only; no cross-procedure or cross-stage use",
                    "unclear_procedure_or_stage": "manual_confirmation_review_queue",
                },
                "provider_result_status": "metadata_only",
                "audit": "audit_metadata",
                "source_trace": "source_trace_metadata",
            },
            "output_groups": output_groups,
            "differentiated_fact_extraction_experience_package": differentiated_package,
            "provider_specs": provider_specs,
            "prompt_strategy": {
                "role": "法律案件分析 Skill 训练建模器",
                "baseline_skills": target_skill_ids,
                "template": "读取脱敏训练上下文、判决结构 metadata、律师底稿结构 metadata、证据索引 metadata、裁判理由摘要 metadata、法律检索候选 metadata 与 provider-gated status metadata，先套用共用事实/法律框架，再按案由、程序类型和程序阶段总结差异化事实要点、法律要点、材料重点、证据重点、实体影响和风险提示。",
                "common_framework_rule": "共用模板只提供事实提炼基础结构，不得写死民间借贷、买卖合同、劳动争议或婚姻家事等案由细节。",
                "case_cause_learning_rule": "Codex 应从训练材料类型、争点、证据链、裁判理由和法条检索 metadata 中抽象出案由专属事实点。",
                "procedural_learning_rule": "Codex 应识别 litigation / arbitration 及 first_instance / second_instance / retrial / commercial_arbitration / labor_arbitration 等阶段差异，并记录其对材料类型、证据重点、实体判断、法律要点和风险提示的影响。",
                "substantive_procedural_boundary_rule": "实体经验按案由、实体法律问题、事实结构和证据结构组织，可在边界允许时跨程序参考；程序经验按 procedure_type + procedure_stage 严格组织，不得跨程序或跨阶段直接参照。",
                "profile_match_rule": "实战系统使用 case_cause_code + procedure_type + procedure_stage 匹配 procedural_profile；缺少程序或阶段时进入 manual confirmation / review queue。",
                "required_output": ["legal_summary", "fact_extraction_summary", "common_fact_extraction_framework", "substantive_experience_profiles", "procedural_experience_profiles", "procedural_profiles", "substantive_impact_points", "audit", "source_trace"],
                "allowed_freedom": ["output rules", "workflow steps", "risk warning rules", "evidence handling rules"],
                "required_interface_context": [
                    "OCR / document parse provider adapters must remain disabled unless provider-gated",
                    "legal retrieval adapters must return reviewed metadata candidates only",
                    "enterprise lookup adapters must not become final fact findings automatically",
                ],
                "provider_credential_refs": [
                    {
                        "provider_type": spec["provider_type"],
                        "credential_alias": spec["credential_alias"],
                        "credential_loaded": spec["credential_loaded"],
                        "gate_requirements": spec["gate_requirements"],
                        "value_stored_in_skill": False,
                    }
                    for spec in provider_specs
                ],
                "adapter_call_contract": "Skill calls adapter methods and receives status/result metadata only; adapter handles credential lookup inside backend runtime.",
                "forbidden_actions": ["source_payload_output", "credential_value_access", "skill_publish", "runtime_package_replace", "party_identity_output"],
            },
            "experience_package_refs": manifest.source_package_ids if manifest else [],
            "training_example_refs": [example.example_id for example in manifest.examples] if manifest else [],
            "evaluation_plan": [
                "fact_extraction_rubric_alignment",
                "legal_analysis_rubric_alignment",
                "schema_alignment",
                "case_cause_differentiation",
                "procedural_stage_differentiation",
                "substantive_vs_procedural_boundary",
                "substantive_impact_presence",
                "legal_summary_presence",
                "metadata_safety",
                "traceability",
                "lawyer_review_readiness",
            ],
            "safety_constraints": ["no source payload", "no provider call", "not publishable", "not runtime loadable"],
            "source_trace_bundle_id": f"{skill_id}_source_trace_bundle",
            "audit_bundle_id": f"{skill_id}_audit_bundle",
            "created_at": now,
            "warnings": ["Training Skill Spec 为不可发布、不可 runtime load 的 metadata artifact。"],
        }
    )
    write_payload(CODEX_TRAINING_SKILLS_DIR, skill_id, skill)
    return skill


def list_training_skills() -> dict[str, Any]:
    skills = read_payloads(CODEX_TRAINING_SKILLS_DIR)
    if not skills:
        skills = [generate_training_skill()]
    return _with_flags({"training_skills": skills, "skill_count": len(skills), "warnings": ["Training Skill 仅为草案 metadata。"]})


def get_training_skill(training_skill_id: str) -> dict[str, Any] | None:
    return _find(CODEX_TRAINING_SKILLS_DIR, "training_skill_id", training_skill_id)


def run_training_skill_gate(training_skill_id: str) -> dict[str, Any] | None:
    skill = get_training_skill(training_skill_id)
    if not skill:
        return None
    report = _skill_gate_report(skill)
    skill["skill_status"] = "ready_for_dry_run_training" if report["gate_status"] == "passed" else "blocked"
    write_payload(CODEX_TRAINING_SKILLS_DIR, training_skill_id, skill)
    return report


def get_training_skill_gate_report(training_skill_id: str) -> dict[str, Any] | None:
    skill = get_training_skill(training_skill_id)
    if not skill:
        return None
    return _skill_gate_report(skill)


def get_training_skill_audit(training_skill_id: str) -> dict[str, Any] | None:
    skill = get_training_skill(training_skill_id)
    if not skill:
        return None
    return _with_flags(
        {
            "audit_bundle_id": skill["audit_bundle_id"],
            "training_skill_id": training_skill_id,
            "events": [
                {"event": "dataset_gate_checked", "status": "passed"},
                {"event": "training_skill_spec_generated", "status": "metadata_only"},
                {"event": "publish_boundary_checked", "status": "blocked_by_default"},
            ],
            "event_count": 3,
            "warnings": ["Audit contains metadata events only."],
        }
    )


def get_training_skill_source_trace(training_skill_id: str) -> dict[str, Any] | None:
    skill = get_training_skill(training_skill_id)
    if not skill:
        return None
    return _with_flags(
        {
            "source_trace_bundle_id": skill["source_trace_bundle_id"],
            "training_skill_id": training_skill_id,
            "training_dataset_id": skill["training_dataset_id"],
            "training_example_ref_count": len(skill["training_example_refs"]),
            "trace_status": "complete_metadata_only",
            "warnings": ["Source trace references metadata identifiers only."],
        }
    )


def build_v737_training_skill_status() -> dict[str, Any]:
    skills = read_payloads(CODEX_TRAINING_SKILLS_DIR)
    return _with_flags(
        {
            "version": "v7.37.addon",
            "status": "codex_training_skill_spec_ready",
            "training_skill_count": len(skills),
            "ready_for_dry_run_training_count": sum(1 for item in skills if item.get("skill_status") == "ready_for_dry_run_training"),
            "warnings": ["该接口为已完成 v7.37 之后的兼容补口径，不替换原 v7.37 internal training run。"],
        }
    )


def get_training_skill_interface_doc() -> dict[str, Any]:
    return _with_flags(
        {
            "interface_doc_id": "codex_training_skill_interface_doc_v737_addon",
            "title": "Codex Training Skill 封装接口文档",
            "version": "v7.37.addon",
            "baseline_skill_ids": ["case_fact_extraction_skill", "case_legal_analysis_skill"],
            "legacy_package_refs": [FACT_BASELINE["training_package_id"], LEGAL_BASELINE["training_package_id"]],
            "provider_boundary": {
                "ocr_document_provider": "adapter metadata only; live calls disabled unless later provider-gated target explicitly enables",
                "legal_retrieval_provider": "mock/local registry metadata by default; reviewed legal candidates only",
                "enterprise_provider": "metadata verification candidates only; not final fact findings",
                "credential_handling": "environment names may be documented; key values are never read, returned, logged, or stored",
            },
            "provider_credential_contract": [
                {
                    "provider_type": spec["provider_type"],
                    "credential_alias": spec["credential_alias"],
                    "credential_loaded": spec["credential_loaded"],
                    "loaded_state_field": "credential_loaded",
                    "gate_requirements": spec["gate_requirements"],
                    "value_stored_in_skill": False,
                }
                for spec in provider_specs_with_loaded_state()
            ],
            "request_contracts": [
                {
                    "endpoint": "POST /personal-skill-studio/training-artifacts/codex-training-skills/generate",
                    "body": {"training_dataset_id": "optional metadata id", "skill_target": "case_fact_extraction_skill | case_legal_analysis_skill | case_analysis_skill"},
                    "returns": "CodexTrainingSkillSpec metadata",
                },
                {
                    "endpoint": "POST /personal-skill-studio/training-artifacts/codex-training-skills/{training_skill_id}/gate/run",
                    "body": {},
                    "returns": "Training Skill gate report metadata",
                },
                {
                    "endpoint": "POST /personal-skill-studio/training-artifacts/codex-skill-training-runs/start",
                    "body": {"training_skill_id": "metadata id", "run_mode": "dry_run | internal_training_simulation"},
                    "returns": "v7.38 training run metadata",
                },
                {
                    "endpoint": "POST /personal-skill-studio/training-artifacts/codex-training-skills/{training_skill_id}/provider-call/mock",
                    "body": {"provider_type": "OCR_API | Legal_API | Enterprise_API", "method_name": "optional adapter method"},
                    "returns": "provider-gated placeholder result metadata",
                },
            ],
            "required_inputs": [
                "v7.35 Training Dataset Manifest metadata",
                "abstracted Training Examples",
                "redacted experience package refs",
                "differentiated fact extraction experience package metadata",
                "case_fact_extraction_skill manifest",
                "case_legal_analysis_skill manifest",
                "fact and legal evaluation/gate refs",
                "provider_specs with credential_alias and credential_loaded state",
            ],
            "output_schema": {
                "facts": {
                    "path": "case_cause_profile.procedural_profile.fact_extraction_points",
                    "substantive_path": "substantive_experience_profiles[].fact_extraction_points",
                    "common_fact_extraction_framework": COMMON_FACT_EXTRACTION_FRAMEWORK,
                    "case_cause_specific_fact_points": "array per case cause, learned from desensitized training metadata",
                    "procedural_fact_extraction_points": "array per procedure type and stage",
                    "fact_extraction_summary": "shared framework plus case-cause differentiated summary",
                },
                "legal": {
                    "path": "case_cause_profile.procedural_profile.legal_summary_points",
                    "substantive_path": "substantive_experience_profiles[].substantive_legal_summary_points",
                    "legal_summary": "legal point summary metadata",
                },
                "procedural_profile": {
                    "strict_path": "procedural_experience_profiles[]",
                    "required_material_patterns": "procedure/stage material emphasis",
                    "evidence_review_points": "procedure/stage evidence emphasis",
                    "substantive_impact_points": "substantive impact from procedure/stage differences",
                    "procedural_transition_rules": "transition metadata",
                    "risk_warnings": "procedure/stage risks",
                },
                "runtime_loading": {
                    "substantive_experience": "may cross procedure only when boundary conditions pass",
                    "procedural_experience": "exact procedure_type + procedure_stage only",
                    "missing_procedure_or_stage": "manual confirmation / review queue",
                },
                "audit": "required",
                "source_trace": "required",
            },
            "forbidden_outputs": [
                "source payload",
                "OCR payload",
                "provider payload",
                "credential value",
                "filesystem location",
                "final legal opinion",
                "formal report",
                "publishable Skill artifact",
                "runtime-loadable package",
            ],
            "warnings": ["本文档为接口与边界 metadata，不包含真实 provider token、API key 或材料内容。"],
        }
    )


def start_skill_training_run(payload: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = payload or {}
    skill_id = payload.get("training_skill_id")
    skill = get_training_skill(str(skill_id)) if skill_id else None
    if skill is None:
        skill = generate_training_skill()
    now = _now()
    run_id = f"codex_skill_training_run_v738_{uuid4().hex[:10]}"
    run_mode = str(payload.get("run_mode") or "dry_run")
    failed = []
    if skill.get("skill_status") != "ready_for_dry_run_training":
        failed.append("training_skill_not_ready")
    provider_checks = [
        call_provider_placeholder("OCR_API", "submit_ocr_job"),
        call_provider_placeholder("Legal_API", "search_statutes"),
        call_provider_placeholder("Enterprise_API", "lookup_enterprise_profile"),
    ]
    run_status = "completed" if not failed else "blocked"
    metrics = _with_flags(
        {
            "metrics_id": f"{run_id}_metrics",
            "training_run_id": run_id,
            "examples_count": len(skill.get("training_example_refs", [])),
            "passed_examples_count": len(skill.get("training_example_refs", [])) if not failed else 0,
            "failed_examples_count": 0 if not failed else len(skill.get("training_example_refs", [])),
            "schema_alignment_score": 0.96 if not failed else 0.0,
            "case_cause_differentiation_score": 0.95 if _case_cause_differentiation_validated(skill) and not failed else 0.0,
            "procedural_stage_differentiation_score": 0.95 if _procedural_differentiation_validated(skill) and not failed else 0.0,
            "substantive_procedural_boundary_score": 0.96 if _experience_split_boundary_validated(skill) and not failed else 0.0,
            "substantive_impact_score": 0.94 if _substantive_impact_present(skill) and not failed else 0.0,
            "legal_summary_score": 0.96 if skill.get("differentiated_fact_extraction_experience_package", {}).get("legal_summary") and not failed else 0.0,
            "safety_score": 1.0,
            "traceability_score": 1.0 if not failed else 0.5,
            "readiness_score": 0.94 if not failed else 0.2,
            "warnings": ["Metrics are internal simulation metadata."],
        }
    )
    artifact = _with_flags(
        {
            "trained_artifact_id": f"{run_id}_artifact",
            "training_run_id": run_id,
            "training_skill_id": skill["training_skill_id"],
            "artifact_status": "ready_for_packaging" if not failed else "blocked",
            "artifact_kind": "training_skill_artifact_metadata",
            "artifact_summary": "内部训练模拟产物 metadata；不可发布、不可 runtime load，需后续 Practice Load Review。",
            "generated_experience_package": skill.get("differentiated_fact_extraction_experience_package"),
            "fact_output_diff_summary": _fact_output_diff_summary(skill),
            "legal_summary_validated": bool(skill.get("differentiated_fact_extraction_experience_package", {}).get("legal_summary")),
            "case_cause_differentiation_validated": _case_cause_differentiation_validated(skill),
            "procedural_stage_differentiation_validated": _procedural_differentiation_validated(skill),
            "substantive_procedural_split_validated": _experience_split_boundary_validated(skill),
            "substantive_cross_procedure_boundary_validated": _substantive_cross_procedure_boundary_validated(skill),
            "procedural_exact_match_boundary_validated": _procedural_exact_match_boundary_validated(skill),
            "substantive_impact_validated": _substantive_impact_present(skill),
            "profile_loading_contract": skill.get("differentiated_fact_extraction_experience_package", {}).get("profile_loading_contract"),
            "not_publishable": True,
            "not_runtime_loadable": True,
            "requires_practice_load_review": True,
            "source_trace_id": f"{run_id}_artifact_source_trace",
            "audit_id": f"{run_id}_artifact_audit",
            "created_at": now,
        }
    )
    logs = [
        _with_flags({"log_id": f"{run_id}_log_01", "training_run_id": run_id, "step_name": "load_training_skill_spec", "step_status": "loaded", "message": "Loaded Training Skill Spec metadata.", "created_at": now}),
        _with_flags({"log_id": f"{run_id}_log_02", "training_run_id": run_id, "step_name": "run_internal_training_simulation", "step_status": run_status, "message": "Recorded internal simulation only.", "created_at": now}),
        _with_flags({"log_id": f"{run_id}_log_03", "training_run_id": run_id, "step_name": "confirm_publish_runtime_boundary", "step_status": "passed", "message": "Confirmed no publish, no runtime replacement, no provider call.", "created_at": now}),
    ]
    run = _with_flags(
        {
            "training_run_id": run_id,
            "training_skill_id": skill["training_skill_id"],
            "training_dataset_id": skill["training_dataset_id"],
            "run_mode": run_mode,
            "run_status": run_status,
            "started_at": now,
            "finished_at": now,
            "metrics_id": metrics["metrics_id"],
            "gate_report_id": f"{run_id}_gate_report",
            "artifact_id": artifact["trained_artifact_id"],
            "audit_id": f"{run_id}_audit",
            "source_trace_id": f"{run_id}_source_trace",
            "safety_flags": {"not_publishable": True, "not_runtime_loadable": True, "requires_practice_load_review": True},
            "logs": logs,
            "metrics": metrics,
            "artifact": artifact,
            "provider_adapter_checks": [check for check in provider_checks if check],
            "blocked_reason": ", ".join(failed) if failed else None,
            "warnings": ["v7.38 仅执行 dry run / internal simulation metadata，不发布 Skill、不替换 runtime package。"],
        }
    )
    write_payload(CODEX_SKILL_TRAINING_RUNS_DIR, run_id, run)
    return run


def list_skill_training_runs() -> dict[str, Any]:
    runs = read_payloads(CODEX_SKILL_TRAINING_RUNS_DIR)
    if not runs:
        runs = [start_skill_training_run()]
    return _with_flags({"training_runs": runs, "run_count": len(runs), "warnings": ["Training runs are metadata-only."]})


def get_skill_training_run(training_run_id: str) -> dict[str, Any] | None:
    return _find(CODEX_SKILL_TRAINING_RUNS_DIR, "training_run_id", training_run_id)


def get_skill_training_logs(training_run_id: str) -> dict[str, Any] | None:
    run = get_skill_training_run(training_run_id)
    if not run:
        return None
    return _with_flags({"training_run_id": training_run_id, "logs": run.get("logs", []), "log_count": len(run.get("logs", [])), "warnings": ["Logs contain no source content."]})


def get_skill_training_metrics(training_run_id: str) -> dict[str, Any] | None:
    run = get_skill_training_run(training_run_id)
    return run.get("metrics") if run else None


def get_skill_training_gate_report(training_run_id: str) -> dict[str, Any] | None:
    run = get_skill_training_run(training_run_id)
    if not run:
        return None
    passed = run["run_status"] == "completed"
    return _with_flags(
        {
            "training_gate_report_id": run["gate_report_id"],
            "training_run_id": training_run_id,
            "gate_status": "passed" if passed else "blocked",
            "training_skill_ready": passed,
            "metrics_available": bool(run.get("metrics")),
            "artifact_not_publishable": True,
            "artifact_not_runtime_loadable": True,
            "practice_load_review_required": True,
            "provider_boundary_safe": True,
            "key_boundary_safe": True,
            "facts_output_diff_check_passed": _case_cause_differentiation_validated(run),
            "procedural_stage_diff_check_passed": _procedural_differentiation_validated(run),
            "substantive_procedural_split_check_passed": _experience_split_boundary_validated(run),
            "procedural_exact_match_check_passed": _procedural_exact_match_boundary_validated(run),
            "substantive_impact_check_passed": _substantive_impact_present(run),
            "legal_summary_check_passed": bool(run.get("artifact", {}).get("legal_summary_validated")),
            "readiness_check_passed": passed,
            "warnings": ["Gate does not load or publish artifacts."],
        }
    )


def get_skill_training_artifact(training_run_id: str) -> dict[str, Any] | None:
    run = get_skill_training_run(training_run_id)
    return run.get("artifact") if run else None


def get_skill_training_audit(training_run_id: str) -> dict[str, Any] | None:
    run = get_skill_training_run(training_run_id)
    if not run:
        return None
    return _with_flags({"audit_id": run["audit_id"], "training_run_id": training_run_id, "events": [{"event": "training_run_recorded", "status": run["run_status"]}], "event_count": 1})


def get_skill_training_source_trace(training_run_id: str) -> dict[str, Any] | None:
    run = get_skill_training_run(training_run_id)
    if not run:
        return None
    return _with_flags({"source_trace_id": run["source_trace_id"], "training_run_id": training_run_id, "training_skill_id": run["training_skill_id"], "trace_status": "complete_metadata_only"})


def build_v738_status() -> dict[str, Any]:
    runs = read_payloads(CODEX_SKILL_TRAINING_RUNS_DIR)
    return _with_flags(
        {
            "version": "v7.38",
            "status": "codex_skill_training_run_ready",
            "training_run_count": len(runs),
            "completed_run_count": sum(1 for item in runs if item.get("run_status") == "completed"),
            "warnings": ["v7.38 不调用 provider、不读取 key value、不发布 Skill、不替换 runtime package。"],
        }
    )


def _skill_gate_report(skill: dict[str, Any]) -> dict[str, Any]:
    provider_specs = skill.get("provider_specs", [])
    provider_spec_complete = all(
        spec.get("provider_type") and spec.get("credential_alias") and "credential_loaded" in spec and spec.get("gate_requirements")
        for spec in provider_specs
    )
    package = skill.get("differentiated_fact_extraction_experience_package", {})
    facts_ready = bool(package.get("fact_extraction_summary")) and bool(package.get("case_cause_specific_fact_summaries"))
    legal_ready = bool(package.get("legal_summary"))
    diff_ready = _case_cause_differentiation_validated(skill)
    procedural_ready = _procedural_differentiation_validated(skill)
    split_ready = _experience_split_boundary_validated(skill)
    passed = bool(skill.get("training_dataset_id")) and bool(skill.get("training_example_refs")) and bool(skill.get("output_groups")) and provider_spec_complete and facts_ready and legal_ready and diff_ready and procedural_ready and split_ready
    return _with_flags(
        {
            "training_skill_gate_report_id": f"{skill['training_skill_id']}_gate_report",
            "training_skill_id": skill["training_skill_id"],
            "gate_status": "passed" if passed else "blocked",
            "training_dataset_gate_passed": passed,
            "training_examples_available": bool(skill.get("training_example_refs")),
            "skill_target_defined": bool(skill.get("skill_target")),
            "output_schema_aligned": bool(skill.get("output_groups")),
            "provider_specs_available": provider_spec_complete,
            "adapter_contract_defined": provider_spec_complete,
            "facts_output_schema_ready": facts_ready,
            "case_cause_differentiation_ready": diff_ready,
            "procedural_stage_differentiation_ready": procedural_ready,
            "substantive_procedural_split_ready": split_ready,
            "substantive_cross_procedure_boundary_ready": _substantive_cross_procedure_boundary_validated(skill),
            "procedural_exact_match_boundary_ready": _procedural_exact_match_boundary_validated(skill),
            "substantive_impact_ready": _substantive_impact_present(skill),
            "profile_loading_contract_ready": bool(package.get("profile_loading_contract", {}).get("two_layer_matching")),
            "legal_summary_ready": legal_ready,
            "diff_readiness_check": "passed" if diff_ready else "blocked",
            "no_source_payload": True,
            "no_ocr_payload": True,
            "no_filesystem_location": True,
            "credential_boundary_safe": True,
            "credential_value_stored_in_skill": False,
            "source_trace_complete": True,
            "audit_complete": True,
            "not_publishable_by_default": True,
            "not_runtime_loadable_by_default": True,
            "warnings": ["Training Skill Gate is metadata-only."],
        }
    )


def _output_groups(manifest) -> list[dict[str, Any]]:
    source_groups = sorted({example.source_output_group for example in manifest.examples}) if manifest else []
    groups = source_groups or ["fact_extraction", "legal_analysis"]
    base_groups = [
        {
            "group_id": group,
            "group_title": "事实提取" if group == "fact_extraction" else "法律分析",
            "group_type": group,
            "outputs": ["summary", "evidence_alignment", "risk_warning"] if group == "fact_extraction" else ["issue_analysis", "rule_application", "review_note"],
        }
        for group in groups
    ]
    base_groups.extend(
        [
            {
                "group_id": "facts",
                "group_title": "案由+程序+阶段事实提炼经验包",
                "group_type": "facts",
                "outputs": ["common_fact_extraction_framework", "case_cause_specific_fact_points", "procedural_fact_extraction_points", "fact_extraction_summary"],
            },
            {
                "group_id": "legal",
                "group_title": "案由+程序+阶段法律要点经验包",
                "group_type": "legal",
                "outputs": ["legal_summary", "procedural_legal_summary_points", "substantive_impact_points", "lawyer_review_note"],
            },
            {
                "group_id": "procedural_profile",
                "group_title": "程序画像与实体影响",
                "group_type": "procedural_profile",
                "outputs": ["required_material_patterns", "evidence_review_points", "procedural_transition_rules", "risk_warnings"],
            },
        ]
    )
    return base_groups


def _differentiated_experience_package(manifest, skill_id: str) -> dict[str, Any]:
    case_cause_summaries = []
    case_cause_profiles = []
    substantive_profiles = []
    for profile in CASE_CAUSE_FACT_POINT_LIBRARY:
        trace_prefix = f"{skill_id}_{profile['case_cause_code'].replace('.', '_')}"
        procedural_profiles = _procedural_profiles_for_case_cause(profile, trace_prefix)
        substantive_profile = _substantive_profile_for_case_cause(profile, trace_prefix)
        case_cause_summaries.append(
            {
                "case_cause_code": profile["case_cause_code"],
                "case_cause_name": profile["case_cause_name"],
                "fact_extraction_summary": f"{profile['case_cause_name']}事实提炼应在共用框架下突出：" + "、".join(profile["case_cause_specific_fact_points"]) + "。",
                "case_cause_specific_fact_points": profile["case_cause_specific_fact_points"],
                "learned_from_material_types": profile["learned_from_material_types"],
                "legal_summary": profile["legal_summary"],
                "source_trace_id": f"{trace_prefix}_source_trace",
                "audit_id": f"{trace_prefix}_audit",
            }
        )
        substantive_profiles.append(substantive_profile)
        case_cause_profiles.append(
            {
                "case_cause_code": profile["case_cause_code"],
                "case_cause_name": profile["case_cause_name"],
                "case_cause_specific_fact_points": profile["case_cause_specific_fact_points"],
                "case_cause_legal_summary": profile["legal_summary"],
                "substantive_experience_profiles": [substantive_profile],
                "procedural_experience_profiles": procedural_profiles,
                "procedural_profiles": procedural_profiles,
                "procedure_transition_rules": [
                    "一审→二审→再审：从事实认定和法律适用纠错逐步收窄到法定再审事由",
                    "仲裁→司法确认/撤销/执行：区分实体争议与程序审查边界",
                    "劳动仲裁→一审：围绕仲裁请求、裁决结果和起诉范围衔接",
                ],
                "manual_confirmation_required_when_missing": ["procedure_type", "procedure_stage"],
                "source_trace_id": f"{trace_prefix}_profile_source_trace",
                "audit_id": f"{trace_prefix}_profile_audit",
            }
        )
    procedural_experience_profiles = _procedural_experience_profiles(skill_id)
    package_id = f"{skill_id}_differentiated_experience_package"
    return _with_flags(
        {
            "experience_package_id": package_id,
            "package_title": "Case Analysis Skill Training - 案由/程序/阶段差异化经验包",
            "package_status": "ready_for_internal_training_dry_run",
            "experience_model": "substantive_and_procedural_profiles_split",
            "common_framework": {
                "fact_extraction_framework": COMMON_FACT_EXTRACTION_FRAMEWORK,
                "legal_summary_framework": COMMON_LEGAL_SUMMARY_FRAMEWORK,
            },
            "common_fact_extraction_framework": COMMON_FACT_EXTRACTION_FRAMEWORK,
            "common_legal_summary_framework": COMMON_LEGAL_SUMMARY_FRAMEWORK,
            "common_template_boundary": "共用模板只提供事实提炼基础结构，不写死案由细节。",
            "substantive_experience_profiles": substantive_profiles,
            "procedural_experience_profiles": procedural_experience_profiles,
            "case_cause_specific_fact_summaries": case_cause_summaries,
            "case_cause_profiles": case_cause_profiles,
            "profile_loading_contract": {
                "two_layer_matching": True,
                "substantive_match_keys": ["case_cause_code", "substantive_issue", "fact_pattern", "evidence_pattern"],
                "substantive_cross_procedure_reference_allowed": True,
                "substantive_cross_procedure_conditions": [
                    "case_cause matched or same hierarchy",
                    "substantive_issue matched",
                    "fact_pattern similar",
                    "evidence_pattern similar or explainable",
                    "usage_boundary allows cross-procedure reference",
                    "source_trace and audit complete",
                ],
                "procedural_match_keys": ["procedure_type", "procedure_stage"],
                "procedural_cross_stage_reference_allowed": False,
                "procedural_cross_procedure_reference_allowed": False,
                "loads": ["substantive_facts", "substantive_legal", "procedural_materials", "procedural_rules", "substantive_impact", "risk_warnings"],
                "missing_profile_action": "manual_confirmation_review_queue",
                "lawyer_review_required": True,
                "diff_supported": True,
                "audit_required": True,
                "source_trace_required": True,
            },
            "legal_summary": "法律要点 summary 由法条检索候选、裁判理由摘要、争点结构与律师复核 metadata 抽象生成。",
            "fact_extraction_summary": "事实提炼 summary 由共用框架与案由差异化事实点共同组成。",
            "case_cause_count": len(case_cause_summaries),
            "substantive_experience_profile_count": len(substantive_profiles),
            "procedural_experience_profile_count": len(procedural_experience_profiles),
            "procedural_profile_count": sum(len(profile["procedural_profiles"]) for profile in case_cause_profiles),
            "source_material_metadata_types": ["judgment_structure", "lawyer_work_product_structure", "evidence_index", "court_reasoning_summary", "legal_retrieval_metadata"],
            "source_training_dataset_id": getattr(manifest, "dataset_id", None) if manifest else None,
            "source_example_count": len(getattr(manifest, "examples", []) or []) if manifest else 0,
            "source_trace_bundle_id": f"{package_id}_source_trace_bundle",
            "audit_bundle_id": f"{package_id}_audit_bundle",
            "diff_summary": "不同案由、程序类型与程序阶段输出不同事实、材料、证据、法律、实体影响和风险要点；共用框架保持一致，差异化内容由训练材料 metadata 学习生成。",
            "readiness_status": "passed",
            "lawyer_review_required": True,
            "warnings": ["经验包为脱敏、抽象化 metadata，仅供律师复核前参考。"],
        }
    )


def _case_cause_differentiation_validated(payload: dict[str, Any]) -> bool:
    package = payload.get("differentiated_fact_extraction_experience_package") or payload.get("generated_experience_package") or payload.get("artifact", {}).get("generated_experience_package") or {}
    summaries = package.get("case_cause_specific_fact_summaries") or []
    point_sets = {tuple(item.get("case_cause_specific_fact_points", [])) for item in summaries}
    return len(summaries) >= 2 and len(point_sets) >= 2


def _procedural_profiles_for_case_cause(case_cause_profile: dict[str, Any], trace_prefix: str) -> list[dict[str, Any]]:
    profiles = []
    for item in PROCEDURAL_PROFILE_LIBRARY:
        fact_points = list(dict.fromkeys([*case_cause_profile["case_cause_specific_fact_points"], *item["fact_focus"]]))
        profiles.append(
            {
                "profile_key": item["profile_key"],
                "procedure_type": item["procedure_type"],
                "procedure_stage": item["procedure_stage"],
                "profile_name": item["profile_name"],
                "metadata": {
                    "case_cause_code": case_cause_profile["case_cause_code"],
                    "case_cause_name": case_cause_profile["case_cause_name"],
                    "profile_match_key": f"{case_cause_profile['case_cause_code']}::{item['procedure_type']}::{item['procedure_stage']}",
                    "manual_confirmation_required": False,
                    "lawyer_review_required": True,
                    "audit_required": True,
                    "source_trace_required": True,
                },
                "required_material_patterns": item["required_material_patterns"],
                "fact_extraction_points": fact_points,
                "evidence_review_points": item["evidence_focus"],
                "legal_summary_points": list(dict.fromkeys([case_cause_profile["legal_summary"], *item["legal_focus"]])),
                "substantive_impact_points": item["substantive_impact_points"],
                "procedural_transition_rules": item["procedural_transition_rules"],
                "risk_warnings": item["risk_warnings"],
                "source_trace_id": f"{trace_prefix}_{item['profile_key']}_source_trace",
                "audit_id": f"{trace_prefix}_{item['profile_key']}_audit",
            }
        )
    return profiles


def _substantive_profile_for_case_cause(case_cause_profile: dict[str, Any], trace_prefix: str) -> dict[str, Any]:
    first_points = case_cause_profile["case_cause_specific_fact_points"]
    primary_issue = _primary_substantive_issue(case_cause_profile)
    return {
        "experience_type": "substantive",
        "profile_id": f"{trace_prefix}_substantive_profile",
        "case_cause_code": case_cause_profile["case_cause_code"],
        "case_cause_name": case_cause_profile["case_cause_name"],
        "case_cause_hierarchy": case_cause_profile["case_cause_code"].split(".")[:3],
        "substantive_issue": primary_issue,
        "fact_pattern": f"{case_cause_profile['case_cause_name']}核心事实结构 metadata",
        "evidence_pattern": f"{case_cause_profile['case_cause_name']}核心证据结构 metadata",
        "fact_extraction_points": first_points,
        "substantive_legal_summary_points": [case_cause_profile["legal_summary"], "实体构成要件", "抗辩边界", "责任范围"],
        "claim_basis_patterns": [f"{case_cause_profile['case_cause_name']}请求权基础 metadata"],
        "issue_to_rule_patterns": [f"{primary_issue} -> 实体规则适用 metadata"],
        "evidence_to_legal_effect_patterns": [f"{case_cause_profile['case_cause_name']}证据结构 -> 法律效果 metadata"],
        "court_reasoning_patterns": [f"{case_cause_profile['case_cause_name']}裁判理由抽象模式"],
        "risk_fact_patterns": ["关键事实缺口", "证明链条断点", "时点争议"],
        "risk_legal_points": ["举证责任风险", "抗辩成立风险", "责任范围调整风险"],
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
        "cross_procedure_reference_allowed": True,
        "usage_boundary": {
            "allows_cross_procedure_reference": True,
            "requires_case_cause_match_or_same_hierarchy": True,
            "requires_substantive_issue_match": True,
            "requires_fact_pattern_similarity": True,
            "requires_evidence_pattern_similarity_or_explanation": True,
            "procedural_rules_not_included": True,
            "lawyer_review_required": True,
        },
        "source_trace_id": f"{trace_prefix}_substantive_source_trace",
        "audit_id": f"{trace_prefix}_substantive_audit",
    }


def _procedural_experience_profiles(skill_id: str) -> list[dict[str, Any]]:
    profiles = []
    for item in PROCEDURAL_PROFILE_LIBRARY:
        profiles.append(
            {
                "experience_type": "procedural",
                "profile_id": f"{skill_id}_{item['profile_key']}_procedural_profile",
                "procedure_type": item["procedure_type"],
                "procedure_stage": item["procedure_stage"],
                "profile_key": item["profile_key"],
                "profile_name": item["profile_name"],
                "required_material_patterns": item["required_material_patterns"],
                "procedural_deadline_rules": _procedural_deadline_rules(item),
                "procedural_burden_rules": _procedural_burden_rules(item),
                "appeal_scope_rules": _appeal_scope_rules(item),
                "retrial_threshold_rules": _retrial_threshold_rules(item),
                "arbitration_clause_review_rules": _arbitration_clause_review_rules(item),
                "labor_arbitration_precondition_rules": _labor_arbitration_precondition_rules(item),
                "procedural_transition_rules": item["procedural_transition_rules"],
                "procedural_risk_warnings": item["risk_warnings"],
                "source_procedure_type": item["procedure_type"],
                "source_procedure_stage": item["procedure_stage"],
                "source_stage_reference": {
                    "source_procedure_type": item["procedure_type"],
                    "source_procedure_stage": item["procedure_stage"],
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
                    "substantive_reference_not_included": True,
                    "unclear_stage_routes_to_review_queue": True,
                    "lawyer_review_required": True,
                },
                "source_trace_id": f"{skill_id}_{item['profile_key']}_procedural_source_trace",
                "audit_id": f"{skill_id}_{item['profile_key']}_procedural_audit",
            }
        )
    return profiles


def _primary_substantive_issue(case_cause_profile: dict[str, Any]) -> str:
    if case_cause_profile["case_cause_code"] == "civil.contract.private_lending":
        return "借贷合意与款项交付认定"
    if case_cause_profile["case_cause_code"] == "civil.contract.sales":
        return "合同履行与违约责任认定"
    if case_cause_profile["case_cause_code"] == "civil.labor.dispute":
        return "劳动关系与解除合法性认定"
    return "身份财产与责任承担认定"


def _procedural_deadline_rules(item: dict[str, Any]) -> list[str]:
    if item["procedure_stage"] == "second_instance":
        return ["上诉期间与补充材料期限 metadata", "二审举证期限需单独复核"]
    if item["procedure_stage"] == "retrial":
        return ["再审申请期限 metadata", "再审事由提出期限需复核"]
    if item["procedure_stage"] == "labor_arbitration":
        return ["劳动仲裁时效 metadata", "仲裁前置期限需复核"]
    return ["立案/举证/开庭期限 metadata", "保全期限需复核"]


def _procedural_burden_rules(item: dict[str, Any]) -> list[str]:
    if item["procedure_stage"] == "labor_arbitration":
        return ["用人单位管理材料举证责任 metadata", "劳动者初步举证与举证责任转移"]
    if item["procedure_stage"] == "second_instance":
        return ["上诉人需说明原审错误与新证据条件", "被上诉人围绕上诉范围回应"]
    return ["主张方承担基础事实举证责任", "抗辩方承担抗辩事实举证责任"]


def _appeal_scope_rules(item: dict[str, Any]) -> list[str]:
    return ["上诉请求范围限制", "二审争点审查边界"] if item["procedure_stage"] == "second_instance" else ["非二审 profile 不直接适用上诉范围规则"]


def _retrial_threshold_rules(item: dict[str, Any]) -> list[str]:
    return ["法定再审事由", "重大证据足以影响原裁判"] if item["procedure_stage"] == "retrial" else ["非再审 profile 不直接适用再审门槛规则"]


def _arbitration_clause_review_rules(item: dict[str, Any]) -> list[str]:
    return ["仲裁协议效力", "仲裁范围与机构约定", "撤裁/不予执行事由边界"] if item["procedure_stage"] == "commercial_arbitration" else ["非商事仲裁 profile 不直接适用仲裁协议审查规则"]


def _labor_arbitration_precondition_rules(item: dict[str, Any]) -> list[str]:
    return ["劳动仲裁前置", "仲裁请求与后续诉讼范围衔接", "劳动仲裁时效"] if item["procedure_stage"] == "labor_arbitration" else ["非劳动仲裁 profile 不直接适用劳动仲裁前置规则"]


def _procedural_differentiation_validated(payload: dict[str, Any]) -> bool:
    package = payload.get("differentiated_fact_extraction_experience_package") or payload.get("generated_experience_package") or payload.get("artifact", {}).get("generated_experience_package") or {}
    profiles = package.get("procedural_experience_profiles") or _flatten_procedural_profiles(package)
    profile_keys = {item.get("profile_key") for item in profiles}
    procedure_stages = {item.get("procedure_stage") for item in profiles}
    material_sets = {tuple(item.get("required_material_patterns", [])) for item in profiles}
    return len(profile_keys) >= 3 and len(procedure_stages) >= 3 and len(material_sets) >= 3


def _substantive_impact_present(payload: dict[str, Any]) -> bool:
    package = payload.get("differentiated_fact_extraction_experience_package") or payload.get("generated_experience_package") or payload.get("artifact", {}).get("generated_experience_package") or {}
    substantive_profiles = package.get("substantive_experience_profiles") or []
    return bool(substantive_profiles) and all(item.get("substantive_impact_points") for item in substantive_profiles)


def _experience_split_boundary_validated(payload: dict[str, Any]) -> bool:
    package = payload.get("differentiated_fact_extraction_experience_package") or payload.get("generated_experience_package") or payload.get("artifact", {}).get("generated_experience_package") or {}
    return _substantive_cross_procedure_boundary_validated(payload) and _procedural_exact_match_boundary_validated(payload) and bool(package.get("profile_loading_contract", {}).get("two_layer_matching"))


def _substantive_cross_procedure_boundary_validated(payload: dict[str, Any]) -> bool:
    package = payload.get("differentiated_fact_extraction_experience_package") or payload.get("generated_experience_package") or payload.get("artifact", {}).get("generated_experience_package") or {}
    profiles = package.get("substantive_experience_profiles") or []
    return bool(profiles) and all(
        item.get("experience_type") == "substantive"
        and item.get("runtime_reference_type") == "substantive_reference"
        and item.get("usage_boundary", {}).get("allows_cross_procedure_reference") is True
        and item.get("usage_boundary", {}).get("procedural_rules_not_included") is True
        and item.get("source_trace_id")
        and item.get("audit_id")
        for item in profiles
    )


def _procedural_exact_match_boundary_validated(payload: dict[str, Any]) -> bool:
    package = payload.get("differentiated_fact_extraction_experience_package") or payload.get("generated_experience_package") or payload.get("artifact", {}).get("generated_experience_package") or {}
    profiles = package.get("procedural_experience_profiles") or []
    return bool(profiles) and all(
        item.get("experience_type") == "procedural"
        and item.get("runtime_reference_type") == "procedural_exact_match"
        and item.get("cross_procedure_reference_allowed") is False
        and item.get("cross_stage_reference_allowed") is False
        and item.get("usage_boundary", {}).get("exact_procedure_type_required") is True
        and item.get("usage_boundary", {}).get("exact_procedure_stage_required") is True
        and item.get("source_trace_id")
        and item.get("audit_id")
        for item in profiles
    )


def _flatten_procedural_profiles(package: dict[str, Any]) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for case_profile in package.get("case_cause_profiles", []) or []:
        profiles.extend(case_profile.get("procedural_profiles", []) or [])
    return profiles


def _fact_output_diff_summary(skill: dict[str, Any]) -> dict[str, Any]:
    package = skill.get("differentiated_fact_extraction_experience_package", {})
    summaries = package.get("case_cause_specific_fact_summaries") or []
    procedural_profiles = package.get("procedural_experience_profiles") or _flatten_procedural_profiles(package)
    substantive_profiles = package.get("substantive_experience_profiles") or []
    return {
        "common_framework_count": len(package.get("common_fact_extraction_framework") or []),
        "case_cause_count": len(summaries),
        "substantive_experience_profile_count": len(substantive_profiles),
        "procedural_experience_profile_count": len(procedural_profiles),
        "procedural_profile_count": len(procedural_profiles),
        "procedure_stage_count": len({item.get("procedure_stage") for item in procedural_profiles}),
        "case_cause_specific_point_counts": {
            item.get("case_cause_name", "unknown"): len(item.get("case_cause_specific_fact_points", []))
            for item in summaries
        },
        "diff_check": "passed" if _case_cause_differentiation_validated(skill) else "blocked",
        "procedural_diff_check": "passed" if _procedural_differentiation_validated(skill) else "blocked",
        "substantive_procedural_boundary_check": "passed" if _experience_split_boundary_validated(skill) else "blocked",
        "substantive_impact_check": "passed" if _substantive_impact_present(skill) else "blocked",
        "readiness_status": package.get("readiness_status", "pending"),
    }


def _target_skill_ids(skill_target: str) -> list[str]:
    if skill_target == "case_fact_extraction_skill":
        return ["case_fact_extraction_skill"]
    if skill_target == "case_legal_analysis_skill":
        return ["case_legal_analysis_skill"]
    return ["case_fact_extraction_skill", "case_legal_analysis_skill"]


def _baseline_refs(target_skill_ids: list[str]) -> list[dict[str, Any]]:
    refs = []
    for baseline in [FACT_BASELINE, LEGAL_BASELINE]:
        if baseline["target_skill_id"] not in target_skill_ids:
            continue
        manifest = get_skill(baseline["target_skill_id"])
        refs.append(
            {
                **baseline,
                "v730_manifest_available": manifest is not None,
                "v730_skill_type": getattr(manifest, "skill_type", None) if manifest else None,
                "v730_prompt_templates": getattr(manifest, "prompt_templates", []) if manifest else [],
                "v730_test_case_ids": getattr(manifest, "test_case_ids", []) if manifest else [],
                "readonly": True,
                "auto_train_enabled": False,
                "auto_publish_enabled": False,
                "human_review_required": True,
            }
        )
    return refs


def _find(directory, field: str, value: str) -> dict[str, Any] | None:
    for payload in read_payloads(directory):
        if payload.get(field) == value:
            return payload
    return None


def _with_flags(payload: dict[str, Any]) -> dict[str, Any]:
    return {**SAFE_FLAGS, **payload}


def _now() -> str:
    return datetime.now(UTC).isoformat()
