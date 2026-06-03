from app.skill_training.case_miner import MinedCase


class PromptGenerator:
    def generate(
        self,
        mined_case: MinedCase,
        fact_patterns: list[dict[str, object]],
        reasoning_patterns: list[dict[str, object]]
    ) -> dict[str, str]:
        skill_context = (
            f"Skill source case: {mined_case.case.case_id}. "
            f"Domain: {mined_case.case.case_type}."
        )
        return {
            "fact_prompt": "\n".join(
                [
                    "Extract reusable fact patterns from case materials.",
                    skill_context,
                    "Identify parties, timeline, claims, evidence references, and missing facts.",
                    "Keep unsupported statements marked as pending verification.",
                    f"Known fact pattern count: {len(fact_patterns)}."
                ]
            ),
            "analysis_prompt": "\n".join(
                [
                    "Perform rule-based legal reasoning from structured fact patterns.",
                    skill_context,
                    "Identify legal issues, apply relevant rules, explain reasoning steps, and state risk level.",
                    "Do not invent law, evidence, or case facts.",
                    f"Known reasoning pattern count: {len(reasoning_patterns)}."
                ]
            ),
            "report_prompt": "\n".join(
                [
                    "Generate a lawyer-reviewable report from facts and legal analysis.",
                    skill_context,
                    "Use sections for summary, facts, issues, analysis, risks, and next actions.",
                    "Write concise professional language suitable for legal review."
                ]
            )
        }

