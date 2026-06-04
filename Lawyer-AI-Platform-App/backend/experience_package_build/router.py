from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from experience_package_build.builder import (
    ExperiencePackageBuildError,
    create_experience_package_candidate,
    get_experience_package_candidate,
    list_experience_package_candidates,
    review_experience_package_candidate
)

router = APIRouter(tags=["experience-package-candidates"])


class CreateExperiencePackageCandidateRequest(BaseModel):
    run_id: str


class ReviewExperiencePackageRequest(BaseModel):
    review_status: str
    reviewed_by: str | None = None


def handle_build_error(error: ExperiencePackageBuildError) -> HTTPException:
    message = str(error)
    if "not found" in message:
        return HTTPException(status_code=404, detail=message)
    return HTTPException(status_code=400, detail=message)


@router.get("/experience-package-candidates")
def list_experience_package_candidates_endpoint() -> dict[str, Any]:
    return {"experience_packages": list_experience_package_candidates()}


@router.get("/experience-package-candidates/{experience_package_id}")
def get_experience_package_candidate_endpoint(experience_package_id: str) -> dict[str, Any]:
    try:
        return get_experience_package_candidate(experience_package_id)
    except ExperiencePackageBuildError as error:
        raise handle_build_error(error) from error


@router.post("/experience-package-candidates/create")
def create_experience_package_candidate_endpoint(payload: CreateExperiencePackageCandidateRequest) -> dict[str, Any]:
    try:
        return create_experience_package_candidate(payload.run_id)
    except ExperiencePackageBuildError as error:
        raise handle_build_error(error) from error


@router.post("/experience-package-candidates/{experience_package_id}/review")
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
        raise handle_build_error(error) from error
