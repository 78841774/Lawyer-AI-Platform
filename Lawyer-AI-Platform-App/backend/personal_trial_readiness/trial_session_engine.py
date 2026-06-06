from datetime import datetime, timezone
from uuid import uuid4

from personal_trial_readiness.schemas import TrialSession, TrialSessionList, TrialSessionMockRequest
from personal_trial_readiness.storage import list_json, read_json, write_json


ALLOWED_CASE_MODES = {"synthetic_case", "low_risk_real_case", "owner_internal_case"}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def default_trial() -> TrialSession:
    return TrialSession(
        trial_id="trial_mock_001",
        trial_name="个人版实战试运行样本",
        case_mode="synthetic_case",
        owner_user_id="local_owner",
        case_reference_label="合成试运行样本",
        trial_status="planned",
        started_at=now_iso(),
        warnings=["仅记录试运行 metadata，不读取案件原始内容，不调用真实 provider。"],
    )


def create_mock_trial(request: TrialSessionMockRequest) -> dict:
    case_mode = request.case_mode if request.case_mode in ALLOWED_CASE_MODES else "synthetic_case"
    trial = TrialSession(
        trial_id=f"trial_{uuid4().hex[:10]}",
        trial_name=request.trial_name,
        case_mode=case_mode,
        owner_user_id=request.owner_user_id,
        case_reference_label=request.case_reference_label,
        trial_status="in_progress",
        started_at=now_iso(),
        warnings=[
            "试运行记录仅为 owner-only metadata。",
            "不会读取案件原始内容、调用真实 provider、训练未结案件或自动对外交付。",
        ],
    )
    write_json("trials", trial.trial_id, trial.model_dump())
    return trial.model_dump()


def list_trials() -> dict:
    records = [TrialSession(**item) for item in list_json("trials")]
    if not records:
        records = [default_trial()]
    return TrialSessionList(trials=records, trial_count=len(records)).model_dump()


def get_trial(trial_id: str) -> TrialSession | None:
    if trial_id == "trial_mock_001":
        return default_trial()
    data = read_json("trials", trial_id)
    return TrialSession(**data) if data else None
