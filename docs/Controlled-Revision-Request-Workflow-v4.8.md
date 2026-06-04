# Controlled Revision Request Workflow v4.8

## Goal

v4.8 adds a controlled revision request workflow after v4.7 lawyer review. It creates a mock revision request, revision checklist, mock draft revision plan, revision cycle audit entry, and lawyer re-review gate.

v4.8 is not production. It is local-only and mock-only by default.

## Relationship To v4.7 And v4.6

v4.6 assembles mock controlled report drafts.
v4.7 lets lawyers review those mock drafts.
v4.8 lets lawyers request controlled revisions after review.

The workflow uses `review_id` and `draft_id` as controlled references. It does not load raw report text, raw material text, OCR text, or real legal search results.

## Not Production

v4.8 remains non-production because:

1. v4.8 默认 mock revision。
2. v4.8 不调用真实 LLM。
3. v4.8 不调用 DeepSeek live。
4. v4.8 不调用真实 OCR。
5. v4.8 不调用真实法律数据库。
6. v4.8 不提交 raw material text。
7. v4.8 不提交 raw OCR text。
8. v4.8 不提交 raw legal search results。
9. v4.8 mock revision 仅存 ignored runtime。
10. v4.8 不生成正式法律意见。
11. A1-A13 不改变。
12. A10 保持：争议焦点法律深化分析。

## Gates

The review-driven revision request requires a non-empty `review_id`.

The explicit revision confirmation gate requires `explicit_revision_confirmation=true`.

The manual review gate requires `manual_review_confirmed=true`.

The provider gate allows only:

1. `mock`
2. `disabled`
3. `local`
4. `local_only`
5. `controlled_local`

The provider gate blocks:

1. `live`
2. `real`
3. `production`
4. `remote`
5. `external`
6. `deepseek_live`
7. `deepseek`

The requested action gate allows only:

1. `request_revision`
2. `revise_summary`
3. `revise_citations`
4. `revise_structure`
5. `revise_risk_warnings`
6. `revise_lawyer_checklist`

## Mock Revision Plan

The mock revision plan includes:

1. title
2. status
3. case ID
4. workspace ID
5. review ID
6. draft ID
7. requested action
8. redacted revision reason
9. redacted revision instructions
10. revision scope
11. affected report sections
12. citation review notes
13. risk warning review notes
14. lawyer re-review checklist

It sets `legal_opinion_finalized=false`, `requires_human_review=true`, and `mock_only=true`.

## Revision Checklist

The revision checklist requires lawyer re-review of:

1. revision scope
2. facts not being overwritten
3. citations remaining mock or manually verified
4. no final legal opinion
5. lawyer re-review requirement
6. A10 not being modified

## Source Trace

Source trace placeholders are marked `mock_or_redacted_only=true`. They include no raw material text, no raw OCR text, and no real legal search results.

## Runtime Storage

Mock revision output is written only to:

`storage/runtime/controlled_revisions`

This path is ignored by Git. v4.8 does not write revision output to docs, backend, frontend, registry, or tracked paths.

## Audit Logs

Audit logs store safe metadata only:

1. audit log ID
2. event type
3. case ID
4. workspace ID
5. review ID
6. draft ID
7. revision ID
8. result
9. warnings
10. timestamp

Audit logs do not store raw material text, raw OCR text, real legal search results, API keys, real paths, real customer names, ID numbers, phone numbers, addresses, or case numbers.

## v4.9 Plan

The next recommended stage is v4.9 Controlled Final Review Lock Workflow:

1. lock a mock final review candidate
2. require final lawyer confirmation
3. preserve complete audit trail
4. avoid final legal opinion generation
5. avoid production deployment

