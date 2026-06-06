import json
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_production_pilot"
RUNS_DIR = RUNTIME_ROOT / "runs"
OUTPUTS_DIR = RUNTIME_ROOT / "outputs"
OWNER_DOWNLOADS_DIR = RUNTIME_ROOT / "owner_downloads"
REVIEW_QUEUE_DIR = RUNTIME_ROOT / "review_queue"
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
