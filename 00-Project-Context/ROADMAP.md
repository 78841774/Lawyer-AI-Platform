# Roadmap

## v7.x Personal Production Route

- v7.0 Personal Production Runtime & Showcase Foundation.
- v7.1 AI Provider Gateway & Prompt Runtime completed.
- v7.2 Controlled Material Parsing & PaddleOCR Runtime completed.
- v7.3 Legal & Enterprise Intelligence Gateway completed.
- v7.4 Experience Package Skill Studio completed.
- v7.5 Real Case Production Workflow completed as part of tag `v7.5-personal-production-workflow-stack`.
- v7.6 Personal Delivery Packet completed.
- v7.7 Personal Production Pilot & Showcase Pack completed and tagged.
- v7.8 UI Polish & Showcase Hardening completed and tagged.
- v7.9 Personal Production Demo Script & Screenshot Pack completed and tagged.
- v7.10-v7.24 Personal Practical Production Workbench completed and released as tag `v7.24-personal-practical-production-workbench`.
- v7.25 Personal Practical Case Trial Readiness is complete in the current uncommitted worktree.
- v7.26 Provider Live Readiness & Secret Boundary is complete in the current uncommitted worktree.
- v7.27 OCR / Document Provider Live Connection is complete in the current uncommitted worktree.
- v7.28 Unified Personal Live Connection Dashboard is complete in the current uncommitted worktree.
- v7.29 Legal / Enterprise API Live Connection is complete in the current uncommitted worktree.
- v7.30 Codex Training Scheme & Multi-Level Case-Cause Artifact Loader is complete in the current uncommitted worktree.
- v7.31 Execute Codex Training on Closed Case Samples is complete in the current uncommitted worktree.
- v7.31a Real Closed-Case Training Intake & Redaction Pipeline is complete at commit `86a0246` and tag `v7.31a`.
- v7.31b Raw Work-Product Controlled Processing Experience Pipeline is complete at commit `e22281f`.
- v7.31c Skill Experience Pool & Codex Skill Draft Builder is complete at commit `e22281f`.
- v7.31d Skill Package Versioning & System Validation Gate through v7.33 Case Analysis Skill Output Schema Driven Workbench Integration are complete at commit `01259cf`.
- v7.34 Case Analysis Output Feedback to Experience Improvement Candidate is complete at the `v7.37` tag target.
- v7.35 Training Dataset Builder & Training Gate is complete at the `v7.37` tag target and tag `v7.35`.
- v7.36 Codex Skill Training Dry Run is complete at the `v7.37` tag target and tag `v7.36`.
- v7.37 Codex Skill Internal Training Run is complete at the `v7.37` tag target and tag `v7.37`.
- v7.35a-v7.38 corrected raw-material-to-safe-training-skill chain is complete in the current uncommitted worktree.

## v7.25-v7.29 Practical Trial And Provider Alignment Cadence

v7.25-v7.29 continue the personal practical production route after the v7.24 stable release and remain local uncommitted large-stage work.

During each sub-stage, run necessary compile, build, smoke, regression, sensitive path, provider live boundary, and forbidden-copy checks. Do not run a full Codex Security audit ledger after every small feature unless the user requests final validation.

v7.25 adds trial readiness metadata. v7.26 adds the provider live readiness and secret boundary layer before true OCR / AI / legal / enterprise API connection. v7.27 adds OCR / Document Provider Live Connection through `personal_material_runtime.live_gateway` and `/personal-material-runtime/live/*`. v7.28 adds Unified Personal Live Connection Dashboard through `/personal-live-connection`. v7.29 adds Legal / Enterprise API Live Connection through `/personal-legal-enterprise`.

v7.30 adds Codex Training Scheme & Multi-Level Case-Cause Artifact Loader: synthetic multi-level case-cause taxonomy, experience package metadata, Skill metadata, evaluations, gates, test cases, loading manifest, fallback matching, and Skill Context dry-run. This is not fine-tuning model parameters.

v7.31 executes Codex training on synthetic closed-case samples and generates loadable metadata artifacts validated through the v7.30 loader dry-run.

v7.31a prepares authorized closed-case training material intake, redaction, case-cause classification, sample segmentation, review, source trace, audit, and safety metadata. It does not execute Codex training.

v7.31b adds controlled raw work-product parsing, OCR/document parse metadata, legal retrieval metadata, redacted experience candidates, manual review, source trace, audit, and safety.

v7.31c imports approved v7.31b experience candidates into a Skill Experience Pool, creates bindings, and generates non-publishable Codex Skill draft metadata requiring manual confirmation.

