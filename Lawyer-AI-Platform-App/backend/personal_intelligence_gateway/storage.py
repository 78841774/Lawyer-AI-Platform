import json
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_intelligence_gateway"
LEGAL_SEARCH_DIR = RUNTIME_ROOT / "legal_search"
ENTERPRISE_QUERY_DIR = RUNTIME_ROOT / "enterprise_query"
SOURCE_TRACES_DIR = RUNTIME_ROOT / "source_traces"
CONFIRMATION_QUEUE_DIR = RUNTIME_ROOT / "confirmation_queue"
AUDIT_DIR = RUNTIME_ROOT / "audit"
LIVE_ROOT = RUNTIME_ROOT / "live"
LIVE_LEGAL_RUNS_DIR = LIVE_ROOT / "legal_search_runs"
LIVE_ENTERPRISE_RUNS_DIR = LIVE_ROOT / "enterprise_query_runs"
LIVE_REVIEW_QUEUE_DIR = LIVE_ROOT / "review_queue"
LIVE_SOURCE_TRACES_DIR = LIVE_ROOT / "source_traces"
LIVE_AUDIT_DIR = LIVE_ROOT / "audit"


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
