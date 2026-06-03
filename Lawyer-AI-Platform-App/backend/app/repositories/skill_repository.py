from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.skill import Skill


class SkillRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def next_skill_id(self) -> str:
        index = self.db.query(Skill).count() + 1
        while self.get_by_skill_id(f"skill_{index:03d}") is not None:
            index += 1
        return f"skill_{index:03d}"

    def create(
        self,
        *,
        skill_id: str,
        case_id: str,
        skill_name: str,
        domain: str,
        version: str,
        status: str,
        fact_patterns: str,
        reasoning_patterns: str,
        prompts: str,
        templates: str,
        evaluation_score: float,
        package_path: str
    ) -> Skill:
        skill = Skill(
            skill_id=skill_id,
            case_id=case_id,
            skill_name=skill_name,
            domain=domain,
            version=version,
            status=status,
            fact_patterns=fact_patterns,
            reasoning_patterns=reasoning_patterns,
            prompts=prompts,
            templates=templates,
            evaluation_score=evaluation_score,
            package_path=package_path
        )
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def get_by_skill_id(self, skill_id: str) -> Skill | None:
        return self.db.execute(
            select(Skill).where(Skill.skill_id == skill_id)
        ).scalar_one_or_none()

    def list_all(self) -> list[Skill]:
        return list(
            self.db.execute(
                select(Skill).order_by(Skill.created_at.asc(), Skill.id.asc())
            ).scalars()
        )

    def count_all(self) -> int:
        return self.db.query(Skill).count()

