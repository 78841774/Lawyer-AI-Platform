from dataclasses import dataclass


@dataclass(frozen=True)
class SkillRegistryEntry:
    skill_id: str
    skill_name: str
    domain: str
    version: str
    status: str
    validation_status: str
    evaluation_score: float
    package_id: str | None
    package_status: str | None


@dataclass(frozen=True)
class SkillRegistryDomainSummary:
    domain: str
    skills: int
    packages: int

