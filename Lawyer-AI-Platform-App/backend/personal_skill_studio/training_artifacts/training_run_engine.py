from datetime import UTC, datetime
from uuid import uuid4

from personal_case_analysis.skill_loader import build_skill_baseline_report
from personal_skill_studio.training_artifacts.closed_case_sample_registry import list_training_samples
from personal_skill_studio.training_artifacts.load_dry_run_engine import create_load_dry_run
from personal_skill_studio.training_artifacts.schemas import (
    CodexTrainingRunList,
    CodexTrainingRunRecord,
    CodexTrainingRunRequest,
    GeneratedEvaluationManifest,
    GeneratedExperiencePackageManifest,
    GeneratedGateManifest,
    GeneratedLoadingManifest,
    GeneratedSkillManifest,
    GeneratedTestCaseManifest,
    GeneratedTrainingRunManifest,
    LoadDryRunRequest,
    safety_flags,
)
from personal_skill_studio.training_artifacts.storage import TRAINING_RUNS_DIR, read_payload, read_payloads, write_payload


def create_training_run(request: CodexTrainingRunRequest) -> dict:
    training_run_id = f"codex_training_run_v7_31_{uuid4().hex[:12]}"
    samples = _filter_samples(request)
    packages = _build_packages(training_run_id, samples, request.target_skill_ids)
    skills = _build_skills(training_run_id, packages)
    evaluations = _build_evaluations(training_run_id, skills)
    gates = _build_gates(training_run_id, skills)
    test_cases = _build_test_cases(training_run_id, samples, packages, skills)
    loading_manifest = _build_loading_manifest(training_run_id, packages, skills, evaluations, gates, test_cases)
    generated_artifact_ids = [
        *[package.package_id for package in packages],
        *[skill.skill_id for skill in skills],
        *[evaluation.evaluation_id for evaluation in evaluations],
        *[gate.gate_id for gate in gates],
        *[test_case.test_case_id for test_case in test_cases],
        loading_manifest.loading_manifest_id,
    ]
    manifest = GeneratedTrainingRunManifest(
        training_run_id=training_run_id,
        source_case_mode="synthetic_closed_case",
        source_case_count=len(samples),
        synthetic_case_count=len(samples),
        target_skill_ids=request.target_skill_ids,
        case_cause_paths=[sample.case_cause_path for sample in samples],
        generated_artifact_ids=generated_artifact_ids,
        loading_manifest_id=loading_manifest.loading_manifest_id,
        safety_status={**safety_flags(), "codex_training": True, "training_run_generated": True},
        created_at=datetime.now(UTC).isoformat(),
    )
    baseline = _baseline_discovery()
    record = CodexTrainingRunRecord(
        training_run_id=training_run_id,
        manifest=manifest,
        baseline_discovery=baseline,
        training_samples=samples,
        experience_packages=packages,
        generated_skills=skills,
        evaluations=evaluations,
        gates=gates,
        test_cases=test_cases,
        loading_manifest=loading_manifest,
        warnings=[
            "v7.31 uses synthetic closed-case samples because no real closed-case sample set is read.",
            "Codex training is metadata generation, not model fine-tuning.",
        ],
    )
    write_payload(TRAINING_RUNS_DIR, training_run_id, record.model_dump())
    return record.model_dump()


def list_training_runs() -> dict:
    records = [CodexTrainingRunRecord(**payload) for payload in read_payloads(TRAINING_RUNS_DIR)]
    if not records:
        records = [CodexTrainingRunRecord(**create_training_run(CodexTrainingRunRequest()))]
    return CodexTrainingRunList(
        training_runs=records,
        run_count=len(records),
        warnings=["Training runs are synthetic closed-case metadata only."],
    ).model_dump()


def get_training_run(run_id: str) -> CodexTrainingRunRecord | None:
    payload = read_payload(TRAINING_RUNS_DIR, run_id)
    if payload:
        return CodexTrainingRunRecord(**payload)
    for payload in read_payloads(TRAINING_RUNS_DIR):
        record = CodexTrainingRunRecord(**payload)
        if record.training_run_id == run_id:
            return record
    return None


