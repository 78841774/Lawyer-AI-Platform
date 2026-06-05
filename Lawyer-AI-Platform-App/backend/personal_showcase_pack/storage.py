import json
import re
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_showcase_pack"
SHOWCASE_RUNS_DIR = RUNTIME_ROOT / "showcase_runs"
PILOT_SAMPLES_DIR = RUNTIME_ROOT / "pilot_samples"
STORY_FLOWS_DIR = RUNTIME_ROOT / "story_flows"
METRICS_DIR = RUNTIME_ROOT / "metrics"
AUDIT_DIR = RUNTIME_ROOT / "audit"
SAFE_RECORD_ID = re.compile(r"^[A-Za-z0-9_-]+$")


def write_payload(directory: Path, record_id: str, payload: dict) -> None:
    if not SAFE_RECORD_ID.fullmatch(record_id):
        raise ValueError("record_id contains unsafe characters")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{record_id}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_payloads(directory: Path) -> list[dict]:
    if not directory.exists():
        return []
    payloads = []
    for path in sorted(directory.glob("*.json")):
        try:
            payloads.append(json.loads(path.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            continue
    return payloads


def read_payload(directory: Path, record_id: str) -> dict | None:
    if not SAFE_RECORD_ID.fullmatch(record_id):
        return None
    path = directory / f"{record_id}.json"
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
