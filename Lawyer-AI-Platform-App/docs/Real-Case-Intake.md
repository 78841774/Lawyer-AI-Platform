# Real Case Intake

AIHome.law v3.4 introduces a small real-case intake foundation for internal alpha use.

## v3.4-A Case Intake

The Create Case page collects the following fields:

* `title`
* `client_name`
* `counterparty_name`
* `case_type`
* `contract_type`
* `dispute_amount`
* `jurisdiction`
* `objective`
* `intake_notes`

Only `title` is required. Existing title-only `POST /cases` requests remain compatible.

## v3.4-B Folder-Aware Material Intake

The material intake flow supports both single-file upload and folder upload.

When a browser supports `webkitdirectory`, the frontend reads each file's `webkitRelativePath` and sends it to the backend as `relative_path`.

The backend stores:

* `original_filename`
* `relative_path`
* `folder_path`
* `file_ext`
* `upload_batch_id`
* `display_order`

Old material rows remain compatible:

* `original_filename` falls back to `filename`.
* `relative_path` falls back to `filename`.
* `folder_path` falls back to an empty string.
* `display_order` falls back to `0`.

The actual file is stored under:

```text
storage_root/original-files/{case_id}/{upload_batch_id}/
```

The saved `relative_path` is cleaned to prevent path traversal. Directory names are retained for legal context, but paths such as `../` are not allowed to escape the storage root.

## Material Context for Fact Extraction

Fact extraction context now includes:

* `material_id`
* `filename`
* `original_filename`
* `relative_path`
* `folder_path`
* `material_type`

This lets the mock or future LLM runtime use directory and filename context when identifying evidence meaning.

## Current Limits

This phase does not add:

* Complex OCR.
* PDF content parsing.
* Zip automatic extraction.
* Formal legal review.
* Team approval workflows.
* Skill Training main-chain changes.

Use only sanitized materials in local testing.

## v3.4-C E2E Validation

v3.4-C adds an end-to-end local validation path:

```text
Intake -> Folder Materials -> Intake Status -> Facts -> Analysis -> Report
```

The backend exposes:

```text
GET /cases/{case_id}/intake/status
```

The status response includes counts and next-step flags:

* `materials_count`
* `facts_count`
* `analyses_count`
* `reports_count`
* `ready_for_fact_extraction`
* `ready_for_analysis`
* `ready_for_report`
* `next_recommended_action`

Recommended actions:

* `upload_material`
* `extract_facts`
* `run_analysis`
* `generate_report`
* `review_report`

The local validation script is:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
python scripts/validate_real_case_intake_v3_4.py
```

The script uses temporary sanitized text files and does not write test material files into the repository.
