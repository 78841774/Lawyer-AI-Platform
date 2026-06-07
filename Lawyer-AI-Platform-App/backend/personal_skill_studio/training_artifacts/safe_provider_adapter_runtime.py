"""Safe provider adapter runtime.

This adapter checks credential presence and calls providers through backend-only code.
It must never return API key values, Authorization headers, raw provider responses,
OCR full text, raw case materials, or local absolute paths.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

from .provider_env_aliases import ENTERPRISE_PROVIDER, LEGAL_PROVIDER, OCR_PROVIDER, ProviderCredentialAlias


@dataclass
class ProviderCredentialStatus:
    provider_type: str
    credential_alias: str
    credential_loaded: bool
    provider_configured: bool
    provider_call_allowed: bool
    last_check_status: str
    redacted_error_summary: str | None = None


def _env_flag_enabled(alias: str | None) -> bool:
    if not alias:
        return False
    return os.getenv(alias, "").strip().lower() in {"1", "true", "yes", "on"}


def check_provider_credential(
    *,
    provider_type: str,
    credential_alias: str,
    enabled_flag_alias: str | None = None,
) -> ProviderCredentialStatus:
    """Return credential status without exposing the credential value."""
    provider_calls_enabled = _env_flag_enabled("PROVIDER_CALLS_ENABLED")
    provider_enabled = _env_flag_enabled(enabled_flag_alias)
    credential_loaded = bool(os.getenv(credential_alias))
    public_alias = _public_credential_alias(credential_alias)

    provider_call_allowed = provider_calls_enabled and provider_enabled and credential_loaded

    if provider_call_allowed:
        status = "credential_loaded"
        error = None
    elif not provider_calls_enabled:
        status = "provider_calls_disabled"
        error = "Provider calls are disabled by PROVIDER_CALLS_ENABLED."
    elif not provider_enabled:
        status = "provider_disabled"
        error = f"Provider is disabled by feature flag {enabled_flag_alias}."
    elif not credential_loaded:
        status = "credential_missing"
        error = f"Credential alias {public_alias} is not loaded."
    else:
        status = "blocked"
        error = "Provider call blocked by safety gate."

    return ProviderCredentialStatus(
        provider_type=provider_type,
        credential_alias=public_alias,
        credential_loaded=credential_loaded,
        provider_configured=provider_enabled,
        provider_call_allowed=provider_call_allowed,
        last_check_status=status,
        redacted_error_summary=error,
    )


def redact_provider_error(exc: Exception) -> str:
    """Return a safe error message without secrets or provider raw payload."""
    name = exc.__class__.__name__
    return f"Provider call failed with {name}. Raw response and credentials were not exposed."


def safe_provider_status_dict(status: ProviderCredentialStatus) -> dict[str, Any]:
    return {
        "provider_type": status.provider_type,
        "credential_alias": status.credential_alias,
        "credential_loaded": status.credential_loaded,
        "provider_configured": status.provider_configured,
        "provider_call_allowed": status.provider_call_allowed,
        "last_check_status": status.last_check_status,
        "redacted_error_summary": status.redacted_error_summary,
    }


def provider_specs_with_loaded_state() -> list[dict[str, Any]]:
    return [_provider_status(alias) for alias in _provider_aliases()]


def list_provider_adapters() -> dict[str, Any]:
    return {"provider_adapters": provider_specs_with_loaded_state()}


def provider_adapter_status(provider_type: str) -> dict[str, Any] | None:
    normalized = str(provider_type or "").strip()
    for status in provider_specs_with_loaded_state():
        if status["provider_type"] == normalized:
            return status
    return None


def call_provider_placeholder(provider_type: str, method_name: str | None = None) -> dict[str, Any] | None:
    status = provider_adapter_status(provider_type)
    if status is None:
        return None
    return {
        **status,
        "method_name": _safe_method_name(method_name),
        "last_check_status": "provider_call_placeholder_blocked",
        "redacted_error_summary": "Live provider call was not executed. Only credential readiness metadata was returned.",
        "live_call_executed": False,
        "credential_value_returned": False,
    }


def _provider_aliases() -> list[ProviderCredentialAlias]:
    return [
        ProviderCredentialAlias(
            provider_type="OCR_API",
            credential_alias=OCR_PROVIDER.credential_alias,
            enabled_flag_alias=OCR_PROVIDER.enabled_flag_alias,
        ),
        ProviderCredentialAlias(
            provider_type="Legal_API",
            credential_alias=LEGAL_PROVIDER.credential_alias,
            enabled_flag_alias=LEGAL_PROVIDER.enabled_flag_alias,
        ),
        ProviderCredentialAlias(
            provider_type="Enterprise_API",
            credential_alias=ENTERPRISE_PROVIDER.credential_alias,
            enabled_flag_alias=ENTERPRISE_PROVIDER.enabled_flag_alias,
        ),
    ]


def _provider_status(alias: ProviderCredentialAlias) -> dict[str, Any]:
    status = check_provider_credential(
        provider_type=alias.provider_type,
        credential_alias=alias.credential_alias,
        enabled_flag_alias=alias.enabled_flag_alias,
    )
    return {
        **safe_provider_status_dict(status),
        "value_stored_in_skill": False,
    }


def _public_credential_alias(alias: str) -> str:
    text = str(alias or "PROVIDER_CREDENTIAL")
    for marker in ("API_KEY", "ACCESS_KEY", "SECRET_KEY", "TOKEN", "KEY"):
        text = text.replace(marker, "CREDENTIAL")
    return text


def _safe_method_name(method_name: str | None) -> str:
    text = str(method_name or "provider_call_placeholder").strip()
    safe = "".join(ch if ch.isalnum() or ch in "-_." else "_" for ch in text)
    return safe[:96] or "provider_call_placeholder"
