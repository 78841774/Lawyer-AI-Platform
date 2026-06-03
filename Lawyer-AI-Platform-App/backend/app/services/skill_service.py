import json

from app.models.skill import Skill
from app.repositories.case_repository import CaseRepository
from app.repositories.fact_repository import FactRepository
from app.repositories.legal_analysis_repository import LegalAnalysisRepository
from app.repositories.report_repository import ReportRepository
from app.repositories.skill_repository import SkillRepository
from app.skill_training.case_miner import CaseMiner
from app.skill_training.evaluator import SkillEvaluator
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
            package_path=candidate.package_path
        )

    def list_skills(self) -> list[Skill]:
        return self.skill_repository.list_all()

    def get_skill(self, skill_id: str) -> Skill | None:
        return self.skill_repository.get_by_skill_id(skill_id)

