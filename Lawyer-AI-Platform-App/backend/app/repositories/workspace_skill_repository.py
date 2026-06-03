from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case_skill_binding import CaseSkillBinding
from app.models.experience_package import ExperiencePackage
from app.models.skill import Skill


class WorkspaceSkillRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_published_skills(self) -> list[tuple[Skill, ExperiencePackage]]:
        rows: list[tuple[Skill, ExperiencePackage]] = []
        skills = list(
            self.db.execute(
                select(Skill)
                .where(Skill.status == "published")
                .order_by(Skill.created_at.asc(), Skill.id.asc())
            ).scalars()
        )
        for skill in skills:
            package = self.get_published_package_for_skill(skill.skill_id)
            if package is not None:
                rows.append((skill, package))
        return rows

    def get_published_skill(self, skill_id: str) -> tuple[Skill, ExperiencePackage] | None:
        skill = self.db.execute(
            select(Skill).where(
                Skill.skill_id == skill_id,
                Skill.status == "published"
            )
        ).scalar_one_or_none()
        if skill is None:
            return None
        package = self.get_published_package_for_skill(skill_id)
        if package is None:
            return None
        return skill, package

    def get_published_package_for_skill(self, skill_id: str) -> ExperiencePackage | None:
        packages = list(
            self.db.execute(
                select(ExperiencePackage)
                .where(
                    ExperiencePackage.skill_id == skill_id,
                    ExperiencePackage.status == "published"
                )
                .order_by(ExperiencePackage.created_at.asc(), ExperiencePackage.id.asc())
            ).scalars()
        )
        if not packages:
            return None
        return packages[-1]

    def get_package_by_package_id(self, package_id: str) -> ExperiencePackage | None:
        return self.db.execute(
            select(ExperiencePackage).where(
                ExperiencePackage.package_id == package_id
            )
        ).scalar_one_or_none()

    def next_binding_id(self) -> str:
        index = self.db.query(CaseSkillBinding).count() + 1
        while self.get_binding_by_id(f"binding_{index:03d}") is not None:
            index += 1
        return f"binding_{index:03d}"

    def create_binding(
        self,
        *,
        binding_id: str,
        case_id: str,
        skill_id: str,
        package_id: str,
        status: str
    ) -> CaseSkillBinding:
        binding = CaseSkillBinding(
            binding_id=binding_id,
            case_id=case_id,
            skill_id=skill_id,
            package_id=package_id,
            status=status
        )
        self.db.add(binding)
        self.db.commit()
        self.db.refresh(binding)
        return binding

    def get_binding_by_id(self, binding_id: str) -> CaseSkillBinding | None:
        return self.db.execute(
            select(CaseSkillBinding).where(
                CaseSkillBinding.binding_id == binding_id
            )
        ).scalar_one_or_none()

    def list_bindings_by_case_id(self, case_id: str) -> list[CaseSkillBinding]:
        return list(
            self.db.execute(
                select(CaseSkillBinding)
                .where(CaseSkillBinding.case_id == case_id)
                .order_by(CaseSkillBinding.created_at.asc(), CaseSkillBinding.id.asc())
            ).scalars()
        )
