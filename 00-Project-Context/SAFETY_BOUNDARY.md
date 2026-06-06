# Safety Boundary

The project safety posture is:

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
- owner-only case/material raw view gated by explicit confirmation
- fact preview correction owner-only and metadata-only
- fact legal-analysis-input readiness does not auto-trigger legal analysis
- legal analysis draft workbench outputs draft metadata only
- Skill final draft workbench outputs owner-only metadata only
- owner-only output center aggregates draft metadata for user-only viewing and download
- dashboard quality scores are reference-only metadata
- legal-tech UI polish must not show raw material, local paths, or key values in visible Personal Production pages
- provider secrets never visible
- live provider calls disabled unless explicitly enabled in the target version

## Forbidden By Default

- Do not call real providers.
- Do not read API keys.
- Do not return API keys.
- Do not expose raw case materials.
- Do not write raw case materials or OCR text into Git, docs, Project Context, README, AGENTS, diagnostics, regression output, frontend console output, or AI prompts by default.
- Do not label AI output as final legal opinion.
- Do not generate final report content without the target version explicitly allowing it.
- Do not publish Skills automatically.
- Do not describe pilot dashboard scores, gates, or optimization suggestions as final legal conclusions, correctness guarantees, or delivery readiness.
- Do not describe fact preview scores, gates, corrections, or legal-analysis-input readiness as final fact findings, legal conclusions, final opinions, final reports, or automatic permission to proceed.
- Do not allow fact correction to generate training data, write training sets, update Skills, publish Skills, create real files, send email, create public links, or trigger external delivery.
- Do not describe legal analysis drafts, quality scores, gates, or review readiness as final legal opinions, final reports, formal lawyer work product, or delivery readiness.
- Do not describe Skill final draft quality scores, gates, optimization suggestions, or owner downloads as automatic Skill publication, training completion, legal correctness guarantees, final legal opinions, formal reports, or external delivery readiness.
- Do not allow Skill final draft owner downloads to create public links, send email, publish Skills, train on open cases, write training sets, create real PDF/DOCX files, or trigger external delivery.
- Do not allow Owner-only Output Center downloads to create real export files, public links, email, third-party uploads, client delivery targets, final legal opinions, formal lawyer reports, Skill publishing, open-case training data, training-set writes, or external delivery.
- Do not let UI polish convert draft metadata into final legal work product, final report readiness, real export readiness, public delivery readiness, or provider live eligibility.
