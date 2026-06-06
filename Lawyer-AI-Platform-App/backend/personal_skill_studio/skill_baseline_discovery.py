from pathlib import Path

from personal_case_analysis.skill_loader import build_skill_baseline_report
from personal_skill_studio.schemas import SkillBaselineDiscoveryMetadata


PROJECT_ROOT = Path(__file__).resolve().parents[3]

SEARCH_ROOTS = [
    "Lawyer-AI-Platform-App/backend/personal_skill_studio",
    "Lawyer-AI-Platform-App/backend/personal_case_analysis",
    "Lawyer-AI-Platform-App/backend/personal_case_workspace",
    "Lawyer-AI-Platform-App/backend/personal_production_pilot",
    "docs",
    "00-Project-Context",
]

SEARCH_TERMS = [
    "case_fact_extraction_skill",
    "case_legal_analysis_skill",
    "case-fact-extractor-v3",
    "case-analysis-pro-v3",
    "skill_001",
    "skill_002",
    "fact_patterns",
    "evidence_mapping_rules",
    "timeline_rules",
    "legal_issue_patterns",
    "claim_basis_patterns",
    "defense_patterns",
    "reasoning_patterns",
    "prompt_templates",
    "evaluation",
    "gate",
    "test_cases",
    "promotion_gate",
    "experience_package",
]


def _iter_project_files() -> list[Path]:
    files: list[Path] = []
    for root in SEARCH_ROOTS:
        directory = PROJECT_ROOT / root
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix in {".py", ".md", ".ts", ".tsx", ".sh"}:
                files.append(path)
    return files


def _relative(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def _scan_files() -> dict[str, list[str]]:
    buckets = {
        "source_skill_files": [],
        "source_package_files": [],
        "source_evaluation_files": [],
        "source_gate_files": [],
        "source_test_case_files": [],
        "source_prompt_template_files": [],
        "source_pattern_files": [],
    }
    for path in _iter_project_files():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        matched_terms = [term for term in SEARCH_TERMS if term in text]
        if not matched_terms:
            continue
        relative = _relative(path)
        if any(term in text for term in ["case_fact_extraction_skill", "case_legal_analysis_skill", "skill_candidate", "Skill"]):
            buckets["source_skill_files"].append(relative)
        if any(term in text for term in ["experience_package", "Experience Package", "经验包"]):
            buckets["source_package_files"].append(relative)
        if "evaluation" in text or "评价" in text:
            buckets["source_evaluation_files"].append(relative)
        if "gate" in text or "门控" in text or "promotion_gate" in text:
            buckets["source_gate_files"].append(relative)
        if "test_case" in text or "test_cases" in text or "测试用例" in text:
            buckets["source_test_case_files"].append(relative)
        if "prompt_template" in text or "prompt_templates" in text or "Prompt" in text:
            buckets["source_prompt_template_files"].append(relative)
        if any(term in text for term in ["fact_patterns", "evidence_mapping_rules", "timeline_rules", "legal_issue_patterns", "claim_basis_patterns", "defense_patterns", "reasoning_patterns"]):
            buckets["source_pattern_files"].append(relative)
    return {key: sorted(set(value)) for key, value in buckets.items()}


def build_baseline_discovery_metadata() -> SkillBaselineDiscoveryMetadata:
    file_buckets = _scan_files()
    report = build_skill_baseline_report()
    missing = list(report.get("missing_baseline_report", []))
    if not file_buckets["source_skill_files"]:
        missing.append("source_skill_files not detected")
    if not file_buckets["source_evaluation_files"]:
        missing.append("source_evaluation_files not detected")
    if not file_buckets["source_gate_files"]:
        missing.append("source_gate_files not detected")
    if not file_buckets["source_test_case_files"]:
        missing.append("source_test_case_files not detected")
    if not file_buckets["source_prompt_template_files"]:
        missing.append("source_prompt_template_files not detected")

    baseline_discovered = bool(file_buckets["source_skill_files"]) or bool(report.get("baselines", []))
    baseline_complete = baseline_discovered and not missing
    return SkillBaselineDiscoveryMetadata(
        **file_buckets,
        missing_baseline_items=sorted(set(missing)),
        missing_baseline_report=sorted(set(missing)),
        derived_from=[
            "v7.15 Skill Training Runtime metadata",
            "v7.16 Controlled Case Analysis Runtime skill_loader metadata",
            "v7.20 Fact Preview & Correction metadata",
            "v7.21 Legal Analysis Draft metadata",
        ],
        baseline_discovered=baseline_discovered,
        baseline_complete=baseline_complete,
        warnings=[
            "Baseline discovery reads project metadata files and ignored runtime metadata only.",
            "If a source item is missing, v7.22 returns missing_baseline_report and placeholder lineage metadata.",
        ],
    )
