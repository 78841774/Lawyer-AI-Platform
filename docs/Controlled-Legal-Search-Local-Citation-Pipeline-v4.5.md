# Controlled Legal Search Local Citation Pipeline v4.5

## Goal

v4.5 adds a controlled legal search citation preview pipeline on top of v4.4 Controlled OCR Adapter Local Pipeline and the v3.8 source trace foundation.

This stage remains local-only and is not production. It defaults to mock legal search, does not call real legal databases, does not call LLMs, does not call DeepSeek live, and does not generate final legal opinions.

## Relationship

v4.5 does not replace the v3.7 `legal_search_adapter`. It adds a separate controlled preview pipeline with explicit confirmation, provider guards, query redaction, mock citations, citation source refs, and ignored runtime storage.

## Safety Boundary

- v4.5 defaults to mock legal search.
- v4.5 does not call real legal databases.
- v4.5 does not call external legal search APIs.
- v4.5 does not call LLMs.
- v4.5 does not call DeepSeek live.
- v4.5 does not commit raw query text.
- v4.5 does not commit real legal search result text.
- v4.5 stores redacted search preview only in ignored runtime storage.
- v4.5 does not generate final legal opinions.
- v4.5 does not automatically enable Workspace Runtime.
- v4.5 does not automatically publish Skills.

## Gates

The preview requires explicit legal search confirmation, manual lawyer review, safe mock/local provider modes, query redaction, ignored runtime storage, and no sensitive staged Git paths.

## Query Redaction

Query redaction masks phone numbers, ID numbers, email addresses, case numbers, and long digit strings. Query redaction is best-effort and requires manual lawyer review.

## Mock Citation Provider

The provider returns mock statute and case citations only. They are not retrieved from a real legal database.

## Citation Trace And Resolver

Source refs use mock placeholders and do not contain real legal search results. Citation resolution is mock-only and returns `real_legal_database_called=false`.

## Runtime Storage

Runtime storage path:

`storage/runtime/controlled_legal_search_previews`

Runtime storage contains only redacted preview text, mock citations, source refs, timestamps, and `mock_or_redacted_only=true`.

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

v4.6 can introduce a controlled report draft assembly pipeline that combines controlled material previews, OCR previews, legal search citations, and source trace while keeping mock-only LLM behavior and manual lawyer review.
