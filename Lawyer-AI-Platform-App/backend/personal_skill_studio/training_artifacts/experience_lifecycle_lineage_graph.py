from personal_skill_studio.training_artifacts.experience_package_version_lineage import lineage_node


def build_lineage(training_packages: list, review_packages: list, runtime_loads: list, candidate_packs: list, next_packages: list):
    root_package_id = (
        (_get(training_packages[0], "package_id") if training_packages else None)
        or (_get(review_packages[0], "package_id") if review_packages else None)
        or "experience_lifecycle_root"
    )
    lineage = []
    for package in training_packages:
        lineage.append(lineage_node(root_package_id, _get(package, "package_id"), _get(package, "package_version"), "training_package", _get(package, "package_status")))
    for package in review_packages:
        lineage.append(lineage_node(root_package_id, _get(package, "package_id"), _get(package, "package_version"), "lawyer_approved_experience_package", _get(package, "review_status")))
    for load in runtime_loads:
        lineage.append(lineage_node(root_package_id, load.experience_package_id, load.package_version, "runtime_loaded_package", load.load_status, loaded_runtime_load_ids=[load.runtime_load_id]))
    for pack in candidate_packs:
        lineage.append(lineage_node(root_package_id, pack.candidate_pack_id, pack.proposed_next_package_version, "candidate_pack", pack.candidate_status, derived_from_feedback_ids=pack.feedback_ids, derived_from_risk_event_ids=pack.risk_event_ids))
    for draft in next_packages:
        lineage.append(lineage_node(root_package_id, draft.next_package_id, draft.next_package_version, "next_experience_package_draft", draft.draft_status, draft.source_package_id, draft.candidate_pack_id))
    return lineage


def _get(item, key: str, default: str = "unknown"):
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)
