from personal_skill_studio.schemas import SkillFinalOptimizationReport
from personal_skill_studio.skill_final_draft_engine import get_skill_final_draft


def build_skill_optimization(skill_id: str) -> SkillFinalOptimizationReport | None:
    draft = get_skill_final_draft(skill_id)
    if draft is None:
        return None
    suggestions = list(draft.optimization_suggestions)
    if not draft.baseline_complete:
        suggestions.append("补齐 evaluation / gate / test case baseline 后再进行下一轮人工优化。")
    return SkillFinalOptimizationReport(
        skill_id=skill_id,
        optimization_suggestions=suggestions,
        baseline_discovered=draft.baseline_discovered,
        baseline_complete=draft.baseline_complete,
        warnings=[
            "Optimization suggestions are reference-only.",
            "They do not trigger training, Skill update, Skill publishing, or external delivery.",
        ],
    )
