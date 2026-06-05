from personal_ai_gateway.schemas import PersonalAIPromptTemplate, PersonalAIPromptTemplateList


SAFE_INPUT_SCHEMA = {
    "case_id": "optional mock-safe case identifier",
    "case_type": "mock-safe case category",
    "task": "draft task label",
    "source_trace_ids": "optional redacted source trace ids",
}

SAFE_OUTPUT_SCHEMA = {
    "title": "draft output title",
    "content": "mock-safe draft placeholder",
    "source_trace_required": True,
    "requires_lawyer_review": True,
}

TEMPLATE_DEFINITIONS = [
    ("fact_summary_draft", "Fact Summary Draft", "Prepare an AI-assisted draft fact summary for lawyer review.", "general"),
    ("evidence_summary_draft", "Evidence Summary Draft", "Prepare a redacted evidence summary draft with source tracing.", "general"),
    ("issue_spotting_draft", "Issue Spotting Draft", "Identify preliminary legal issues as draft-only review material.", "general"),
    ("legal_analysis_draft", "Legal Analysis Draft", "Prepare a draft legal analysis outline without final legal opinion.", "general"),
    ("report_outline_draft", "Report Outline Draft", "Prepare a draft report structure without generating final report text.", "general"),
    ("risk_warning_draft", "Risk Warning Draft", "Prepare draft risk warnings for lawyer validation.", "general"),
    (
        "experience_package_skill_candidate",
        "Experience Package Skill Candidate",
        "Prepare metadata for a candidate skill package without automatic publishing.",
        "workflow",
    ),
]


def list_prompt_templates() -> dict:
    templates = [_build_template(*definition) for definition in TEMPLATE_DEFINITIONS]
    return PersonalAIPromptTemplateList(
        templates=templates,
        template_count=len(templates),
        enabled_template_count=sum(1 for template in templates if template.enabled),
        warnings=["Prompt templates contain metadata and mock-safe placeholders only. No raw case material is included."],
    ).model_dump()


def get_prompt_template(template_id: str) -> PersonalAIPromptTemplate | None:
    for template in list_prompt_templates()["templates"]:
        if template.get("template_id") == template_id:
            return PersonalAIPromptTemplate(**template)
    return None


def _build_template(template_id: str, name: str, purpose: str, case_type: str) -> PersonalAIPromptTemplate:
    return PersonalAIPromptTemplate(
        template_id=template_id,
        name=name,
        purpose=purpose,
        case_type=case_type,
        input_schema=SAFE_INPUT_SCHEMA,
        output_schema=SAFE_OUTPUT_SCHEMA,
        warnings=[
            "Draft-only template metadata.",
            "No raw material, personal information, or final legal opinion content is embedded.",
        ],
    )
