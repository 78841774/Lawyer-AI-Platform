from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class PersonalAlphaStatus(BaseModel):
    enabled: bool = True
    mode: str = "personal_local_alpha"
    production_enabled: bool = False
    team_mode_enabled: bool = False
    real_case_processing_enabled: bool = False
    material_content_reading_enabled: bool = False
    ocr_live_enabled: bool = False
    legal_search_live_enabled: bool = False
    llm_live_enabled: bool = False
    deepseek_live_enabled: bool = False
    requires_manual_review: bool = True
    local_only: bool = True
    dry_run_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class RedactionChecklist(BaseModel):
    client_name_removed: bool = False
    id_numbers_removed: bool = False
    phone_numbers_removed: bool = False
    addresses_removed: bool = False
    bank_info_removed: bool = False
    case_number_removed_or_masked: bool = False
    file_names_redacted: bool = False
    material_content_not_committed: bool = True
    api_keys_not_committed: bool = True
    local_only_confirmed: bool = True
    manual_review_required: bool = True


class PersonalCaseManifestPreviewRequest(BaseModel):
    case_id: str = "case_personal_alpha_001"
    workspace_id: str = "workspace_demo_001"
    case_title_redacted: str = "合同纠纷测试样本"
    local_case_root: str | None = "~/Lawyer-AI-Local-Cases/demo_case"
    case_cause_code: str = "payment_dispute"
    jurisdiction: str = "CN"
    dry_run_only: bool = True
    manual_review_confirmed: bool = False


class PersonalCaseManifestPreview(BaseModel):
    manifest_id: str
    case_id: str
    workspace_id: str
    case_title_redacted: str
    case_cause_code: str
    jurisdiction: str
    local_case_root_redacted: str = "<local_case_root_redacted>"
    dry_run_only: bool
    manual_review_confirmed: bool
    allowed_to_continue: bool
    redaction_checklist: RedactionChecklist
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class MaterialInventoryRequest(BaseModel):
    case_id: str = "case_personal_alpha_001"
    workspace_id: str = "workspace_demo_001"
    local_case_root: str | None = "~/Lawyer-AI-Local-Cases/demo_case"
    include_file_names: bool = False
    dry_run_only: bool = True


class MaterialInventoryItem(BaseModel):
    item_id: str
    filename_redacted: str
    extension: str | None = None
    relative_path_redacted: str = "<relative_path_redacted>"
    size_bytes: int | None = None
    content_read: bool = False
    mock_only: bool = True


class MaterialInventoryResult(BaseModel):
    inventory_id: str
    case_id: str
    workspace_id: str
    local_case_root_redacted: str = "<local_case_root_redacted>"
    item_count: int
    items: list[MaterialInventoryItem]
    content_read: bool = False
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class PersonalAlphaDryRunRequest(BaseModel):
    case_id: str = "case_personal_alpha_001"
    workspace_id: str = "workspace_demo_001"
    local_case_root: str | None = "~/Lawyer-AI-Local-Cases/demo_case"
    case_cause_code: str = "payment_dispute"
    jurisdiction: str = "CN"
    provider_mode: str = "mock"
    ocr_mode: str = "mock"
    legal_search_mode: str = "mock"
    llm_mode: str = "mock"
    dry_run_only: bool = True
    manual_review_confirmed: bool = False


class PersonalAlphaDryRunResult(BaseModel):
    personal_alpha_dry_run_id: str
    manifest_preview: dict[str, Any]
    material_inventory: dict[str, Any]
    internal_alpha_dry_run_result: dict[str, Any]
    local_sandbox_dry_run_result: dict[str, Any]
    mock_ocr_preview: dict[str, Any]
    mock_legal_search_preview: dict[str, Any]
    mock_source_trace_preview: dict[str, Any]
    mock_report_draft_preview: dict[str, Any]
    allowed_to_continue: bool
    manual_review_required: bool
    audit_log_id: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class PersonalAlphaAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    personal_alpha_dry_run_id: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str
