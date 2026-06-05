from personal_showcase_pack.schemas import ShowcaseRuntime, ShowcaseRuntimeList


RUNTIME_DEFINITIONS = [
    {
        "runtime_id": "showcase_pack_runtime",
        "display_name": "展示包 Runtime",
        "runtime_type": "showcase_pack_runtime",
        "capabilities": ["组织试点展示数据", "汇总产品流程状态", "生成 mock showcase summary", "不触发真实交付"],
    },
    {
        "runtime_id": "pilot_sample_runtime",
        "display_name": "试点样本 Runtime",
        "runtime_type": "pilot_sample_runtime",
        "capabilities": ["创建低风险 mock pilot sample", "记录样本流程状态", "显示 readiness / review / lock metadata"],
    },
    {
        "runtime_id": "story_flow_runtime",
        "display_name": "故事流程 Runtime",
        "runtime_type": "story_flow_runtime",
        "capabilities": ["组织演示故事线", "关联 v7.3-v7.6 mock runtime metadata", "显示从案件到交付包的受控流程"],
    },
    {
        "runtime_id": "showcase_metrics_runtime",
        "display_name": "展示指标 Runtime",
        "runtime_type": "showcase_metrics_runtime",
        "capabilities": ["统计 mock sample 数", "统计 source trace 覆盖率", "统计 review gate 状态", "统计 final lock 状态"],
    },
    {
        "runtime_id": "trust_panel_runtime",
        "display_name": "安全与信任面板 Runtime",
        "runtime_type": "trust_panel_runtime",
        "capabilities": ["汇总安全边界", "显示未调用真实 provider", "显示不生成最终意见/报告/交付"],
    },
]


def list_runtimes() -> dict:
    runtimes = [ShowcaseRuntime(**definition) for definition in RUNTIME_DEFINITIONS]
    return ShowcaseRuntimeList(
        runtimes=runtimes,
        runtime_count=len(runtimes),
        live_runtime_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        warnings=["所有 v7.7 runtime 均为 mock metadata runtime，live provider disabled。"],
    ).model_dump()


def get_runtime(runtime_id: str) -> ShowcaseRuntime | None:
    for runtime in RUNTIME_DEFINITIONS:
        if runtime["runtime_id"] == runtime_id:
            return ShowcaseRuntime(**runtime)
    return None
