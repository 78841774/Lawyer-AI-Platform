from personal_delivery_packet.schemas import DeliveryPacketRuntime, DeliveryPacketRuntimeList


RUNTIME_DEFINITIONS = [
    {
        "runtime_id": "delivery_packet_runtime",
        "display_name": "交付包草案 Runtime",
        "runtime_type": "delivery_packet_runtime",
        "capabilities": ["创建交付包草案", "汇总生产案件 metadata", "标记律师复核状态", "标记最终锁定状态"],
    },
    {
        "runtime_id": "packet_item_runtime",
        "display_name": "交付项清单 Runtime",
        "runtime_type": "packet_item_runtime",
        "capabilities": ["生成交付项 metadata", "记录材料、草稿、来源追踪、复核状态", "标记是否可纳入交付包"],
    },
    {
        "runtime_id": "source_bundle_runtime",
        "display_name": "来源追踪包 Runtime",
        "runtime_type": "source_bundle_runtime",
        "capabilities": ["聚合 source trace metadata", "标记引用确认状态", "保留 raw content excluded 标志"],
    },
    {
        "runtime_id": "export_readiness_engine",
        "display_name": "导出准备度引擎",
        "runtime_type": "export_readiness_engine",
        "capabilities": ["检查交付包是否可导出", "检查律师复核", "检查最终锁定", "检查禁止自动交付"],
    },
    {
        "runtime_id": "final_lock_engine",
        "display_name": "最终锁定引擎",
        "runtime_type": "final_lock_engine",
        "capabilities": ["记录人工最终锁定动作", "锁定后禁止继续修改 metadata", "不触发外部发送"],
    },
]


def list_runtimes() -> dict:
    runtimes = [DeliveryPacketRuntime(**definition) for definition in RUNTIME_DEFINITIONS]
    return DeliveryPacketRuntimeList(
        runtimes=runtimes,
        runtime_count=len(runtimes),
        live_runtime_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        warnings=["Personal Delivery Packet Runtime 仅生成草案和受控导出 metadata。"],
    ).model_dump()


def get_runtime(runtime_id: str) -> DeliveryPacketRuntime | None:
    for runtime in list_runtimes()["runtimes"]:
        if runtime.get("runtime_id") == runtime_id:
            return DeliveryPacketRuntime(**runtime)
    return None
