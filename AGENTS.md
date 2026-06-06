# Coding Agent Guide

## Current Direction

AIHome.law / Lawyer-AI-Platform is prioritizing personal production validation and showcase-ready presentation. Team workspace and external client delivery versions are deferred.

## Required Context

Read these files before substantial work:

- `00-Project-Context/CURRENT_STATE.md`
- `00-Project-Context/ROADMAP.md`
- `00-Project-Context/PROVIDER_ROADMAP.md`
- `00-Project-Context/SAFETY_BOUNDARY.md`
- `00-Project-Context/RELEASE_INDEX.md`
- `00-Project-Context/CODEX_HANDOFF.md`
- `00-Project-Context/NEXT_TASK.md`

## Safety Boundary

- mock-first by default
- controlled-first
- provider-gated
- manual-approval-required
- lawyer-review-required
- draft-only
- source-trace-required
- no automatic final legal opinion
- no automatic final report
- no automatic external delivery
- no automatic Skill publish
- no uncontrolled raw content exposure
- provider secrets never visible
- live provider calls disabled unless explicitly enabled in the target version

## Forbidden

- Do not reset the repository.
- Do not checkout over user changes.
- Do not call real providers.
- Do not read API keys.
- Do not return API keys.
- Do not expose raw case materials.
- Do not commit `.env`, `local.db`, `storage/runtime`, `node_modules`, `__pycache__`, `.DS_Store`, or real case materials.
- Do not mark AI output as final legal opinion.
- Do not generate final report text unless the target version explicitly permits it.

## Pre-Commit Checks

Before committing, run:

- backend compileall
- frontend build
- API smoke checks for the active version
- Personal Production regression checks
- full regression suite when feasible
- `git diff --check`
- sensitive-file status checks

## Current Next Task

Next Task: run unified v7.10-v7.24 validation, final security audit, and release preparation only after the user explicitly confirms large-stage release handling, or continue to a later personal-version sub-stage only after explicit user instruction. Do not commit, tag, push, or release until then.

## Codex Surgical Development Rules

This project follows a surgical development discipline for all Codex-assisted work. These rules are inspired by lightweight AI coding-agent guidance and are mandatory for this repository.

### Core Principles

1. **Read context before editing**
   - Read `AGENTS.md`, `00-Project-Context/CURRENT_STATE.md`, `ROADMAP.md`, `PROVIDER_ROADMAP.md`, `NEXT_TASK.md`, `CODEX_HANDOFF.md`, and the relevant docs/changelog for the current version.
   - Inspect existing modules, schemas, API clients, types, regression scripts, and shared UI components before adding new code.

2. **Do only the current task**
   - Implement only the current version or current instruction.
   - Do not jump to the next version.
   - Do not add speculative features.
   - Do not turn a narrow task into a broad rewrite.

3. **Prefer existing structure**
   - Reuse existing runtime modules, services, schemas, routers, API clients, types, shared UI components, and regression patterns.
   - Add new modules only when the concept boundary is clearly independent.
   - Do not duplicate existing business logic.

4. **Make surgical changes**
   - Modify the smallest necessary set of files.
   - Avoid unrelated refactors.
   - Avoid formatting-only churn.
   - Avoid renaming files, APIs, fields, or components unless the task requires it.

5. **Do not invent new systems when existing materials exist**
   - For Skill work, first read existing Skill files, Experience Packages, evaluation files, gate files, test cases, prompt templates, and pattern files.
   - Do not invent a new Skill taxonomy, evaluation system, or gate system if a prior baseline exists.
   - Preserve lineage using fields such as `source_skill_id`, `source_package_id`, `derived_from`, `source_evaluation_files`, and `source_gate_files`.

6. **Keep safety boundaries intact**
   - Never read or expose API keys.
   - Never put `.env`, `local.db`, `storage/runtime`, `node_modules`, `__pycache__`, `.DS_Store`, raw OCR text, raw case material, customer data, or local absolute paths into Git.
   - Never write raw case content to docs, changelog, README, Project Context, AGENTS, Developer Diagnostics, regression stdout, error stacks, or browser console.
   - Keep provider calls gated and disabled by default unless a task explicitly enables a controlled live path.
   - Keep source trace, lawyer review, audit, owner-only access, and final lock boundaries explicit.

7. **Training and practical case analysis must stay separated**
   - Closed cases may be used for training after the required processing and redaction rules.
   - Open/unresolved cases are for practical analysis only.
   - Open-case outputs must not automatically write to training sets.
   - Open-case outputs must not automatically update or publish Skills.
   - Any future training use from practical work requires manual selection, appropriate processing, and confirmation.

