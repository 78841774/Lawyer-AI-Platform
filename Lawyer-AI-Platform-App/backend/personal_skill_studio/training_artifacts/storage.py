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
SKILL_PACKAGES_DIR = RUNTIME_ROOT / "v731d_skill_packages"
INTERNAL_TRAINING_TASKS_DIR = RUNTIME_ROOT / "v731e_internal_training_tasks"
TRAINING_PACKAGES_DIR = RUNTIME_ROOT / "v731e_training_packages"
PRACTICE_LOAD_REVIEW_PACKAGES_DIR = RUNTIME_ROOT / "v731f_practice_load_review_packages"
PRACTICE_RUNTIME_LOADS_DIR = RUNTIME_ROOT / "v731g_practice_runtime_loads"
PRACTICE_RUNTIME_USAGE_DIR = RUNTIME_ROOT / "v731g_practice_runtime_usage"
PRACTICE_RUNTIME_RISK_EVENTS_DIR = RUNTIME_ROOT / "v731g_practice_runtime_risk_events"
PRACTICE_OUTPUT_OBSERVATIONS_DIR = RUNTIME_ROOT / "v731h_practice_output_observations"
PRACTICE_LAWYER_FEEDBACK_DIR = RUNTIME_ROOT / "v731h_practice_lawyer_feedback"
PRACTICE_FEEDBACK_RISK_EVENTS_DIR = RUNTIME_ROOT / "v731h_practice_feedback_risk_events"
PRACTICE_FEEDBACK_CANDIDATE_PACKS_DIR = RUNTIME_ROOT / "v731i_practice_feedback_candidate_packs"
NEXT_EXPERIENCE_PACKAGES_DIR = RUNTIME_ROOT / "v731j_next_experience_packages"
EXPERIENCE_LIFECYCLES_DIR = RUNTIME_ROOT / "v732_experience_lifecycles"
CASE_ANALYSIS_WORKBENCH_VIEWS_DIR = RUNTIME_ROOT / "v733_case_analysis_workbench_views"
CASE_ANALYSIS_OUTPUT_FEEDBACK_DIR = RUNTIME_ROOT / "v733_case_analysis_output_feedback"
CASE_ANALYSIS_OUTPUT_RISK_EVENTS_DIR = RUNTIME_ROOT / "v733_case_analysis_output_risk_events"
CASE_ANALYSIS_IMPROVEMENT_CANDIDATES_DIR = RUNTIME_ROOT / "v734_case_analysis_improvement_candidates"
CASE_ANALYSIS_IMPROVEMENT_TRACES_DIR = RUNTIME_ROOT / "v734_case_analysis_improvement_traces"
CASE_ANALYSIS_IMPROVEMENT_DIFFS_DIR = RUNTIME_ROOT / "v734_case_analysis_improvement_diffs"
TRAINING_DATASETS_DIR = RUNTIME_ROOT / "v735_training_datasets"
TRAINING_GATE_REPORTS_DIR = RUNTIME_ROOT / "v735_training_gate_reports"
CODEX_TRAINING_DRYRUNS_DIR = RUNTIME_ROOT / "v736_codex_training_dryruns"
CODEX_INTERNAL_TRAINING_RUNS_DIR = RUNTIME_ROOT / "v737_codex_internal_training_runs"
TRAINING_MATERIALS_DIR = RUNTIME_ROOT / "v735a_training_materials"
TRAINING_MATERIAL_OCR_JOBS_DIR = RUNTIME_ROOT / "v735a_training_material_ocr_jobs"
TRAINING_MATERIAL_PARSE_JOBS_DIR = RUNTIME_ROOT / "v735a_training_material_parse_jobs"
TRAINING_MATERIAL_JUDGMENT_STRUCTURES_DIR = RUNTIME_ROOT / "v735a_judgment_structures"
TRAINING_MATERIAL_WORK_PRODUCT_STRUCTURES_DIR = RUNTIME_ROOT / "v735a_work_product_structures"
TRAINING_MATERIAL_EVIDENCE_INDEXES_DIR = RUNTIME_ROOT / "v735a_evidence_indexes"
TRAINING_MATERIAL_LEGAL_RETRIEVAL_JOBS_DIR = RUNTIME_ROOT / "v735a_legal_retrieval_jobs"
TRAINING_MATERIAL_RULE_ALIGNMENTS_DIR = RUNTIME_ROOT / "v735a_rule_alignments"
TRAINING_MATERIAL_PARSE_GATES_DIR = RUNTIME_ROOT / "v735a_parse_quality_gates"
RAW_BASED_EXPERIENCE_CANDIDATES_DIR = RUNTIME_ROOT / "v735b_raw_based_experience_candidates"
REDACTED_EXPERIENCE_PACKAGES_DIR = RUNTIME_ROOT / "v735b_redacted_experience_packages"
CODEX_TRAINING_SKILLS_DIR = RUNTIME_ROOT / "v737_codex_training_skills"
CODEX_SKILL_TRAINING_RUNS_DIR = RUNTIME_ROOT / "v738_codex_skill_training_runs"
EXTERNAL_OCR_PARSE_RUNS_DIR = RUNTIME_ROOT / "v735a_external_ocr_parse_runs"
EXTERNAL_OCR_JOBS_DIR = RUNTIME_ROOT / "v738c_external_ocr_jobs"


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
