import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from versioned_skill_training_runs.runner import (
    MockTrainingRunError,
    create_mock_training_run,
    normalize_run_id,
    registry_packages
)

router = APIRouter(tags=["versioned-skill-training-runs"])

RUNS_ROOT = Path(__file__).resolve().parent
REGISTRY_PATH = RUNS_ROOT / "registry.json"


class MockTrainingRunRequest(BaseModel):
    package_id: str


def load_registry() -> dict[str, Any]:
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="versioned skill training run registry not found") from error
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=500, detail="versioned skill training run registry invalid") from error
    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="versioned skill training run registry payload invalid")
    return data


def registry_runs() -> list[dict[str, Any]]:
    runs = load_registry().get("runs", [])
    if not isinstance(runs, list):
        raise HTTPException(status_code=500, detail="versioned skill training run registry invalid")
    return [run for run in runs if isinstance(run, dict)]


@router.get("/versioned-skill-training-runs")
def list_versioned_skill_training_runs() -> dict[str, Any]:
    registry = load_registry()
    return {
        "schema_version": registry.get("schema_version"),
        "runs": registry.get("runs", [])
    }


@router.get("/versioned-skill-training-runs/{run_id}")
def get_versioned_skill_training_run(run_id: str) -> dict[str, Any]:
    for run in registry_runs():
        if run.get("run_id") == run_id:
            return run
    for package in registry_packages():
        package_id = package.get("training_package_id")
        if isinstance(package_id, str) and normalize_run_id(package_id) == run_id:
            return create_mock_training_run(package_id)
    raise HTTPException(status_code=404, detail="versioned skill training run not found")


@router.post("/versioned-skill-training-runs/mock")
def create_versioned_skill_mock_training_run(payload: MockTrainingRunRequest) -> dict[str, Any]:
    try:
        return create_mock_training_run(payload.package_id)
    except MockTrainingRunError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
