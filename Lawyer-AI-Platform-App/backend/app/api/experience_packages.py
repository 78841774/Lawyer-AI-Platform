import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.experience_package import ExperiencePackage
from app.repositories.experience_package_repository import ExperiencePackageRepository
from app.repositories.skill_repository import SkillRepository
from app.services.experience_package_service import ExperiencePackageService
from experience_package_build.builder import (
    ExperiencePackageBuildError,
    create_experience_package_candidate,
    get_experience_package_candidate,
    list_experience_package_candidates,
    review_experience_package_candidate
)

router = APIRouter(tags=["experience-packages"])


class CreateExperiencePackageCandidateRequest(BaseModel):
    run_id: str


class ReviewExperiencePackageRequest(BaseModel):
    review_status: str
    reviewed_by: str | None = None


def get_experience_package_service(db: Session) -> ExperiencePackageService:
    return ExperiencePackageService(
        experience_package_repository=ExperiencePackageRepository(db),
        skill_repository=SkillRepository(db)
    )


def serialize_package(package: ExperiencePackage) -> dict[str, Any]:
    return {
        "package_id": package.package_id,
        "skill_id": package.skill_id,
        "name": package.name,
        "domain": package.domain,
        "version": package.version,
        "status": package.status,
        "package_path": package.package_path,
        "created_at": package.created_at
    }


def serialize_package_detail(package: ExperiencePackage) -> dict[str, Any]:
    payload = serialize_package(package)
    payload["manifest"] = json.loads(package.manifest_json)
    return payload


def handle_candidate_error(error: ExperiencePackageBuildError) -> HTTPException:
    message = str(error)
    if "not found" in message:
        return HTTPException(status_code=404, detail=message)
    return HTTPException(status_code=400, detail=message)


@router.post("/skills/{skill_id}/packages/build")
def build_experience_package(
    skill_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_experience_package_service(db)
    try:
        package = service.build_package(skill_id)
    except ValueError as error:
        if str(error) == "skill not found":
            raise HTTPException(status_code=404, detail=str(error)) from error
        if str(error) == "skill not evaluated":
            raise HTTPException(status_code=400, detail=str(error)) from error
        if str(error) == "skill not validated":
            raise HTTPException(status_code=400, detail=str(error)) from error
        raise HTTPException(status_code=500, detail="experience package build failed") from error
    except Exception as error:
        raise HTTPException(status_code=500, detail="experience package build failed") from error
    return serialize_package(package)


@router.get("/experience-packages")
def list_experience_packages(
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    service = get_experience_package_service(db)
    return {
        "experience_packages": list_experience_package_candidates() + [
            serialize_package(package)
            for package in service.list_packages()
        ]
    }


@router.post("/experience-packages/create")
def create_experience_package_candidate_endpoint(payload: CreateExperiencePackageCandidateRequest) -> dict[str, Any]:
    try:
        return create_experience_package_candidate(payload.run_id)
    except ExperiencePackageBuildError as error:
        raise handle_candidate_error(error) from error


@router.post("/experience-packages/{experience_package_id}/review")
def review_experience_package_candidate_endpoint(
    experience_package_id: str,
    payload: ReviewExperiencePackageRequest
) -> dict[str, Any]:
    try:
        return review_experience_package_candidate(
            experience_package_id,
            payload.review_status,
            payload.reviewed_by
        )
    except ExperiencePackageBuildError as error:
        raise handle_candidate_error(error) from error


@router.get("/experience-packages/{package_id}/manifest")
def get_experience_package_manifest(
    package_id: str,
    db: Session = Depends(get_db)
) -> dict[str, object]:
    try:
        candidate = get_experience_package_candidate(package_id)
        return {
            "experience_package_id": candidate["experience_package_id"],
            "source_run_id": candidate["source_run_id"],
            "package_contents": candidate["package_contents"],
            "review": candidate["review"],
            "safety": candidate["safety"]
        }
    except ExperiencePackageBuildError:
        pass
    service = get_experience_package_service(db)
    manifest = service.get_manifest(package_id)
    if manifest is None:
        raise HTTPException(status_code=404, detail="experience package not found")
    return manifest


@router.get("/experience-packages/{package_id}")
def get_experience_package(
    package_id: str,
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    try:
        return get_experience_package_candidate(package_id)
    except ExperiencePackageBuildError:
        pass
    service = get_experience_package_service(db)
    package = service.get_package(package_id)
    if package is None:
        raise HTTPException(status_code=404, detail="experience package not found")
    return serialize_package_detail(package)
