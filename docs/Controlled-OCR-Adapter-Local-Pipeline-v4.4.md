# Controlled OCR Adapter Local Pipeline v4.4

## Goal

v4.4 adds a controlled local OCR preview pipeline on top of v4.3 Controlled Local Material Read Implementation.

This stage remains local-only and is not production. It defaults to mock OCR, does not call a real OCR provider, does not call an LLM, does not call DeepSeek live, does not query a real legal database, and does not generate a final legal opinion.

## Relationship To v4.3

v4.3 introduced controlled local text read preview for `.txt`, `.md`, and `.json`.

v4.4 adds a separate `controlled_ocr_pipeline` module for OCR preview. It does not replace or modify the existing v3.7 `ocr_adapter`, and it does not bypass the v4.3 no-Git and runtime-storage safety model.

## Safety Boundary

- v4.4 defaults to mock OCR.
- v4.4 does not call real OCR.
- v4.4 does not read PDF or image binary content.
- v4.4 does not call LLMs.
- v4.4 does not call DeepSeek live.
- v4.4 does not call real legal databases.
- v4.4 does not commit real materials.
- v4.4 does not commit OCR text.
- v4.4 does not commit raw OCR output.
- v4.4 stores redacted OCR preview only in ignored runtime storage.
- v4.4 does not generate final legal opinions.
- v4.4 does not automatically enable Workspace Runtime.
- v4.4 does not automatically publish Skills.

## Explicit OCR Confirmation

`explicit_ocr_confirmation=true` is required before controlled OCR preview can proceed.

If confirmation is missing, the API returns `allowed_to_continue=false` and `ocr_called=false`.

## Manual Review Gate

`manual_review_confirmed=true` is required. OCR redaction is best-effort and requires manual lawyer review.

## OCR Provider Gate

Allowed modes:

- `mock`
- `disabled`
- `local`
- `local_only`
- `controlled_local`

Blocked modes:

- `live`
- `real`
- `deepseek_live`
- `deepseek`
- `production`
- `remote`
- `external`

## Local OCR File Guard

The file path must exist, must be a regular file, must be outside the Git repository, and must not be inside runtime storage or blocked case material directories.

Responses and audit logs only expose `<local_file_path_redacted>`.

## Extension Guard

Allowed extensions:

- `.pdf`
- `.png`
- `.jpg`
- `.jpeg`
- `.txt`

PDF and image files are mock-only in v4.4. Their binary content is not read.

Blocked examples:

- `.doc`
- `.docx`
- `.heic`
- `.xlsx`
- `.zip`
- `.rar`
- `.7z`
- `.eml`
- `.msg`

## Size Guard

The maximum file size is `5000000` bytes. Oversized files are blocked before OCR preview.

## Runtime Storage

Redacted OCR preview storage is restricted to:

`storage/runtime/controlled_ocr_previews`

This path is ignored by Git. Runtime storage contains only:

- `ocr_preview_id`
- `redacted_ocr_preview`
- `created_at`
- `mock_or_redacted_only=true`

It does not store raw OCR text, real paths, real filenames, API keys, or final legal opinions.

## OCR Redaction

The OCR redaction layer masks common sensitive patterns such as phone numbers, ID numbers, bank card-like numbers, email addresses, addresses, case numbers, and long digit strings.

OCR redaction is best-effort and requires manual lawyer review.

## OCR Source Trace

OCR source refs include redacted metadata only. They do not include raw OCR text, real OCR output, or full local paths.

## OCR Audit Logs

Audit logs may record OCR preview identifiers, case/workspace identifiers, material id, redacted filename marker, result, warnings, and timestamps.

Audit logs must not record raw OCR text, real OCR text, real filenames, full paths, customer names, ID numbers, phone numbers, addresses, case numbers, or API keys.

## A1-A13

A1-A13 remain unchanged:

- A1: 案由分析
- A2: 法规清单
- A3: 类案检索
- A4: 请求权 / 抗辩权基础
- A5: 举证策略
- A6: 诉状 / 答辩状
- A7: 诉求量化 / 反请求
- A8: 证据清单
- A9: 质证意见
- A10: 争议焦点法律深化分析
- A11: 庭审提纲
- A12: 代理词
- A13: 结案报告 / 结案框架

A10 remains: 争议焦点法律深化分析.

## Next Step

v4.5 can introduce a controlled legal search local citation pipeline with mock legal citation by default, manual confirmation before any real provider, source refs, citation trace, no real legal database calls by default, and no final legal opinion generation.
