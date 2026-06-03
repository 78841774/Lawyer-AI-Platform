import json

from app.models.case_skill_binding import CaseSkillBinding
from app.models.experience_package import ExperiencePackage
from app.models.skill import Skill
from app.repositories.case_repository import CaseRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository


class WorkspaceSkillService:
    def __init__(
        self,
        *,
        workspace_skill_repository: WorkspaceSkillRepository,
        case_repository: CaseRepository,
        skill_repository: SkillRepository
    ) -> None:
        self.workspace_skill_repository = workspace_skill_repository
        self.case_repository = case_repository
        self.skill_repository = skill_repository

    def list_workspace_skills(self) -> list[tuple[Skill, ExperiencePackage]]:
        return self.workspace_skill_repository.list_published_skills()

    def get_workspace_skill(self, skill_id: str) -> tuple[Skill, ExperiencePackage]:
        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            raise ValueError("skill not found")
        published = self.workspace_skill_repository.get_published_skill(skill_id)
        if published is None:
            raise ValueError("skill not published")
        return published

    def apply_skill_to_case(
        self,
        *,
        case_id: str,
        skill_id: str
    ) -> CaseSkillBinding:
        case = self.case_repository.get_by_case_id(case_id)
        if case is None:
            raise ValueError("case not found")

        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            raise ValueError("skill not found")
        published = self.workspace_skill_repository.get_published_skill(skill_id)
        if published is None:
            raise ValueError("skill not published")

        _, package = published
        return self.workspace_skill_repository.create_binding(
            binding_id=self.workspace_skill_repository.next_binding_id(),
            case_id=case_id,
            skill_id=skill_id,
            package_id=package.package_id,
            status="applied"
        )

    def list_case_skills(self, case_id: str) -> list[dict[str, object]]:
        if self.case_repository.get_by_case_id(case_id) is None:
            raise ValueError("case not found")

        bindings = self.workspace_skill_repository.list_bindings_by_case_id(case_id)
        return [
            self._serialize_binding(binding)
            for binding in bindings
        ]

    def build_skill_detail(
        self,
        *,
        skill: Skill,
        package: ExperiencePackage
    ) -> dict[str, object]:
        prompts = json.loads(skill.prompts or "{}")
        templates = json.loads(skill.templates or "{}")
        return {
            "skill": self._serialize_workspace_skill(skill, package),
            "package": {
                "package_id": package.package_id,
                "name": package.name,
                "domain": package.domain,
                "version": package.version,
                "status": package.status,
                "package_path": package.package_path
            },
            "prompts_summary": {
                key: self._summarize_text(value)
                for key, value in prompts.items()
            },
            "templates_summary": {
                key: self._summarize_text(value)
                for key, value in templates.items()
            }
        }

    def _serialize_workspace_skill(
        self,
        skill: Skill,
        package: ExperiencePackage
    ) -> dict[str, object]:
        return {
            "skill_id": skill.skill_id,
            "skill_name": skill.skill_name,
            "domain": skill.domain,
            "version": skill.version,
            "package_id": package.package_id,
            "package_path": package.package_path,
            "status": skill.status
        }

    def _serialize_binding(self, binding: CaseSkillBinding) -> dict[str, object]:
        return {
            "binding_id": binding.binding_id,
            "case_id": binding.case_id,
            "skill_id": binding.skill_id,
            "package_id": binding.package_id,
            "status": binding.status,
            "created_at": binding.created_at
        }

    def _summarize_text(self, value: object) -> dict[str, object]:
        text = str(value)
        return {
            "length": len(text),
            "preview": text[:160]
        }

