from personal_trial_readiness.schemas import SafetyConfirmation
from personal_trial_readiness.storage import read_json, write_json


def build_safety_confirmation(trial_id: str = "trial_mock_001") -> SafetyConfirmation:
    data = read_json("safety_confirmations", trial_id)
    if data:
        return SafetyConfirmation(**data)
    return SafetyConfirmation(
        trial_id=trial_id,
        warnings=["安全确认仅记录 metadata，不读取密钥、案件原始内容或 raw OCR。"],
    )


def create_mock_safety_confirmation(trial_id: str) -> dict:
    confirmation = build_safety_confirmation(trial_id)
    write_json("safety_confirmations", trial_id, confirmation.model_dump())
    return confirmation.model_dump()
