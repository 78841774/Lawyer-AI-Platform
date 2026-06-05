import json
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_case_production"
PRODUCTION_CASES_DIR = RUNTIME_ROOT / "production_cases"
WORKFLOW_RUNS_DIR = RUNTIME_ROOT / "workflow_runs"
STAGE_RUNS_DIR = RUNTIME_ROOT / "stage_runs"
READINESS_DIR = RUNTIME_ROOT / "readiness"
REVIEW_GATES_DIR = RUNTIME_ROOT / "review_gates"
SOURCE_TRACES_DIR = RUNTIME_ROOT / "source_traces"
AUDIT_DIR = RUNTIME_ROOT / "audit"


def write_payload(directory: Path, record_id: str, payload: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{record_id}.json").write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def read_payloads(directory: Path) -> list[dict]:
    if not directory.exists():
        return []
    payloads: list[dict] = []
    for path in sorted(directory.glob("*.json")):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            continue
    return payloads


def read_payload(directory: Path, record_id: str) -> dict | None:
    path = directory / f"{record_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
