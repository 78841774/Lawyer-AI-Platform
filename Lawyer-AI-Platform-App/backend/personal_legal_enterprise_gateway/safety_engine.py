from personal_legal_enterprise_gateway.schemas import SafetyStatus


SAFETY_ITEMS = [
    "法律 / 企业接口 provider-gated",
    "live disabled by default",
    "dry-run default",
    "key value 不读取、不显示、不记录",
    "法律检索结果不自动作为最终引用",
    "企业信息不自动作为最终事实认定",
    "结果必须进入 source trace",
    "结果必须进入律师复核",
    "不训练未结案件",
    "不更新或发布 Skill",
    "不生成最终法律意见或正式报告",
    "不自动外部交付",
]


def build_safety_status() -> dict:
    return SafetyStatus(safety_items=SAFETY_ITEMS, safety_item_count=len(SAFETY_ITEMS)).model_dump()

