# Personal AI Gateway & Prompt Runtime v7.1

## Objective

v7.1 adds a controlled AI Provider Gateway and Prompt Runtime on top of the v7.0 Personal Production Runtime & Showcase Foundation.

The goal is to prepare OpenAI, DeepSeek, and Local Model provider metadata for future controlled-live integration while keeping v7.1 mock-first, provider-gated, draft-only, and lawyer-review required.

## Relationship to v7.0

v7.0 introduced the Personal Production Console, runtime registry, provider capability preview, safety panel, readiness views, and showcase-safe frontend.

v7.1 extends that foundation with:

- AI Gateway backend module.
- Provider metadata registry.
- Prompt template registry.
- Prompt render preview.
- Draft-only mock AI run workflow.
- Audit metadata.
- Token usage metadata estimate.
- Safety checklist.
- AI Gateway frontend page.
- Personal Production Console integration.

## Provider Gateway

The gateway registers metadata for:

- `openai_provider`
- `deepseek_provider`
- `local_model_provider`

All providers remain:

- `configured=false`
- `live_enabled=false`
- `mock_supported=true`
- `controlled_live_supported=true`
- `api_key_present=false`
- `api_key_visible=false`

v7.1 does not read API keys, inspect `.env`, or call real providers.

## Prompt Template Registry

The registry provides metadata-only prompt templates:

- `fact_summary_draft`
- `evidence_summary_draft`
- `issue_spotting_draft`
- `legal_analysis_draft`
- `report_outline_draft`
- `risk_warning_draft`
- `experience_package_skill_candidate`

Each template is draft-only, requires lawyer review, requires source tracing, and contains mock-safe placeholder schema metadata. Templates do not embed raw materials, personal information, or final legal opinion text.

## Prompt Render Preview

`POST /personal-ai-gateway/prompt-render-preview` renders a mock-safe prompt preview only after the required confirmations are present.

The preview:

- Does not call a provider.
- Does not read real case materials.
- Does not include raw content.
- Returns `would_call_provider=false`.
- Returns draft-only and lawyer-review flags.
- Blocks safely when confirmations are incomplete.

## Mock AI Runs

`POST /personal-ai-gateway/runs/mock` creates a mock AI run metadata record only when all safety confirmations are true.

The mock run:

- Does not call a provider.
- Does not store raw prompts.
- Does not store real provider responses.
- Returns mock-safe draft output.
- Requires source tracing and lawyer review.
- Keeps `final_legal_opinion_generated=false`.
- Keeps `final_report_generated=false`.

## Audit Metadata

Mock run audit metadata is written under ignored runtime storage:

`Lawyer-AI-Platform-App/backend/storage/runtime/personal_ai_gateway/audit/`

Returned audit API data is metadata-only and excludes raw material, local paths, provider secrets, raw prompts, and provider responses.

## Token Usage Metadata

v7.1 estimates token usage only:

- `estimated_input_tokens`
- `estimated_output_tokens`
- `estimated_total_tokens`

Actual live usage remains unavailable:

- `actual_input_tokens=null`
- `actual_output_tokens=null`
- `actual_total_tokens=null`
- `live_usage_available=false`

## Safety Checklist

`GET /personal-ai-gateway/safety` returns all safety flags as true:

- mock-first enabled
- live provider disabled by default
- provider secret hidden
- manual approval required
- lawyer review required
- draft-only output
- no final legal opinion
- no final report
- no external delivery
- source trace required
- audit log enabled
- token usage metadata enabled

## Frontend Page

The page at `/personal-ai-gateway` includes:

- Gateway Hero.
- Provider Cards.
- Prompt Template Registry.
- Prompt Render Preview Form.
- Mock AI Run Form.
- Runs, Audit, and Token Usage sections.
- Safety Panel.
- Developer Diagnostics collapsed by default.

The UI does not show API keys, raw content, local paths, or debug stacks, and it does not claim to replace lawyers or generate final legal opinions.

## Personal Production Integration

The Personal Production registry now marks the AI Model Runtime as `gateway_registered=true` with `target_route=/personal-ai-gateway`.

Provider capability preview points OpenAI, DeepSeek, and Local Model metadata to the AI Gateway. Live runtime count remains `0`, and real provider calls remain disabled.

## Regression Updates

The regression suite adds `scripts/regression/check_personal_ai_gateway_apis.sh` and includes it in `run_personal_alpha_regression.sh`.

The v7.1 script checks status, providers, prompt templates, prompt preview, mock run, audit, token usage, and safety metadata. It also checks that responses do not expose raw content, local paths, secrets, `.env`, runtime paths, or final output flags.

## No Live Provider Call

v7.1 is intentionally mock-first and controlled-first. No live OpenAI, DeepSeek, or Local Model call is executed.

## No Final Legal Opinion

All AI output remains draft-only and requires lawyer review. v7.1 does not generate final legal opinions.

## No Final Report

v7.1 does not generate final report text and does not enable external delivery.

## v7.2 Readiness

The next recommended stage is Controlled Material Parsing & PaddleOCR Runtime:

- Material Parser Runtime.
- MinerU and Docling placeholders.
- PaddleOCR controlled OCR runtime.
- OCR job create/status/result preview.
- OCR confidence metadata.
- OCR review queue.
- Source trace required.
- Lawyer and manual review required.
