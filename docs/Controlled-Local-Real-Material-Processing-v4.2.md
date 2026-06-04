# Controlled Local Real-Material Processing v4.2

## Goal

v4.2 prepares a controlled local real-material processing gate on top of v4.1 Personal Alpha, v4.0 Internal Alpha, and v3.9 Local Sandbox.

This stage is not production. It does not read real material body text. It only establishes explicit read confirmation, manual lawyer review, provider guards, audit boundaries, and mock controlled report draft behavior for the next stage.

## Safety Boundary

- v4.2 does not read real material body text.
- v4.2 does not store material content.
- v4.2 does not store OCR text.
- v4.2 does not call real OCR.
- v4.2 does not call real legal databases.
- v4.2 does not call real LLMs.
- v4.2 does not call DeepSeek live provider.
- v4.2 does not commit real materials.
- v4.2 does not commit real local paths.
- v4.2 does not commit real filenames.
- v4.2 does not commit API keys.
- v4.2 does not generate final legal opinions.
- v4.2 does not automatically enable Workspace Runtime.
- v4.2 does not automatically publish Skills.

## Controlled Read Gate

The controlled read API requires:

- `explicit_read_confirmation=true`
- `manual_review_confirmed=true`
- local-only or mock provider modes
- no live OCR mode
- no live LLM mode
- no live legal search mode
- no DeepSeek live mode

Even when all gates pass, v4.2 returns `content_read=false`. The result means the controlled local read gate is ready, not that real material content was processed.

## Report Draft Boundary

The report draft endpoint returns a mock draft placeholder only. It does not call an LLM, does not read material content, does not finalize legal advice, and always requires human lawyer review.

`final_legal_opinion_enabled=false` must remain visible in status and report draft results.

## Audit Log

Controlled material audit logs record only sanitized identifiers, redacted filename markers, redacted local root markers, result, warnings, and timestamps.

Audit logs must not record real paths, real filenames, material body text, OCR text, client names, ID numbers, phone numbers, addresses, case numbers, or API keys.

## Git Storage Boundary

The following must not be staged or committed:

- `.env`
- `local.db`
- `*.db`
- `runtime`
- `sandbox_cases`
- `real_cases`
- `case_workspaces`
- `Lawyer-AI-Local-Cases`
- `AIHome-Law-Local-Sandbox`
- `node_modules`
- `__pycache__`
- `.DS_Store`

Material content and extracted text must remain outside Git.

## Relationship To Earlier Versions

v4.2 depends on v4.1 Personal Alpha and does not bypass its dry-run safety boundary.

v4.2 keeps v4.0 Internal Alpha local-only controls and v3.9 Local Sandbox provider guards. It adds a more explicit controlled material read gate, but still does not perform real content reading in this version.

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

v4.3 may introduce actual local real-material reading only after stricter content-read safeguards, encrypted or local-only runtime storage design, source trace persistence rules, OCR text handling rules, and manual lawyer review workflow are validated.
