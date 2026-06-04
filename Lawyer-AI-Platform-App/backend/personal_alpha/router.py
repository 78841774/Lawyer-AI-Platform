from typing import Any

from fastapi import APIRouter

from personal_alpha.audit import list_personal_alpha_audit_logs
from personal_alpha.dry_run import run_personal_alpha_dry_run
from personal_alpha.manifest import preview_case_manifest
from personal_alpha.material_inventory import build_material_inventory_preview
from personal_alpha.schemas import (
    MaterialInventoryRequest,
    PersonalAlphaDryRunRequest,
    PersonalCaseManifestPreviewRequest,
)
from personal_alpha.status import get_personal_alpha_status

router = APIRouter(prefix="/personal-alpha", tags=["personal-alpha"])


@router.get("/status")
def personal_alpha_status() -> dict[str, Any]:
    return get_personal_alpha_status()


@router.post("/manifest/preview")
def personal_alpha_manifest_preview(request: PersonalCaseManifestPreviewRequest) -> dict[str, Any]:
    return preview_case_manifest(request)


@router.post("/materials/inventory")
def personal_alpha_material_inventory(request: MaterialInventoryRequest) -> dict[str, Any]:
    return build_material_inventory_preview(request)


@router.post("/dry-run")
def personal_alpha_dry_run(request: PersonalAlphaDryRunRequest) -> dict[str, Any]:
    return run_personal_alpha_dry_run(request)


@router.get("/audit-logs")
def personal_alpha_audit_logs() -> dict[str, Any]:
    return {"audit_logs": list_personal_alpha_audit_logs()}
