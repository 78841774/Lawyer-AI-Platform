import json
from pathlib import Path
from typing import Any


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_trial_readiness"


def storage_dir(name: str) -> Path:
    path = RUNTIME_ROOT / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(directory: str, object_id: str, data: dict[str, Any]) -> None:
    path = storage_dir(directory) / f"{object_id}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def read_json(directory: str, object_id: str) -> dict[str, Any] | None:
    path = storage_dir(directory) / f"{object_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def list_json(directory: str) -> list[dict[str, Any]]:
    path = storage_dir(directory)
    return [json.loads(item.read_text(encoding="utf-8")) for item in sorted(path.glob("*.json"))]

