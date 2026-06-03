import json
from pathlib import Path

from app.models.skill import Skill
from app.skill_training.package_manifest import PackageManifestBuilder


class PackageBuilder:
    def __init__(
        self,
        *,
        package_root: str = "../experience-packages",
        manifest_builder: PackageManifestBuilder | None = None
    ) -> None:
        self.package_root = Path(package_root)
        self.manifest_builder = manifest_builder or PackageManifestBuilder()

    def build(
        self,
        *,
        package_id: str,
        skill: Skill,
        package_name: str
    ) -> tuple[dict[str, object], Path]:
        prompts = self._load_json_dict(skill.prompts)
        templates = self._load_json_dict(skill.templates)
        fact_patterns = self._load_json(skill.fact_patterns, [])
        reasoning_patterns = self._load_json(skill.reasoning_patterns, [])
        evaluation_details = self._load_json(skill.evaluation_details, {})

        manifest = self.manifest_builder.build(
            package_id=package_id,
            skill=skill,
            package_name=package_name
        )
        target_dir = self.package_root / package_id
        prompts_dir = target_dir / "prompts"
        templates_dir = target_dir / "templates"
        tests_dir = target_dir / "tests"
        prompts_dir.mkdir(parents=True, exist_ok=True)
        templates_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)

        skill_payload = {
            "skill_id": skill.skill_id,
            "case_id": skill.case_id,
            "skill_name": skill.skill_name,
            "domain": skill.domain,
            "version": skill.version,
            "status": skill.status,
            "validation_status": skill.validation_status,
            "evaluation_score": skill.evaluation_score,
            "evaluation_details": evaluation_details,
            "fact_patterns": fact_patterns,
            "reasoning_patterns": reasoning_patterns,
            "prompts": {
                "fact_prompt": "prompts/fact_prompt.txt",
                "analysis_prompt": "prompts/analysis_prompt.txt",
                "report_prompt": "prompts/report_prompt.txt"
            },
            "templates": {
                "report_template": "templates/report_template.md"
            }
        }
        test_case = {
            "package_id": package_id,
            "skill_id": skill.skill_id,
            "case_id": skill.case_id,
            "expected_validation_status": "validated",
            "expected_minimum_score": 0.75
        }

        self._write_json(target_dir / "package.json", manifest)
        self._write_json(target_dir / "skill.json", skill_payload)
        (prompts_dir / "fact_prompt.txt").write_text(
            prompts.get("fact_prompt", ""),
            encoding="utf-8"
        )
        (prompts_dir / "analysis_prompt.txt").write_text(
            prompts.get("analysis_prompt", ""),
            encoding="utf-8"
        )
        (prompts_dir / "report_prompt.txt").write_text(
            prompts.get("report_prompt", ""),
            encoding="utf-8"
        )
        (templates_dir / "report_template.md").write_text(
            templates.get("report_template", ""),
            encoding="utf-8"
        )
        self._write_json(tests_dir / "test_case.json", test_case)

        return manifest, target_dir

    def _load_json(self, value: str | None, fallback: object) -> object:
        if not value:
            return fallback
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return fallback

    def _load_json_dict(self, value: str | None) -> dict[str, str]:
        parsed = self._load_json(value, {})
        if not isinstance(parsed, dict):
            return {}
        return {
            str(key): str(item)
            for key, item in parsed.items()
        }

    def _write_json(self, path: Path, payload: dict[str, object]) -> None:
        path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

