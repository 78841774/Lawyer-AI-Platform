import json
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN

from app.models.skill import Skill
from app.skill_training.evaluation_metrics import EvaluationMetrics
from app.skill_training.evaluation_report_builder import EvaluationReportBuilder


@dataclass(frozen=True)
class EvaluationResult:
    evaluation_score: float
    validation_status: str
    evaluation_details: dict[str, object]


class EvaluationEngine:
    def __init__(
        self,
        *,
        metrics: EvaluationMetrics | None = None,
        report_builder: EvaluationReportBuilder | None = None
    ) -> None:
        self.metrics = metrics or EvaluationMetrics()
        self.report_builder = report_builder or EvaluationReportBuilder()

    def evaluate(self, skill: Skill) -> EvaluationResult:
        fact_patterns = self._load_json_list(skill.fact_patterns)
        reasoning_patterns = self._load_json_list(skill.reasoning_patterns)
        prompts = self._load_json_dict(skill.prompts)
        templates = self._load_json_dict(skill.templates)

        if not fact_patterns and not reasoning_patterns and not prompts and not templates:
            raise ValueError("skill content insufficient")

        metric_results = [
            self.metrics.score_fact_pattern_quality(fact_patterns),
            self.metrics.score_reasoning_quality(reasoning_patterns),
            self.metrics.score_prompt_quality(prompts),
            self.metrics.score_template_quality(templates),
            self.metrics.score_legal_relevance(
                domain=skill.domain,
                reasoning_patterns=reasoning_patterns
            ),
            self.metrics.score_report_reusability(templates, prompts)
        ]
        average_score = float(
            (
                sum(Decimal(str(metric.score)) for metric in metric_results)
                / Decimal(len(metric_results))
            ).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
        )
        validation_status = (
            "validated"
            if average_score >= 0.75
            else "needs_improvement"
        )
        details = self.report_builder.build(
            skill_id=skill.skill_id,
            metrics=metric_results,
            average_score=average_score,
            validation_status=validation_status
        )

        return EvaluationResult(
            evaluation_score=average_score,
            validation_status=validation_status,
            evaluation_details=details
        )

    def _load_json_list(self, value: str | None) -> list[dict[str, object]]:
        if not value:
            return []
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return []
        if isinstance(parsed, list):
            return [
                item for item in parsed
                if isinstance(item, dict)
            ]
        return []

    def _load_json_dict(self, value: str | None) -> dict[str, str]:
        if not value:
            return {}
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        if isinstance(parsed, dict):
            return {
                str(key): str(item)
                for key, item in parsed.items()
            }
        return {}