v7.31d packages confirmed v7.31c Skill Draft metadata into versioned Skill Package metadata and runs a system validation gate for redaction, approval, source trace, audit, manifest, structure, and sensitive metadata boundaries. Manual review of training output is not applicable in v7.31d; practice runtime load review is deferred to v7.31f.

v7.31e builds internal training task metadata and experience package metadata only from v7.31d system-validated Skill Packages. It outputs structured prompt / input-output pair metadata, preserves source trace and audit bundles, and leaves experience packages in `pending_practice_load_review` for v7.31f.

v7.31f preserves generated experience package metadata, lets lawyers edit experience cards, saves lawyer-approved package metadata, reruns system revalidation, and approves or rejects future practice runtime loading candidates. Actual controlled loading and monitoring are deferred to v7.31g.

v7.31g loads only v7.31f lawyer-approved package metadata into a controlled practice runtime registry with gray rollout, active rollout, scope limits, policy evaluation, usage monitoring, risk event metadata, source trace, audit, disable, and rollback controls.

v7.31h records practice output observation metadata, lawyer feedback metadata, feedback risk event metadata, rule-based classification, source trace, audit, and feedback summary for later iteration. Feedback recommendations do not automatically mutate loaded packages, disable, rollback, train, publish, or deliver anything.

v7.31i builds practice feedback candidate pack metadata only from triaged v7.31h feedback/risk/observation metadata. Candidate packs prepare later iteration and do not automatically mutate loaded packages or Skills.

v7.31j rebuilds next experience package draft metadata only from v7.31i ready candidate packs. Drafts may enter `pending_practice_load_review`, but they do not load into practice runtime without later review.

v7.32 consolidates the experience lifecycle across v7.31b-v7.31j through state, graph, audit timeline, source trace, integrity, and safety views. Recompute is view-level only.

v7.33 integrates the Case Analysis Skill Output Schema Driven Workbench. Backend schema defines fact extraction and legal analysis output groups; the frontend renders backend `output_groups` and does not hardcode output names, counts, or groups.

v7.34 maps v7.33 case-analysis output feedback, risk event, audit, and source trace metadata into experience improvement candidate metadata, output-to-experience traces, diff summaries, and readiness reports. It does not mutate loaded packages, lawyer-approved packages, output schemas, runtime packages, Skills, or training artifacts.

v7.35 builds Training Dataset Manifest metadata, abstracted Training Examples, Training Task Plan metadata, and a reference-only Training Gate Report from v7.34 candidates marked `ready_for_training_dataset_build`.

v7.36 runs a Codex Skill Training Dry Run simulation over v7.35 dataset and gate artifacts, with safe logs, audit, source trace, and gate summary metadata only.

v7.37 starts a controlled Codex Skill Internal Training Run metadata flow, records metrics, logs, dry-run comparison, audit, source trace, and gate report metadata, and keeps any generated run artifacts internal and metadata-only.

v7.35a adds controlled private parsing metadata for training materials, OCR/document parse checks, legal retrieval checks, rule alignment, and parse quality gates.

v7.35b generates redacted / abstracted experience packages with legal point summary, common fact extraction framework, case-cause-specific fact points, fact summary, diff readiness, audit, and source trace metadata.

v7.36 keeps compatibility aliases for the corrected Training Dataset Builder & Gate stage while preserving the completed v7.35 implementation.

v7.37 add-on generates a safe callable Training Skill Spec with OCR / Legal / Enterprise provider specs, credential aliases, `credential_loaded` state, gate requirements, output schema, prompt strategy, differentiated fact extraction experience package, audit, and source trace. Credential values are never stored in the Skill.

v7.38 connects the safe Training Skill Spec into dry-run / internal simulation metadata and produces a non-publishable, non-runtime-loadable artifact carrying the differentiated experience package, facts diff check, legal summary check, readiness, audit, and source trace.

v7.38b adds the Codex Panel Training Skill at `.agents/skills/lawyer-ai-training-skill/`. This is an agent workflow Skill for Codex training development and validation, not a business-system Training Skill Spec, production legal analysis Skill, runtime package, or registry-published Skill.

## Product Design Cadence

UI / Showcase / promotional / Demo / Landing / screenshot / recording work must use a Product Design closed loop. Product Design ideation or prototype brief is planning only until the chosen direction is implemented in React / TypeScript / Tailwind, produces a visible UI change, and is browser-validated when the environment permits.

## Later

- Team Workspace is deferred.
- External Client Delivery is deferred.

## Current Priority

Current execution priority is complete through v7.38b in the current uncommitted worktree. The next recommended action is lightweight validation / release preparation after explicit approval, or an explicitly scoped next personal-version sub-stage. Do not repeat v7.27-v7.38b implementations. Do not start Team Workspace or External Client Delivery before the user explicitly approves that direction.
