# Controlled Lawyer Review Workflow v4.7

## Goal

v4.7 adds a controlled lawyer review workflow for v4.6 mock report drafts. It allows a lawyer to submit a mock draft for review, inspect review metadata and history, and record approve, reject, or request revision actions.

v4.7 does not generate a final legal opinion. It does not call a real LLM, DeepSeek live, real OCR, or a real legal database. It does not publish a Skill and does not enable production.

## Scope

The workflow only accepts v4.6 mock controlled report draft IDs. The review layer stores review metadata and action history only. It does not read raw case materials, raw OCR text, or real legal search results.

## API

1. `GET /controlled-review/status`
2. `POST /controlled-review/submit`
3. `GET /controlled-review/{review_id}`
4. `POST /controlled-review/{review_id}/approve`
5. `POST /controlled-review/{review_id}/reject`
6. `POST /controlled-review/{review_id}/request-revision`
7. `GET /controlled-review/audit-logs`

## Gates

The explicit review confirmation gate requires `explicit_review_confirmation=true`.

The explicit v4.6 assembly confirmation gate requires `explicit_assembly_confirmation=true` on submit.

The manual review gate requires `manual_review_confirmed=true`.

The provider gate allows only local mock modes and blocks:

1. `live`
2. `real`
3. `production`
4. `remote`
5. `external`
6. `deepseek_live`
7. `deepseek`

## Runtime Storage

Controlled review records are written only to:

`storage/runtime/controlled_lawyer_reviews`

This path is ignored by Git. Review records must not be written to docs, backend, frontend, registry, or tracked paths.

## Audit Logs

Audit logs record safe metadata only:

1. audit log ID
2. event type
3. review ID
4. draft ID
5. case ID
6. workspace ID
7. action
8. result
9. warnings
10. timestamp

Audit logs do not record raw material text, raw OCR text, real legal search results, API keys, real file paths, real customer names, ID numbers, phone numbers, addresses, or case numbers.

## Safety Boundary

v4.7 keeps these boundaries:

1. local-only mock review。
2. mock report draft 写入 ignored runtime storage。
3. 不生成正式法律意见。
4. explicit review confirmation gate 必须通过。
5. explicit assembly confirmation gate 必须通过。
6. manual review gate 必须通过。
7. provider gate 拦截 live / deepseek / external。
8. 不读取真实材料。
9. 不调用真实 OCR。
10. 不调用真实 LLM。
11. 不调用真实法律数据库。
12. 不发布 Skill。
13. 不启用 production。
14. raw content 不入 Git，不返回。
15. A1-A13 不改变。
16. A10 保持：争议焦点法律深化分析。

## Next Step

After v4.7, the next stage can introduce a controlled revision loop that lets lawyers request a new mock-only draft iteration while preserving the same no-production and no-live-provider boundaries.

