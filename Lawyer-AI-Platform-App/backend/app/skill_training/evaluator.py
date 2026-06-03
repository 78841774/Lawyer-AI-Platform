from app.skill_training.case_miner import MinedCase


class SkillEvaluator:
    def evaluate(
        self,
        mined_case: MinedCase,
        fact_patterns: list[dict[str, object]],
        reasoning_patterns: list[dict[str, object]],
        prompts: dict[str, str],
        templates: dict[str, str]
    ) -> float:
        score = 0.0

        if mined_case.facts:
            score += 0.15
        if mined_case.analyses:
            score += 0.15
        if mined_case.reports:
            score += 0.10
        if fact_patterns:
            score += 0.10
        if reasoning_patterns:
            score += 0.10
        if {"fact_prompt", "analysis_prompt", "report_prompt"}.issubset(prompts):
            score += 0.10
        if templates.get("report_template"):
            score += 0.05

        return round(score, 2)
