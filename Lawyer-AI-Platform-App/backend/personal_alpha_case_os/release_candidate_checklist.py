from pathlib import Path

from personal_alpha_case_os.schemas import PersonalAlphaCaseOSReleaseCandidateChecklistItem

REPO_ROOT = Path(__file__).resolve().parents[3]
CASE_OS_ROOT = REPO_ROOT / "Lawyer-AI-Platform-App/backend/personal_alpha_case_os"
DOCS_ROOT = REPO_ROOT / "docs"
CHANGELOG_ROOT = REPO_ROOT / "09-Change-Logs"
REGRESSION_ROOT = REPO_ROOT / "scripts/regression"

RELEASE_CANDIDATE_VERSION = "v6.9"

DOC_FILES = [
    "Personal-Alpha-Case-OS-v6.0.md",
    "Personal-Alpha-Case-OS-Stage-Orchestrator-v6.1.md",
    "Personal-Alpha-Case-OS-Unified-Audit-Timeline-v6.2.md",
    "Personal-Alpha-Case-OS-Review-State-Machine-v6.3.md",
    "Personal-Alpha-Case-OS-Final-Lock-Consolidation-v6.4.md",
    "Personal-Alpha-Case-OS-Export-Package-v6.5.md",
    "Personal-Alpha-Case-OS-Quality-Checklist-v6.6.md",
    "Personal-Alpha-Case-OS-Regression-Suite-v6.7.md",
    "Personal-Alpha-Case-OS-Hardening-v6.8.md",
    "Personal-Alpha-Case-OS-Release-Candidate-v6.9.md",
]

CHANGELOG_FILES = [f"v6.{index}.md" for index in range(0, 10)]


def build_release_candidate_checklist() -> dict[str, object]:
    items = [
        _item("v6_0_case_os_foundation", "Case OS Foundation exists", _module_exists("case_os_engine.py"), "capability", "v6.0"),
        _item("v6_1_stage_orchestrator", "Stage orchestrator exists", _module_exists("stage_orchestrator.py"), "capability", "v6.1"),
        _item("v6_2_unified_audit_timeline", "Unified audit timeline exists", _module_exists("unified_audit_engine.py"), "capability", "v6.2"),
        _item("v6_3_review_state_machine", "Review state machine exists", _module_exists("review_state_machine.py"), "capability", "v6.3"),
        _item("v6_4_final_lock_consolidation", "Final lock consolidation exists", _module_exists("final_lock_consolidation.py"), "capability", "v6.4"),
        _item("v6_5_export_package", "Export package metadata exists", _module_exists("export_package_engine.py"), "capability", "v6.5"),
        _item("v6_6_quality_checklist", "Quality checklist exists", _module_exists("quality_checklist_engine.py"), "capability", "v6.6"),
        _item("v6_7_regression_suite", "Regression suite exists and is documented", _regression_exists(), "regression", "v6.7"),
        _item("v6_8_hardening_layer", "Hardening layer exists", _hardening_exists(), "hardening", "v6.8"),
        _item("docs_v6_0_to_v6_8_available", "Case OS docs v6.0-v6.8 are available", _docs_exist(include_v69=False), "documentation", "v6.0-v6.8"),
        _item("changelogs_v6_0_to_v6_8_available", "Case OS changelogs v6.0-v6.8 are available", _changelogs_exist(include_v69=False), "documentation", "v6.0-v6.8"),
        _item("regression_scripts_available", "Regression scripts are available", _regression_scripts_exist(), "regression", "v6.7-v6.9"),
        _item("safety_boundary_documented", "Safety boundary is documented", _docs_exist(include_v69=True) and _changelogs_exist(include_v69=True), "safety", "v6.8-v6.9"),
        _item("no_raw_content_guard_available", "No source-content guard is available", _module_exists("safety_guard.py"), "safety", "v6.8"),
        _item("runtime_guard_available", "Runtime storage guard is available", _module_exists("runtime_guard.py"), "safety", "v6.8"),
        _item("response_consistency_available", "Response consistency check is available", _module_exists("response_consistency.py"), "safety", "v6.8"),
        _item("v7_0_personal_production_direction_defined", "Next stage is Personal Production Workspace Foundation", True, "roadmap", "v6.9"),
    ]
    passed_count = sum(1 for item in items if item.passed)
    failed_count = len(items) - passed_count
    required_failed_count = sum(1 for item in items if item.required and not item.passed)
    return {
        "checklist": items,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "required_failed_count": required_failed_count,
        "release_candidate_ready": required_failed_count == 0,
    }


def release_candidate_summary_flags() -> dict[str, bool]:
    checklist = build_release_candidate_checklist()
    passed_by_id = {item.check_id: item.passed for item in checklist["checklist"]}
    release_candidate_ready = bool(checklist["release_candidate_ready"])
    return {
        "case_os_foundation": passed_by_id["v6_0_case_os_foundation"],
        "stage_orchestration": passed_by_id["v6_1_stage_orchestrator"],
        "unified_audit_timeline": passed_by_id["v6_2_unified_audit_timeline"],
        "review_state_machine": passed_by_id["v6_3_review_state_machine"],
        "final_lock_consolidation": passed_by_id["v6_4_final_lock_consolidation"],
        "export_package": passed_by_id["v6_5_export_package"],
        "quality_checklist": passed_by_id["v6_6_quality_checklist"],
        "regression_suite": passed_by_id["v6_7_regression_suite"],
        "hardening_layer": passed_by_id["v6_8_hardening_layer"],
        "docs_available": passed_by_id["docs_v6_0_to_v6_8_available"],
        "changelogs_available": passed_by_id["changelogs_v6_0_to_v6_8_available"],
        "personal_production_next_step_defined": passed_by_id["v7_0_personal_production_direction_defined"],
        "release_candidate_ready": release_candidate_ready,
    }


def _item(check_id: str, label: str, passed: bool, category: str, source: str) -> PersonalAlphaCaseOSReleaseCandidateChecklistItem:
    return PersonalAlphaCaseOSReleaseCandidateChecklistItem(
        check_id=check_id,
        label=label,
        passed=passed,
        required=True,
        category=category,
        source=source,
    )


def _module_exists(filename: str) -> bool:
    return (CASE_OS_ROOT / filename).is_file()


def _regression_exists() -> bool:
    return (REGRESSION_ROOT / "run_personal_alpha_regression.sh").is_file() and (REGRESSION_ROOT / "README.md").is_file()


def _regression_scripts_exist() -> bool:
    required = [
        "check_case_os_core_apis.sh",
        "check_case_os_quality_apis.sh",
        "check_case_os_hardening_apis.sh",
        "check_case_os_release_candidate_apis.sh",
        "check_metadata_only_responses.sh",
    ]
    return all((REGRESSION_ROOT / filename).is_file() for filename in required)


def _hardening_exists() -> bool:
    required = ["safety_guard.py", "safety_response.py", "runtime_guard.py", "response_consistency.py"]
    return all(_module_exists(filename) for filename in required)


def _docs_exist(*, include_v69: bool) -> bool:
    files = DOC_FILES if include_v69 else DOC_FILES[:-1]
    return all((DOCS_ROOT / filename).is_file() and (DOCS_ROOT / filename).stat().st_size > 0 for filename in files)


def _changelogs_exist(*, include_v69: bool) -> bool:
    files = CHANGELOG_FILES if include_v69 else CHANGELOG_FILES[:-1]
    return all((CHANGELOG_ROOT / filename).is_file() and (CHANGELOG_ROOT / filename).stat().st_size > 0 for filename in files)