def create_training_run_load_dry_run(run_id: str) -> dict | None:
    record = get_training_run(run_id)
    if record is None:
        return None
    path = record.training_samples[0].case_cause_path if record.training_samples else ["civil"]
    request = LoadDryRunRequest(
        case_domain=path[0] if path else "civil",
        case_cause_level_1=path[1] if len(path) > 1 else "civil",
        case_cause_level_2=path[2] if len(path) > 2 else "",
        case_cause_name="synthetic_closed_case_training_metadata",
        case_cause_code="v7.31.training.metadata",
        case_cause_path=path,
        evidence_types=record.training_samples[0].applicable_evidence_types if record.training_samples else [],
        target_skill_ids=[skill.skill_id for skill in record.generated_skills],
    )
    dry_run = create_load_dry_run(request)
    record.load_dry_run_result = dry_run
    write_payload(TRAINING_RUNS_DIR, run_id, record.model_dump())
    return {
        "training_run_id": run_id,
        "load_dry_run_result": dry_run,
        **_safety_response(),
        "warnings": ["Training run artifacts were validated through the v7.30 loader dry-run only."],
    }


def build_training_run_audit(run_id: str) -> dict | None:
    record = get_training_run(run_id)
    if record is None:
        return None
    return {
        "training_run_id": run_id,
        "events": [
            {"event_id": f"{run_id}_discover_baseline", "action": "discover_baseline", "metadata_only": True},
            {"event_id": f"{run_id}_prepare_samples", "action": "prepare_synthetic_closed_case_samples", "metadata_only": True},
            {"event_id": f"{run_id}_generate_artifacts", "action": "generate_training_artifacts", "metadata_only": True},
            {"event_id": f"{run_id}_loading_manifest", "action": "generate_loading_manifest", "metadata_only": True},
        ],
        "event_count": 4,
        **_safety_response(),
    }


def build_training_run_safety(run_id: str) -> dict | None:
    if get_training_run(run_id) is None:
        return None
    return {
        "training_run_id": run_id,
        "safety_checklist": [
            "仅 synthetic closed-case samples",
            "不使用未结案件训练",
            "不读取真实案件原文",
            "不读取密钥",
            "不调用 provider",
            "不写正式 Skill registry",
            "不自动发布 Skill",
            "不生成最终法律意见",
            "不生成正式报告",
        ],
        "all_safety_checks_passed": True,
        **_safety_response(),
    }


def _filter_samples(request: CodexTrainingRunRequest):
    requested_paths = {tuple(path) for path in request.target_case_cause_paths}
    samples = [sample for sample in list_training_samples() if tuple(sample.case_cause_path) in requested_paths]
    return samples or list_training_samples()


def _build_packages(training_run_id: str, samples, target_skill_ids: list[str]) -> list[GeneratedExperiencePackageManifest]:
    base_packages = [
        GeneratedExperiencePackageManifest(
            package_id=f"{training_run_id}_pkg_civil_general",
            package_name="v7.31 民事通用训练经验包",
            case_cause_scope="civil",
            case_cause_path=["civil"],
            case_cause_level=1,
            parent_package_ids=[],
            fallback_package_ids=[],
            priority=10,
            load_strategy="common_package_fallback",
            target_skill_ids=target_skill_ids,
            extracted_patterns=["主体关系", "时间线", "证据链", "请求权基础"],
            reasoning_templates=["事实-证据-争点", "请求-抗辩-风险"],
            evidence_rules=["证据必须关联 source trace metadata", "缺失证据进入 review checklist"],
            source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        )
    ]
    for index, sample in enumerate(samples, start=1):
        base_packages.append(
            GeneratedExperiencePackageManifest(
                package_id=f"{training_run_id}_pkg_{sample.case_cause_code.replace('.', '_')}",
                package_name=f"v7.31 {sample.case_cause_name}训练经验包",
                case_cause_scope=sample.case_cause_scope,
                case_cause_path=sample.case_cause_path,
                case_cause_level=len(sample.case_cause_path),
                parent_package_ids=[f"{training_run_id}_pkg_civil_general"],
                fallback_package_ids=[f"{training_run_id}_pkg_civil_general"],
                priority=40 + index,
                load_strategy="exact_match",
                target_skill_ids=target_skill_ids,
                extracted_patterns=[*sample.applicable_fact_patterns, *sample.applicable_claim_basis],
                reasoning_templates=sample.applicable_legal_relationships,
                evidence_rules=sample.applicable_evidence_types,
                source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
            )
        )
    base_packages.append(
        GeneratedExperiencePackageManifest(
            package_id=f"{training_run_id}_pkg_evidence_overlay",
            package_name="v7.31 证据类型覆盖训练包",
            case_cause_scope="evidence_overlay",
            case_cause_path=["civil"],
            case_cause_level=0,
            parent_package_ids=[f"{training_run_id}_pkg_civil_general"],
            fallback_package_ids=[f"{training_run_id}_pkg_civil_general"],
            priority=95,
            load_strategy="evidence_type_overlay",
            target_skill_ids=target_skill_ids,
            extracted_patterns=["证据类型映射", "证据缺口提示", "来源追踪"],
            reasoning_templates=["证据-事实-争点 overlay"],
            evidence_rules=sorted({item for sample in samples for item in sample.applicable_evidence_types}),
            source_trace_policy={"source_trace_required": True, "raw_content_allowed": False},
        )
    )
    return base_packages


