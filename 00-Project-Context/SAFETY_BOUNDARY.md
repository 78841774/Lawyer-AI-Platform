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
- provider readiness may show key_loaded boolean metadata but must never read or expose key values, prefixes, suffixes, or masked keys
- live provider calls disabled unless explicitly enabled in the target version
- v7.27-v7.29 provider connection surfaces remain provider-gated, dry-run by default, metadata-only, draft-only, and owner-only
- OCR / Document Provider Live Connection, Unified Personal Live Connection Dashboard, and Legal / Enterprise API Live Connection do not automatically generate final legal opinions, final reports, real PDF/DOCX files, email, public links, or external delivery
- legal / enterprise provider results must enter source trace and lawyer review metadata and must not automatically become final citations or final fact findings
- Codex training artifact loader and Codex training runs are metadata-only and are not model fine-tuning
- closed-case training and open-case practical analysis must remain separated
- v7.31 training runs may use only closed-case or synthetic closed-case samples with redaction completed and raw content excluded
- v7.31a real closed-case training intake may prepare authorized closed-case metadata only and must complete redaction before future real closed-case Codex training
- open or unresolved cases must not be written into training sets

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
- Do not let Provider Readiness or dry-run health checks call provider networks, upload case materials, read key values, expose masked keys, or imply live provider eligibility.
- Do not let v7.27 OCR / Document provider dry-runs upload materials, expose raw OCR text, expose raw document content, or inject raw content into AI prompts.
- Do not let v7.28 Unified Personal Live Connection Dashboard execute provider calls or expose raw provider responses.
- Do not let v7.29 Legal / Enterprise API Live Connection convert legal search candidates into final citations or enterprise lookup metadata into final fact findings.
- Do not let v7.30 training artifact loader execute real training, use open cases, write training sets, update Skills, publish Skills, or load raw case content.
- Do not let v7.31 Codex training runs use open/unresolved cases, raw OCR, real unredacted materials, provider calls, key values, local paths, real identity data, or automatic Skill publishing.
- Do not let v7.31a real closed-case intake execute Codex training, read or return raw content, use open/unresolved cases, write training sets, call providers, read key values, expose local paths, update Skills, publish Skills, generate final legal opinions, generate final reports, create public links, send email, or trigger external delivery.
- Do not let practical open-case outputs generate training data, write training sets, update Skills, or publish Skills automatically.
