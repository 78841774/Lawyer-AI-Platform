import json
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["case-cause-taxonomy"])

BACKEND_ROOT = Path(__file__).resolve().parents[2]
TAXONOMY_ROOT = BACKEND_ROOT / "case_cause_taxonomy"
REGISTRY_PATH = TAXONOMY_ROOT / "registry.json"


def load_registry() -> dict[str, Any]:
    try:
        data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="case cause taxonomy not found") from error
    except json.JSONDecodeError as error:
        raise HTTPException(status_code=500, detail="case cause taxonomy invalid") from error
    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="case cause taxonomy payload invalid")
    return data


def case_causes() -> list[dict[str, Any]]:
    data = load_registry().get("case_causes", [])
    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="case cause taxonomy invalid")
    return [item for item in data if isinstance(item, dict)]


def find_case_cause(case_cause_code: str) -> dict[str, Any]:
    for item in case_causes():
        if item.get("case_cause_code") == case_cause_code:
            return item
    raise HTTPException(status_code=404, detail="case cause not found")


@router.get("/case-cause-taxonomy")
def list_case_cause_taxonomy() -> dict[str, Any]:
    return load_registry()


@router.get("/case-cause-taxonomy/{case_cause_code}")
def get_case_cause(case_cause_code: str) -> dict[str, Any]:
    return find_case_cause(case_cause_code)


@router.get("/case-cause-taxonomy/{case_cause_code}/ancestors")
def get_case_cause_ancestors(case_cause_code: str) -> dict[str, Any]:
    current = find_case_cause(case_cause_code)
    path = current.get("path", [])
    if not isinstance(path, list):
        raise HTTPException(status_code=500, detail="case cause path invalid")
    by_code = {item.get("case_cause_code"): item for item in case_causes()}
    ancestors = [
        by_code[code]
        for code in path
        if code in by_code
    ]
    return {
        "case_cause_code": case_cause_code,
        "ancestors": ancestors
    }


@router.get("/case-cause-taxonomy/{case_cause_code}/children")
def get_case_cause_children(case_cause_code: str) -> dict[str, Any]:
    find_case_cause(case_cause_code)
    children = [
        item
        for item in case_causes()
        if item.get("parent_case_cause_code") == case_cause_code
    ]
    return {
        "case_cause_code": case_cause_code,
        "children": children
    }