def _build_skills(training_run_id: str, packages) -> list[GeneratedSkillManifest]:
    package_ids = [package.package_id for package in packages]
    return [
        GeneratedSkillManifest(
            skill_id="case_fact_extraction_skill",
            skill_name="案件事实提炼 Skill",
            skill_type="fact_extraction",
            source_package_ids=package_ids,
            derived_from=["v7.30 training artifact loader", "v7.31 synthetic closed-case samples"],
            baseline_complete=False,
            pattern_sections={
                "fact_patterns": ["主体关系", "时间线", "履行节点", "损害节点"],
                "evidence_mapping_rules": ["证据到事实 metadata 映射", "缺失证据提示"],
                "timeline_rules": ["按日期 metadata 排序", "不确定日期进入复核"],
                "party_relation_rules": ["身份字段仅使用脱敏 metadata"],
                "claim_defense_fact_rules": ["请求事实与抗辩事实分组"],
                "disputed_fact_rules": ["争议事实不作为最终认定"],
                "missing_fact_rules": ["金额缺失", "证据缺失", "确认状态缺失"],
                "confidence_rules": ["置信度仅供参考"],
                "source_trace_rules": ["source_trace_required=true"],
                "correction_suggestion_rules": ["更正建议不自动覆盖"],
                "case_cause_specific_fact_patterns": ["货款矩阵", "借款矩阵", "事故责任矩阵", "劳动关系矩阵"],
                "case_cause_specific_evidence_rules": ["合同证据", "转账证据", "事故证明", "劳动合同证据"],
            },
            prompt_templates=["v7_31_fact_metadata_prompt", "v7_31_case_cause_fact_prompt"],
            test_case_ids=[f"{training_run_id}_tc_fact"],
            evaluation_manifest_id=f"{training_run_id}_eval_fact",
            gate_manifest_id=f"{training_run_id}_gate_fact",
            optimization_suggestions=["补齐更多细分案由 synthetic samples", "为冲突证据增加人工复核状态"],
        ),
        GeneratedSkillManifest(
            skill_id="case_legal_analysis_skill",
            skill_name="案件法律分析 Skill",
            skill_type="legal_analysis",
            source_package_ids=package_ids,
            derived_from=["v7.30 training artifact loader", "v7.31 synthetic closed-case samples"],
            baseline_complete=False,
            pattern_sections={
                "legal_issue_patterns": ["法律关系", "争议焦点", "请求权基础"],
                "claim_basis_patterns": ["合同请求权", "侵权赔偿请求权", "劳动报酬请求权"],
                "defense_path_patterns": ["履行抗辩", "质量抗辩", "责任比例抗辩", "合法解除抗辩"],
                "burden_of_proof_rules": ["举证责任仅为草稿提示"],
                "legal_search_question_patterns": ["法规检索问题", "类案检索问题"],
                "citation_boundary_rules": ["候选引用不自动成为最终引用"],
                "enterprise_verification_rules": ["企业信息仅作 verification metadata"],
                "risk_assessment_rules": ["风险提示不构成结果保证"],
                "next_action_rules": ["下一步仅进入 lawyer review checklist"],
                "analysis_structure_templates": ["事实基础", "争议焦点", "请求权基础", "抗辩路径", "风险与下一步"],
                "case_cause_specific_issue_patterns": ["货款争议", "利息争议", "赔偿项目争议", "解除争议"],
                "case_cause_specific_claim_basis": ["付款请求", "返还借款", "损害赔偿", "工资支付"],
                "case_cause_specific_defense_patterns": ["质量抗辩", "已还款抗辩", "责任比例抗辩", "已支付抗辩"],
            },
            prompt_templates=["v7_31_legal_metadata_prompt", "v7_31_case_cause_legal_prompt"],
            test_case_ids=[f"{training_run_id}_tc_legal"],
            evaluation_manifest_id=f"{training_run_id}_eval_legal",
            gate_manifest_id=f"{training_run_id}_gate_legal",
            optimization_suggestions=["补齐抗辩路径评价样本", "增加法律检索问题的 source trace 完整度评分"],
        ),
    ]


