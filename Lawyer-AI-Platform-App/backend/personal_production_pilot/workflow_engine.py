from personal_production_pilot.schemas import PilotWorkflow, PilotWorkflowStep


WORKFLOW_STEPS = [
    ("materials_ocr", "材料与 OCR", "ocr_document_provider_live_gateway", "materials"),
    ("controlled_ai_analysis", "AI 受控分析", "ai_provider_live_gateway", "ai"),
    ("legal_enterprise_lookup", "法律/企业信息检索", "legal_enterprise_api_live_gateway", "intelligence"),
    ("skill_invocation", "Skill 调用", "skill_training_runtime", "skill"),
    ("fact_preview_correction", "事实预览与纠正", "controlled_case_analysis_runtime", "fact"),
    ("legal_analysis_draft", "法律分析草稿", "controlled_case_analysis_runtime", "legal"),
    ("delivery_packet_draft", "交付包草稿", "personal_delivery_packet_runtime", "delivery"),
    ("owner_download", "用户本人下载", "owner_download_runtime", "download"),
]


def build_workflow() -> dict:
    steps = [
        PilotWorkflowStep(
            step_id=step_id,
            display_name=display_name,
            target_runtime_id=runtime_id,
            stage=stage,
            warnings=["Step is gated and metadata-only; it does not auto-deliver, email, publish, or final-label output."],
        )
        for step_id, display_name, runtime_id, stage in WORKFLOW_STEPS
    ]
    return PilotWorkflow(steps=steps, step_count=len(steps), warnings=["v7.17 pilot workflow is owner-only and provider-gated."]).model_dump()
