from personal_skill_studio.schemas import SkillCandidateDraft, SkillEvaluationDraft, SkillTestCaseDraft
from personal_skill_studio.skill_candidate_runtime import list_skill_candidates
from personal_skill_studio.test_case_runtime import list_test_cases
from personal_skill_studio.evaluation_runtime import list_evaluations


def build_skill_sample_registry() -> dict:
    candidates: list[SkillCandidateDraft] = list_skill_candidates()
    test_cases: list[SkillTestCaseDraft] = list_test_cases()
    evaluations: list[SkillEvaluationDraft] = list_evaluations()
    return {
        "skill_candidate_metadata": [candidate.model_dump() for candidate in candidates],
        "test_case_metadata": [test_case.model_dump() for test_case in test_cases],
        "evaluation_metadata": [evaluation.model_dump() for evaluation in evaluations],
        "metadata_only": True,
        "draft_only": True,
        "live_call_executed": False,
        "used_in_ai_prompt": False,
        "final_skill_published": False,
        "source_trace_required": True,
        "lawyer_review_required": True,
        "warnings": ["Skill sample registry contains desensitized metadata only. Raw sample content is not returned."],
    }
