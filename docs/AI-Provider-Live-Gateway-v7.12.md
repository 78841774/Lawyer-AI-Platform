# AI Provider Live Gateway v7.12

## 定位

v7.12 属于 v7.10-v7.17 Personal Live Intelligence & Controlled Case Analysis 连续大阶段。本阶段建立 AI Provider 真实接口受控网关地基，但 live mode 默认关闭，不自动调用真实 provider。

本版本允许后端具备 provider metadata、key_loaded 布尔状态、dry-run、gated live run、prompt boundary、response boundary、usage metadata 和 audit metadata。前端只显示 provider 状态、确认门禁和 AI 草稿 metadata，不显示 API key。

## Provider Config

支持 provider metadata：

- `openai`
- `deepseek`
- `local_model_placeholder`

每个 provider 返回：

- `provider_id`
- `display_name`
- `provider_type`
- `live_supported`
- `live_enabled`
- `key_required`
- `key_loaded`
- `key_source`
- `model_options`
- `timeout_seconds`
- `safety_notes`

API key 只由后端环境变量读取。前端和 API response 只返回 `key_loaded=true/false`，不返回 key 值，不返回 env var 原始值。

## Live Gate

默认：

- `AI_LIVE_MODE_ENABLED=false`
- provider `live_enabled=false`
- live provider disabled

非 dry-run live request 必须确认：

- `explicit_live_confirmation=true`
- `lawyer_review_acknowledged=true`
- `draft_only_acknowledged=true`
- `no_final_opinion_acknowledged=true`
- `no_final_report_acknowledged=true`
- `no_external_delivery_acknowledged=true`

缺任一确认时，返回 `live_call_blocked` metadata，不执行 provider call。

## Dry-run / Gated Live Run

- `dry_run=true`：不调用真实 provider，只返回 `would_call_provider` metadata。
- `dry_run=false`：必须通过全局 live gate、provider gate、key_loaded 和确认门禁。
- v7.12 不实现真实 provider adapter；即使 gate 满足，也应保持 provider adapter 未配置状态，不假装成功。

## Prompt Boundary

Prompt boundary 记录：

- `prompt_template_id`
- `prompt_purpose`
- `case_id`
- `source_trace_ids`
- `raw_content_included=false`
- `final_legal_opinion_requested=false`
- `final_report_requested=false`

禁止 purpose：

- `final_legal_opinion`
- `final_report`
- `external_delivery`
- `auto_send_client`

## Response Boundary

AI response 只能是 draft metadata：

- `ai_draft`
- `draft_type`
- `provider_id`
- `model`
- `token_usage`
- `latency_ms`
- `source_trace_required=true`
- `lawyer_review_required=true`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `external_delivery_triggered=false`

不自动写入 final report，不自动送入 delivery packet，不自动对外交付。

## Audit

每次 dry-run、blocked live attempt 或 live attempt 都写 audit metadata 到 ignored runtime storage：

- `event_id`
- `provider_id`
- `action`
- `actor_id`
- `live_call_requested`
- `live_call_executed`
- `blocked_reason`
- `confirmations`
- `token_usage`
- `created_at`

Audit 不返回 raw prompt、raw provider response、local path、API key 或真实案件材料。

## API

- `GET /personal-ai-gateway/live/status`
- `GET /personal-ai-gateway/live/providers`
- `GET /personal-ai-gateway/live/providers/{provider_id}`
- `POST /personal-ai-gateway/live/dry-run`
- `POST /personal-ai-gateway/live/runs`
- `GET /personal-ai-gateway/live/runs`
- `GET /personal-ai-gateway/live/runs/{run_id}`
- `GET /personal-ai-gateway/live/audit`
- `GET /personal-ai-gateway/live/safety`

## Frontend

`/personal-ai-gateway` 增加 AI Live Gateway 受控接入区域：

- Live status cards。
- Provider cards。
- Dry-run panel。
- Gated live run panel。
- Confirmation checklist。
- Draft output metadata preview。
- Live audit timeline。
- Trust / Safety Panel。
- Developer Diagnostics 默认折叠。

前端没有 API key 输入框，不显示 API key，不展示 raw provider response，不展示真实材料 prompt。

## 下一步

下一步进入 v7.13 OCR / Document Provider Live Gateway。Team Workspace 后置，External Client Delivery 后置。v7.10-v7.17 完成后统一运行 full regression、final security audit、commit、tag 和 release。
