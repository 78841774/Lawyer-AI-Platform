from app.skill_training.case_miner import MinedCase


class TemplateGenerator:
    def generate(self, mined_case: MinedCase) -> dict[str, str]:
        return {
            "report_template": "\n".join(
                [
                    "# Skill Candidate Report Template",
                    "",
                    f"Source Case: {mined_case.case.case_id}",
                    f"Domain: {mined_case.case.case_type}",
                    "",
                    "## Executive Summary",
                    "",
                    "## Fact Patterns",
                    "",
                    "## Legal Issues",
                    "",
                    "## Reasoning Patterns",
                    "",
                    "## Risk Assessment",
                    "",
                    "## Recommended Next Actions",
                    ""
                ]
            )
        }

