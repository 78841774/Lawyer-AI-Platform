from personal_provider_readiness.schemas import ProviderSafetyStatus


SAFETY_ITEMS = [
    "只显示 provider 配置与 gate metadata",
    "不读取密钥值",
    "不显示 key prefix / suffix / masked key",
    "不允许前端输入 key",
    "不真实调用 provider",
    "不上传案件材料",
    "dry-run 默认开启",
    "live 默认关闭",
    "人工确认必需",
    "律师复核必需",
    "来源追踪必需",
    "不生成最终法律意见或正式报告",
]


def build_safety_status() -> dict:
    return ProviderSafetyStatus(
        safety_items=SAFETY_ITEMS,
        safety_item_count=len(SAFETY_ITEMS),
        warnings=["v7.26 is readiness-only and does not execute provider calls."],
    ).model_dump()

