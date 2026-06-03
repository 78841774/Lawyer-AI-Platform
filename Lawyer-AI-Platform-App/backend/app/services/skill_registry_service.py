import json

from app.models.skill_registry import SkillRegistryDomainSummary, SkillRegistryEntry
from app.repositories.skill_registry_repository import SkillRegistryRepository


class SkillRegistryService:
    def __init__(
        self,
        *,
        skill_registry_repository: SkillRegistryRepository
    ) -> None:
        self.skill_registry_repository = skill_registry_repository

    def list_registry(self) -> list[SkillRegistryEntry]:
        return self.skill_registry_repository.list_entries()

    def get_registry_detail(self, skill_id: str) -> dict[str, object]:
        skill = self.skill_registry_repository.get_skill(skill_id)
        if skill is None:
            raise ValueError("skill not found")

        package = self.skill_registry_repository.get_latest_package(skill_id)
        return {
            "skill": {
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "domain": skill.domain,
                "version": skill.version,
                "status": skill.status,
                "validation_status": skill.validation_status,
                "evaluation_score": skill.evaluation_score
            },
            "evaluation": json.loads(skill.evaluation_details or "{}"),
            "package": {
                "package_id": package.package_id,
                "name": package.name,
                "domain": package.domain,
                "version": package.version,
                "status": package.status,
                "package_path": package.package_path
            } if package is not None else None,
            "lifecycle_status": {
                "skill_status": skill.status,
                "validation_status": skill.validation_status,
                "package_status": package.status if package else None
            }
        }

    def publish(self, skill_id: str) -> dict[str, object]:
        skill = self.skill_registry_repository.get_skill(skill_id)
        if skill is None:
            raise ValueError("skill not found")
        if skill.status == "deprecated":
            raise ValueError("skill deprecated")
        if skill.validation_status != "validated":
            raise ValueError("skill not validated")

        package = self.skill_registry_repository.get_latest_package(skill_id)
        if package is None:
            raise ValueError("package not built")
        if package.status != "built":
            raise ValueError("package not built")

        updated_skill, updated_package = self.skill_registry_repository.publish(
            skill=skill,
            package=package
        )
        return {
            "skill_id": updated_skill.skill_id,
            "package_id": updated_package.package_id,
            "skill_status": updated_skill.status,
            "package_status": updated_package.status,
            "message": "skill and package published"
        }

    def deprecate(self, skill_id: str) -> dict[str, object]:
        skill = self.skill_registry_repository.get_skill(skill_id)
        if skill is None:
            raise ValueError("skill not found")
        package = self.skill_registry_repository.get_latest_package(skill_id)
        updated_skill, updated_package = self.skill_registry_repository.deprecate(
            skill=skill,
            package=package
        )
        return {
            "skill_id": updated_skill.skill_id,
            "package_id": updated_package.package_id if updated_package else None,
            "skill_status": updated_skill.status,
            "package_status": updated_package.status if updated_package else None,
            "message": "skill and package deprecated"
        }

    def list_domains(self) -> list[SkillRegistryDomainSummary]:
        return self.skill_registry_repository.list_domain_summaries()

