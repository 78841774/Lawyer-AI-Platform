from personal_skill_studio.training_artifacts.schemas import (
    CodexTrainingScheme,
    EvaluationManifest,
    ExperiencePackageManifest,
    GateManifest,
    LoadingManifest,
    SkillManifest,
    TestCaseManifest,
)


def build_scheme() -> CodexTrainingScheme:
    return CodexTrainingScheme(
        training_steps=[
            "discover_synthetic_closed_case_training_metadata",
            "validate_case_cause_taxonomy",
            "match_multi_level_case_cause",
            "load_common_and_specific_packages",
            "merge_fact_and_legal_skill_metadata",
            "build_skill_context_dry_run",
        ],
        output_artifacts=[
            "experience_package_manifest",
            "skill_manifest",
            "evaluation_manifest",
            "gate_manifest",
            "test_case_manifest",
            "loading_manifest",
            "skill_context_manifest",
        ],
        validation_steps=[
            "schema_validation",
            "safety_boundary_validation",
            "lineage_validation",
            "case_cause_fallback_validation",
        ],
        loading_requirements=[
            "exact_match_first",
            "ancestor_fallback_second",
            "common_package_fallback_third",
            "evidence_overlay_merge",
            "dry_run_only",
        ],
        warnings=[
            "Codex training means metadata reading and artifact generation, not model fine-tuning.",
            "Open-case data is forbidden for training artifacts in v7.30.",
        ],
    )


