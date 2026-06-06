# Provider Adapter Contract

Training-related Skill metadata may describe provider access, but it must not contain provider secrets.

## Allowed Fields

- provider_type
- credential_alias
- credential_loaded
- gate_requirements
- adapter_status
- provider_call_allowed

## Required Provider Types

- OCR_API
- Legal_API
- Enterprise_API

## Rules

- credential_alias is the environment variable name or secret alias only.
- credential_loaded is a boolean confirmed by backend adapter or provider-gated loader.
- gate_requirements must include credential_loaded=true before a provider-backed operation is eligible.
- provider_call_allowed remains false unless a target version explicitly enables a controlled live path.
- Dry-run and metadata inspection must not call providers.
- Adapter responses must never return key values, token values, provider raw response payloads, source material text, OCR full text, or local filesystem paths.
