# Controlled Local Material Read Implementation v4.3

## Goal

v4.3 implements the minimum controlled local material read preview loop on top of v4.2 Controlled Local Real-Material Processing.

This stage remains local-only and is not production. It reads only explicitly confirmed small local text files, builds a best-effort redacted preview, stores that redacted preview only in ignored runtime storage, and keeps raw text out of responses, audit logs, registry files, and Git.

## Difference From v4.2

v4.2 prepared controlled read gates but returned `content_read=false`.

v4.3 allows `content_read=true` only when all required gates pass, and only for `.txt`, `.md`, and `.json` files under the size limit. It still does not process PDF, Word, image, spreadsheet, archive, or email files.

## Safety Boundary

- v4.3 only supports `.txt`, `.md`, and `.json`.
- v4.3 does not read PDF, Word, images, spreadsheets, archives, or email files.
- v4.3 does not upload real materials.
- v4.3 does not commit real materials.
- v4.3 does not commit `raw_text`.
- v4.3 does not commit OCR text.
- v4.3 does not call OCR.
- v4.3 does not call real LLMs.
- v4.3 does not call DeepSeek live.
- v4.3 does not call real legal databases.
- v4.3 does not generate final legal opinions.
- v4.3 does not automatically enable Workspace Runtime.
- v4.3 does not automatically publish Skills.

## Explicit Read Confirmation

`explicit_read_confirmation=true` is required before any local read preview can proceed.

If confirmation is missing, the API returns `allowed_to_continue=false` and `content_read=false`.

## Manual Review Gate

`manual_review_confirmed=true` is required. The redaction preview is best-effort only and must be reviewed by a lawyer before any further use.

## Local File Path Guard

The local file path must exist, must be a regular file, and must not be inside the Git repository, runtime storage, or blocked case material directories.

Responses and audit logs only expose `<local_file_path_redacted>`.

## Extension Guard

Allowed extensions:

- `.txt`
- `.md`
- `.json`

Blocked examples:

- `.pdf`
- `.doc`
- `.docx`
- `.jpg`
- `.jpeg`
- `.png`
- `.heic`
- `.xlsx`
- `.zip`
- `.rar`
- `.7z`
- `.eml`
- `.msg`

## Size Guard

The maximum file size is `200000` bytes. Oversized files are blocked before content is read.

## Path Outside Repo Guard

The file must be outside the Git repository. Repo-internal test files and tracked or trackable paths are blocked.

## Runtime Storage Guard

Redacted preview storage is restricted to:

`storage/runtime/controlled_material_previews`

This path is ignored by Git. Runtime storage contains only:

- `preview_id`
- `redacted_preview`
- `created_at`
- `mock_or_redacted_only=true`

It does not store raw text, real paths, real filenames, API keys, or OCR text.

## Redacted Preview

The redaction preview replaces common sensitive patterns such as phone numbers, ID numbers, bank card-like long numbers, email addresses, addresses, case numbers, and long digit strings.

Redaction is best-effort and requires manual lawyer review.

## Source Trace Placeholder

Source refs identify the redacted preview and material id with redacted path markers only. They do not contain raw text.

## Audit Log

Audit logs may record `preview_id`, case/workspace identifiers, material id, redacted filename marker, result, warnings, and timestamps.

Audit logs must not record raw text, real material body text, real file names, full paths, OCR text, customer names, ID numbers, phone numbers, addresses, case numbers, or API keys.

## Report Draft

The report draft remains mock-only. It does not call an LLM, does not finalize legal advice, and requires human review.

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

v4.4 can introduce a controlled OCR adapter local pipeline for explicitly confirmed PDF or image material previews. OCR must remain gated, local-only by default, and restricted to ignored runtime storage.
