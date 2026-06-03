import json

from app.models.experience_package import ExperiencePackage
from app.repositories.experience_package_repository import ExperiencePackageRepository
from app.repositories.skill_repository import SkillRepository
from app.skill_training.package_builder import PackageBuilder
from app.skill_training.package_validator import PackageValidator


class ExperiencePackageService:
    def __init__(
        self,
        *,
        experience_package_repository: ExperiencePackageRepository,
        skill_repository: SkillRepository,
        package_root: str = "../experience-packages"
    ) -> None:
        self.experience_package_repository = experience_package_repository
        self.skill_repository = skill_repository
        self.package_validator = PackageValidator()
        self.package_builder = PackageBuilder(package_root=package_root)

    def build_package(self, skill_id: str) -> ExperiencePackage:
        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            raise ValueError("skill not found")

        self.package_validator.validate_skill(skill)

        package_id = self.experience_package_repository.next_package_id()
        package_name = self._build_package_name(skill.domain)
        manifest, package_path = self.package_builder.build(
            package_id=package_id,
            skill=skill,
            package_name=package_name
        )

        return self.experience_package_repository.create(
            package_id=package_id,
            skill_id=skill.skill_id,
            name=package_name,
            domain=skill.domain,
            version=skill.version,
            status="built",
            manifest_json=json.dumps(manifest, ensure_ascii=False),
            package_path=str(package_path)
        )

    def list_packages(self) -> list[ExperiencePackage]:
        return self.experience_package_repository.list_all()

    def get_package(self, package_id: str) -> ExperiencePackage | None:
        return self.experience_package_repository.get_by_package_id(package_id)

    def get_manifest(self, package_id: str) -> dict[str, object] | None:
        package = self.experience_package_repository.get_by_package_id(package_id)
        if package is None:
            return None
        return json.loads(package.manifest_json)

    def _build_package_name(self, domain: str) -> str:
        if domain == "contract_dispute":
            return "Contract Dispute Experience Package"
        return f"{domain.replace('_', ' ').title()} Experience Package"

