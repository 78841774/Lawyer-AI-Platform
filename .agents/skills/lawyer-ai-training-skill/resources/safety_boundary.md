# Safety Boundary

Training workflow outputs must be metadata-safe.

## Forbidden Output Classes

The following must not appear as returned content, stored values, logs, frontend display, regression stdout, or training artifacts:

- raw_text
- ocr_text
- original_text
- full_document_text
- raw_material
- raw_case_material
- local_path
- file_path
- absolute_path
- api_key
- secret
- private_key
- access_token
- refresh_token
- provider_response
- provider_raw_response
- unredacted

## Required Flags

- metadata_only=true
- redacted_output_only=true
- abstracted_output_only=true
- source_trace_required=true
- audit_required=true
- provider_call_executed=false by default
- key_value_read=false
- credential_value_returned=false
- source_content_returned=false
- skill_published=false
- runtime_package_replaced=false
- final_legal_opinion_generated=false
- final_report_generated=false
- public_link_created=false
- email_sent=false
- external_delivery_triggered=false

## Review Boundary

Lawyer review is required before any future practice runtime load candidate may be considered. Review metadata must not itself publish Skills or replace runtime packages.
