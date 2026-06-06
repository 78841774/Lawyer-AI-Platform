from personal_skill_studio.training_artifacts.artifact_registry import get_package, get_skill
from personal_skill_studio.training_artifacts.schemas import CaseCauseMatchResult, SkillContextManifest


def build_skill_context(match_result: CaseCauseMatchResult, selected_skill_ids: list[str]) -> SkillContextManifest:
    package_ids = match_result.selected_package_ids
    package_names = [package.package_name for package_id in package_ids if (package := get_package(package_id))]
    skills = [skill for skill_id in selected_skill_ids if (skill := get_skill(skill_id))]
    pattern_sections = sorted({section for skill in skills for section in skill.pattern_sections.keys()})
    test_case_ids = sorted({test_case_id for skill in skills for test_case_id in skill.test_case_ids})
    evaluation_ids = sorted({skill.evaluation_id for skill in skills})
    gate_ids = sorted({skill.gate_id for skill in skills})
    suggestions = sorted({item for skill in skills for item in skill.optimization_suggestions})
    return SkillContextManifest(
        skill_context_id=f"skill_context_{match_result.match_id.replace('case_cause_match_', '')}",
        source_match_id=match_result.match_id,
        selected_skill_ids=[skill.skill_id for skill in skills],
        selected_package_ids=package_ids,
        case_cause_path=match_result.requested_case_cause_path,
        fallback_chain=match_result.fallback_chain,
        merge_metadata={
            "merge_strategy": "common_then_ancestor_then_exact_then_evidence_overlay_then_skill_manifest",
            "package_names": package_names,
            "pattern_sections": pattern_sections,
            "test_case_ids": test_case_ids,
            "evaluation_ids": evaluation_ids,
            "gate_ids": gate_ids,
            "specific_package_wins": True,
            "safety_flags_are_most_restrictive": True,
        },
        lineage={
            "source_scheme_id": "codex_training_scheme_v7_30",
            "source_package_ids": package_ids,
            "source_skill_ids": [skill.skill_id for skill in skills],
            "derived_from": ["synthetic_closed_case_training_metadata", "v7.22_final_draft_metadata"],
        },
        quality={
            "quality_score": 82 if match_result.exact_package_ids else 74,
            "quality_status": "reference_only",
            "quality_dimensions": ["case_cause_match", "package_merge", "lineage", "source_trace", "safety"],
        },
        gate={
            "gate_status": "reference_only",
            "gate_reference_only": True,
            "blocks_next_stage": False,
            "load_executed": False,
        },
        optimization_suggestions=suggestions,
    )

