from app.repositories.skill_repository import SkillRepository
from app.repositories.workspace_skill_repository import WorkspaceSkillRepository
from app.skill_training.package_loader import SkillPackageLoader


class SkillRuntimeService:
    def __init__(
        self,
        *,
        skill_repository: SkillRepository,
        workspace_skill_repository: WorkspaceSkillRepository,
        package_loader: SkillPackageLoader | None = None
    ) -> None:
        self.skill_repository = skill_repository
        self.workspace_skill_repository = workspace_skill_repository
        self.package_loader = package_loader or SkillPackageLoader()

    def get_runtime_summary(self, skill_id: str) -> dict[str, object]:
        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            raise ValueError("skill not found")

        published = self.workspace_skill_repository.get_published_skill(skill_id)
        if published is None:
            raise ValueError("skill not published")

        _, package = published
        runtime_package = self.package_loader.load(package.package_id)
        summary = self.package_loader.summarize(runtime_package)
        summary["status"] = "loaded"
        return summary