EXPERIENCE_PACKAGES = [
    ExperiencePackageManifest(
        package_id="pkg_common_civil",
        package_name="民事通用经验包",
        package_type="common",
        source_case_count=12,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="civil",
        case_cause_path=["civil"],
        case_cause_level=1,
        case_cause_ids=["civil"],
        priority=10,
        load_strategy="common_package_fallback",
        applicable_patterns=["主体关系", "时间线", "证据链", "请求权基础"],
        extracted_patterns=["事实摘要结构", "证据映射结构", "争议焦点结构"],
        reasoning_templates=["事实-证据-争议", "请求-抗辩-风险"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
    ),
    ExperiencePackageManifest(
        package_id="pkg_civil_contract",
        package_name="合同纠纷通用经验包",
        package_type="ancestor",
        source_case_count=8,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="civil.contract_dispute",
        case_cause_path=["civil", "contract_dispute"],
        case_cause_level=2,
        case_cause_ids=["civil_contract_dispute"],
        parent_package_ids=["pkg_common_civil"],
        fallback_package_ids=["pkg_common_civil"],
        priority=30,
        load_strategy="ancestor_fallback",
        applicable_patterns=["合同成立", "履行节点", "违约事实", "损失计算"],
        extracted_patterns=["合同履行时间线", "付款/交付对照表", "违约抗辩候选"],
        reasoning_templates=["合同效力-履行-违约", "付款请求-质量抗辩"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        evidence_types=["contract", "invoice", "delivery_record", "payment_record"],
    ),
    ExperiencePackageManifest(
        package_id="pkg_sales_contract",
        package_name="买卖合同纠纷经验包",
        package_type="exact",
        source_case_count=5,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="civil.contract_dispute.sales_contract_dispute",
        case_cause_path=["civil", "contract_dispute", "sales_contract_dispute"],
        case_cause_level=3,
        case_cause_ids=["civil_contract_sales"],
        parent_package_ids=["pkg_civil_contract"],
        fallback_package_ids=["pkg_civil_contract", "pkg_common_civil"],
        priority=80,
        load_strategy="exact_match",
        applicable_patterns=["订单", "交付", "验收", "对账", "欠款"],
        extracted_patterns=["货款事实矩阵", "质量异议节点", "交付证明链"],
        reasoning_templates=["货款请求权结构", "质量抗辩结构"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        evidence_types=["contract", "invoice", "delivery_record", "reconciliation_record"],
    ),
    ExperiencePackageManifest(
        package_id="pkg_loan_contract",
        package_name="借款合同纠纷经验包",
        package_type="exact",
        source_case_count=4,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="civil.contract_dispute.loan_contract_dispute",
        case_cause_path=["civil", "contract_dispute", "loan_contract_dispute"],
        case_cause_level=3,
        case_cause_ids=["civil_contract_loan"],
        parent_package_ids=["pkg_civil_contract"],
        fallback_package_ids=["pkg_civil_contract", "pkg_common_civil"],
        priority=78,
        load_strategy="exact_match",
        applicable_patterns=["借款交付", "利息约定", "还款节点", "催收记录"],
        extracted_patterns=["本金利息矩阵", "还款时间线", "担保责任候选"],
        reasoning_templates=["借款返还结构", "利息边界结构"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        evidence_types=["loan_contract", "transfer_record", "repayment_record"],
    ),
    ExperiencePackageManifest(
        package_id="pkg_civil_tort",
        package_name="侵权责任纠纷通用经验包",
        package_type="ancestor",
        source_case_count=6,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="civil.tort_dispute",
        case_cause_path=["civil", "tort_dispute"],
        case_cause_level=2,
        case_cause_ids=["civil_tort_dispute"],
        parent_package_ids=["pkg_common_civil"],
        fallback_package_ids=["pkg_common_civil"],
        priority=28,
        load_strategy="ancestor_fallback",
        applicable_patterns=["侵权行为", "损害后果", "因果关系", "责任比例"],
        extracted_patterns=["损害项目清单", "责任比例候选", "证据缺口清单"],
        reasoning_templates=["行为-损害-因果-责任"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        evidence_types=["medical_record", "expense_record", "accident_record"],
    ),
    ExperiencePackageManifest(
        package_id="pkg_traffic_accident",
        package_name="交通事故责任纠纷经验包",
        package_type="exact",
        source_case_count=3,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="civil.tort_dispute.traffic_accident_dispute",
        case_cause_path=["civil", "tort_dispute", "traffic_accident_dispute"],
        case_cause_level=3,
        case_cause_ids=["civil_tort_traffic"],
        parent_package_ids=["pkg_civil_tort"],
        fallback_package_ids=["pkg_civil_tort", "pkg_common_civil"],
        priority=75,
        load_strategy="exact_match",
        applicable_patterns=["事故经过", "责任认定", "保险关系", "损害项目"],
        extracted_patterns=["事故责任矩阵", "损失项目汇总", "保险赔付边界"],
        reasoning_templates=["责任认定-损失-保险"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        evidence_types=["traffic_accident_certificate", "medical_record", "insurance_policy"],
    ),
    ExperiencePackageManifest(
        package_id="pkg_evidence_overlay",
        package_name="证据映射覆盖包",
        package_type="evidence_overlay",
        source_case_count=10,
        target_skill_ids=["case_fact_extraction_skill", "case_legal_analysis_skill"],
        case_cause_scope="evidence_overlay",
        case_cause_path=["civil"],
        case_cause_level=0,
        case_cause_ids=["civil"],
        priority=95,
        load_strategy="evidence_type_overlay",
        applicable_patterns=["证据类型映射", "缺失证据提示", "来源追踪"],
        extracted_patterns=["证据到事实映射", "证据到争点映射"],
        reasoning_templates=["证据-事实-争点 overlay"],
        source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        evidence_types=["contract", "invoice", "delivery_record", "payment_record", "medical_record"],
    ),
]


SKILL_MANIFESTS = [
    SkillManifest(
        skill_id="case_fact_extraction_skill",
        skill_name="案件事实提炼 Skill",
        skill_type="fact_extraction",
        source_package_ids=[package.package_id for package in EXPERIENCE_PACKAGES],
        derived_from=["v7.15 Skill Training Runtime metadata", "v7.22 Skill Final Draft metadata", "v7.30 training artifact loader"],
        supported_case_cause_paths=[
            ["civil"],
            ["civil", "contract_dispute"],
            ["civil", "contract_dispute", "sales_contract_dispute"],
            ["civil", "contract_dispute", "loan_contract_dispute"],
            ["civil", "tort_dispute"],
            ["civil", "tort_dispute", "traffic_accident_dispute"],
        ],
        pattern_sections={
            "fact_patterns": ["事实主体", "时间线", "合同履行节点", "侵权损害节点"],
            "evidence_mapping_rules": ["证据必须关联 source trace metadata", "缺失证据标记为 review item"],
            "timeline_rules": ["日期 metadata 归并", "无法确认日期进入律师复核"],
            "party_relation_rules": ["仅使用脱敏身份 metadata"],
            "disputed_fact_rules": ["争议事实单独进入 review queue"],
            "missing_fact_rules": ["缺失金额", "缺失履行节点", "缺失证据链"],
            "confidence_rules": ["置信度仅作参考"],
            "source_trace_rules": ["source_trace_required=true"],
            "correction_suggestion_rules": ["更正建议不自动覆盖原 metadata"],
            "case_cause_specific_fact_patterns": ["货款矩阵", "借款本金利息矩阵", "事故责任矩阵"],
        },
        prompt_templates=["fact_extraction_metadata_prompt", "case_cause_specific_fact_prompt"],
        test_case_ids=["tc_fact_sales_contract", "tc_fact_loan_contract", "tc_fact_traffic_accident"],
        evaluation_id="eval_case_fact_extraction_v7_30",
        gate_id="gate_case_fact_extraction_v7_30",
        optimization_suggestions=["补齐更多案由层级测试 metadata", "为证据覆盖包增加更多冲突证据场景"],
    ),
    SkillManifest(
        skill_id="case_legal_analysis_skill",
        skill_name="案件法律分析 Skill",
        skill_type="legal_analysis",
        source_package_ids=[package.package_id for package in EXPERIENCE_PACKAGES],
        derived_from=["v7.15 Skill Training Runtime metadata", "v7.22 Skill Final Draft metadata", "v7.30 training artifact loader"],
        supported_case_cause_paths=[
            ["civil"],
            ["civil", "contract_dispute"],
            ["civil", "contract_dispute", "sales_contract_dispute"],
            ["civil", "contract_dispute", "loan_contract_dispute"],
            ["civil", "tort_dispute"],
            ["civil", "tort_dispute", "traffic_accident_dispute"],
        ],
        pattern_sections={
            "legal_issue_patterns": ["法律关系识别", "争议焦点提炼", "请求权基础候选"],
            "claim_basis_patterns": ["合同请求权", "侵权损害赔偿请求权"],
            "defense_path_patterns": ["履行抗辩", "质量抗辩", "责任比例抗辩"],
            "burden_of_proof_rules": ["举证责任仅作草稿提示"],
            "legal_search_question_patterns": ["法律检索问题候选", "类案检索问题候选"],
            "citation_boundary_rules": ["候选引用不自动成为最终引用"],
            "enterprise_verification_rules": ["企业信息仅作为 verification metadata"],
            "risk_assessment_rules": ["风险提示不表述为结果保证"],
            "next_action_rules": ["下一步仅为 lawyer review checklist"],
            "case_cause_specific_legal_patterns": ["货款请求权", "利息边界", "交通事故赔偿项目"],
        },
        prompt_templates=["legal_analysis_metadata_prompt", "case_cause_specific_legal_prompt"],
        test_case_ids=["tc_legal_sales_contract", "tc_legal_loan_contract", "tc_legal_traffic_accident"],
        evaluation_id="eval_case_legal_analysis_v7_30",
        gate_id="gate_case_legal_analysis_v7_30",
        optimization_suggestions=["补齐抗辩路径评价 metadata", "为法律检索问题增加 source trace 完整度评分"],
    ),
]


EVALUATIONS = [
    EvaluationManifest(
        evaluation_id="eval_case_fact_extraction_v7_30",
        target_skill_id="case_fact_extraction_skill",
        dimensions=["事实完整性", "证据映射", "案由匹配", "来源追踪", "安全边界"],
        optimization_fields=["missing_fact_rules", "source_trace_rules", "case_cause_specific_fact_patterns"],
    ),
    EvaluationManifest(
        evaluation_id="eval_case_legal_analysis_v7_30",
        target_skill_id="case_legal_analysis_skill",
        dimensions=["争议焦点", "请求权基础", "抗辩路径", "引用边界", "安全边界"],
        optimization_fields=["claim_basis_patterns", "defense_path_patterns", "citation_boundary_rules"],
    ),
]


GATES = [
    GateManifest(
        gate_id="gate_case_fact_extraction_v7_30",
        target_skill_id="case_fact_extraction_skill",
        gate_fields=["source_trace_required", "raw_content_included=false", "lawyer_review_required", "gate_reference_only"],
    ),
    GateManifest(
        gate_id="gate_case_legal_analysis_v7_30",
        target_skill_id="case_legal_analysis_skill",
        gate_fields=["final_legal_opinion_generated=false", "final_report_generated=false", "citation_boundary_rules", "gate_reference_only"],
    ),
]


TEST_CASES = [
    TestCaseManifest(
        test_case_id="tc_fact_sales_contract",
        target_skill_id="case_fact_extraction_skill",
        scenario_type="sales_contract_metadata",
        case_cause_path=["civil", "contract_dispute", "sales_contract_dispute"],
        expected_metadata_fields=["fact_patterns", "evidence_mapping_rules", "source_trace_rules"],
    ),
    TestCaseManifest(
        test_case_id="tc_fact_loan_contract",
        target_skill_id="case_fact_extraction_skill",
        scenario_type="loan_contract_metadata",
        case_cause_path=["civil", "contract_dispute", "loan_contract_dispute"],
        expected_metadata_fields=["timeline_rules", "confidence_rules", "missing_fact_rules"],
    ),
    TestCaseManifest(
        test_case_id="tc_fact_traffic_accident",
        target_skill_id="case_fact_extraction_skill",
        scenario_type="traffic_accident_metadata",
        case_cause_path=["civil", "tort_dispute", "traffic_accident_dispute"],
        expected_metadata_fields=["evidence_mapping_rules", "disputed_fact_rules"],
    ),
    TestCaseManifest(
        test_case_id="tc_legal_sales_contract",
        target_skill_id="case_legal_analysis_skill",
        scenario_type="sales_contract_legal_metadata",
        case_cause_path=["civil", "contract_dispute", "sales_contract_dispute"],
        expected_metadata_fields=["claim_basis_patterns", "defense_path_patterns", "citation_boundary_rules"],
    ),
    TestCaseManifest(
        test_case_id="tc_legal_loan_contract",
        target_skill_id="case_legal_analysis_skill",
        scenario_type="loan_contract_legal_metadata",
        case_cause_path=["civil", "contract_dispute", "loan_contract_dispute"],
        expected_metadata_fields=["burden_of_proof_rules", "risk_assessment_rules"],
    ),
    TestCaseManifest(
        test_case_id="tc_legal_traffic_accident",
        target_skill_id="case_legal_analysis_skill",
        scenario_type="traffic_accident_legal_metadata",
        case_cause_path=["civil", "tort_dispute", "traffic_accident_dispute"],
        expected_metadata_fields=["legal_issue_patterns", "claim_basis_patterns", "risk_assessment_rules"],
    ),
]


LOADING_MANIFESTS = [
    LoadingManifest(
        loading_manifest_id="loading_manifest_v7_30",
        supported_load_strategies=[
            "exact_match",
            "ancestor_fallback",
            "common_package_fallback",
            "evidence_type_overlay",
            "merge_with_skill_manifest",
        ],
        merge_order=["common", "ancestor", "exact", "evidence_overlay", "skill_manifest"],
        conflict_resolution=["specific_package_wins", "evidence_overlay_appends", "safety_flags_are_most_restrictive"],
    )
]


def list_packages() -> list[ExperiencePackageManifest]:
    return list(EXPERIENCE_PACKAGES)


def get_package(package_id: str) -> ExperiencePackageManifest | None:
    return next((package for package in EXPERIENCE_PACKAGES if package.package_id == package_id), None)


def list_skills() -> list[SkillManifest]:
    return list(SKILL_MANIFESTS)


def get_skill(skill_id: str) -> SkillManifest | None:
    return next((skill for skill in SKILL_MANIFESTS if skill.skill_id == skill_id), None)


def list_evaluations() -> list[EvaluationManifest]:
    return list(EVALUATIONS)


def list_gates() -> list[GateManifest]:
    return list(GATES)


def list_test_cases() -> list[TestCaseManifest]:
    return list(TEST_CASES)


def list_loading_manifests() -> list[LoadingManifest]:
    return list(LOADING_MANIFESTS)

