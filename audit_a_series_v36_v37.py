from pathlib import Path
import json
import re
from datetime import datetime

BASE = Path.home() / "Lawyer-AI-Platform"

EXPECTED = {
    "A1": ["案由分析"],
    "A2": ["法规清单"],
    "A3": ["类案检索"],
    "A4": ["请求权", "抗辩权"],
    "A5": ["举证策略"],
    "A6": ["诉状", "答辩状"],
    "A7": ["诉求量化", "反请求"],
    "A8": ["证据清单"],
    "A9": ["质证意见"],
    "A10": ["争议焦点法律深化分析"],
    "A11": ["庭审提纲"],
    "A12": ["代理词"],
    "A13": ["结案报告", "结案框架"],
}

FORBIDDEN_A10_TERMS = [
    r"A10.*诉状",
    r"A10.*答辩状",
    r"A10.*代理词",
    r"A10.*结案报告",
    r"A10.*文书起草",
    r"A10.*文书结构",
    r"第十步.*诉状",
    r"第十步.*答辩状",
    r"第十步.*代理词",
    r"第十步.*结案报告",
    r"第十步.*文书起草",
    r"第十步.*文书结构",
]

SUSPICIOUS_PATTERNS = [
    r"A1.*诉状",
    r"A1.*代理词",
    r"A2.*诉状",
    r"A2.*代理词",
    r"A3.*诉状",
    r"A3.*代理词",
    r"A4.*诉状",
    r"A4.*代理词",
    r"A5.*诉状",
    r"A5.*代理词",
    r"A6.*争议焦点法律深化分析",
    r"A7.*争议焦点法律深化分析",
    r"A8.*争议焦点法律深化分析",
    r"A9.*争议焦点法律深化分析",
    r"A11.*争议焦点法律深化分析",
    r"A12.*争议焦点法律深化分析",
    r"A13.*争议焦点法律深化分析",
]

IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".next",
    "out",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
}

TEXT_EXTS = {
    ".md", ".txt", ".json", ".py", ".ts", ".tsx", ".js", ".jsx",
    ".yml", ".yaml", ".toml", ".html", ".css"
}

SEARCH_DIRS = [
    BASE / "docs",
    BASE / "09-Change-Logs",
    BASE / "08-Skill-Training",
    BASE / "Lawyer-AI-Platform-App" / "backend",
    BASE / "Lawyer-AI-Platform-App" / "frontend",
    BASE / "templates",
    BASE / "training_samples",
]

def md_escape(value):
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", " ").replace("\r", " ")

def should_skip(path: Path) -> bool:
    return any(part in IGNORE_DIRS for part in path.parts)

def iter_text_files():
    seen = set()
    for root in SEARCH_DIRS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path in seen:
                continue
            seen.add(path)
            if path.is_file() and path.suffix.lower() in TEXT_EXTS and not should_skip(path):
                yield path