def _build_evaluations(training_run_id: str, skills) -> list[GeneratedEvaluationManifest]:
    return [
        GeneratedEvaluationManifest(
            evaluation_id=f"{training_run_id}_eval_{'fact' if skill.skill_id == 'case_fact_extraction_skill' else 'legal'}",
            skill_id=skill.skill_id,
            case_cause_scope="multi_level_case_cause",
            evaluation_scope="reference_only_metadata_quality",
            dimension_scores_schema={"completeness": "0-100", "source_trace": "0-100", "case_cause_fit": "0-100"},
            overall_score_schema={"overall_score": "weighted_reference_score"},
            optimization_suggestions_schema={"suggestions": "string_list"},
        )
        for skill in skills
    ]


def _build_gates(training_run_id: str, skills) -> list[GeneratedGateManifest]:
    return [
        GeneratedGateManifest(
            gate_id=f"{training_run_id}_gate_{'fact' if skill.skill_id == 'case_fact_extraction_skill' else 'legal'}",
            skill_id=skill.skill_id,
            case_cause_scope="multi_level_case_cause",
            gate_status_values=["reference_ready", "needs_review", "insufficient_metadata"],
            optimization_required=False,
        )
        for skill in skills
    ]


def _build_test_cases(training_run_id: str, samples, packages, skills) -> list[GeneratedTestCaseManifest]:
    package_id_by_path = {tuple(package.case_cause_path): package.package_id for package in packages}
    test_cases: list[GeneratedTestCaseManifest] = []
    for sample in samples:
        for skill in skills:
            suffix = "fact" if skill.skill_id == "case_fact_extraction_skill" else "legal"
            test_cases.append(
                GeneratedTestCaseManifest(
                    test_case_id=f"{training_run_id}_tc_{suffix}_{sample.case_cause_code.replace('.', '_')}",
                    skill_id=skill.skill_id,
                    case_cause_path=sample.case_cause_path,
                    test_case_name=f"{sample.case_cause_name} {suffix} metadata test",
                    source_package_id=package_id_by_path.get(tuple(sample.case_cause_path), f"{training_run_id}_pkg_civil_general"),
                    input_metadata_schema={"case_cause_path": "string_list", "evidence_types": "string_list"},
                    expected_output_metadata_schema={"source_trace_required": "boolean", "raw_content_included": "false"},
                )
            )
    return test_cases


def _build_loading_manifest(training_run_id: str, packages, skills, evaluations, gates, test_cases) -> GeneratedLoadingManifest:
    return GeneratedLoadingManifest(
        loading_manifest_id=f"{training_run_id}_loading_manifest",
        skill_ids=[skill.skill_id for skill in skills],
        package_ids=[package.package_id for package in packages],
        evaluation_ids=[evaluation.evaluation_id for evaluation in evaluations],
        gate_ids=[gate.gate_id for gate in gates],
        test_case_ids=[test_case.test_case_id for test_case in test_cases],
        case_cause_match_strategy="exact_then_ancestor_then_common_with_evidence_overlay",
        load_order_by_case_cause=[
            "civil_general_package",
            "level_1_case_cause_package",
            "level_2_case_cause_package",
            "level_3_case_cause_package",
            "fact_type_package",
            "evidence_type_package",
            "case_fact_extraction_skill",
            "case_legal_analysis_skill",
        ],
        fallback_order=["exact_case_cause", "parent_case_cause", "civil_general"],
        conflict_resolution_policy=["specific_package_wins", "evidence_overlay_appends", "safety_flags_are_most_restrictive"],
        checksum_metadata={"artifact_set": "synthetic_metadata_checksum_v7_31"},
        compatible_runtime_modules=["personal_skill_studio.training_artifacts", "personal_case_analysis.skill_loader"],
    )


def _baseline_discovery() -> dict[str, bool | list[str] | str]:
    baseline = build_skill_baseline_report()
    missing = baseline.get("missing_baseline_report", [])
    return {
        "baseline_source": "personal_case_analysis.skill_loader",
        "baseline_complete": not bool(missing),
        "missing_baseline_report": missing,
        "baseline_read_as_metadata_only": True,
    }


def _safety_response() -> dict:
    return {
        **safety_flags(),
        "codex_training": True,
        "training_run_generated": True,
        "redaction_completed": True,
        "quality_reference_only": True,
    }

