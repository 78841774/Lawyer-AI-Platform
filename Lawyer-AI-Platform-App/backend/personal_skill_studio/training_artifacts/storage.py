import json
from pathlib import Path


RUNTIME_ROOT = Path(__file__).resolve().parents[2] / "storage" / "runtime" / "training_artifacts"
LOAD_DRY_RUNS_DIR = RUNTIME_ROOT / "load_dry_runs"
TRAINING_RUNS_DIR = RUNTIME_ROOT / "training_runs"
REAL_CLOSED_CASE_INTAKES_DIR = RUNTIME_ROOT / "real_closed_case_intakes"
OCR_JOBS_DIR = RUNTIME_ROOT / "v731b_ocr_jobs"
LEGAL_RETRIEVAL_JOBS_DIR = RUNTIME_ROOT / "v731b_legal_retrieval_jobs"
EXPERIENCE_CANDIDATES_DIR = RUNTIME_ROOT / "v731b_experience_candidates"
SKILL_EXPERIENCE_POOL_DIR = RUNTIME_ROOT / "v731c_skill_experience_pool"
SKILL_EXPERIENCE_BINDINGS_DIR = RUNTIME_ROOT / "v731c_skill_experience_bindings"
CODEX_SKILL_DRAFTS_DIR = RUNTIME_ROOT / "v731c_codex_skill_drafts"


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
