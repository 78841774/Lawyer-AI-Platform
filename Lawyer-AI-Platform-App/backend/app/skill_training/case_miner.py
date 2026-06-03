from dataclasses import dataclass

from app.models.case import Case
from app.models.fact import Fact
from app.models.legal_analysis import LegalAnalysis
from app.models.report import Report


@dataclass(frozen=True)
class MinedCase:
    case: Case
    facts: list[Fact]
    analyses: list[LegalAnalysis]
    reports: list[Report]


class CaseMiner:
    def mine(
        self,
        *,
        case: Case,
        facts: list[Fact],
        analyses: list[LegalAnalysis],
        reports: list[Report]
    ) -> MinedCase:
        return MinedCase(
            case=case,
            facts=facts,
            analyses=analyses,
            reports=reports
        )

