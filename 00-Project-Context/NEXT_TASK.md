# Next Task

Next Task: v7.10-v7.24 unified validation after user confirmation, or user-confirmed continuation to a later personal-version sub-stage.

## Current Gate

v7.9 Personal Production Demo Script & Screenshot Pack is complete at commit `c59e137` and tag `v7.9-personal-production-demo-pack`.

v7.10 Personal Version Polish & Public Demo Readiness, v7.11 Personal Production Stability & Local Pilot Hardening, v7.12 AI Provider Live Gateway, v7.13 OCR / Document Provider Live Gateway, v7.14 Legal / Enterprise API Live Gateway, v7.15 Skill Training Runtime, v7.16 Controlled Case Analysis Runtime, v7.17 Personal Production Pilot with Real AI Gated Mode, v7.18 Case Intake & Material Workspace Hardening, v7.19 Personal Production Pilot Dashboard Enhancement, v7.20 Fact Preview & Correction Workbench, v7.21 Legal Analysis Draft Workbench, v7.22 Skill Final Draft & Optimization Workbench, v7.23 Owner-only Output Center, and v7.24 Legal-Tech UI/UX Polish are complete in the current uncommitted large-stage worktree.

Do not commit, tag, push, or release until the full large stage is ready and the user explicitly approves release handling.

## Completed Large-stage Sub-stages

- v7.10 Personal Version Polish & Public Demo Readiness.
- v7.11 Personal Production Stability & Local Pilot Hardening.
- v7.12 AI Provider Live Gateway.
- v7.13 OCR / Document Provider Live Gateway.
- v7.14 Legal / Enterprise API Live Gateway.
- v7.15 Skill Training Runtime.
- v7.16 Controlled Case Analysis Runtime.
- v7.17 Personal Production Pilot with Real AI Gated Mode.
- v7.18 Case Intake & Material Workspace Hardening.
- v7.19 Personal Production Pilot Dashboard Enhancement.
- v7.20 Fact Preview & Correction Workbench.
- v7.21 Legal Analysis Draft Workbench.
- v7.22 Skill Final Draft & Optimization Workbench.
- v7.23 Owner-only Output Center.
- v7.24 Legal-Tech UI/UX Polish.

## Unified Validation Goal

When the user confirms the large-stage implementation scope is complete, prepare v7.10-v7.24 for one combined validation, final security audit, and user-confirmed release path:

- backend compileall full
- frontend build
- all active API smoke regressions
- full Personal Alpha regression
- provider live boundary regression
- owner-only case/material workspace boundary regression
- fact preview / correction boundary regression
- legal-analysis-input readiness without auto-trigger regression
- legal analysis draft boundary regression
- Skill final draft baseline / owner-download / no-auto-publish boundary regression
- Owner-only Output Center output registry / owner-download / no-external-delivery boundary regression
- legal-tech UI/UX polish regression
- owner-download boundary regression
- pilot dashboard quality-score boundary regression
- UI visible-change verification
- docs / changelog / Project Context checks
- git diff check
- empty markdown check
- runtime ignore check
- sensitive path check
- final comprehensive Codex Security audit
- final diff review
- user-confirmed commit / tag / push / release handling

## Boundaries

- Team Workspace deferred.
- External Client Delivery deferred.
- Final comprehensive Codex Security audit deferred until the large-stage implementation and baseline validation are complete.
- Do not call real providers unless a gated target version explicitly enables adapter eligibility and the user authorizes it.
- Do not read API keys.
- Do not read or expose raw case materials.
- Do not generate final legal opinions.
- Do not generate final reports.
- Do not generate real final delivery files.
- Do not send email.
- Do not trigger external delivery.
- Do not automatically publish Skills.

Continue the Personal Live Intelligence & Controlled Case Analysis large stage only when the user explicitly requests the next sub-stage. Use compile/build/regression/smoke/basic safety checks at each sub-stage, and run one final comprehensive Codex Security audit after the implementation scope is complete before the combined release tag.
