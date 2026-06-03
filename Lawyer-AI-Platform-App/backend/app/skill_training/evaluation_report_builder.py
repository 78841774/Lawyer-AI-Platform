from datetime import datetime

from app.skill_training.evaluation_metrics import MetricResult


class EvaluationReportBuilder:
    def build(
        self,
        *,
        skill_id: str,
        metrics: list[MetricResult],
        average_score: float,
        validation_status: str
    ) -> dict[str, object]:
        return {
            "skill_id": skill_id,
            "evaluated_at": datetime.utcnow().isoformat(),
            "average_score": average_score,
            "validation_status": validation_status,
            "metrics": {
                metric.name: metric.score
                for metric in metrics
            },
            "metric_reasons": {
                metric.name: metric.reason
                for metric in metrics
            },
            "threshold": 0.75
        }

