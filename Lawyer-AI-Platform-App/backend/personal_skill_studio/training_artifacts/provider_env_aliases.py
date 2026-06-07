"""Provider environment aliases for safe external provider access.

This file intentionally contains only environment variable names / aliases.
Do not add real key values here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCredentialAlias:
    provider_type: str
    credential_alias: str
    base_url_alias: str | None = None
    enabled_flag_alias: str | None = None


OCR_PROVIDER = ProviderCredentialAlias(
    provider_type="external_ocr",
    credential_alias="OCR_PROVIDER_API_KEY",
    base_url_alias="OCR_PROVIDER_JOB_URL",
    enabled_flag_alias="EXTERNAL_OCR_ENABLED",
)

LEGAL_PROVIDER = ProviderCredentialAlias(
    provider_type="external_legal_retrieval",
    credential_alias="FAZHI_LAW_API_KEY",
    base_url_alias=None,
    enabled_flag_alias="LEGAL_RETRIEVAL_ENABLED",
)

ENTERPRISE_PROVIDER = ProviderCredentialAlias(
    provider_type="external_enterprise_lookup",
    credential_alias="TIANYAN_AI_API_KEY",
    base_url_alias=None,
    enabled_flag_alias="ENTERPRISE_LOOKUP_ENABLED",
)