def read_text(path: Path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

def rel(path: Path):
    try:
        return str(path.relative_to(BASE))
    except Exception:
        return str(path)

def find_matches(pattern: str):
    rx = re.compile(pattern)
    results = []
    for path in iter_text_files():
        text = read_text(path)
        for idx, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                results.append((rel(path), idx, line.strip()))
    return results

def find_literal(term: str):
    results = []
    for path in iter_text_files():
        text = read_text(path)
        for idx, line in enumerate(text.splitlines(), start=1):
            if term in line:
                results.append((rel(path), idx, line.strip()))
    return results

def json_files():
    for path in iter_text_files():
        if path.suffix.lower() == ".json":
            yield path

def validate_json_files():
    rows = []
    for path in json_files():
        try:
            json.loads(read_text(path))
            rows.append((rel(path), "OK", ""))
        except Exception as e:
            rows.append((rel(path), "ERROR", str(e)))
    return rows

def main():
    report = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report.append("# A1–A13 Legacy Skill Structure Audit Report")
    report.append("")
    report.append(f"- Generated at: {now}")
    report.append(f"- Project: `{BASE}`")
    report.append("- Scope: docs / changelogs / backend / frontend / training samples / templates")
    report.append("")

    report.append("## 1. Expected A-Series Structure")
    report.append("")
    report.append("| Code | Expected Meaning |")
    report.append("|---|---|")
    for code, terms in EXPECTED.items():
        report.append(f"| {code} | {' / '.join(terms)} |")
    report.append("")

    report.append("## 2. Presence Check")
    report.append("")
    report.append("| Code | Expected Terms | Status | Hit Count | Sample Locations |")
    report.append("|---|---|---|---:|---|")

    presence_summary = {}

    for code, terms in EXPECTED.items():
        term_hits = []
        for term in terms:
            term_hits.extend(find_literal(term))

        hit_count = len(term_hits)
        status = "OK" if hit_count > 0 else "MISSING"
        presence_summary[code] = status

        samples = []
        for file, line, content in term_hits[:5]:
            safe_content = md_escape(content)
            samples.append(f"`{file}:{line}` {safe_content[:120]}")

        sample_text = "<br>".join(samples) if samples else ""
        report.append(f"| {code} | {' / '.join(terms)} | {status} | {hit_count} | {sample_text} |")

    report.append("")

    report.append("## 3. Forbidden A10 Misclassification Check")
    report.append("")
    report.append("A10 must remain: `争议焦点法律深化分析`.")
    report.append("")
    report.append("| Pattern | Status | Hit Count | Sample Locations |")
    report.append("|---|---|---:|---|")

    forbidden_total = 0

    for pattern in FORBIDDEN_A10_TERMS:
        hits = find_matches(pattern)
        forbidden_total += len(hits)
        status = "OK" if not hits else "REVIEW_REQUIRED"

        samples = []
        for file, line, content in hits[:10]:
            safe_content = md_escape(content)
            samples.append(f"`{file}:{line}` {safe_content[:120]}")

        report.append(f"| `{md_escape(pattern)}` | {status} | {len(hits)} | {'<br>'.join(samples)} |")

    report.append("")

    report.append("## 4. Suspicious Cross-Classification Check")
    report.append("")
    report.append("| Pattern | Status | Hit Count | Sample Locations |")
    report.append("|---|---|---:|---|")

    suspicious_total = 0

    for pattern in SUSPICIOUS_PATTERNS:
        hits = find_matches(pattern)
        suspicious_total += len(hits)
        status = "OK" if not hits else "REVIEW_REQUIRED"

        samples = []
        for file, line, content in hits[:10]:
            safe_content = md_escape(content)
            samples.append(f"`{file}:{line}` {safe_content[:120]}")

        report.append(f"| `{md_escape(pattern)}` | {status} | {len(hits)} | {'<br>'.join(samples)} |")

    report.append("")

    report.append("## 5. JSON Parse Check")
    report.append("")
    report.append("| JSON File | Status | Error |")
    report.append("|---|---|---|")

    json_rows = validate_json_files()
    json_errors = 0

    for file, status, err in json_rows:
        if status != "OK":
            json_errors += 1
        safe_err = md_escape(err)
        report.append(f"| `{file}` | {status} | {safe_err} |")

    report.append("")

    report.append("## 6. Key Registry / Package Files")
    report.append("")
    key_paths = [
        "Lawyer-AI-Platform-App/backend/versioned_skill_training_packages/registry.json",
        "Lawyer-AI-Platform-App/backend/versioned_skill_training_runs/registry.json",
        "Lawyer-AI-Platform-App/backend/experience_package_build/registry.json",
        "Lawyer-AI-Platform-App/backend/controlled_skill_registry_publish/registry.json",
        "Lawyer-AI-Platform-App/backend/case_cause_taxonomy/registry.json",
        "docs/Skill-Factory-Foundation-v3.6.md",
        "09-Change-Logs/v3.6.md",
    ]

    report.append("| Path | Exists | Notes |")
    report.append("|---|---|---|")
    for p in key_paths:
        path = BASE / p
        exists = "YES" if path.exists() else "NO"
        report.append(f"| `{p}` | {exists} |  |")

    report.append("")

    report.append("## 7. Summary")
    report.append("")

    missing = [code for code, status in presence_summary.items() if status != "OK"]

    if not missing and forbidden_total == 0 and json_errors == 0:
        overall = "PASS"
    else:
        overall = "REVIEW_REQUIRED"

    report.append(f"- Overall: **{overall}**")
    report.append(f"- Missing A-series items: `{', '.join(missing) if missing else 'None'}`")
    report.append(f"- Forbidden A10 misclassification hits: `{forbidden_total}`")
    report.append(f"- Suspicious cross-classification hits: `{suspicious_total}`")
    report.append(f"- JSON parse errors: `{json_errors}`")
    report.append("")

    report.append("## 8. Required Manual Interpretation")
    report.append("")
    report.append("- Some hits may appear in historical changelog text explaining old mistakes. Those are acceptable if they clearly describe past cleanup and not current runtime rules.")
    report.append("- Any current rule, runtime package, registry, prompt, or frontend label that maps A10 to pleadings / agency statement / closing report must be corrected.")
    report.append("- A6 may contain `诉状 / 答辩状`, A12 may contain `代理词`, and A13 may contain `结案报告 / 结案框架`; those are expected.")
    report.append("- A10 must remain `争议焦点法律深化分析`.")
    report.append("")

    out_path = BASE / "A-Series-Audit-Report-v3.6-v3.7.md"
    out_path.write_text("\n".join(report), encoding="utf-8")

    print(f"Audit complete: {out_path}")
    print(f"Overall: {overall}")
    print(f"Missing A-series items: {missing if missing else 'None'}")
    print(f"Forbidden A10 hits: {forbidden_total}")
    print(f"Suspicious cross-classification hits: {suspicious_total}")
    print(f"JSON parse errors: {json_errors}")

if __name__ == "__main__":
    main()
