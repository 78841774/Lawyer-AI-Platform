import json

from app.models.fact import Fact
from app.models.legal_analysis import LegalAnalysis
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository


class LegalAnalysisService:
    def __init__(
        self,
        *,
        legal_analysis_repository: LegalAnalysisRepository,
        fact_repository: FactRepository,
        case_repository: CaseRepository
    ) -> None:
        self.legal_analysis_repository = legal_analysis_repository
        self.fact_repository = fact_repository
        self.case_repository = case_repository

    def run_analysis(self, case_id: str) -> LegalAnalysis:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")

        facts = self.fact_repository.list_by_case_id(case_id)
        if not facts:
            raise ValueError("facts required")

        payload = self._build_rule_based_analysis(facts)
        return self.legal_analysis_repository.create(
            analysis_id=self.legal_analysis_repository.next_analysis_id(),
            case_id=case_id,
            issues=json.dumps(payload["issues"], ensure_ascii=False),
            rules=json.dumps(payload["rules"], ensure_ascii=False),
            reasoning=json.dumps(payload["reasoning"], ensure_ascii=False),
            conclusion=payload["conclusion"],
            risk_level=payload["risk_level"],
            confidence=payload["confidence"],
            status="completed"
        )

    def list_analyses(self, case_id: str) -> list[LegalAnalysis]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")
        return self.legal_analysis_repository.list_by_case_id(case_id)

    def _build_rule_based_analysis(self, facts: list[Fact]) -> dict[str, object]:
        extracted_facts = [fact for fact in facts if fact.status == "extracted"]
        skipped_facts = [fact for fact in facts if fact.status != "extracted"]

        issues = [
            {
                "issue": "是否存在可分析的法律事实",
                "confidence": 0.8 if extracted_facts else 0.4
            }
        ]
        rules = [
            {
                "source": "MVP Rule Engine",
                "rule": "基于已抽取事实进行初步法律问题识别"
            }
        ]
        reasoning = [
            f"系统已发现 {len(facts)} 条案件事实",
            f"其中 {len(extracted_facts)} 条事实可用于进一步法律分析"
        ]
        if skipped_facts:
            reasoning.append(f"另有 {len(skipped_facts)} 条事实记录处于跳过或异常状态，需要后续复核")

        return {
            "issues": issues,
            "rules": rules,
            "reasoning": reasoning,
            "conclusion": self._build_conclusion(extracted_facts),
            "risk_level": self._build_risk_level(extracted_facts, skipped_facts),
            "confidence": 0.75 if extracted_facts else 0.45
        }

    def _build_conclusion(self, extracted_facts: list[Fact]) -> str:
        if extracted_facts:
            return "案件具备初步法律分析条件"
        return "案件事实记录不足，暂不具备稳定法律分析条件"

    def _build_risk_level(
        self,
        extracted_facts: list[Fact],
        skipped_facts: list[Fact]
    ) -> str:
        if not extracted_facts:
            return "high"
        if skipped_facts:
            return "medium"
        return "medium"
