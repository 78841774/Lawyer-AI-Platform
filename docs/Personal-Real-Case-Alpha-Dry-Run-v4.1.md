# Personal Real Case Alpha Dry-Run v4.1

## Goal

v4.1 prepares a personal local real-case Alpha dry-run preview foundation on top of v3.9 Local Sandbox and v4.0 Internal Alpha.

It is not production. It is not team-wide usage. It does not automatically process large numbers of real cases. It is limited to local sandbox external folders, metadata-only previews, mock provider previews, and manual lawyer review.

## Safety Boundary

- v4.1 does not read real case material body text.
- v4.1 does not call real OCR.
- v4.1 does not call real legal databases.
- v4.1 does not call real LLMs.
- v4.1 does not call DeepSeek live provider.
- v4.1 does not commit real case materials.
- v4.1 does not commit sensitive real file names.
- v4.1 does not commit API keys.
- v4.1 does not automatically generate formal legal opinions.
- v4.1 does not automatically enable Workspace Runtime.
- v4.1 does not automatically publish Skills.
- v4.1 only provides personal local dry-run, preview, and audit log foundation.

## Local External Case Folder

Personal Alpha expects materials to remain in an external local folder such as `~/Lawyer-AI-Local-Cases` or `~/AIHome-Law-Local-Sandbox`. These folders are ignored by Git and must not be committed.

The application may check whether a local folder path matches an approved local-only prefix. It does not output the real path and uses `<local_case_root_redacted>`.

## Case Manifest Preview

The manifest preview creates a redacted preview record with case/workspace identifiers, case cause code, jurisdiction, manual review status, and redaction checklist. It does not read material content or scan document text.

## Material Inventory Preview

The material inventory preview is metadata-only. It always outputs redacted filenames and redacted relative paths. Even when the request sets `include_file_names=true`, v4.1 keeps filenames redacted.

`content_read` must remain `false`.

## Redaction Checklist

The redaction checklist is not automatic redaction. It is an explicit manual review checklist for:

- client names
- ID numbers
- phone numbers
- addresses
- bank information
- case numbers
- file names
- material content
- API keys
- local-only confirmation

## Provider Guards

v4.1 reuses v3.9 Local Sandbox and v4.0 Internal Alpha guards. It blocks live, DeepSeek live, production, remote, and external modes for provider, OCR, legal search, and LLM.

## Mock Previews

The Personal Alpha dry-run returns:

- mock OCR preview, without OCR text
- mock legal search preview, without querying legal databases
- mock source trace preview, without persisted extracted text
- mock report draft preview, without LLM calls

The report draft preview is not legal advice and requires lawyer review.

## Manual Review Gate

`manual_review_confirmed=true` is required before the dry-run can continue. If manual review is not confirmed, the result is blocked and `manual_review_required=true`.

## Audit Log

Personal Alpha audit logs record only dry-run identifiers, case/workspace identifiers, result, warnings, timestamps, and `<local_case_root_redacted>`. They do not record real paths, real filenames, OCR text, customer names, ID numbers, phone numbers, addresses, case numbers, or API keys.

## Relationship To v4.0 And v3.9

v4.1 depends on v4.0 Internal Alpha readiness and v3.9 Local Sandbox guards. It does not bypass them. It adds personal local manifest, inventory, mock preview, and report draft preview foundations.

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

v4.2 can introduce controlled local real-material processing only after explicit content-read guards, controlled OCR provider gate, controlled LLM provider gate, source trace persistence, report draft generation with manual review, and strict no-Git handling for material and extracted text.
