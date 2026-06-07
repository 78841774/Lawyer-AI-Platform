# Codex Instructions: External Provider Safe Calls

Use these instructions when connecting external OCR, legal retrieval, or enterprise lookup.

## Mandatory rule

Do not read, print, copy, summarize, or store real API keys.

Do not open `.env`.
Do not extract key/token values from uploaded interface documents.
If a document contains key-like values, use only endpoint names, parameter names, model names, and response structure.

## Provider alias contract

Use aliases only:

```text
OCR_PROVIDER_API_KEY
FAZHI_LAW_API_KEY
TIANYAN_AI_API_KEY
```

## Safe adapter workflow

1. Check feature flag.
2. Check `credential_loaded`.
3. Call provider only through backend adapter.
4. Store provider raw response only in ignored runtime if needed.
5. Return only redacted summaries, status, audit, and source trace.
6. Never return OCR full text to frontend or training artifacts.

## Required output for OCR

For every file, return:

```json
{
  "file_ref": "redacted_file_ref",
  "ocr_mode": "external_ocr",
  "parse_status": "completed|failed",
  "external_ocr_completed": true,
  "document_content_parsed": true,
  "per_file_parse_summary_available": true,
  "redacted_summary": "...",
  "quality_score": 0.0,
  "source_trace_id": "...",
  "audit_id": "..."
}
```

If external OCR fails:

```json
{
  "ocr_mode": "external_ocr_failed",
  "external_ocr_completed": false,
  "real_material_training_allowed": false,
  "training_status": "blocked_for_external_ocr",
  "redacted_error_summary": "External OCR failed. Real material training was not executed."
}
```
