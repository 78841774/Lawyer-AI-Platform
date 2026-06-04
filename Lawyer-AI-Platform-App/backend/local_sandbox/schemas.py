from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class LocalSandboxStatus(BaseModel):
    enabled: bool = True
    mode: str = "local_only"
    real_case_processing_enabled: bool = False
    live_provider_enabled: bool = False
    deepseek_live_enabled: bool = False
    real_ocr_enabled: bool = False
    real_legal_search_enabled: bool = False
    workspace_runtime_auto_enable: bool = False
    skill_aware_case_processing_auto_enable: bool = False
    requires_manual_review: bool = True
    mock_only: bool = True
    warnings: list[str] = Field(default_factory=list)


class ProviderModeGuard(BaseModel):
    provider_mode: str
    ocr_mode: str = "mock"
    legal_search_mode: str = "mock"
    live_provider_blocked: bool = True
    deepseek_live_blocked: bool = True
    allowed: bool
    warnings: list[str] = Field(default_factory=list)


class MaterialSafetyGuard(BaseModel):
    local_case_root: str | None = None
    local_case_root_redacted: str | None = None
    path_allowed: bool
    content_read: bool = False
    real_material_committed: bool = False
    allowed: bool
    warnings: list[str] = Field(default_factory=list)


class GitSafetyGuard(BaseModel):
    git_status_checked: bool
    forbidden_paths_detected: list[str] = Field(default_factory=list)
    staged_sensitive_files_detected: list[str] = Field(default_factory=list)
    allowed: bool
    warnings: list[str] = Field(default_factory=list)


class LocalSandboxGuardStatus(BaseModel):
    provider_mode_guard: ProviderModeGuard
    material_safety_guard: MaterialSafetyGuard
    git_safety_guard: GitSafetyGuard


class LocalSandboxDryRunRequest(BaseModel):
    case_id: str = "case_demo_001"
    workspace_id: str = "workspace_demo_001"
    local_case_root: str | None = "~/Lawyer-AI-Local-Cases/demo_case"
    provider_mode: str = "mock"
    ocr_mode: str = "mock"
    legal_search_mode: str = "mock"
    dry_run_only: bool = True


class LocalSandboxDryRunResult(BaseModel):
    dry_run_id: str
    case_id: str
    workspace_id: str
    status: str
    allowed_to_continue: bool
    guard_results: dict[str, Any]
    audit_log_id: str
    warnings: list[str] = Field(default_factory=list)
    dry_run_only: bool = True
    created_at: str


class LocalSandboxAuditLog(BaseModel):
    audit_log_id: str
    event_type: str
    case_id: str
    workspace_id: str
    dry_run_id: str
    provider_mode: str
    ocr_mode: str
    legal_search_mode: str
    result: str
    warnings: list[str] = Field(default_factory=list)
    local_case_root_redacted: str = "<local_case_root_redacted>"
    created_at: str
