# Legal-Tech UI/UX Polish v7.24

## Scope

v7.24 polishes the Personal Production page matrix with a unified legal-tech workbench style:

- `/personal-production`
- `/personal-showcase-pack`
- `/personal-delivery-packet`
- `/personal-case-production`
- `/personal-skill-studio`
- `/personal-intelligence`
- `/personal-material-runtime`
- `/personal-ai-gateway`
- `/personal-case-analysis`
- `/personal-case-workspace`
- `/personal-production-pilot`
- `/personal-owner-output-center`

No backend business logic, provider behavior, export behavior, final legal opinion flow, final report flow, email flow, or external delivery flow is added.

## Product Design Loop

Product Design tool status: no callable Product Design get-context / ideation / prototype brief tool was available in the current Codex environment, so v7.24 used a local design audit and prototype brief.

Considered directions:

1. 判例档案室型：good for long reading and documentation, but less suitable for active runtime and gate operations.
2. 混合工作台型：best fit for the current Personal Production stage because it supports page heroes, runtime cards, status cards, steppers, safety badges, owner-only downloads, and diagnostics without feeling like a debug console.
3. 风控指挥台型：strong for dashboard-heavy pages, but too narrow for drafting, Skill, material, and output-center workflows.

Chosen direction: 混合工作台型 legal-tech UI.

## UI Changes

- Shared badge language now uses five standard safety badges:
  - 受控运行
  - 仅模拟结果
  - 律师复核必需
  - 来源可追踪
  - 不自动对外交付
- Shared status cards, runtime cards, steppers, trust / safety panels, diagnostics, and info rows use a more product-like legal-tech presentation.
- Diagnostics default title is Chinese and remains folded by default.
- Stepper final stages show: `不会触发真实导出/最终报告/最终法律意见`.
- User-facing visible copy is Chinese by default, while API field names and folded diagnostic JSON may remain English.
- Sensitive visible strings were removed from the target Personal Production page copy.

## Safety Boundary

v7.24 remains:

- mock-first
- metadata-only
- draft-only
- owner-only where output/download workflows are involved
- provider-gated
- lawyer-review-required
- source-trace-required

v7.24 does not:

- call real providers
- read keys
- read real case materials
- expose raw materials or local paths
- generate final legal opinions
- generate final reports
- create real PDF/DOCX files
- send email
- create public links
- trigger external delivery
- publish Skills

## Regression

`scripts/regression/check_personal_ui_polish.sh` is upgraded for v7.24. It verifies:

- target page files exist
- shared Personal Production UI components exist
- five standard safety badges are present
- diagnostics remain folded by default
- Trust / Safety panel copy is complete
- Stepper final-stage safety wording is present
- target frontend pages do not contain visible sensitive/local markers
- target frontend pages keep Chinese safety copy

`scripts/regression/run_personal_alpha_regression.sh` continues to run the UI polish check as part of the large-stage regression suite.
