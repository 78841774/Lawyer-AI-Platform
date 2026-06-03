import json
from pathlib import Path


class SkillPackageLoader:
    def __init__(self, package_root: str = "../experience-packages") -> None:
        self.package_root = Path(package_root)

    def load(self, package_id: str) -> dict[str, object]:
        package_dir = self.package_root / package_id
        if not package_dir.exists():
            raise ValueError("package not found")

        package_json = self._read_json(package_dir / "package.json")
        skill_json = self._read_json(package_dir / "skill.json")
        prompts = {
            "fact_prompt": self._read_text(package_dir / "prompts" / "fact_prompt.txt"),
            "analysis_prompt": self._read_text(package_dir / "prompts" / "analysis_prompt.txt"),
            "report_prompt": self._read_text(package_dir / "prompts" / "report_prompt.txt")
        }
        templates = {
            "report_template": self._read_text(package_dir / "templates" / "report_template.md")
        }

        return {
            "skill_id": str(skill_json.get("skill_id") or package_json.get("skill_id")),
            "package_id": str(package_json.get("package_id") or package_id),
            "domain": str(package_json.get("domain") or skill_json.get("domain")),
            "version": str(package_json.get("version") or skill_json.get("version")),
            "prompts": prompts,
            "templates": templates
        }

    def summarize(self, package: dict[str, object]) -> dict[str, object]:
        prompts = package.get("prompts", {})
        templates = package.get("templates", {})
        return {
            "skill_id": package.get("skill_id"),
            "package_id": package.get("package_id"),
            "domain": package.get("domain"),
            "version": package.get("version"),
            "prompts": self._summarize_text_map(prompts),
            "templates": self._summarize_text_map(templates)
        }

    def _read_json(self, path: Path) -> dict[str, object]:
        if not path.exists():
            raise ValueError(f"package file missing: {path.name}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            raise ValueError(f"package file invalid: {path.name}") from error
        if not isinstance(payload, dict):
            raise ValueError(f"package file invalid: {path.name}")
        return payload

    def _read_text(self, path: Path) -> str:
        if not path.exists():
            raise ValueError(f"package file missing: {path.name}")
        return path.read_text(encoding="utf-8")

    def _summarize_text_map(self, value: object) -> dict[str, dict[str, object]]:
        if not isinstance(value, dict):
            return {}
        return {
            str(key): {
                "loaded": bool(str(item).strip()),
                "length": len(str(item))
            }
            for key, item in value.items()
        }

