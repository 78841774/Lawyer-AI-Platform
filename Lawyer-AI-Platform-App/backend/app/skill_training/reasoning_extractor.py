import json

from app.skill_training.case_miner import MinedCase


class ReasoningExtractor:
    def extract(self, mined_case: MinedCase) -> list[dict[str, object]]:
        latest_analysis = mined_case.analyses[-1]
        issues = self._load_json(latest_analysis.issues, [])
        rules = self._load_json(latest_analysis.rules, [])
        reasoning = self._load_json(latest_analysis.reasoning, [])

        return [
            {
                "pattern": "legal_issue_identification",
                "description": "Identify legal issues from extracted facts.",
                "issues": issues
            },
            {
                "pattern": "rule_based_reasoning",
                "description": "Apply declared rules to facts and form a preliminary conclusion.",
                "rules": rules,
                "reasoning_steps": reasoning,
                "conclusion": latest_analysis.conclusion,
                "risk_level": latest_analysis.risk_level,
                "confidence": latest_analysis.confidence
            }
        ]

    def _load_json(self, value: str, fallback: object) -> object:
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return fallback

