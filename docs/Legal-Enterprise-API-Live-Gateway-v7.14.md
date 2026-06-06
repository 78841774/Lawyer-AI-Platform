# Legal / Enterprise API Live Gateway v7.14

## 定位

v7.14 属于 v7.10-v7.17 Personal Live Intelligence & Controlled Case Analysis 连续大阶段。本阶段在 `personal_intelligence_gateway` 上建立法律检索与企业信息 API live gateway 地基，但 live mode 默认关闭，dry-run 优先，不返回 provider 原始全文。

## Provider Config

支持 provider metadata：

- `kuaicha365_lawskills_provider`
- `tianyancha_ai_provider`
- `qichacha_provider_placeholder`
- `pkulaw_provider_placeholder`
- `national_law_database_provider_placeholder`

API key 只允许后端读取。API response 和前端只展示 `key_loaded=true/false` 与 `key_source` 枚举，不展示 key 值、env var 值、secret 或本地路径。

## Live Gate

默认：

- `LEGAL_LIVE_MODE_ENABLED=false`
- `ENTERPRISE_LIVE_MODE_ENABLED=false`
- provider `live_enabled=false`

非 dry-run live request 必须确认：

- `explicit_live_confirmation=true`
- `query_owner_confirmation=true`
- `raw_content_handling_acknowledged=true`
- `no_ai_prompt_injection_acknowledged=true`
- `lawyer_review_acknowledged=true`
- `draft_only_acknowledged=true`
- `no_final_citation_acknowledged=true`

缺任一确认时，返回 `live_call_blocked` metadata，不执行法律检索或企业信息 provider call。

## Boundary

必须保持：

- legal raw result 不默认返回。
- enterprise raw result 不默认返回。
- citation 仅为 metadata candidate。
- enterprise risk 仅为 metadata candidate。
- 不自动进入 AI Prompt。
- 不自动进入 fact extraction。
- 不自动进入 legal analysis。
- 不自动生成 final citation。
- 不生成最终法律意见。
- 不生成最终报告。
- 不自动对外交付。

## API

- `GET /personal-intelligence/live/status`
- `GET /personal-intelligence/live/providers`
- `GET /personal-intelligence/live/providers/{provider_id}`
- `POST /personal-intelligence/live/legal-search/dry-run`
- `POST /personal-intelligence/live/legal-search/runs`
- `GET /personal-intelligence/live/legal-search/runs`
- `GET /personal-intelligence/live/legal-search/runs/{run_id}`
- `POST /personal-intelligence/live/enterprise-query/dry-run`
- `POST /personal-intelligence/live/enterprise-query/runs`
- `GET /personal-intelligence/live/enterprise-query/runs`
- `GET /personal-intelligence/live/enterprise-query/runs/{run_id}`
- `GET /personal-intelligence/live/review-queue`
- `POST /personal-intelligence/live/review-queue/{review_item_id}/actions`
- `GET /personal-intelligence/live/source-traces`
- `GET /personal-intelligence/live/source-traces/{source_trace_id}`
- `GET /personal-intelligence/live/audit`
- `GET /personal-intelligence/live/safety`

## 下一步

下一步进入 v7.15 Skill Training Runtime。Team Workspace 后置，External Client Delivery 后置。v7.10-v7.17 完成后统一运行 full regression、final security audit、commit、tag 和 release。
