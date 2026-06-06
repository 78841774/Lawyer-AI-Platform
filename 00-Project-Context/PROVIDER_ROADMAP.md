# Provider Roadmap

## Provider Categories

- AI: OpenAI, DeepSeek, Local Model.
- OCR: PaddleOCR / Baidu AI Studio.
- File Parsing: MinerU, Docling.
- Legal Search: Kuaicha 365 LawSkills API.
- Enterprise Info: Tianyancha AI.
- Optional: Qichacha, PKULaw, National Law Database.

## Version Scope

- v7.1 only builds the AI Gateway for AI provider metadata, prompt rendering preview, and draft-only mock AI runs.
- v7.2 introduces MinerU, Docling, and PaddleOCR placeholders for Controlled Material Parsing and OCR runtime foundations.
- v7.3 builds Kuaicha 365 LawSkills API and Tianyancha AI gateway foundations.
- v7.4 builds Experience Package Skill Studio foundations without automatic Skill publishing.
- v7.5 builds Real Case Production Workflow foundations without final report generation or external delivery.
- v7.6 builds Personal Delivery Packet foundations without live provider calls, final legal opinion generation, final report generation, real PDF/DOCX generation, email sending, or external delivery.
- v7.7 builds Personal Production Pilot & Showcase Pack foundations without live provider calls, API key access, raw content exposure, final legal opinion generation, final report generation, real PDF/DOCX generation, email sending, external delivery, or Skill publishing.
- v7.8 does not add provider runtime scope. It unifies UI polish, Trust / Safety presentation, diagnostics folding, and showcase navigation while preserving provider-gated behavior.
- v7.9 does not add provider runtime scope. It packages demo scripts, screenshot routes, README display copy, one-pager copy, deck outline, visual brief, and promotional safety checks.
- v7.10 does not add provider runtime scope. It polishes personal-version public demo readiness, README copy, homepage entry, and safety-boundary presentation.
- v7.12 is the AI Provider Live Gateway foundation. It adds dry-run and gated live run metadata while live mode remains disabled by default. It must remain provider-gated, lawyer-review-required, source-trace-required, draft-only, and manually approved.
- v7.13 OCR / Document Provider Live Gateway is complete in the current uncommitted large-stage worktree. It adds dry-run and gated live run metadata for OCR and document providers while live modes remain disabled by default. OCR raw content and document raw content must not automatically enter AI prompts.
- v7.14 Legal / Enterprise API Live Gateway is complete in the current uncommitted large-stage worktree. Results remain source-traced metadata candidates, not final citations.
- v7.15 Skill Training Runtime is complete in the current uncommitted large-stage worktree. Training data remains desensitized, manually confirmed, and never auto-published.
- v7.16 Controlled Case Analysis Runtime is complete in the current uncommitted large-stage worktree. Open-case analysis remains draft-only, lawyer-review-required, source-trace-required, and separated from training data generation.
- v7.17 Personal Production Pilot with Real AI Gated Mode is complete in the current uncommitted large-stage worktree. It integrates AI, OCR / document, legal / enterprise, Skill Training metadata, Controlled Case Analysis metadata, Delivery Packet metadata, and owner-only download metadata into one gated pilot while live providers remain disabled by default.
- v7.18 Case Intake & Material Workspace Hardening is complete in the current uncommitted large-stage worktree. It adds owner-only case and material workspace metadata without reading real case materials or returning raw content.
- v7.19 Personal Production Pilot Dashboard Enhancement is complete in the current uncommitted large-stage worktree. It adds dashboard metrics, reference-only quality scores, gate status, optimization suggestions, source trace summary, export boundary, and safety presentation without changing provider live mode.
- v7.20 Fact Preview & Correction Workbench is complete in the current uncommitted large-stage worktree. It adds owner-only fact preview, correction, version, quality, gate, source trace, audit, safety, and legal-analysis-input-readiness metadata without changing provider live mode.
- v7.21 Legal Analysis Draft Workbench is complete in the current uncommitted large-stage worktree. It adds legal analysis draft, version, quality, gate, review confirmation, source trace, audit, and safety metadata without changing provider live mode.
- v7.22 Skill Final Draft & Optimization Workbench is complete in the current uncommitted large-stage worktree. It adds owner-only Skill final draft metadata, baseline discovery, lineage, reference-only quality / gate, optimization, source trace, audit, safety, and owner-only download metadata without changing provider live mode.
- v7.23 Owner-only Output Center is complete in the current uncommitted large-stage worktree. It aggregates Skill final drafts, fact outputs, legal analysis drafts, and Pilot / Delivery drafts into owner-only output registry and download metadata without changing provider live mode.
- v7.24 Legal-Tech UI/UX Polish is complete in the current uncommitted large-stage worktree. It updates shared frontend presentation, visible Chinese safety copy, folded diagnostics, and UI regression coverage without changing provider live mode.

## Boundary

Provider metadata may be registered before live integrations exist. Live provider calls stay disabled unless the target version explicitly enables them behind controlled gates.

## Security Audit Cadence

For v7.11-v7.24, run basic checks at each sub-stage and defer the full Codex Security audit to the end of the large stage. The final audit must cover API key handling, raw content governance, provider live call gating, prompt boundaries, token/cost metadata, source trace, lawyer review, Skill training governance, open-case training separation, Skill final draft baseline discovery, Skill final draft owner-only downloads, no Skill auto-publish, no open-case training, owner-only case/material workspace, fact preview / correction boundaries, legal-analysis-input readiness without auto-triggering legal analysis, legal analysis draft boundaries, owner-only output center aggregation, owner-only downloads, dashboard quality-score boundaries, public-link / email / external-delivery restrictions, case analysis draft boundaries, final fact finding restrictions, final legal opinion restrictions, final report restrictions, frontend diagnostics, UI text safety, audit trail, and regression coverage.
