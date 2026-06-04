# Controlled Report Draft Assembly Pipeline v4.6

## v4.6 Goal

v4.6 adds a Controlled Report Draft Assembly Pipeline for local Personal Alpha dry-run work. It assembles a mock report draft from controlled material preview IDs, controlled OCR preview IDs, controlled legal search preview IDs, and citation IDs.

The pipeline is a controlled assembly layer only. It does not read raw case materials, does not call live providers, and does not generate a final legal opinion.

## Relationship To v4.3, v4.4, And v4.5

v4.3 introduced controlled local material read previews.
v4.4 introduced controlled OCR previews.
v4.5 introduced controlled legal search citation previews.
v4.6 merges those controlled preview references into a mock report draft with source trace placeholders.

The inputs are preview IDs and citation IDs only. v4.6 does not re-open local files, does not load OCR raw text, and does not retrieve real legal search results.

## Not Production

v4.6 is still not production because:

1. It defaults to mock report assembly.
2. It requires explicit assembly confirmation.
3. It requires manual lawyer review.
4. It blocks live, real, production, remote, external, DeepSeek, and DeepSeek live provider modes.
5. It stores mock report drafts only in ignored runtime storage.
6. It does not generate a final legal opinion.

## Gates

The explicit assembly confirmation gate requires `explicit_assembly_confirmation=true`.

The manual review gate requires `manual_review_confirmed=true`.

The provider gate allows only:

1. `mock`
2. `disabled`
3. `local`
4. `local_only`
5. `controlled_local`

The provider gate rejects:

1. `live`
2. `real`
3. `production`
4. `remote`
5. `external`
6. `deepseek_live`
7. `deepseek`

## Mock Report Assembler

The mock assembler creates:

1. `Mock Controlled Report Draft`
2. controlled material summary placeholder
3. controlled OCR summary placeholder
4. controlled legal search summary placeholder
5. source trace summary placeholder
6. lawyer review checklist

The assembler sets:

1. `final_legal_opinion_generated=false`
2. `llm_called=false`
3. `deepseek_live_called=false`
4. `real_ocr_called=false`
5. `real_legal_database_called=false`
6. `raw_material_text_included=false`
7. `raw_ocr_text_included=false`
8. `raw_legal_search_results_included=false`

## Source Trace Merge

v4.6 creates source trace placeholders from controlled preview IDs and citation IDs. The placeholders are marked `mock_or_redacted_only=true` and contain no raw material text, no raw OCR text, and no real legal search result.

## Runtime Storage

Mock report drafts are written only to:

`storage/runtime/controlled_report_drafts`

The path is ignored by Git. v4.6 does not store report drafts in `docs`, `backend`, `frontend`, registry files, or tracked paths.

## Audit Logs

Audit logs record only safe metadata:

1. audit log ID
2. event type
3. case ID
4. workspace ID
5. draft ID
6. result
7. warnings
8. timestamp

Audit logs do not record raw material text, raw OCR text, raw legal search results, API keys, real paths, real customer names, ID numbers, phone numbers, addresses, or case numbers.

## Safety Boundary

v4.6 explicitly keeps these boundaries:

1. v4.6 默认 mock report assembly。
2. v4.6 不调用真实 LLM。
3. v4.6 不调用 DeepSeek live。
4. v4.6 不调用真实 OCR。
5. v4.6 不调用真实法律数据库。
6. v4.6 不提交 raw material text。
7. v4.6 不提交 raw OCR text。
8. v4.6 不提交 raw legal search results。
9. v4.6 mock report draft 仅存 ignored runtime。
10. v4.6 不生成正式法律意见。
11. A1-A13 不改变。
12. A10 保持：争议焦点法律深化分析。

## v4.7 Plan

The next planned stage is v4.7 Controlled Lawyer Review Workflow:

1. mock report draft human review
2. review status
3. approve / reject / request revision
4. no final legal opinion
5. no production deployment
6. audit trail

