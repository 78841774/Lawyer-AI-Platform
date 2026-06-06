# v7.26 Provider Live Readiness & Secret Boundary

中文定位：真实接口接入准备与密钥边界。

v7.26 在真正接入 OCR / AI / 法律检索 / 企业信息 provider 前，新增统一 provider readiness 层。它只做 provider registry、secret boundary、live gate、usage / cost metadata、dry-run health、provider audit 和 safety metadata。

本阶段不真实调用 provider，不读取密钥值，不读取真实案件材料，不做训练，不做实战分析，不生成最终法律意见或正式报告，不创建公开链接、不发送邮件、不自动对外交付。

## Scope

- Backend runtime: `personal_provider_readiness`.
- Frontend route: `/personal-provider-readiness`.
- API prefix: `/personal-provider-readiness`.
- Personal Production integration: runtime registry、readiness、provider capabilities、总控台、Pilot Dashboard、AppShell navigation.
- Regression: `scripts/regression/check_personal_provider_readiness_apis.sh`.

## Provider Registry

The registry covers:

- AI: `openai`, `deepseek`, `local_model_placeholder`.
- OCR / Document: `paddleocr_local`, `baidu_paddle_ai_studio_placeholder`, `mineru_placeholder`, `docling_placeholder`.
- Legal Search: `kuaicha_365_lawskills_placeholder`, `legal_search_placeholder`, `national_law_database_placeholder`.
- Enterprise: `tianyancha_ai_placeholder`, `qichacha_placeholder`, `enterprise_registry_placeholder`.

Each provider returns metadata such as provider category, live support, dry-run support, gate state, key environment variable names, key_loaded boolean, key_source, usage/cost support, and adapter state.

## Secret Boundary

The secret boundary only checks whether configured environment variable names exist in the backend process environment. It does not read, slice, mask, log, return, or store key values.

Allowed response fields:

- `key_loaded=true/false`
- `key_source=env/unavailable/not_required`
- `key_value_exposed=false`
- `secret_value_returned=false`
- `secret_logged=false`
- `frontend_key_input_enabled=false`

## Live Gate

v7.26 always keeps live execution blocked:

- `global_live_enabled=false`
- `provider_live_enabled=false`
- `dry_run=true`
- `live_call_allowed=false`
- `live_call_executed=false`

Even if `key_loaded=true`, this version does not execute provider calls.

## Usage / Cost Metadata

Usage and cost fields are dry-run metadata only:

- `usage_meter_enabled=false`
- `estimated_token_count`
- `estimated_page_count`
- `estimated_document_count`
- `estimated_call_count`
- `estimated_cost_available=false`
- `actual_cost_recorded=false`
- `billable_call_executed=false`
- `usage_recorded_as_metadata_only=true`

## Dry-run Health

Dry-run health never performs a network call. It only returns config detected status, key_loaded boolean metadata, live gate status, adapter registration status, dry-run readiness, blocked reason, and next required confirmation.

## Next

v7.27 should begin OCR / Document Provider Live Connection work behind the provider readiness and secret boundary established here.

