from personal_skill_studio.training_artifacts.schemas import (
    SkillPackage,
    SkillPackageAudit,
    SkillPackageBuildRequest,
    SkillPackageBuildResponse,
    SkillPackageList,
)
from personal_skill_studio.training_artifacts.skill_package_audit_engine import build_package_audit
from personal_skill_studio.training_artifacts.skill_package_builder import build_skill_package
from personal_skill_studio.training_artifacts.skill_package_safety_engine import build_v731d_status, v731d_safety_flags
from personal_skill_studio.training_artifacts.skill_package_validation_gate import validate_package
from personal_skill_studio.training_artifacts.storage import SKILL_PACKAGES_DIR, read_payload, read_payloads, write_payload


def build_package_record(request: SkillPackageBuildRequest) -> dict | None:
    package = build_skill_package(request)
    if package is None:
        return None
    write_payload(SKILL_PACKAGES_DIR, package.package_id, package.model_dump())
    return SkillPackageBuildResponse(
        skill_package=package,
        packaged_experience_count=package.experience_count,
        warnings=[
            "Only approved and redacted Skill Experience Pool entries are packaged.",
            "v7.31d package build does not trigger provider calls, real training, or Skill publishing.",
        ],
        **v731d_safety_flags(),
    ).model_dump()


def list_package_records() -> dict:
    packages = _all_packages()
    return SkillPackageList(
        skill_packages=packages,
        package_count=len(packages),
        system_validated_count=sum(1 for package in packages if package.pre_publish_gate_status == "system_validated"),
        warnings=["Skill Packages are versioned metadata only and remain pre-training artifacts in v7.31d."],
        **v731d_safety_flags(),
    ).model_dump()


def get_package_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    return package.model_dump() if package else None


def validate_package_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    if package is None:
        return None
    validated = validate_package(package)
    write_payload(SKILL_PACKAGES_DIR, validated.package_id, validated.model_dump())
    return {
        "package_id": validated.package_id,
        "pre_publish_gate_status": validated.pre_publish_gate_status,
        "package_status": validated.package_status,
        "validation_result": validated.validation_result.model_dump() if validated.validation_result else None,
        **v731d_safety_flags(),
        "warnings": ["System validation does not perform manual review and does not publish a Skill."],
    }


def get_package_manifest_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    return package.manifest.model_dump() if package else None


def get_package_audit_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    if package is None:
        return None
    return build_package_audit(package_id, package.audit_events).model_dump()


def get_package_source_trace_record(package_id: str) -> dict | None:
    package = _read_package(package_id)
    return package.source_trace_bundle.model_dump() if package else None


def get_v731d_pipeline_status() -> dict:
    return build_v731d_status()


def _read_package(package_id: str) -> SkillPackage | None:
    payload = read_payload(SKILL_PACKAGES_DIR, package_id)
    if payload:
        return SkillPackage(**payload)
    return None


def _all_packages() -> list[SkillPackage]:
    return [SkillPackage(**payload) for payload in read_payloads(SKILL_PACKAGES_DIR)]
