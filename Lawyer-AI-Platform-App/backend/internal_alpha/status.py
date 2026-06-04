from typing import Any

from app.llm.llm_service import get_llm_status
from internal_alpha.readiness import get_deployment_readiness_checklist
from internal_alpha.schemas import InternalAlphaStatus, InternalAlphaSubsystemStatus
from legal_search_adapter.mock_provider import MockLegalSearchProvider
from local_sandbox.router import get_local_sandbox_status
from ocr_adapter.mock_provider import MockOCRProvider
from source_refs.router import get_source_refs_status


def get_internal_alpha_status() -> dict[str, Any]:
    readiness = get_deployment_readiness_checklist()
    subsystems = [
        _subsystem("auth", True, "available", True, "JWT/dev-token auth foundation is available for local alpha."),
        _subsystem("workspace", True, "available", True, "Workspace APIs are available; auto runtime enablement remains disabled."),
        _subsystem("case_intake", True, "available", True, "Case intake exists; real case processing remains disabled by alpha guards."),
        _subsystem("material_center", True, "available", True, "Material APIs exist; Internal Alpha does not read real materials."),
        _subsystem("skill_factory", True, "available", True, "v3.6 Skill Factory foundation is available in controlled/mock mode."),
        _ocr_status(),
        _legal_search_status(),
        _source_refs_status(),
        _local_sandbox_status(),
        _report_runtime_status(),
        _subsystem("skill_registry", True, "available", True, "Skill Registry APIs are available; auto publish remains disabled."),
        _subsystem("experience_packages", True, "available", True, "Experience Package candidate flow remains human-reviewed."),
        _subsystem("versioned_training_runs", True, "available", True, "Mock versioned training runs remain available."),
    ]
    return InternalAlphaStatus(
        warnings=[
            "v4.0 is Internal Alpha only.",
            "No production deployment is enabled.",
            "No real OCR, legal database, LLM, or DeepSeek live provider is called.",
            "Manual review is required before any future real case workflow.",
        ],
        subsystems=subsystems,
        readiness=readiness,
    ).model_dump()


def _subsystem(name: str, enabled: bool, status: str, mock_only: bool, notes: str) -> InternalAlphaSubsystemStatus:
    return InternalAlphaSubsystemStatus(
        name=name,
        enabled=enabled,
        status=status,
        mock_only=mock_only,
        notes=notes,
    )


def _ocr_status() -> InternalAlphaSubsystemStatus:
    status = MockOCRProvider().get_status()
    return _subsystem("ocr_adapter", True, "available" if status.connected else "mock_available", True, status.notes)


def _legal_search_status() -> InternalAlphaSubsystemStatus:
    status = MockLegalSearchProvider().get_status()
    return _subsystem("legal_search_adapter", True, "available" if status.connected else "mock_available", True, status.notes)


def _source_refs_status() -> InternalAlphaSubsystemStatus:
    status = get_source_refs_status()
    return _subsystem("source_refs", bool(status.get("source_refs_enabled")), "available", True, str(status.get("notes")))


def _local_sandbox_status() -> InternalAlphaSubsystemStatus:
    status = get_local_sandbox_status()
    return _subsystem("local_sandbox", bool(status.get("enabled")), "available", bool(status.get("mock_only")), "v3.9 local sandbox guard is available.")


def _report_runtime_status() -> InternalAlphaSubsystemStatus:
    llm_status = get_llm_status()
    mock_only = llm_status.get("provider") == "mock" or not bool(llm_status.get("configured"))
    return _subsystem("report_runtime", True, "available", mock_only, "Report runtime basic status inferred without generating reports.")
