import json
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[1] / "storage" / "runtime" / "personal_skill_studio"
EXPERIENCE_PACKAGES_DIR = RUNTIME_ROOT / "experience_packages"
SKILL_CANDIDATES_DIR = RUNTIME_ROOT / "skill_candidates"
TEST_CASES_DIR = RUNTIME_ROOT / "test_cases"
EVALUATIONS_DIR = RUNTIME_ROOT / "evaluations"
PROMOTION_QUEUE_DIR = RUNTIME_ROOT / "promotion_queue"
SOURCE_TRACES_DIR = RUNTIME_ROOT / "source_traces"
AUDIT_DIR = RUNTIME_ROOT / "audit"
SKILL_TRAINING_ROOT = RUNTIME_ROOT / "skill_training"
SKILL_TRAINING_AUDIT_DIR = SKILL_TRAINING_ROOT / "audit"
SKILL_TRAINING_SOURCE_TRACES_DIR = SKILL_TRAINING_ROOT / "source_traces"
SKILL_TRAINING_CONFIRMATION_QUEUE_DIR = SKILL_TRAINING_ROOT / "confirmation_queue"
SKILL_FINAL_DRAFT_DOWNLOADS_DIR = RUNTIME_ROOT / "skill_final_draft_downloads"


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
