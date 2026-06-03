from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.legal_analysis import LegalAnalysis


class LegalAnalysisRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_analysis_id(self) -> str:
        index = self.db.query(LegalAnalysis).count() + 1
        while self.get_by_analysis_id(f"analysis_{index:03d}") is not None:
            index += 1
        return f"analysis_{index:03d}"

    def create(
        self,
        *,
        analysis_id: str,
        case_id: str,
        issues: str,
        rules: str,
        reasoning: str,
        conclusion: str,
        risk_level: str,
        confidence: float,
        status: str
    ) -> LegalAnalysis:
        analysis = LegalAnalysis(
            analysis_id=analysis_id,
            case_id=case_id,
            issues=issues,
            rules=rules,
            reasoning=reasoning,
            conclusion=conclusion,
            risk_level=risk_level,
            confidence=confidence,
            status=status
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)
        return analysis

    def get_by_analysis_id(self, analysis_id: str) -> LegalAnalysis | None:
        return self.db.execute(
            select(LegalAnalysis).where(LegalAnalysis.analysis_id == analysis_id)
        ).scalar_one_or_none()

    def list_by_case_id(self, case_id: str) -> list[LegalAnalysis]:
        return list(
            self.db.execute(
                select(LegalAnalysis)
                .where(LegalAnalysis.case_id == case_id)
                .order_by(LegalAnalysis.created_at.asc(), LegalAnalysis.id.asc())
            ).scalars()
        )
