from personal_case_analysis.schemas import CaseAnalysisRuntime, CaseAnalysisRuntimeList


RUNTIME_DEFINITIONS = [
    {
        "runtime_id": "controlled_case_analysis_runtime",
        "display_name": "受控案件分析 Runtime",
        "runtime_type": "case_analysis",
        "stage": "orchestration",
        "warnings": ["未结案件实战分析仅生成 draft metadata，不产生训练数据。"],
    },
    {
        "runtime_id": "fact_analysis_stage",
        "display_name": "Fact Analysis Stage",
        "runtime_type": "fact_analysis",
        "stage": "fact",
        "warnings": ["调用案件事实提炼 Skill metadata，不读取 raw full content。"],
    },
    {
        "runtime_id": "legal_analysis_stage",
        "display_name": "Legal Analysis Stage",
        "runtime_type": "legal_analysis",
        "stage": "legal",
        "warnings": ["法律分析读取结构化事实 draft 和 source trace metadata，不生成最终法律意见。"],
    },
    {
        "runtime_id": "legal_analysis_draft_workbench",
        "display_name": "法律分析草稿工作台",
        "runtime_type": "legal_analysis_draft",
        "stage": "legal_draft_workbench",
        "warnings": [
            "v7.21 基于事实输入 metadata 生成法律分析草稿。",
            "输出仅为 draft metadata，不生成最终法律意见、最终报告或外部交付。",
        ],
    },
    {
        "runtime_id": "case_analysis_review_readiness",
        "display_name": "Review & Readiness Stage",
        "runtime_type": "review_readiness",
        "stage": "review",
        "warnings": ["readiness 仅为状态 metadata，不触发真实交付。"],
    },
]


def list_runtimes() -> dict:
    runtimes = [CaseAnalysisRuntime(**definition) for definition in RUNTIME_DEFINITIONS]
    return CaseAnalysisRuntimeList(
        runtimes=runtimes,
        runtime_count=len(runtimes),
        live_runtime_count=sum(1 for runtime in runtimes if runtime.live_enabled),
        warnings=["v7.16 runtime 全部 mock-first、draft-only、metadata-only。"],
    ).model_dump()


def get_runtime(runtime_id: str) -> CaseAnalysisRuntime | None:
    for definition in RUNTIME_DEFINITIONS:
        if definition["runtime_id"] == runtime_id:
            return CaseAnalysisRuntime(**definition)
    return None
