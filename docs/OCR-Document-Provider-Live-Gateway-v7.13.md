# OCR / Document Provider Live Gateway v7.13

## 定位

v7.13 属于 v7.10-v7.17 Personal Live Intelligence & Controlled Case Analysis 连续大阶段。本阶段在 `personal_material_runtime` 上建立 OCR / Document provider live gateway 地基，但 live mode 默认关闭，dry-run 优先，不读取或返回真实材料原文。

## Provider Config

支持 provider metadata：

- `paddleocr`
- `mineru`
- `docling`
- `local_document_parser_placeholder`

每个 provider 返回：

- `provider_id`
- `display_name`
- `provider_type`
- `live_supported`
- `live_enabled`
- `key_required`
- `key_loaded`
- `key_source`
- `supported_file_types`
- `max_file_size_mb`
- `supports_page_range`
- `supports_bbox`
- `supports_table_extraction`
- `supports_layout_extraction`
- `timeout_seconds`
- `safety_notes`

API key 只允许后端读取。API response 和前端只展示 `key_loaded=true/false` 与 `key_source` 枚举，不展示 key 值或 env var 值。

## Live Gate

默认：

- `OCR_LIVE_MODE_ENABLED=false`
- `DOCUMENT_LIVE_MODE_ENABLED=false`
- provider `live_enabled=false`

非 dry-run live request 必须确认：

- `explicit_live_confirmation=true`
- `material_owner_confirmation=true`
- `raw_content_handling_acknowledged=true`
- `no_ai_prompt_injection_acknowledged=true`
- `lawyer_review_acknowledged=true`
- `draft_only_acknowledged=true`

缺任一确认时，返回 `live_call_blocked` metadata，不执行 OCR 或 document provider call。

## Dry-run / Gated Live Run

- Document dry-run 返回 would-parse metadata，不调用 provider。
- OCR dry-run 返回 would-OCR metadata，不调用 provider。
- Gated live run 在 gate 未满足时必须 blocked。
- Gate 满足但 adapter 未实现时返回 `provider_adapter_unavailable`，`live_call_executed=false`。

v7.13 不假装真实 OCR 或真实文档解析成功。

## Raw Content Boundary

必须保持：

- raw OCR text 不默认返回。
- raw document text 不默认返回。
- OCR 原文不自动进入 AI Prompt。
- 文档原文不自动进入事实抽取。
- 不自动触发法律分析。
- 不生成最终法律意见。
- 不生成最终报告。
- 不自动对外交付。

允许返回安全 metadata：

- page count / estimate。
- file type。
- byte size。
- parse status。
- confidence summary。
- layout blocks count。
- table count。
- image count。
- bbox available。
- redacted preview available。
- raw content exposed = false。

## Review Queue

新增 live review queue：

- `approve_metadata_only`
- `request_manual_review`
- `reject`
- `mark_low_confidence`
- `allow_redacted_preview`
- `block_raw_content`

`approve_metadata_only` 不等于允许 raw content 进入 AI Prompt。`allow_redacted_preview` 也仅允许脱敏 preview metadata，不允许 raw full content。

## Audit / Source Trace

每次 dry-run、blocked live attempt、adapter unavailable attempt、review action 都写 audit metadata 到 ignored runtime storage。

Audit 和 source trace 不返回：

- API key。
- raw OCR text。
- raw document content。
- local path。
- 真实案件材料。

## API

- `GET /personal-material-runtime/live/status`
- `GET /personal-material-runtime/live/providers`
- `GET /personal-material-runtime/live/providers/{provider_id}`
- `POST /personal-material-runtime/live/document/dry-run`
- `POST /personal-material-runtime/live/document/runs`
- `GET /personal-material-runtime/live/document/runs`
- `GET /personal-material-runtime/live/document/runs/{run_id}`
- `POST /personal-material-runtime/live/ocr/dry-run`
- `POST /personal-material-runtime/live/ocr/runs`
- `GET /personal-material-runtime/live/ocr/runs`
- `GET /personal-material-runtime/live/ocr/runs/{run_id}`
- `GET /personal-material-runtime/live/review-queue`
- `POST /personal-material-runtime/live/review-queue/{review_item_id}/actions`
- `GET /personal-material-runtime/live/source-traces`
- `GET /personal-material-runtime/live/audit`
- `GET /personal-material-runtime/live/safety`

## 下一步

下一步进入 v7.14 Legal / Enterprise API Live Gateway。Team Workspace 后置，External Client Delivery 后置。v7.10-v7.17 完成后统一运行 full regression、final security audit、commit、tag 和 release。
