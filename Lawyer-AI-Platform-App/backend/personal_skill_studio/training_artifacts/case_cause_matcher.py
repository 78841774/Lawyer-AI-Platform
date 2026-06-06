from uuid import uuid4

from personal_skill_studio.training_artifacts.artifact_registry import list_packages
from personal_skill_studio.training_artifacts.case_cause_taxonomy import find_node_by_path
from personal_skill_studio.training_artifacts.schemas import CaseCauseMatchRequest, CaseCauseMatchResult


def match_case_cause(request: CaseCauseMatchRequest) -> CaseCauseMatchResult:
    path = _normalized_path(request.case_cause_path)
    node = find_node_by_path(path)
    packages = list_packages()
    exact = [package for package in packages if package.load_strategy == "exact_match" and package.case_cause_path == path]
    ancestors = [
        package
        for package in packages
        if package.load_strategy == "ancestor_fallback"
        and package.case_cause_path in _ancestor_paths(path)
    ]
    common = [package for package in packages if package.load_strategy == "common_package_fallback"]
    evidence_overlay = [
        package
        for package in packages
        if package.load_strategy == "evidence_type_overlay"
        and (not request.evidence_types or set(package.evidence_types).intersection(request.evidence_types))
    ]
    selected = _ordered_unique([*common, *ancestors, *exact, *evidence_overlay])
    fallback_chain = [package.package_id for package in [*exact, *ancestors, *common] if package.package_id in {item.package_id for item in selected}]
    return CaseCauseMatchResult(
        match_id=f"case_cause_match_{uuid4().hex[:12]}",
        requested_case_cause_path=path,
        matched_case_cause_id=node.case_cause_id if node else None,
        exact_package_ids=[package.package_id for package in exact],
        ancestor_fallback_package_ids=[package.package_id for package in ancestors],
        common_package_ids=[package.package_id for package in common],
        evidence_overlay_package_ids=[package.package_id for package in evidence_overlay],
        selected_package_ids=[package.package_id for package in selected],
        fallback_chain=fallback_chain,
        merge_order=[package.package_id for package in selected],
        warnings=[
            "Match is metadata-only and dry-run.",
            "Fallback selects ancestor and common packages when exact package is absent.",
        ],
    )


def _ancestor_paths(path: list[str]) -> list[list[str]]:
    return [path[:index] for index in range(1, len(path)) if path[:index]]


def _normalized_path(path: list[str]) -> list[str]:
    return [str(item).strip() for item in path if str(item).strip()]


def _ordered_unique(packages):
    seen: set[str] = set()
    ordered = sorted(packages, key=lambda package: (package.priority, package.package_id))
    result = []
    for package in ordered:
        if package.package_id in seen:
            continue
        seen.add(package.package_id)
        result.append(package)
    return result

