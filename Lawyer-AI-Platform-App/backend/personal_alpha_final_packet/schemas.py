from typing import Any

from pydantic import BaseModel, Field


class PersonalAlphaFinalPacketStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only_personal_alpha_final_packet"
    production_enabled: bool = False
    mock_first_enabled: bool = True
    controlled_first_enabled: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    requires_final_gate_approval: bool = True
    requires_manual_review: bool = True
    final_report_generation_enabled: bool = False
    final_legal_opinion_enabled: bool = False
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    runtime_storage_enabled: bool = True
    runtime_storage_path: str = "storage/runtime/personal_alpha_final_packet/packets"
    warnings: list[str] = Field(default_factory=list)


class PersonalAlphaFinalPacketSection(BaseModel):
    section_id: str
    title: str
    status: str = "metadata_ready"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    items: list[dict[str, Any]] = Field(default_factory=list)


class PersonalAlphaFinalPacketSafetyChecklist(BaseModel):
    local_only: bool = True
    mock_first: bool = True
    controlled_first: bool = True
    metadata_only: bool = True
    redacted_only: bool = True
    preview_only: bool = True
    advisory_only: bool = True
    manual_review_required: bool = True
    requires_final_gate_approval: bool = True
    raw_material_text_included: bool = False
    raw_ocr_text_included: bool = False
    raw_legal_search_results_included: bool = False
    raw_quote_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    llm_called: bool = False
    deepseek_live_called: bool = False
    real_ocr_called: bool = False
    real_legal_database_called: bool = False
    auto_skill_publish_enabled: bool = False
    auto_workspace_runtime_enabled: bool = False
    runtime_storage_ignored: bool = True


class PersonalAlphaFinalPacketPreview(BaseModel):
    workspace_run_id: str
    status: str
    packet_preview: dict[str, Any] = Field(default_factory=dict)
    can_create_packet: bool = False
    requires_final_gate_approval: bool = True
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalPacketCreateRequest(BaseModel):
    reviewer_id: str = "local_demo_reviewer"
    manual_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False


class PersonalAlphaFinalPacketCreateResult(BaseModel):
    packet_id: str = ""
    workspace_run_id: str
    status: str = "blocked"
    can_proceed_to_controlled_final_review: bool = False
    packet: dict[str, Any] = Field(default_factory=dict)
    reviewer_id: str = "local_demo_reviewer"
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    manual_review_confirmed: bool = False
    metadata_only_confirmation: bool = False
    no_final_legal_opinion_confirmation: bool = False
    no_final_report_generation_confirmation: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalPacketRecord(BaseModel):
    packet_id: str
    workspace_run_id: str
    status: str = "packet_created"
    can_proceed_to_controlled_final_review: bool = True
    packet: dict[str, Any] = Field(default_factory=dict)
    reviewer_id: str = "local_demo_reviewer"
    safety_checklist: dict[str, Any] = Field(default_factory=dict)
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    final_legal_opinion_generated: bool = False
    final_report_generated: bool = False
    manual_review_confirmed: bool = True
    metadata_only_confirmation: bool = True
    no_final_legal_opinion_confirmation: bool = True
    no_final_report_generation_confirmation: bool = True
    warnings: list[str] = Field(default_factory=list)
    created_at: str = ""


class PersonalAlphaFinalPacketList(BaseModel):
    packets: list[dict[str, Any]] = Field(default_factory=list)
    packet_count: int = 0
    mock_or_redacted_only: bool = True
    raw_content_included: bool = False
    warnings: list[str] = Field(default_factory=list)
