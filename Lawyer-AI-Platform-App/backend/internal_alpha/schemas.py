from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class InternalAlphaSubsystemStatus(BaseModel):
    name: str
    enabled: bool
    status: str
    mock_only: bool = True
    notes: str


class DeploymentReadinessItem(BaseModel):
    item_id: str
    label: str
    status: str
    required: bool
    passed: bool
    notes: str


class InternalAlphaReadinessChecklist(BaseModel):
    items: list[DeploymentReadinessItem]
    required_passed: bool
    manual_verification_required: bool
    warnings: list[str] = Field(default_factory=list)


class SecretManagementChecklist(BaseModel):
    env_file_not_committed: bool
    api_key_not_committed: bool
    jwt_secret_not_default_for_production: bool
    deepseek_key_not_committed: bool
    ocr_legal_search_keys_not_committed: bool
    external_secret_management_required_for_production: bool
    notes: list[str] = Field(default_factory=list)


class DatabaseReadinessStatus(BaseModel):
    sqlite_local_ready: bool
    local_db_ignored: bool
    database_url_supported: bool
    postgresql_ready: bool
    alembic_ready: bool
    production_migration_out_of_scope: bool = True
    notes: list[str] = Field(default_factory=list)


class InternalAlphaStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_internal_alpha"
    production_enabled: bool = False
    team_mode_enabled: bool = False
    real_case_processing_enabled: bool = False
    workspace_runtime_auto_enable: bool = False
    skill_aware_case_processing_auto_enable: bool = False
    requires_manual_review: bool = True
    local_only: bool = True
    mock_only: bool = True
    warnings: list[str] = Field(default_factory=list)
    subsystems: list[InternalAlphaSubsystemStatus] = Field(default_factory=list)
    readiness: InternalAlphaReadinessChecklist | None = None


class InternalAlphaDryRunRequest(BaseModel):
    case_id: str = "case_demo_alpha_001"
    workspace_id: str = "workspace_demo_001"
    local_case_root: str | None = "~/Lawyer-AI-Local-Cases/demo_case"
    provider_mode: str = "mock"
    ocr_mode: str = "mock"
    legal_search_mode: str = "mock"
    dry_run_only: bool = True
    manual_review_confirmed: bool = False


class InternalAlphaDryRunResult(BaseModel):
    alpha_dry_run_id: str
    local_sandbox_dry_run_result: dict[str, Any]
    readiness_summary: dict[str, Any]
    allowed_to_continue: bool
    manual_review_required: bool
    audit_log_id: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str


class InternalAlphaAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    alpha_dry_run_id: str
    local_sandbox_dry_run_id: str | None = None
    result: str
    warnings: list[str] = Field(default_factory=list)
    created_at: str
