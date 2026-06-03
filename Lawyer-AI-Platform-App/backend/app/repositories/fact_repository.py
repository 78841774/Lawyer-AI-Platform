from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.fact import Fact


class FactRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_fact_id(self) -> str:
        index = self.db.query(Fact).count() + 1
        while self.get_by_fact_id(f"fact_{index:03d}") is not None:
            index += 1
        return f"fact_{index:03d}"

    def create(
        self,
        *,
        fact_id: str,
        case_id: str,
        material_id: str,
        content: str,
        fact_type: str,
        confidence: float,
        source_text: str | None,
        status: str
    ) -> Fact:
        fact = Fact(
            fact_id=fact_id,
            case_id=case_id,
            material_id=material_id,
            content=content,
            fact_type=fact_type,
            confidence=confidence,
            source_text=source_text,
            status=status
        )
        self.db.add(fact)
        self.db.commit()
        self.db.refresh(fact)
        return fact

    def get_by_fact_id(self, fact_id: str) -> Fact | None:
        return self.db.execute(
            select(Fact).where(Fact.fact_id == fact_id)
        ).scalar_one_or_none()

    def list_by_case_id(self, case_id: str) -> list[Fact]:
        return list(
            self.db.execute(
                select(Fact)
                .where(Fact.case_id == case_id)
                .order_by(Fact.created_at.asc(), Fact.id.asc())
            ).scalars()
        )
