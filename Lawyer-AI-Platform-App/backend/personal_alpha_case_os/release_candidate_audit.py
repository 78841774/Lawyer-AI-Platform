from typing import Any

from personal_alpha_case_os.response_consistency import check_response_consistency, normalize_response_metadata
from personal_alpha_case_os.runtime_guard import assert_runtime_storage_ignored
from personal_alpha_case_os.safety_guard import scan_scoped_payloads


def build_release_candidate_audit(
    *,
    status: dict[str, Any],
    summary: dict[str, Any],
    checklist: dict[str, Any],
    readiness: dict[str, Any],
    release_notes_preview: dict[str, Any],
) -> dict[str, Any]:
    scoped_payloads = {
        "rc_status": status,
        "rc_summary": summary,
        "rc_checklist": checklist,
        "rc_readiness": readiness,
        "rc_release_notes_preview": release_notes_preview,
    }
    safety_scan = scan_scoped_payloads(scoped_payloads)
    consistency = check_response_consistency(
        {
            "/case-os/release-candidate/status": normalize_response_metadata(status),
            "/case-os/release-candidate/summary": normalize_response_metadata(summary),
            "/case-os/release-candidate/checklist": normalize_response_metadata(checklist),
            "/case-os/release-candidate/readiness": normalize_response_metadata(readiness),
            "/case-os/release-candidate/release-notes-preview": normalize_response_metadata(release_notes_preview),
        }
    )
    runtime_storage_check_passed = all(
        assert_runtime_storage_ignored(path)
        for path in [
            "personal_alpha_case_os/export_packages",
            "personal_alpha_final_lock",
            "personal_alpha_workspace/audit",
        ]
    )
    regression_suite_check_passed = _check_by_id(checklist, "regression_scripts_available")
    docs_check_passed = _check_by_id(checklist, "docs_v6_0_to_v6_8_available")
    changelog_check_passed = _check_by_id(checklist, "changelogs_v6_0_to_v6_8_available")
    roadmap_check_passed = _check_by_id(checklist, "v7_0_personal_production_direction_defined")
    raw_content_check_passed = bool(safety_scan.get("passed", False))
    provider_check_passed = (
        status.get("production_enabled") is False
        and status.get("mock_first_enabled") is True
        and status.get("final_legal_opinion_generated") is False
        and status.get("final_report_generated") is False
    )
    response_consistency_check_passed = bool(consistency.get("passed", False))
    passed = all(
        [
            raw_content_check_passed,
            provider_check_passed,
            runtime_storage_check_passed,
            response_consistency_check_passed,
            regression_suite_check_passed,
            docs_check_passed,
            changelog_check_passed,
            roadmap_check_passed,
        ]
    )
    return {
        "passed": passed,
        "raw_content_check_passed": raw_content_check_passed,
        "provider_check_passed": provider_check_passed,
        "runtime_storage_check_passed": runtime_storage_check_passed,
        "response_consistency_check_passed": response_consistency_check_passed,
        "regression_suite_check_passed": regression_suite_check_passed,
        "docs_check_passed": docs_check_passed,
        "changelog_check_passed": changelog_check_passed,
        "roadmap_check_passed": roadmap_check_passed,
        "unsafe_item_count": int(safety_scan.get("unsafe_value_count", 0) or 0),
        "unsafe_items": safety_scan.get("unsafe_items", []),
    }


def _check_by_id(checklist: dict[str, Any], check_id: str) -> bool:
    for item in checklist.get("checklist", []):
        if isinstance(item, dict):
            if item.get("check_id") == check_id:
                return bool(item.get("passed", False))
            continue
        if getattr(item, "check_id", "") == check_id:
            return bool(getattr(item, "passed", False))
    return False
