from personal_case_analysis.skill_loader import get_skill_baseline
from personal_skill_studio.schemas import SkillFinalDraftList, SkillFinalDraftRecord
from personal_skill_studio.skill_baseline_discovery import build_baseline_discovery_metadata


FACT_SKILL_ID = "case_fact_extraction_skill"
LEGAL_SKILL_ID = "case_legal_analysis_skill"


def _fact_skill(discovery: object) -> SkillFinalDraftRecord:
    baseline = get_skill_baseline(FACT_SKILL_ID)
    baseline_complete = bool(baseline.baseline_detected and baseline.evaluation_detected and baseline.gate_detected)
    return SkillFinalDraftRecord(
        skill_id=FACT_SKILL_ID,
        skill_name="案件事实提炼 Skill",
        skill_type="fact_extraction",
        source_skill_id=baseline.source_skill_id,
        source_package_id=baseline.source_package_id,
        derived_from=[*baseline.derived_from, "v7.20 fact preview and correction metadata"],
        baseline_discovered=bool(baseline.baseline_detected or getattr(discovery, "baseline_discovered", False)),
        baseline_complete=baseline_complete,
        fact_patterns=["事实主体", "时间线", "合同履行节点", "争议事实", "缺失事实"],
        evidence_mapping_rules=["事实项必须关联 source trace metadata", "证据映射仅作为 review checklist", "缺失证据标记 low confidence"],
        timeline_rules=["按日期 metadata 归并", "无法确认日期时标记待律师复核"],
        party_relation_rules=["当事人关系仅使用脱敏身份 metadata", "不展示真实客户或对手方信息"],
        claim_defense_fact_rules=["区分请求事实与抗辩事实", "争议事实单独进入 review queue"],
        disputed_fact_rules=["低置信度和冲突事实不得进入最终表述", "争议事实仅作为草稿提示"],
        missing_fact_rules=["缺失金额", "缺失履行节点", "缺失证据链", "缺失律师确认"],
        confidence_rules=["高/中/低置信度仅为参考", "低置信度需要人工修订"],
        source_trace_rules=["source_trace_required=true", "raw content excluded", "audit_required=true"],
        prompt_templates=["使用既有 skill candidate prompt template metadata；如缺失则返回 placeholder lineage"],
        evaluation_cases=baseline.source_evaluation_files,
        test_cases=baseline.source_test_case_ids,
        review_checklist=["事实是否可追踪", "证据链是否完整", "是否仍含缺失事实", "是否经过律师复核"],
        optimization_suggestions=[
            "补齐 fact_patterns 对应的测试样本 metadata。",
            "为证据映射规则增加更多人工确认状态。",
            "将低置信度事实与争议事实分开展示，避免被理解为事实认定。",
        ],
        quality_score=76 if baseline_complete else 61,
        gate_status="reference_ready" if baseline_complete else "insufficient_baseline",
        warnings=[
            "案件事实提炼 Skill 最终稿仅为 owner-only metadata。",
            "不自动写入训练集，不自动发布 Skill，不使用未结案件训练。",
        ],
    )


def _legal_skill(discovery: object) -> SkillFinalDraftRecord:
    baseline = get_skill_baseline(LEGAL_SKILL_ID)
    baseline_complete = bool(baseline.baseline_detected and baseline.evaluation_detected and baseline.gate_detected)
    return SkillFinalDraftRecord(
        skill_id=LEGAL_SKILL_ID,
        skill_name="案件法律分析 Skill",
        skill_type="legal_analysis",
        source_skill_id=baseline.source_skill_id,
        source_package_id=baseline.source_package_id,
        derived_from=[*baseline.derived_from, "v7.21 legal analysis draft metadata"],
        baseline_discovered=bool(baseline.baseline_detected or getattr(discovery, "baseline_discovered", False)),
        baseline_complete=baseline_complete,
        legal_issue_patterns=["法律关系识别", "争议焦点提炼", "请求权基础候选", "抗辩路径候选"],
        claim_basis_patterns=["合同请求权 metadata", "违约责任 metadata", "损害计算 metadata"],
        defense_patterns=["履行抗辩", "证据不足", "时效/期间", "责任减轻"],
        burden_of_proof_rules=["举证责任仅作草稿提示", "律师复核前不得作为最终法律判断"],
        legal_search_question_patterns=["法律检索问题候选", "类案检索问题候选", "企业信息核验问题候选"],
        citation_selection_rules=["候选引用必须进入 source trace", "未确认来源不得作为最终引用"],
        risk_assessment_rules=["风险提示仅为 review note", "不得表述为胜诉概率或结果保证"],
        argument_structure_templates=["事实基础", "争议焦点", "请求权基础", "抗辩路径", "风险与下一步"],
        analysis_prompt_templates=["使用既有 legal analysis prompt template metadata；如缺失则返回 placeholder lineage"],
        evaluation_cases=baseline.source_evaluation_files,
        test_cases=baseline.source_test_case_ids,
        review_checklist=["是否仍为草稿", "是否存在最终意见措辞", "引用候选是否可追踪", "律师复核是否完成"],
        optimization_suggestions=[
            "补齐 claim_basis_patterns 对应的评价样本 metadata。",
            "为法律检索候选增加 source trace 完整度评分。",
            "把风险提示与法律结论分离，保持 draft-only。",
        ],
        quality_score=78 if baseline_complete else 63,
        gate_status="reference_ready" if baseline_complete else "insufficient_baseline",
        warnings=[
            "案件法律分析 Skill 最终稿仅为 owner-only metadata。",
            "不生成最终法律意见，不生成正式报告，不自动发布 Skill。",
        ],
    )


def list_skill_final_drafts() -> dict:
    discovery = build_baseline_discovery_metadata()
    drafts = [_fact_skill(discovery), _legal_skill(discovery)]
    return SkillFinalDraftList(
        final_drafts=drafts,
        draft_count=len(drafts),
        baseline_discovered=discovery.baseline_discovered,
        baseline_complete=all(draft.baseline_complete for draft in drafts),
        warnings=[
            "Two Skill final drafts are owner-only metadata.",
            "Gate and quality scores are reference-only and do not block next stage.",
        ],
    ).model_dump()


def get_skill_final_draft(skill_id: str) -> SkillFinalDraftRecord | None:
    for draft in SkillFinalDraftList(**list_skill_final_drafts()).final_drafts:
        if draft.skill_id == skill_id:
            return draft
    return None
