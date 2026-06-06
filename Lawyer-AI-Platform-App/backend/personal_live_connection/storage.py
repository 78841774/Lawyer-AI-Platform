import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_live_connection"
RUNS_DIR = BASE_DIR / "runs"
AUDIT_DIR = BASE_DIR / "audit"


def write_payload(directory: Path, payload_id: str, payload: dict) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / f"{payload_id}.json").write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def read_payload(directory: Path, payload_id: str) -> dict | None:
    path = directory / f"{payload_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def read_payloads(directory: Path) -> list[dict]:
    if not directory.exists():
        return []
    return [json.loads(path.read_text(encoding="utf-8")) for path in sorted(directory.glob("*.json"))]

