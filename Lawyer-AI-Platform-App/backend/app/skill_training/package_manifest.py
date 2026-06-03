from datetime import datetime

from app.models.skill import Skill


class PackageManifestBuilder:
    def build(
        self,
        *,
        package_id: str,
        skill: Skill,
        package_name: str
    ) -> dict[str, object]:
        return {
            "package_id": package_id,
            "skill_id": skill.skill_id,
            "name": package_name,
            "domain": skill.domain,
            "version": skill.version,
            "status": "built",
            "created_at": datetime.utcnow().isoformat(),
            "entrypoints": {
                "skill": "skill.json",
                "fact_prompt": "prompts/fact_prompt.txt",
                "analysis_prompt": "prompts/analysis_prompt.txt",
                "report_prompt": "prompts/report_prompt.txt",
                "report_template": "templates/report_template.md",
                "test_case": "tests/test_case.json"
            },
            "validation": {
                "validation_status": skill.validation_status,
                "evaluation_score": skill.evaluation_score
            }
        }

