from app.models.experience_package import ExperiencePackage
from app.models.skill import Skill
from app.models.skill_registry import SkillRegistryDomainSummary, SkillRegistryEntry
from app.repositories.experience_package_repository import ExperiencePackageRepository
from app.repositories.skill_repository import SkillRepository


class SkillRegistryRepository:
    def __init__(
        self,
        *,
        skill_repository: SkillRepository,
        experience_package_repository: ExperiencePackageRepository
    ) -> None:
        self.skill_repository = skill_repository
        self.experience_package_repository = experience_package_repository

    def list_entries(self) -> list[SkillRegistryEntry]:
        return [
            self._build_entry(skill)
            for skill in self.skill_repository.list_all()
        ]

    def get_entry(self, skill_id: str) -> SkillRegistryEntry | None:
        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            return None
        return self._build_entry(skill)

    def get_skill(self, skill_id: str) -> Skill | None:
        return self.skill_repository.get_by_skill_id(skill_id)

    def get_latest_package(self, skill_id: str) -> ExperiencePackage | None:
        return self.experience_package_repository.get_latest_by_skill_id(skill_id)

    def publish(
        self,
        *,
        skill: Skill,
        package: ExperiencePackage
    ) -> tuple[Skill, ExperiencePackage]:
        updated_skill = self.skill_repository.update_status(
            skill=skill,
            status="published"
        )
        updated_package = self.experience_package_repository.update_status(
            package=package,
            status="published"
        )
        return updated_skill, updated_package

    def deprecate(
        self,
        *,
        skill: Skill,
        package: ExperiencePackage | None
    ) -> tuple[Skill, ExperiencePackage | None]:
        updated_skill = self.skill_repository.update_status(
            skill=skill,
            status="deprecated"
        )
        updated_package = None
        if package is not None:
            updated_package = self.experience_package_repository.update_status(
                package=package,
                status="deprecated"
            )
        return updated_skill, updated_package

    def list_domain_summaries(self) -> list[SkillRegistryDomainSummary]:
        entries = self.list_entries()
        packages = self.experience_package_repository.list_all()
        domains = sorted({
            entry.domain for entry in entries
        } | {
            package.domain for package in packages
        })
        return [
            SkillRegistryDomainSummary(
                domain=domain,
                skills=sum(1 for entry in entries if entry.domain == domain),
                packages=sum(1 for package in packages if package.domain == domain)
            )
            for domain in domains
        ]

    def _build_entry(self, skill: Skill) -> SkillRegistryEntry:
        package = self.experience_package_repository.get_latest_by_skill_id(
            skill.skill_id
        )
        return SkillRegistryEntry(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            domain=skill.domain,
            version=skill.version,
            status=skill.status,
            validation_status=skill.validation_status,
            evaluation_score=skill.evaluation_score,
            package_id=package.package_id if package else None,
            package_status=package.status if package else None
        )

