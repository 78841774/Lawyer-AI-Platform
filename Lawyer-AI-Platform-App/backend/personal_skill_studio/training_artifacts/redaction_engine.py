from personal_skill_studio.training_artifacts.intake_safety_engine import intake_safety_flags
from personal_skill_studio.training_artifacts.schemas import RedactionReport


def build_redaction_report(intake_id: str) -> RedactionReport:
    return RedactionReport(
        redaction_report_id=f"{intake_id}_redaction_report",
        intake_id=intake_id,
        redaction_completed=True,
        redaction_notes=[
            "身份字段以主体类型 metadata 保留。",
            "地区保留为 jurisdiction_context metadata。",
            "年龄与行为能力信息保留为区间化 metadata。",
            "合同类型、标的类型、时间节点和证据类型保留为法律分析 metadata。",
        ],
        safety_status=intake_safety_flags(redaction_completed=True, ready_for_codex_training=False),
    )
