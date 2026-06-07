# Codex Instruction: Safe External OCR / Legal / Enterprise Provider Integration

Task:
Connect external OCR, legal retrieval, and enterprise lookup providers safely.

Use only the uploaded interface document for endpoint/model/parameter names.
Do not copy key/token values from the document.

Requirements:

1. Do not read or print `.env`.
2. Do not store real keys in code, Skill, docs, frontend, regression, logs, or training artifacts.
3. Use only credential aliases:
   - OCR_PROVIDER_API_KEY
   - FAZHI_LAW_API_KEY
   - TIANYAN_AI_API_KEY
4. Implement backend adapter / provider-gated loader.
5. Adapter may return:
   - provider_type
   - credential_alias
   - credential_loaded
   - provider_configured
   - provider_call_allowed
   - last_check_status
   - redacted_error_summary
6. Adapter must not return:
   - key value
   - Authorization header
   - provider raw response
   - OCR full text
   - local absolute path
   - raw case material
7. If external OCR is not successful, set:
   - ocr_mode = external_ocr_failed
   - external_ocr_completed = false
   - real_material_training_allowed = false
   - training_status = blocked_for_external_ocr
8. If external OCR succeeds, only expose:
   - per_file_parse_summary_redacted
   - parse_quality_report
   - audit
   - source_trace

Validation:
- run backend compileall
- run training provider regression
- run no-secret/raw-material checks
- run git diff --check
