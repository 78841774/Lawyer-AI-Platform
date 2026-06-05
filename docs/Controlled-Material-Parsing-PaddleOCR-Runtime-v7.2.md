# Controlled Material Parsing & PaddleOCR Runtime v7.2

## Objective

v7.2 adds a controlled Material Parsing and PaddleOCR Runtime foundation for personal production validation. It prepares mock-first material parser and OCR metadata workflows without reading real files or calling live providers.

## Relationship to v7.1

v7.1 introduced the AI Provider Gateway and Prompt Runtime. v7.2 does not send OCR results into the AI Gateway. It only creates source-trace-ready metadata that may become eligible after lawyer review in a later controlled workflow.

## Material Parsing Runtime

The material parsing runtime supports mock job metadata for:

- `pdf_text_extract_preview`
- `pdf_to_images_preview`
- `docx_structure_preview`
- `excel_table_preview`
- `image_metadata_preview`
- `archive_listing_preview`

Jobs require manual approval, mock-data-only confirmation, no raw-content confirmation, and no external-upload confirmation.

## Provider Placeholders

v7.2 registers:

- MinerU File Parser placeholder.
- Docling File Parser placeholder.
- PaddleOCR / Baidu AI Studio placeholder.

All providers are metadata-only, not configured, not live, and do not expose provider secrets.

## Parse Job Mock Workflow

`POST /personal-material-runtime/parse-jobs/mock` creates mock parse metadata only after confirmations are complete.

The workflow:

- Does not read real files.
- Does not call MinerU or Docling.
- Does not upload externally.
- Does not return source document text.
- Creates source trace metadata.
- Writes audit metadata under ignored runtime storage.

## OCR Job Mock Workflow

`POST /personal-material-runtime/ocr-jobs/mock` creates mock OCR job metadata only after required confirmations are complete.

The workflow:

- Does not call PaddleOCR.
- Does not read real images or PDFs.
- Does not expose recognized source text.
- Returns controlled preview metadata.
- Requires lawyer review.
- Requires source trace metadata.

## OCR Preview

`GET /personal-material-runtime/ocr-jobs/{ocr_job_id}/preview` returns metadata including page count, block count, confidence, table detection, layout detection, key information detection, and safe placeholder block types.

The preview keeps:

- `controlled_preview_only=true`
- `raw_ocr_text_exposed=false`
- `requires_lawyer_review=true`
- `source_trace_required=true`
- `used_in_ai_prompt=false`
- `used_in_final_output=false`

## OCR Review Queue

The OCR review queue tracks pending and reviewed OCR job metadata.

Supported mock actions:

- `approve_preview_for_analysis`
- `request_manual_correction`
- `reject_ocr_preview`
- `mark_low_confidence`

Review actions require manual review confirmation, no source text exposure confirmation, and lawyer-review confirmation. Approval can mark metadata as eligible after review, but it does not send content into AI prompts automatically.

## Source Trace

Material parse and OCR jobs create source trace metadata:

- source trace id
- case id
- material id
- job id
- source type
- provider id
- mock page number
- mock block id
- redacted bbox metadata
- confidence
- review status

Source traces do not include recognized text, real filenames, local paths, provider secrets, or final-output usage.

## Audit Metadata

Audit metadata is written under ignored runtime storage:

`Lawyer-AI-Platform-App/backend/storage/runtime/personal_material_runtime/audit/`

Audit APIs return metadata only and do not expose provider secrets, source document text, recognized source text, local paths, or provider responses.

## Safety Checklist

`GET /personal-material-runtime/safety` returns:

- mock-first enabled
- live provider disabled by default
- provider secret hidden
- manual approval required
- lawyer review required
- controlled OCR preview
- no uncontrolled raw content exposure
- source trace required
- audit log enabled
- no final legal opinion
- no final report
- no external delivery

## Personal Production Integration

The Personal Production Console now shows:

- Material Parsing Runtime registered.
- OCR Runtime registered.
- MinerU / Docling placeholders.
- PaddleOCR placeholder.
- `target_route=/personal-material-runtime`
- `live_runtime_count=0`
- real provider calls disabled.

## AI Gateway Integration Boundary

v7.2 does not call the AI Gateway, render real prompts, or send OCR output into AI prompts.

Metadata includes `used_in_ai_prompt=false`, `used_in_final_output=false`, and `eligible_for_ai_prompt_after_review` for future controlled workflows.

## Regression Updates

The regression suite adds `scripts/regression/check_personal_material_runtime_apis.sh` and includes it after the v7.1 AI Gateway API checks.

The script checks status, providers, parse jobs, OCR jobs, OCR preview, review queue, source traces, audit, safety, safe flags, and sensitive-string absence.

## No Live OCR Call

v7.2 does not call PaddleOCR, MinerU, Docling, or Baidu AI Studio.

## No Raw OCR Exposure

v7.2 returns controlled preview metadata only and does not expose recognized source text.

## No Final Legal Opinion

v7.2 does not generate final legal opinions.

## No Final Report

v7.2 does not generate final reports and does not enable external delivery.

## v7.3 Readiness

The next stage is Legal & Enterprise Intelligence Gateway:

- Kuaicha 365 LawSkills API placeholder.
- Tianyancha AI placeholder.
- Legal search query metadata.
- Enterprise information verification metadata.
- Citation and source trace metadata.
- Lawyer confirmation required.
- No automatic legal conclusion.
- No final legal opinion.
- No final report.
