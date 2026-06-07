# External OCR / Legal / Enterprise Provider Setup

This document describes how to connect external OCR, legal retrieval, and enterprise lookup providers safely.

## Source document summary

The uploaded interface document describes:

- PaddleOCR AIStudio OCR job endpoint.
- PaddleOCR model name: `PaddleOCR-VL-1.6`.
- Optional OCR payload flags:
  - `useDocOrientationClassify`
  - `useDocUnwarping`
  - `useChartRecognition`
- Legal retrieval through `law-search` with `FAZHI_LAW_API_KEY`.
- Tianyan AI enterprise provider integration.

The uploaded document also contains real key/token-like values. Those values are intentionally **not copied** here.

## Required security rule

Real provider keys must only be stored in backend `.env`, system environment variables, or a secret manager.

Never write real key values into:

- Codex Skill
- `SKILL.md`
- source code
- frontend
- docs
- regression scripts
- logs
- training artifacts
- experience packages
- Git-tracked files

## Local setup

Create or edit:

```bash
Lawyer-AI-Platform-App/backend/.env
```

Add real values manually:

```bash
OCR_PROVIDER_API_KEY=...
FAZHI_LAW_API_KEY=...
TIANYAN_AI_API_KEY=...
PROVIDER_CALLS_ENABLED=true
EXTERNAL_OCR_ENABLED=true
LEGAL_RETRIEVAL_ENABLED=true
ENTERPRISE_LOOKUP_ENABLED=true
```

Do not let Codex open or print `.env`.

## Runtime contract

Training Skill and API responses may expose only:

- `provider_type`
- `credential_alias`
- `credential_loaded`
- `provider_configured`
- `last_check_status`
- `redacted_error_summary`

They must never expose:

- API key value
- token value
- authorization header
- provider raw response
- OCR full text
- local absolute path
- raw case material

## External OCR readiness states

Use these explicit states:

```text
ocr_mode:
- mock_metadata
- local_text_parse
- external_ocr
- external_ocr_failed

training_status:
- mock_chain_verified
- blocked_for_external_ocr
- blocked_for_parse_quality
- ready_for_real_material_training
- real_material_training_completed
```

A real-material training run is allowed only when:

```text
external_ocr_completed = true
document_content_parsed = true
per_file_parse_summary_available = true
parse_quality_passed = true
redacted_summary_available = true
source_trace_complete = true
audit_complete = true
raw_content_not_exported = true
```
