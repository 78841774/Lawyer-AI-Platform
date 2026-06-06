from personal_case_analysis.schemas import SkillBaselineMetadata, SkillBaselineReport
from personal_skill_studio.evaluation_runtime import list_evaluations
from personal_skill_studio.skill_candidate_runtime import list_skill_candidates
from personal_skill_studio.storage import PROMOTION_QUEUE_DIR, read_payloads
from personal_skill_studio.test_case_runtime import list_test_cases


EXPECTED_SKILLS = [
    {
        "skill_key": "case_fact_extraction_skill",
        "skill_title_cn": "案件事实提炼 Skill",
        "keywords": ["fact", "事实", "提炼", "case_fact_extraction_skill"],
    },
    {
        "skill_key": "case_legal_analysis_skill",
        "skill_title_cn": "案件法律分析 Skill",
        "keywords": ["legal", "法律", "分析", "case_legal_analysis_skill"],
    },
]


def _matches(candidate: object, keywords: list[str]) -> bool:
    title = str(getattr(candidate, "skill_title", "")).lower()
    skill_type = str(getattr(candidate, "skill_type", "")).lower()
    return any(keyword.lower() in title or keyword.lower() in skill_type for keyword in keywords)


def _gate_ids_for_candidate(candidate_id: str | None) -> list[str]:
    if not candidate_id:
        return []
    gate_ids: list[str] = []
    for payload in read_payloads(PROMOTION_QUEUE_DIR):
        if payload.get("skill_candidate_id") == candidate_id:
            gate_ids.append(str(payload.get("skill_candidate_id")))
    return gate_ids


def build_skill_baseline_report() -> dict:
    candidates = list_skill_candidates()
    evaluations = list_evaluations()
    test_cases = list_test_cases()
    baselines: list[SkillBaselineMetadata] = []
    missing: list[str] = []

    for expected in EXPECTED_SKILLS:
        candidate = next((item for item in candidates if _matches(item, expected["keywords"])), None)
        candidate_id = getattr(candidate, "skill_candidate_id", None) if candidate else None
        package_id = getattr(candidate, "experience_package_id", None) if candidate else None
        candidate_evaluations = [evaluation for evaluation in evaluations if getattr(evaluation, "skill_candidate_id", None) == candidate_id]
        candidate_test_cases = [test_case for test_case in test_cases if getattr(test_case, "skill_candidate_id", None) == candidate_id]
        gate_ids = _gate_ids_for_candidate(candidate_id)
        baseline_missing: list[str] = []
        if candidate is None:
            baseline_missing.append(f"{expected['skill_key']} skill candidate metadata not detected")
        if not candidate_evaluations:
            baseline_missing.append(f"{expected['skill_key']} evaluation metadata not detected")
        if not gate_ids:
            baseline_missing.append(f"{expected['skill_key']} promotion gate metadata not detected")
        missing.extend(baseline_missing)
        baselines.append(
            SkillBaselineMetadata(
                skill_key=expected["skill_key"],
                skill_title_cn=expected["skill_title_cn"],
                expected_skill_id=expected["skill_key"],
                source_skill_id=candidate_id or expected["skill_key"],
                source_package_id=package_id,
                source_candidate_id=candidate_id,
                source_evaluation_files=[evaluation.evaluation_id for evaluation in candidate_evaluations],
                source_gate_files=gate_ids,
                source_test_case_ids=[test_case.test_case_id for test_case in candidate_test_cases],
                derived_from=[
                    "v7.15 Skill Training Runtime metadata",
                    "personal_skill_studio.skill_candidate_runtime",
                    "personal_skill_studio.evaluation_runtime",
                    "personal_skill_studio.promotion_gate",
                ],
                baseline_detected=candidate is not None,
                prompt_template_detected=bool(getattr(candidate, "prompt_template_draft", {})) if candidate else False,
                evaluation_detected=bool(candidate_evaluations),
                gate_detected=bool(gate_ids),
                missing_baseline_report=baseline_missing,
                warnings=[
                    "Baseline is read as metadata only.",
                    "If incomplete, v7.16 uses placeholder lineage and does not create or update Skill training data.",
                ],
            )
        )

    return SkillBaselineReport(
        baselines=baselines,
        baseline_count=len(baselines),
        detected_count=sum(1 for baseline in baselines if baseline.baseline_detected),
        missing_baseline_report=missing,
        warnings=[
            "v7.16 references existing v7.15 Skill metadata only.",
            "No Skill is trained, updated, or published by Controlled Case Analysis Runtime.",
        ],
    ).model_dump()


def get_skill_baseline(skill_key: str) -> SkillBaselineMetadata:
    report = SkillBaselineReport(**build_skill_baseline_report())
    for baseline in report.baselines:
        if baseline.skill_key == skill_key:
            return baseline
    return SkillBaselineMetadata(
        skill_key=skill_key,
        skill_title_cn=skill_key,
        expected_skill_id=skill_key,
        source_skill_id=skill_key,
        baseline_detected=False,
        missing_baseline_report=[f"{skill_key} baseline not detected"],
        warnings=["Runtime placeholder baseline only; no Skill training data is generated."],
    )
