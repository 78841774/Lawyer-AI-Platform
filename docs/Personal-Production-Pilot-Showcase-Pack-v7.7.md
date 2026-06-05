# Personal Production Pilot & Showcase Pack v7.7

## Positioning

Personal Production Pilot & Showcase Pack organizes the v7.3-v7.6 personal production stack into a controlled, demo-friendly showcase surface. It is intended for internal pilot validation, screenshots, recordings, and non-technical walkthroughs.

Chinese UI title:

- 个人生产试点与展示包

Route:

- `/personal-showcase-pack`

Backend API prefix:

- `/personal-showcase-pack`

## Product Design Direction

v7.7 implements Product Design direction C: Story Flow.

The page presents:

- Hero and safety badges.
- Trust / Safety panel.
- Pilot sample cards.
- Story Flow Stepper:
  - 案件录入
  - 材料处理
  - AI 草稿
  - 法律/企业信息核验
  - 技能沉淀
  - 交付包
  - 最终锁定
- Showcase metrics.
- Source Trace coverage metadata.
- Lawyer Review and Final Lock metadata.
- Safety checklist.
- Developer Diagnostics, collapsed by default.

Direction C also incorporates:

- Direction A trust and safety presentation.
- Direction B pilot sample cards and readiness metadata.

## Scope

v7.7 covers:

- Showcase runtime registry metadata.
- Low-risk mock pilot sample metadata.
- Story Flow metadata across v7.3-v7.6 capabilities.
- Trust and safety metadata.
- Showcase metrics metadata.
- Audit timeline metadata.
- Safe record id access for runtime metadata reads.
- Sensitive mock metadata text blocking for local paths, secret-like tokens, runtime storage references, and raw-material markers.
- Personal Production Console integration.
- Regression checks for the showcase API surface.

## Safety Boundary

v7.7 remains:

- mock-first.
- controlled-first.
- provider-gated.
- metadata-only.
- draft-only.
- synthetic-demo-only.
- lawyer-review-required.
- final-lock-required.
- source-trace-required.

v7.7 does not:

- call real providers.
- read API keys.
- read raw case materials.
- expose raw content.
- expose local paths.
- use real customer, case, judgment, or company information.
- generate final legal opinions.
- generate final reports.
- generate real PDF/DOCX files.
- send email.
- trigger external delivery.
- automatically publish Skills.

## API Surface

- `GET /personal-showcase-pack/status`
- `GET /personal-showcase-pack/runtimes`
- `GET /personal-showcase-pack/runtimes/{runtime_id}`
- `POST /personal-showcase-pack/pilot-samples/mock`
- `GET /personal-showcase-pack/pilot-samples`
- `GET /personal-showcase-pack/pilot-samples/{pilot_sample_id}`
- `POST /personal-showcase-pack/story-flows/mock`
- `GET /personal-showcase-pack/story-flows`
- `GET /personal-showcase-pack/story-flows/{story_flow_id}`
- `GET /personal-showcase-pack/metrics`
- `GET /personal-showcase-pack/trust-panel`
- `GET /personal-showcase-pack/audit`
- `GET /personal-showcase-pack/safety`

## Personal Production Integration

Personal Production now registers:

- `showcase_pack_runtime`
- `pilot_sample_runtime`
- `story_flow_runtime`
- `showcase_metrics_runtime`
- `trust_panel_runtime`

The `/personal-production` page includes a `个人生产试点与展示包` workflow step, readiness card, and runtime registry grouping.

## Validation

Validation commands:

- backend compileall including `personal_showcase_pack`
- frontend build
- `bash scripts/regression/check_personal_showcase_pack_apis.sh`
- `CASE_ID=case_v55_approve_all bash scripts/regression/run_personal_alpha_regression.sh`
- `git diff --check`
- docs not empty check
- runtime storage ignore check
- sensitive path status check
- local security review for secrets, raw content, local paths, live provider calls, final output generation, and external delivery triggers

## Local Validation State

v7.7 is implemented for local validation and release preparation. It is not committed, tagged, pushed, or released until the user explicitly approves commit and release work.