8. **Evaluation and gates are reference-only unless explicitly stated otherwise**
   - Evaluation and gate outputs provide quality scores and optimization suggestions.
   - They must not block next-stage execution by default.
   - Use `gate_reference_only=true` and `blocks_next_stage=false` for current personal-production workflows unless a task explicitly changes this boundary.

9. **Owner-only output boundary**
   - Generated drafts and final Skill drafts may be viewable or downloadable by the owner only.
   - The system must not automatically create public links, send email, upload to third parties, deliver to clients, submit to courts, or mark drafts as final legal opinions or formal lawyer reports.
   - Use fields such as `owner_only=true`, `downloadable_by_owner_only=true`, `public_link_created=false`, `email_sent=false`, and `external_delivery_triggered=false`.

10. **Validate only what the task requires**
    - Run the lightweight checks requested for the current task.
    - Run backend compileall when backend Python changes.
    - Run frontend build when frontend code changes.
    - Run relevant API smoke/regression scripts when endpoints change.
    - Full Personal Alpha regression and full security audit are reserved for explicit final validation phases.

### Required Completion Report

Every Codex task must end with a concise report containing:

1. Changed files.
2. What was implemented.
3. What was intentionally not changed.
4. Safety boundaries preserved.
5. Lightweight checks run and results.
6. Current `git status --short`.
7. Whether the next step is recommended.
8. Confirmation that no commit/tag/push was performed unless explicitly requested.

## v7.10 Personal Version Notes

- Keep the `个人生产` AppShell group as the primary route for v7.x showcase work.
- Keep Developer Diagnostics folded by default.
- Use shared Personal Production UI components for safety badges, Trust / Safety panels, steppers, status cards, and diagnostics where practical.
- Keep frontend display copy Chinese by default while allowing API field names and diagnostics JSON to remain English.
- Keep demo, promotional material, and public-facing README copy mock-first, metadata-only, lawyer-review-required, source-trace-required, and provider-gated.
- Do not describe mock samples as real cases or imply automatic external delivery.
- Team Workspace is deferred.
- External Client Delivery is deferred.
- AI Provider Live Gateway, OCR / Document Provider Live Gateway, Legal / Enterprise API Live Gateway, Skill Training, Controlled Case Analysis, Personal Real AI Gated Pilot, and Fact Preview & Correction Workbench are personal-version phases and must remain gated by safety review.
- For v7.11-v7.24, use a continuous large-stage cadence: basic checks per sub-stage, final comprehensive Codex Security audit only after the whole large stage is implemented and baseline validation passes.

## v7.11 Local Pilot Notes

- Keep backend on port 8001 and frontend on port 3001 for local pilot flows.
- Avoid backend reload for the local pilot startup helper.
- Use safe Chinese fallback states when APIs are unavailable.
- Do not surface backend stack traces, local paths, provider details, API keys, or raw content in frontend error messages.
- Keep live provider disabled until a later explicitly gated version enables it.

## v7.12 AI Live Gateway Notes

- Live mode is disabled by default through `AI_LIVE_MODE_ENABLED=false`.
- Provider live_enabled remains false unless the global gate, provider gate, key_loaded, and explicit confirmations are all satisfied.
- API keys are checked only in backend environment lookup and must never be returned to frontend responses.
- Dry-run must not call a provider.
- Gated live run must return blocked metadata when confirmations are missing or provider adapter is unavailable.
- AI output is draft metadata only and must require lawyer review and source trace.

## v7.13 OCR / Document Live Gateway Notes

- OCR live mode is disabled by default through `OCR_LIVE_MODE_ENABLED=false`.
- Document live mode is disabled by default through `DOCUMENT_LIVE_MODE_ENABLED=false`.
- Provider live_enabled remains false unless the global gate, provider gate, backend key_loaded boolean metadata, and explicit confirmations are all satisfied.
- API keys are checked only in backend environment lookup and must never be returned to frontend responses.
- Document dry-run and OCR dry-run must not call a provider.
- Gated live runs must return blocked metadata when confirmations are missing, and `provider_adapter_unavailable` when the adapter is not implemented.
- Raw OCR text and raw document content are blocked by default and must not be injected into AI prompts.
- OCR / document metadata must not trigger fact extraction, legal analysis, final legal opinions, final reports, email sending, real final PDF/DOCX generation, or external delivery.
- Review queue actions are metadata-only. `approve_metadata_only` does not allow raw content into AI prompts.

## v7.14 Legal / Enterprise API Live Gateway Notes

