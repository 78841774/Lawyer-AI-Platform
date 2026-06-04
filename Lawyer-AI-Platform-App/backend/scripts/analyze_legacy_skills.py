#!/usr/bin/env python3
"""Analyze legacy Codex skills and SkillOpt assets for v3.6-B.

This script is intentionally read-only. It does not execute legacy scripts,
call LLMs, create Skills, build Experience Packages, or publish anything.
It writes only summarized reports and avoids copying sensitive source text.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPORTS_DIR = BACKEND_ROOT / "reports"
MARKDOWN_REPORT = REPORTS_DIR / "legacy_skill_analysis.md"
JSON_REPORT = REPORTS_DIR / "legacy_skill_analysis.json"

EXTERNAL_SKILLOPT_ROOT = Path(
    "/Users/wazhen/Documents/Codex/2026-05-28/law-search-users-wazhen-codex-skills"
)

SEARCH_ROOTS = [
    Path.home() / "SkillOpt",
    Path.home() / "legal-skillopt",
    Path.home() / "Downloads" / "SkillOpt",
    Path.home() / "Downloads" / "legal-skillopt",
    Path.home() / "Documents" / "SkillOpt",
    Path.home() / "Documents" / "legal-skillopt",
    REPO_ROOT / "SkillOpt",
    REPO_ROOT / "legal-skillopt",
    REPO_ROOT / "skills",
    BACKEND_ROOT / "skills",
    BACKEND_ROOT / "legacy_codex_skills",
    REPO_ROOT / "training_samples",
    REPO_ROOT / "08-Skill-Training",
    Path.home() / ".codex" / "skills" / "case-fact-extractor-v3",
    Path.home() / ".codex" / "skills" / "case-analysis-pro-v3",
    EXTERNAL_SKILLOPT_ROOT / "SkillOpt",
    EXTERNAL_SKILLOPT_ROOT / "legal-skillopt"
]

TARGET_FILE_NAMES = {
    "SKILL.md",
    "best_skill.md",
    "skill.md",
    "manifest.json",
    "skill.json",
    "evaluation.json",
    "train.jsonl",
    "eval.jsonl",
    "test.jsonl",
    "examples.json",
    "tasks.json",
    "prompts.md",
    "templates.md"
}

SKIP_DIR_NAMES = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "build",
    "dist",
    "skillopt.egg-info",
    "storage",
    "runtime"
}

MODULE_KEYWORDS = {
    "fact_extraction": ["事实提炼", "fact_extraction", "Extracted fact", "事实"],
    "evidence_matrix": ["证据事实矩阵", "evidence_matrix", "证据矩阵"],
    "amount_audit": ["金额核算", "amount_audit", "三轮核验", "金额"],
    "contradiction_detection": ["矛盾", "contradiction"],
    "legal_element_mapping": ["法律要件", "要件映射", "构成要件"],
    "case_analysis": ["案件分析", "case_analysis", "A1", "A13"],
    "claim_basis_analysis": ["请求权", "claim_basis"],
    "defense_analysis": ["抗辩", "defense"],
    "litigation_strategy": ["诉讼策略", "举证策略", "庭审", "代理词"],
    "report_generation": ["报告", "report_template", "report_generation"],
    "judgment_review": ["判后", "judgment", "裁判文书", "判决书"],
    "execution_assessment": ["执行评估", "execution"],
    "scoring": ["评分", "score", "rubric", "metrics"],
    "admission_gate": ["准入", "门控", "gate"]
}

INPUT_KEYWORDS = {
    "case_profile": ["案件概览", "case_meta", "case_profile"],
    "materials": ["材料", "materials"],
    "folder_structure": ["文件夹", "relative_path", "folder_structure"],
    "material_text": ["正文", "material_text", "text"],
    "facts": ["facts", "事实"],
    "evidence_list": ["证据清单", "evidence_list"],
    "analysis": ["analysis", "法律分析"],
    "report": ["report", "报告"],
    "judgment": ["judgment", "判决", "裁判"],
    "statutes": ["法条", "statutes", "法律法规"],
    "similar_cases": ["类案", "similar_cases"],
    "user_goal": ["诉求", "目标", "user_goal"]
}

OUTPUT_KEYWORDS = {
    "fact_summary": ["事实摘要", "事实提炼报告", "fact_summary"],
    "evidence_matrix": ["证据事实矩阵"],
    "amount_table": ["金额", "amount_table"],
    "issue_list": ["争议焦点", "issue_list"],
    "legal_analysis": ["法律分析", "A10"],
    "risk_assessment": ["风险", "risk"],
    "litigation_strategy": ["诉讼策略", "庭审提纲"],
    "report_draft": ["报告", "report_draft"],
    "scoring_result": ["评分", "score"],
    "handoff_payload": ["交接清单", "handoff"]
}

RISK_KEYWORDS = {
    "depends_on_ocr": ["OCR", "PaddleOCR", "vision_ocr", "扫描"],
    "depends_on_external_legal_search": ["law-search", "类案检索", "search-law", "search-case"],
    "depends_on_manual_judgment": ["人工", "律师复核", "人工确认"],
    "sensitive_data_risk": ["身份证", "手机号", "银行卡", "raw-private", "隐私", "脱敏"],
    "not_safe_for_automatic_execution": ["不得自动", "禁止", "不得直接"],
    "requires_lawyer_review": ["律师复核", "法言法语", "可提交"]
}


@dataclass
class LegacySkillAnalysis:
    legacy_skill_id: str
    display_name: str
    source_path: str
    skill_type: str
    domain: str
    version: str
    entry_file: str
    references_count: int
    scripts_count: int
    config_count: int
    dataset_count: int
    evaluation_count: int
    ability_modules: list[str]
    input_requirements: list[str]
    output_structures: list[str]
    scoring_dimensions: list[str]
    pass_threshold: str
    admission_gate: list[str]
    quality_gate: list[str]
    review_rules: list[str]
    rejection_rules: list[str]
    migration_candidates: list[str]
    risk_flags: list[str]
    recommended_actions: list[str]
    recommended_level: str
    source_files_summary: list[str]


def main() -> int:
    analyses = discover_and_analyze()
    dataset_summary = analyze_skillopt_datasets()
    output_summary = analyze_skillopt_outputs()
    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "search_roots": [str(path) for path in SEARCH_ROOTS],
        "legacy_skills": [asdict(analysis) for analysis in analyses],
        "skillopt_datasets": dataset_summary,
        "skillopt_outputs": output_summary,
        "summary": {
            "legacy_skills_count": len(analyses),
            "dataset_files_count": dataset_summary["dataset_files_count"],
            "dataset_items_count": dataset_summary["dataset_items_count"],
            "skillopt_output_runs_count": output_summary["output_runs_count"],
            "best_skill_files_count": output_summary["best_skill_files_count"]
        }
    }
    write_reports(report)
    print_summary(report)
    return 0


def discover_and_analyze() -> list[LegacySkillAnalysis]:
    candidates = discover_candidate_entries()
    return [analyze_candidate(path) for path in candidates]


def discover_candidate_entries() -> list[Path]:
    candidates: set[Path] = set()
    for root in existing_roots():
        for file_path in walk_files(root):
            if is_skillopt_prediction_snapshot(file_path):
                continue
            name = file_path.name
            if name == "SKILL.md":
                candidates.add(file_path)
            elif name == "best_skill.md":
                candidates.add(file_path)
            elif file_path.parent.name == "skills" and name.endswith(".initial.md"):
                candidates.add(file_path)
    return sorted(candidates, key=lambda path: str(path))


def is_skillopt_prediction_snapshot(file_path: Path) -> bool:
    """Skip transient SkillOpt prediction copies; they are output evidence, not source skills."""
    normalized = str(file_path)
    return (
        "/selection_eval_baseline/predictions/" in normalized
        or "/steps/" in normalized and "/.agents/skills/skillopt-target/" in normalized
    )


def analyze_candidate(entry_file: Path) -> LegacySkillAnalysis:
    source_dir = entry_file.parent
    if entry_file.name == "SKILL.md":
        source_dir = entry_file.parent
    elif entry_file.name == "best_skill.md":
        source_dir = entry_file.parent
    text_bundle = read_candidate_bundle(entry_file, source_dir)
    text = "\n".join(text_bundle.values())
    references = list((source_dir / "references").glob("*.md")) if (source_dir / "references").exists() else []
    scripts = list((source_dir / "scripts").glob("*")) if (source_dir / "scripts").exists() else []
    configs = list(source_dir.glob("config*.json")) + list(source_dir.glob("config*.yaml")) + list(source_dir.glob("config*.yml"))
    datasets = [
        path for path in walk_files(source_dir)
        if path.name in {"train.jsonl", "eval.jsonl", "test.jsonl", "items.json", "examples.json", "tasks.json"}
    ]
    evaluations = [
        path for path in walk_files(source_dir)
        if path.name == "evaluation.json" or path.name.startswith("score") or path.name.startswith("metrics") or path.name == "summary.json"
    ]

    ability_modules = detect_keywords(text, MODULE_KEYWORDS)
    input_requirements = detect_keywords(text, INPUT_KEYWORDS)
    output_structures = detect_keywords(text, OUTPUT_KEYWORDS)
    risk_flags = detect_keywords(text, RISK_KEYWORDS)
    scoring_dimensions = detect_scoring_dimensions(text)
    migration_candidates = classify_migration_candidates(entry_file, text, datasets, scripts)
    recommended_level = recommend_level(migration_candidates, risk_flags, entry_file)

    return LegacySkillAnalysis(
        legacy_skill_id=legacy_id(entry_file),
        display_name=display_name(entry_file, text),
        source_path=safe_path(source_dir),
        skill_type=skill_type(entry_file),
        domain=detect_domain(entry_file, text),
        version=detect_version(text),
        entry_file=safe_path(entry_file),
        references_count=len(references),
        scripts_count=len([path for path in scripts if path.is_file()]),
        config_count=len(configs),
        dataset_count=len(datasets),
        evaluation_count=len(evaluations),
        ability_modules=ability_modules,
        input_requirements=input_requirements,
        output_structures=output_structures,
        scoring_dimensions=scoring_dimensions,
        pass_threshold=detect_pass_threshold(text),
        admission_gate=find_lines(text, ["准入", "门控", "gate"], limit=5),
        quality_gate=find_lines(text, ["质量", "评分", "quality"], limit=5),
        review_rules=find_lines(text, ["复核", "人工", "律师"], limit=5),
        rejection_rules=find_lines(text, ["不得", "禁止", "exclude", "must_not_include"], limit=5),
        migration_candidates=migration_candidates,
        risk_flags=risk_flags,
        recommended_actions=recommend_actions(migration_candidates, risk_flags),
        recommended_level=recommended_level,
        source_files_summary=summarize_source_files(source_dir, entry_file)
    )


def read_candidate_bundle(entry_file: Path, source_dir: Path) -> dict[str, str]:
    files = [entry_file]
    reference_dir = source_dir / "references"
    if reference_dir.exists():
        files.extend(sorted(reference_dir.glob("*.md")))
    for file_name in ["config.json", "summary.json", "runtime_state.json"]:
        file_path = source_dir / file_name
        if file_path.exists():
            files.append(file_path)

    bundle: dict[str, str] = {}
    for file_path in files:
        bundle[safe_path(file_path)] = read_text_limited(file_path)
    return bundle


def analyze_skillopt_datasets() -> dict[str, Any]:
    dataset_files = [
        path for root in existing_roots()
        for path in walk_files(root)
        if path.name in {"train.jsonl", "eval.jsonl", "test.jsonl", "items.json"}
        and ("legal_casework_split" in str(path) or "case-samples" in str(path))
    ]
    split_counts: dict[str, int] = {}
    sample_targets: Counter[str] = Counter()
    task_types: Counter[str] = Counter()
    privacy_levels: Counter[str] = Counter()
    dataset_items_count = 0
    for path in dataset_files:
        items = load_json_items(path)
        count = len(items)
        dataset_items_count += count
        split_counts[safe_path(path)] = count
        for item in items:
            sample_targets[str(item.get("skill_target") or "unknown")] += 1
            task_types[str(item.get("task_type") or "unknown")] += 1
            case_meta = item.get("case_meta") if isinstance(item.get("case_meta"), dict) else {}
            privacy_levels[str(case_meta.get("privacy_level") or "unknown")] += 1
    return {
        "dataset_files_count": len(dataset_files),
        "dataset_items_count": dataset_items_count,
        "split_counts": split_counts,
        "sample_targets": dict(sample_targets),
        "task_types": dict(task_types),
        "privacy_levels": dict(privacy_levels)
    }


def analyze_skillopt_outputs() -> dict[str, Any]:
    output_dirs = [
        path for root in existing_roots()
        for path in root.glob("outputs*")
        if path.is_dir()
    ]
    runs: list[dict[str, Any]] = []
    best_skill_files = []
    for output_dir in sorted(output_dirs):
        summary_path = output_dir / "summary.json"
        config_path = output_dir / "config.json"
        best_skill_path = output_dir / "best_skill.md"
        summary = load_json_object(summary_path)
        config = load_json_object(config_path)
        if best_skill_path.exists():
            best_skill_files.append(best_skill_path)
        runs.append(
            {
                "output_dir": safe_path(output_dir),
                "has_summary": summary_path.exists(),
                "has_config": config_path.exists(),
                "has_best_skill": best_skill_path.exists(),
                "best_step": summary.get("best_step"),
                "baseline_selection_hard": summary.get("baseline_selection_hard"),
                "best_selection_hard": summary.get("best_selection_hard"),
                "test_delta_hard": summary.get("test_delta_hard"),
                "total_steps": summary.get("total_steps"),
                "skill_init": config.get("skill_init") or config.get("skill_init_path")
            }
        )
    return {
        "output_runs_count": len(output_dirs),
        "best_skill_files_count": len(best_skill_files),
        "runs": runs
    }


def write_reports(report: dict[str, Any]) -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    MARKDOWN_REPORT.write_text(build_markdown(report), encoding="utf-8")


def build_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Legacy Skill Analysis",
        "",
        f"Generated at: {report['generated_at']}",
        "",
        "## Summary",
        "",
        f"* Legacy skills analyzed: {report['summary']['legacy_skills_count']}",
        f"* SkillOpt dataset files: {report['summary']['dataset_files_count']}",
        f"* SkillOpt dataset items: {report['summary']['dataset_items_count']}",
        f"* SkillOpt output runs: {report['summary']['skillopt_output_runs_count']}",
        f"* best_skill files: {report['summary']['best_skill_files_count']}",
        "",
        "## Legacy Skills",
        "",
        "| legacy_skill_id | display_name | skill_type | domain | ability_modules | recommended_level | migration_candidates | risk_flags |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |"
    ]
    for skill in report["legacy_skills"]:
        lines.append(
            "| "
            + " | ".join(
                [
                    md(skill["legacy_skill_id"]),
                    md(skill["display_name"]),
                    md(skill["skill_type"]),
                    md(skill["domain"]),
                    md(", ".join(skill["ability_modules"]) or "暂无"),
                    md(skill["recommended_level"]),
                    md(", ".join(skill["migration_candidates"]) or "暂无"),
                    md(", ".join(skill["risk_flags"]) or "暂无")
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Dataset Summary",
            "",
            f"* Sample targets: `{json.dumps(report['skillopt_datasets']['sample_targets'], ensure_ascii=False)}`",
            f"* Task types: `{json.dumps(report['skillopt_datasets']['task_types'], ensure_ascii=False)}`",
            f"* Privacy levels: `{json.dumps(report['skillopt_datasets']['privacy_levels'], ensure_ascii=False)}`",
            "",
            "## Migration Notes",
            "",
            "* v3.6-B is analysis only.",
            "* Do not import legacy assets into Skill Registry directly.",
            "* Do not train from raw-private or unreviewed inbox data.",
            "* Reshape reusable assets into Runtime Rules, Prompt Templates, Evaluation Rubrics, Report Templates, and Dataset Packages before v3.6-D training."
        ]
    )
    return "\n".join(lines) + "\n"


def print_summary(report: dict[str, Any]) -> None:
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print("\nLegacy skills:")
    for skill in report["legacy_skills"]:
        print(
            f"- {skill['legacy_skill_id']}: {skill['display_name']} | "
            f"{skill['recommended_level']} | modules={', '.join(skill['ability_modules']) or '暂无'}"
        )
    print(f"\nMarkdown report: {MARKDOWN_REPORT}")
    print(f"JSON report: {JSON_REPORT}")


def existing_roots() -> list[Path]:
    seen: set[str] = set()
    roots = []
    for root in SEARCH_ROOTS:
        if not root.exists():
            continue
        resolved = str(root.resolve())
        if resolved in seen:
            continue
        seen.add(resolved)
        roots.append(root)
    return roots


def walk_files(root: Path):
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP_DIR_NAMES and not name.startswith(".git")]
        for name in files:
            yield Path(current_root) / name


def read_text_limited(path: Path, limit: int = 120_000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    return text[:limit]


def load_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(read_text_limited(path))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def load_json_items(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(read_text_limited(path, limit=2_000_000))
    except json.JSONDecodeError:
        return []
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return [item for item in data["items"] if isinstance(item, dict)]
    return []


def detect_keywords(text: str, mapping: dict[str, list[str]]) -> list[str]:
    return [
        key for key, keywords in mapping.items()
        if any(keyword.lower() in text.lower() for keyword in keywords)
    ]


def detect_scoring_dimensions(text: str) -> list[str]:
    dimensions = detect_keywords(text, {"scoring": MODULE_KEYWORDS["scoring"]})
    for keyword in ["accuracy", "consistency", "completeness", "legal_relevance", "report_quality", "评分", "门控"]:
        if keyword.lower() in text.lower():
            dimensions.append(keyword)
    return sorted(set(dimensions))


def detect_pass_threshold(text: str) -> str:
    match = re.search(r"(?:评分|score)[^\n]{0,30}(?:>=|≥)\s*(\d+)", text, flags=re.IGNORECASE)
    if match:
        return f">={match.group(1)}"
    return "暂无"


def find_lines(text: str, keywords: list[str], limit: int) -> list[str]:
    lines = []
    for line in text.splitlines():
        cleaned = " ".join(line.strip().split())
        if not cleaned:
            continue
        if any(keyword.lower() in cleaned.lower() for keyword in keywords):
            lines.append(cleaned[:180])
        if len(lines) >= limit:
            break
    return lines


def classify_migration_candidates(entry_file: Path, text: str, datasets: list[Path], scripts: list[Path]) -> list[str]:
    candidates = {"manual_reference_only"}
    if any(keyword in text for keyword in ["必须", "不得", "门控", "准入", "P1", "P2", "P3"]):
        candidates.add("runtime_rule_candidate")
    if any(keyword in text.lower() for keyword in ["prompt", "输出结构", "模板", "report template"]):
        candidates.add("prompt_template_candidate")
    if any(keyword in text for keyword in ["报告模板", "A10", "代理词", "事实提炼报告"]):
        candidates.add("report_template_candidate")
    if any(keyword in text.lower() for keyword in ["score", "评分", "rubric", "must_include", "must_not_include"]):
        candidates.add("evaluation_rubric_candidate")
    if datasets or "case-samples" in str(entry_file) or "data/legal_casework_split" in str(entry_file):
        candidates.add("dataset_candidate")
    if scripts:
        candidates.add("script_candidate")
    if entry_file.name.endswith(".initial.md") or entry_file.name == "best_skill.md":
        candidates.add("experience_package_template_candidate")
    return sorted(candidates)


def recommend_level(migration_candidates: list[str], risk_flags: list[str], entry_file: Path) -> str:
    if "dataset_candidate" in migration_candidates:
        return "Level 5: Training Dataset Candidate"
    if "experience_package_template_candidate" in migration_candidates:
        return "Level 6: Experience Package Template Candidate"
    if "evaluation_rubric_candidate" in migration_candidates:
        return "Level 4: Evaluation Rubric Candidate"
    if "prompt_template_candidate" in migration_candidates:
        return "Level 3: Prompt Template Candidate"
    if "runtime_rule_candidate" in migration_candidates:
        return "Level 2: Runtime Rule Candidate"
    return "Level 1: Readonly Reference"


def recommend_actions(migration_candidates: list[str], risk_flags: list[str]) -> list[str]:
    actions = ["import_as_readonly"]
    if "runtime_rule_candidate" in migration_candidates:
        actions.append("convert_to_runtime_rules")
    if "prompt_template_candidate" in migration_candidates:
        actions.append("convert_to_prompt_template")
    if "evaluation_rubric_candidate" in migration_candidates:
        actions.append("convert_to_evaluation_rubric")
    if "experience_package_template_candidate" in migration_candidates:
        actions.append("convert_to_experience_package_template")
    if "manual_reference_only" in migration_candidates or risk_flags:
        actions.append("keep_as_reference_only")
    if "sensitive_data_risk" in risk_flags:
        actions.append("exclude_from_training")
    return sorted(set(actions))


def legacy_id(entry_file: Path) -> str:
    if entry_file.name == "SKILL.md":
        return entry_file.parent.name
    if entry_file.name.endswith(".initial.md"):
        return entry_file.stem.replace(".initial", "")
    if entry_file.name == "best_skill.md":
        return f"skillopt-{entry_file.parent.name}"
    return entry_file.stem


def display_name(entry_file: Path, text: str) -> str:
    name_match = re.search(r"^name:\s*(.+)$", text, flags=re.MULTILINE)
    if name_match:
        return name_match.group(1).strip()
    heading_match = re.search(r"^#\s+(.+)$", text, flags=re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    return legacy_id(entry_file)


def skill_type(entry_file: Path) -> str:
    text_path = str(entry_file)
    if "/.codex/skills/" in text_path and entry_file.name == "SKILL.md":
        return "codex_legacy_skill"
    if entry_file.name.endswith(".initial.md"):
        return "skillopt_initial_skill"
    if entry_file.name == "best_skill.md":
        return "skillopt_best_skill"
    return "legacy_asset"


def detect_domain(entry_file: Path, text: str) -> str:
    lower = f"{entry_file} {text}".lower()
    if "contract" in lower or "合同" in lower:
        return "contract_dispute"
    if "labor" in lower or "劳动" in lower:
        return "labor_dispute"
    if "router" in lower:
        return "legal_casework_router"
    if "legal" in lower or "案件" in lower:
        return "legal_casework"
    return "unknown"


def detect_version(text: str) -> str:
    match = re.search(r"\bv?(\d+\.\d+(?:\.\d+)?)\b", text)
    return match.group(1) if match else "暂无"


def summarize_source_files(source_dir: Path, entry_file: Path) -> list[str]:
    selected = [entry_file]
    for rel in ["references", "scripts"]:
        child = source_dir / rel
        if child.exists():
            selected.extend(sorted(path for path in child.iterdir() if path.is_file())[:20])
    for name in ["config.json", "summary.json", "runtime_state.json"]:
        child = source_dir / name
        if child.exists():
            selected.append(child)
    return [safe_path(path) for path in selected[:40]]


def safe_path(path: Path) -> str:
    try:
        return str(path.resolve())
    except OSError:
        return str(path)


def md(value: Any) -> str:
    if value is None:
        return "暂无"
    text = str(value).strip()
    return (text or "暂无").replace("|", "\\|").replace("\n", " ")


if __name__ == "__main__":
    raise SystemExit(main())
