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
        if skill.status != "published":
            raise ValueError("skill not published")

        package = self.workspace_skill_repository.get_published_package_for_skill(skill_id)
        if package is None:
            raise ValueError("package not published")

        runtime_package = self.package_loader.load(package.package_id)
        return self.package_loader.summarize(runtime_package)

    def get_case_runtime_context(self, case_id: str) -> dict[str, object] | None:
        bindings = [
            binding
            for binding in self.workspace_skill_repository.list_bindings_by_case_id(case_id)
            if binding.status == "applied"
        ]
        if not bindings:
            return None

        for binding in reversed(bindings):
            published = self.workspace_skill_repository.get_published_skill(binding.skill_id)
            if published is None:
                continue

            runtime_package = self.package_loader.load(binding.package_id)
            return {
                "skill_id": str(runtime_package.get("skill_id") or binding.skill_id),
                "package_id": str(runtime_package.get("package_id") or binding.package_id),
                "domain": runtime_package.get("domain"),
                "version": runtime_package.get("version")
            }

        return None