- Legal live mode is disabled by default through `LEGAL_LIVE_MODE_ENABLED=false`.
- Enterprise live mode is disabled by default through `ENTERPRISE_LIVE_MODE_ENABLED=false`.
- API keys are checked only in backend environment lookup and must never be returned to frontend responses.
- Legal and enterprise dry-runs must not call providers.
- Legal / enterprise results remain metadata candidates and are not final citations.
- Raw legal results and raw enterprise results must not be injected into AI prompts.

## v7.15 Skill Training Runtime Notes

- Training samples must remain desensitized metadata.
- Manual confirmation, lawyer review, and source trace are required.
- Skill output is draft metadata only.
- Skill Training Runtime must not trigger AI prompts, real training, final Skill publishing, final legal opinions, final reports, email sending, or external delivery.

## v7.16 Controlled Case Analysis Runtime Notes

- v7.16 is the open-case execution stage, not the closed-case training stage.
- Training and execution must remain separated.
- It may reference `case_fact_extraction_skill` and `case_legal_analysis_skill` metadata from v7.15.
- If Skill baseline metadata is incomplete, report missing baseline metadata and use placeholder lineage only.
- v7.16 must not generate training data, write to training sets, update Skills, publish Skills, or create Experience Packages.
- Fact and legal analysis output must remain draft metadata only.
- Evaluation and gate are reference-only and must not block the next stage.
- No raw material, raw OCR text, API key, final legal opinion, final report, real PDF/DOCX, email, or external delivery is allowed.

## v7.17 Personal Production Pilot Notes

- v7.17 connects the core v7.10-v7.24 Personal Live Intelligence & Controlled Case Analysis large stage into one gated pilot route.
- It connects AI, OCR / document, legal / enterprise, Skill Training metadata, Controlled Case Analysis metadata, Delivery Packet metadata, and owner-only download metadata into one gated pilot route.
- Live providers remain disabled by default and require explicit confirmation before live-provider eligibility.
- Provider adapter gaps must return gated / adapter-unavailable metadata, not fake success.
- Skill final drafts are owner-only metadata and must not be auto-published.
- Open-case execution must not generate training data, write to training sets, update Skills, or publish Skills.
- Owner downloads may be represented as Markdown / JSON / PDF draft / DOCX draft metadata, but must not create public links, send email, upload to third-party systems, or trigger external delivery.
- Generated drafts must not be labeled as final legal opinions or formal lawyer reports.
- Raw case material and OCR text must not appear in Git, docs, Project Context, README, AGENTS, diagnostics, regression output, public showcase pages, or frontend console output.

## v7.18 Case Workspace Notes

- v7.18 adds the owner-only personal case and material workspace route `/personal-case-workspace`.
- Case and material lists, material detail, OCR status, fact input, correction, source trace, audit, and safety outputs must remain metadata-only and draft-only.
- Owner raw view actions require explicit owner confirmation but still must not return real raw content from API responses.
- Raw material, OCR text, local paths, API keys, real customer / case / judgment / enterprise information, and secret values must not appear in frontend UI, Developer Diagnostics, docs, Project Context, README, AGENTS, regression output, or Git.
- v7.18 must not trigger AI prompts, provider calls, training data generation, training set writes, Skill updates, Skill publishing, final legal opinions, final reports, real PDF/DOCX generation, email, public links, or external delivery.

## v7.19 Pilot Dashboard Notes

- v7.19 enhances `/personal-production-pilot` with dashboard status, metrics, quality score cards, gate status, optimization suggestions, review queue, source trace summary, export boundary, and unified safety presentation.
- Quality scores, gate status, and optimization suggestions are reference-only mock metadata and must not be described as real case quality, legal correctness guarantees, final legal opinions, formal reports, or external delivery readiness.
- Dashboard outputs must stay owner-only, metadata-only, draft-only, dry-run default, source-trace-required, audit-required, and lawyer-review-required.
- No provider call, API key access, real material reading, raw content exposure, public link, email, final legal opinion, final report, real PDF/DOCX, Skill publish, or external delivery is allowed.

## v7.20 Fact Preview & Correction Notes

- v7.20 enhances `/personal-case-workspace` as the owner-only fact preview and correction workbench.
- Fact previews, corrections, version history, quality scores, gates, source traces, audit, safety, and legal-analysis-input readiness must remain metadata-only and draft-only.
- Users may confirm fact metadata as legal analysis input, but this must not auto-trigger legal analysis.
- Quality scores and gates are reference-only and must not be described as final fact findings, legal correctness guarantees, final legal opinions, formal reports, or delivery readiness.
- Fact correction must not generate training data, write to training sets, update Skills, publish Skills, generate final fact findings, generate final legal opinions, generate final reports, create real PDF/DOCX, send email, create public links, or trigger external delivery.

