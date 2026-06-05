from typing import Any

from fastapi import APIRouter

from personal_production.production_mode import build_personal_production_mode, build_personal_production_status
from personal_production.provider_capabilities import build_provider_capabilities
from personal_production.readiness_engine import build_console_summary, build_personal_production_readiness
from personal_production.runtime_registry import build_runtime_registry
from personal_production.safety_engine import build_personal_production_safety
from personal_production.showcase_mode import build_showcase_mode

router = APIRouter(prefix="/personal-production", tags=["personal-production"])


@router.get("/status")
def personal_production_status() -> dict[str, Any]:
    return build_personal_production_status()


@router.get("/mode")
def personal_production_mode() -> dict[str, Any]:
    return build_personal_production_mode()


@router.get("/showcase")
def personal_production_showcase() -> dict[str, Any]:
    return build_showcase_mode()


@router.get("/runtime-registry")
def personal_production_runtime_registry() -> dict[str, Any]:
    return build_runtime_registry()


@router.get("/provider-capabilities")
def personal_production_provider_capabilities() -> dict[str, Any]:
    return build_provider_capabilities()


@router.get("/readiness")
def personal_production_readiness() -> dict[str, Any]:
    return build_personal_production_readiness()


@router.get("/safety")
def personal_production_safety() -> dict[str, Any]:
    return build_personal_production_safety()


@router.get("/console-summary")
def personal_production_console_summary() -> dict[str, Any]:
    return build_console_summary()
