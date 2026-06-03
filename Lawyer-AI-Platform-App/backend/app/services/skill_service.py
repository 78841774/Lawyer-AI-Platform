import json
from pathlib import Path

from app.models.skill import Skill
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.skill_repository import SkillRepository
from app.skill_training.case_miner import CaseMiner
from app.skill_training.evaluator import SkillEvaluator
from app.skill_training.evaluation_engine import EvaluationEngine
from app.skill_training.fact_pattern_extractor import FactPatternExtractor
from app.skill_training.package_exporter import PackageExporter
from app.skill_training.prompt_generator import PromptGenerator
from app.skill_training.reasoning_extractor import ReasoningExtractor
from app.skill_training.skill_builder import SkillBuilder
from app.skill_training.template_generator import TemplateGenerator


class SkillService:
    def __init__(
        self,
        *,
        skill_repository: SkillRepository,
        case_repository: CaseRepository,
        fact_repository: FactRepository,
        legal_analysis_repository: LegalAnalysisRepository,
        report_repository: ReportRepository,
        package_root: str = "../skills"
    ) -> None:
        self.skill_repository = skill_repository
        self.case_repository = case_repository
        self.fact_repository = fact_repository
        self.legal_analysis_repository = legal_analysis_repository
        self.report_repository = report_repository
        self.case_miner = CaseMiner()
        self.evaluation_engine = EvaluationEngine()
        self.skill_builder = SkillBuilder(
            skill_repository=skill_repository,
            fact_pattern_extractor=FactPatternExtractor(),
            reasoning_extractor=ReasoningExtractor(),
            prompt_generator=PromptGenerator(),
            template_generator=TemplateGenerator(),
            evaluator=SkillEvaluator(),
            package_exporter=PackageExporter(package_root=package_root)
        )

    def build_skill(self, case_id: str) -> Skill:
        case = self.case_repository.get_by_case_id(case_id)
        if case is None:
            raise ValueError("case not found")

        facts = self.fact_repository.list_by_case_id(case_id)
        if not facts:
            raise ValueError("facts required")

        analyses = self.legal_analysis_repository.list_by_case_id(case_id)
        if not analyses:
            raise ValueError("analysis required")

        reports = self.report_repository.list_by_case_id(case_id)
        if not reports:
            raise ValueError("reports required")

        mined_case = self.case_miner.mine(
            case=case,
            facts=facts,
            analyses=analyses,
            reports=reports
        )
        candidate = self.skill_builder.build(mined_case)

        return self.skill_repository.create(
            skill_id=candidate.skill_id,
            case_id=case_id,
            skill_name=candidate.skill_name,
            domain=candidate.domain,
            version=candidate.version,
            status=candidate.status,
            fact_patterns=json.dumps(candidate.fact_patterns, ensure_ascii=False),
            reasoning_patterns=json.dumps(candidate.reasoning_patterns, ensure_ascii=False),
            prompts=json.dumps(candidate.prompts, ensure_ascii=False),
            templates=json.dumps(candidate.templates, ensure_ascii=False),
            evaluation_score=candidate.evaluation_score,
            package_path=candidate.package_path,
            evaluation_details="{}",
            validation_status="candidate"
        )

    def list_skills(self) -> list[Skill]:
        return self.skill_repository.list_all()

    def get_skill(self, skill_id: str) -> Skill | None:
        return self.skill_repository.get_by_skill_id(skill_id)

    def evaluate_skill(self, skill_id: str) -> Skill:
        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            raise ValueError("skill not found")

        result = self.evaluation_engine.evaluate(skill)
        updated_skill = self.skill_repository.update_evaluation(
            skill=skill,
            evaluation_score=result.evaluation_score,
            evaluation_details=json.dumps(
                result.evaluation_details,
                ensure_ascii=False
            ),
            validation_status=result.validation_status
        )
        self._update_skill_package(updated_skill)
        return updated_skill

    def get_evaluation_details(self, skill_id: str) -> dict[str, object]:
        skill = self.skill_repository.get_by_skill_id(skill_id)
        if skill is None:
            raise ValueError("skill not found")
        if not skill.evaluation_details or skill.evaluation_details == "{}":
            return {
                "skill_id": skill_id,
                "message": "evaluation_details is empty. Run POST /skills/{skill_id}/evaluate first.",
                "evaluation_details": {}
            }
        return json.loads(skill.evaluation_details)

    def _update_skill_package(self, skill: Skill) -> None:
        if not skill.package_path:
            return

        skill_json_path = Path(skill.package_path) / "skill.json"
        if not skill_json_path.exists():
            return

        try:
            payload = json.loads(skill_json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            payload = {}

        payload.update(
            {
                "evaluation_score": skill.evaluation_score,
                "validation_status": skill.validation_status,
                "evaluation_details": json.loads(skill.evaluation_details or "{}")
            }
        )
        skill_json_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