## v7.21 Legal Analysis Draft Notes

- v7.21 adds `/personal-case-analysis/legal-drafts` as the owner-only legal analysis draft workbench.
- Legal analysis draft output must remain metadata-only and draft-only.
- Legal analysis draft readiness must not be described as a final legal opinion, final report, formal lawyer work product, or delivery readiness.
- Quality scores and gates are reference-only and must not block the next stage.
- Legal drafts must not read raw materials, expose local paths, read API keys, generate training data, write training sets, update Skills, publish Skills, generate final legal opinions, generate final reports, create real PDF/DOCX, send email, create public links, or trigger external delivery.

## v7.22 Skill Final Draft Notes

- v7.22 adds `/personal-skill-studio/final-drafts` as the owner-only workbench for `case_fact_extraction_skill` and `case_legal_analysis_skill` final draft metadata.
- Baseline discovery must read existing Skill Studio, Controlled Case Analysis, Fact Preview, Legal Draft, docs, and Project Context metadata; do not invent a new evaluation system or overwrite existing Skills.
- If baseline metadata is incomplete, return `baseline_complete=false`, missing baseline metadata, and placeholder lineage only.
- Gate and quality outputs are reference-only and must keep `blocks_next_stage=false`.
- Owner downloads are metadata-only; do not create public links, send email, publish Skills, train on open cases, write training sets, generate final legal opinions, generate final reports, create real PDF/DOCX, or trigger external delivery.

## v7.23 Owner-only Output Center Notes

- v7.23 adds `/personal-owner-output-center` as the 用户本人产出下载中心.
- It aggregates Skill final drafts, fact outputs, legal analysis drafts, and Pilot / Delivery drafts into owner-only output registry metadata.
- All outputs must keep `owner_only=true`, `downloadable_by_owner_only=true`, `draft_or_metadata=true`, `public_link_created=false`, `email_sent=false`, and `external_delivery_triggered=false`.
- Mock owner downloads may expose Markdown / JSON / PDF draft metadata / DOCX draft metadata options, but must not create real files, public links, email, third-party upload, client delivery targets, final legal opinions, or formal lawyer reports.
- Gate and quality outputs are reference-only and must not block owner-only downloads or trigger Skill publishing, training, final reports, final legal opinions, public links, email, or external delivery.
- The next step is v7.10-v7.24 unified validation after user confirmation or a later personal-version sub-stage only after explicit instruction.

## v7.24 Legal-Tech UI/UX Polish Notes

- v7.24 upgrades Personal Production pages with a mixed legal-tech workbench style.
- Standard visible badges are: 受控运行、仅模拟结果、律师复核必需、来源可追踪、不自动对外交付。
- Diagnostics remain folded by default and visible diagnostics copy should be Chinese.
- Stepper final stages must state: 不会触发真实导出/最终报告/最终法律意见。
- UI copy must not visibly expose local paths, key values, raw material, real customer/case/judgment/enterprise information, or secret values.
- v7.24 must not add backend business logic, provider calls, final legal opinions, final reports, real PDF/DOCX files, email, public links, Skill publishing, or external delivery.

## Product Design Closed Loop

For UI polish, Showcase work, promotional pages, Demo pages, Landing pages, README visual alignment, frontend styling, screenshots, or recording experience, Product Design must be treated as a closed loop:

1. Design input: use Product Design get-context / ideation / prototype brief when available, output 2-3 directions, and recommend one direction.
2. Design choice: state the chosen direction, why it fits the current stage, and why the other directions are not used.
3. Code implementation: convert the chosen direction into React / TypeScript / Tailwind code. Prefer shared components over one-off page edits. Reuse or upgrade SafetyBadge, StatusCard, RuntimeCard, ShowcaseStepper, TrustSafetyPanel, DiagnosticsPanel, and AppShell navigation where practical.
4. Visible change: at least one visible change must land in the web UI, such as a stronger Hero, clearer cards, improved Stepper, more visible Trust / Safety Panel, clearer AppShell navigation, more product-like Chinese copy, smoother screenshot / recording route, or reduced debug-console feel.
5. Browser validation: after frontend changes, start backend and frontend when the environment permits, open target pages with Browser or Computer Use, confirm pages load, confirm the design change is visible, confirm Diagnostics are folded by default, and check that raw content, API keys, and local paths are not shown.
6. Final report: include whether Product Design was actually callable, the chosen design direction, changed components, pages with visible UI changes, previous UI problem, resulting effect, browser validation result, and remaining UI issues.

Do not claim Product Design is complete based only on ideation, prototype brief, or suggestions. If the design is not visible in React / Tailwind and not checked in a browser-capable environment, report it as design planning only.
