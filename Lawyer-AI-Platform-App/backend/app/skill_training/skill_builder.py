from dataclasses import dataclass

from app.repositories.skill_repository import SkillRepository
from app.skill_training.case_miner import MinedCase
from app.skill_training.evaluator import SkillEvaluator
from app.skill_training.fact_pattern_extractor import FactPatternExtractor
from app.skill_training.package_exporter import PackageExporter
from app.skill_training.prompt_generator import PromptGenerator
from app.skill_training.reasoning_extractor import ReasoningExtractor
from app.skill_training.template_generator import TemplateGenerator


@dataclass(frozen=True)
class BuiltSkillCandidate:
    skill_id: str
    skill_name: str
    domain: str
    version: str
    status: str
    fact_patterns: list[dict[str, object]]
    reasoning_patterns: list[dict[str, object]]
    prompts: dict[str, str]
    templates: dict[str, str]
    evaluation_score: float
    package_path: str


class SkillBuilder:
    def __init__(
        self,
        *,
        skill_repository: SkillRepository,
        fact_pattern_extractor: FactPatternExtractor,
        reasoning_extractor: ReasoningExtractor,
        prompt_generator: PromptGenerator,
        template_generator: TemplateGenerator,
        evaluator: SkillEvaluator,
        package_exporter: PackageExporter
    ) -> None:
        self.skill_repository = skill_repository
        self.fact_pattern_extractor = fact_pattern_extractor
        self.reasoning_extractor = reasoning_extractor
        self.prompt_generator = prompt_generator
        self.template_generator = template_generator
        self.evaluator = evaluator
        self.package_exporter = package_exporter

    def build(self, mined_case: MinedCase) -> BuiltSkillCandidate:
        skill_id = self.skill_repository.next_skill_id()
        domain = mined_case.case.case_type or "contract_dispute"
        skill_name = self._build_skill_name(domain)
        version = "0.1.0"
        status = "candidate"

        fact_patterns = self.fact_pattern_extractor.extract(mined_case)
        reasoning_patterns = self.reasoning_extractor.extract(mined_case)
        prompts = self.prompt_generator.generate(
            mined_case,
            fact_patterns,
            reasoning_patterns
        )
        templates = self.template_generator.generate(mined_case)
        evaluation_score = self.evaluator.evaluate(
            mined_case,
            fact_patterns,
            reasoning_patterns,
            prompts,
            templates
        )

        payload = {
            "skill_id": skill_id,
            "case_id": mined_case.case.case_id,
            "skill_name": skill_name,
            "domain": domain,
            "version": version,
            "status": status,
            "fact_patterns": fact_patterns,
            "reasoning_patterns": reasoning_patterns,
            "prompts": prompts,
            "templates": templates,
            "evaluation_score": evaluation_score
        }
        package_path = self.package_exporter.export(
            skill_payload=payload,
            prompts=prompts,
            templates=templates
        )

        return BuiltSkillCandidate(
            skill_id=skill_id,
            skill_name=skill_name,
            domain=domain,
            version=version,
            status=status,
            fact_patterns=fact_patterns,
            reasoning_patterns=reasoning_patterns,
            prompts=prompts,
            templates=templates,
            evaluation_score=evaluation_score,
            package_path=str(package_path)
        )

    def _build_skill_name(self, domain: str) -> str:
        if domain == "contract_dispute":
            return "Contract Dispute Skill Candidate"
        return f"{domain.replace('_', ' ').title()} Skill Candidate"

