# Next Task

Next Task: v7.31d Skill Package Versioning & Pre-Publish Gate.

## Current Gate

v7.24 Personal Practical Production Workbench is complete at commit `b4e4bca`, tag `v7.24-personal-practical-production-workbench`, and release `v7.24 Personal Practical Production Workbench`.

v7.25-v7.31a are complete through commit `86a0246` and tag `v7.31a`. v7.31b-v7.31c are complete in the current local worktree:

- v7.25 Personal Practical Case Trial Readiness.
- v7.26 Provider Live Readiness & Secret Boundary.
- v7.27 OCR / Document Provider Live Connection.
- v7.28 Unified Personal Live Connection Dashboard.
- v7.29 Legal / Enterprise API Live Connection.
- v7.30 Codex Training Scheme & Multi-Level Case-Cause Artifact Loader.
- v7.31 Execute Codex Training on Closed Case Samples.
- v7.31a Real Closed-Case Training Intake & Redaction Pipeline.
- v7.31b Raw Work-Product Controlled Processing Experience Pipeline.
- v7.31c Skill Experience Pool & Codex Skill Draft Builder.

Do not commit, tag, push, or release until the user explicitly approves release handling.

## Completed Local Sub-stages

- v7.25 adds `/personal-trial-readiness` for trial readiness metadata.
- v7.26 adds `/personal-provider-readiness` for provider registry, secret boundary, live gate, usage / cost metadata, dry-run health, audit, and safety.
- v7.27 adds `personal_material_runtime.live_gateway` and `/personal-material-runtime/live/*` for OCR / Document provider dry-run, live gate, secret boundary, health, review, source trace, audit, and safety metadata.
- v7.28 adds `personal_live_connection` and `/personal-live-connection/*` for unified AI / OCR / Document / Legal / Enterprise provider readiness, secret boundary, live gate, usage / cost, health, audit, and safety metadata.
- v7.29 adds `personal_legal_enterprise_gateway` and `/personal-legal-enterprise/*` for legal search / enterprise lookup dry-run, live gate, secret boundary, review queue, source trace, audit, and safety metadata.
- v7.30 adds `personal_skill_studio.training_artifacts` and `/personal-skill-studio/training-artifacts/*` for Codex training scheme metadata, multi-level case-cause taxonomy, training artifact manifests, fallback matching, Skill Context dry-run, audit, safety, and regression metadata.
- v7.31 adds synthetic closed-case Codex training runs under `/personal-skill-studio/training-artifacts/training-runs/*` for generated training run manifest, experience packages, two generated Skill manifests, evaluation / gate / test case manifests, loading manifest, v7.30 loader dry-run validation, audit, safety, frontend panels, and regression metadata.
- v7.31a adds real closed-case training intake metadata under `/personal-skill-studio/training-artifacts/real-closed-case-*` for intake, redaction, case-cause classification, training sample segmentation, review queue, source trace, audit, and safety metadata.

## v7.31d Direction

Skill Package Versioning & Pre-Publish Gate.

- Do not continue provider gateway stacking.
- Do not re-implement OCR / Document provider live connection.
- Do not re-implement unified live connection dashboard.
- Do not re-implement Legal / Enterprise API live connection.
- Do not re-implement the v7.30 training artifact loader.
- Do not re-implement the v7.31 closed-case Codex training run generator.
- Do not re-implement the v7.31a real closed-case intake and redaction pipeline.
- Do not re-implement the v7.31b controlled experience candidate pipeline.
- Do not re-implement the v7.31c Skill Experience Pool and draft builder.
- Codex training remains metadata artifact generation and loading, not fine-tuning model parameters.
- Use only v7.31c non-publishable Skill draft metadata as input if v7.31d is started.
- Closed-case training and open-case practical analysis must remain separated.

## Validation Goal Before Any Release Handling

When the user confirms validation / release handling for v7.25-v7.31c, run the appropriate lightweight-to-full validation set:

- backend compileall full
- frontend build
- active API smoke regressions
- Personal Production regression checks
- provider live boundary regression
- trial readiness regression
- provider readiness / secret boundary regression
- v7.27 OCR / Document live connection regression
- v7.28 unified live connection regression
- v7.29 legal / enterprise API live connection regression
- v7.30 training artifact loader regression
- v7.31 Codex training run regression
- v7.31a real closed-case training intake regression
- v7.31b training experience pipeline regression
- v7.31c Skill Experience Pool / draft builder regression
- docs / changelog / Project Context checks
- git diff check
- empty markdown check
- runtime ignore check
- sensitive path check
- final comprehensive Codex Security audit only after user confirmation
- final diff review
- user-confirmed commit / tag / push / release handling

## Boundaries

- Team Workspace deferred.
- External Client Delivery deferred.
- Do not call real providers unless a gated target version explicitly enables adapter eligibility and the user authorizes it.
- Do not read API keys.
- Do not read or expose raw case materials.
- Do not generate final legal opinions.
- Do not generate final reports.
- Do not generate real final delivery files.
- Do not send email.
- Do not trigger external delivery.
- Do not automatically publish Skills.
