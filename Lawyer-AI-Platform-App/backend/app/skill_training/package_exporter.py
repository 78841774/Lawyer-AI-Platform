import json
from pathlib import Path


class PackageExporter:
    def __init__(self, package_root: str = "../skills") -> None:
        self.package_root = Path(package_root)

    def export(
        self,
        *,
        skill_payload: dict[str, object],
        prompts: dict[str, str],
        templates: dict[str, str]
    ) -> Path:
        skill_id = str(skill_payload["skill_id"])
        target_dir = self.package_root / skill_id
        template_dir = target_dir / "templates"
        template_dir.mkdir(parents=True, exist_ok=True)

        (target_dir / "skill.json").write_text(
            json.dumps(skill_payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        (target_dir / "fact_prompt.txt").write_text(
            prompts["fact_prompt"],
            encoding="utf-8"
        )
        (target_dir / "analysis_prompt.txt").write_text(
            prompts["analysis_prompt"],
            encoding="utf-8"
        )
        (target_dir / "report_prompt.txt").write_text(
            prompts["report_prompt"],
            encoding="utf-8"
        )
        (template_dir / "report_template.md").write_text(
            templates["report_template"],
            encoding="utf-8"
        )

        return target_dir

