# Next Task

Next recommended task: an explicitly scoped next personal-version sub-stage.

## Current Gate

v7.24 Personal Practical Production Workbench is complete at commit `b4e4bca`, tag `v7.24-personal-practical-production-workbench`, and release `v7.24 Personal Practical Production Workbench`.

v7.25-v7.31a are complete through commit `86a0246` and tag `v7.31a`. v7.31b-v7.33 are complete through commits `e22281f` and `01259cf`. v7.34-v7.37 are complete at the `v7.37` tag target. v7.35a-v7.38b are complete in the current uncommitted worktree:

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
- v7.31d Skill Package Versioning & System Validation Gate.
- v7.31e Internal Training / Experience Package Builder.
- v7.31f Practice Runtime Load Review Gate.
- v7.31g Practice Runtime Controlled Loading & Monitoring.
- v7.31h Practice Runtime Output Observation & Lawyer Feedback Loop.
- v7.31i Practice Feedback Candidate Pack & Next Experience Package Iteration.
- v7.31j Feedback Candidate Pack to Next Experience Package Rebuild.
- v7.32 Experience Lifecycle Consolidation.
- v7.33 Case Analysis Skill Output Schema Driven Workbench Integration.
- v7.34 Case Analysis Output Feedback to Experience Improvement Candidate.
- v7.35 Training Dataset Builder & Training Gate.
- v7.35a Raw Training Material Controlled Parsing, OCR / Legal Retrieval Check.
- v7.35b Redacted Experience Package Output.
- v7.36 Codex Skill Training Dry Run.
- v7.37 Codex Skill Internal Training Run.
- v7.37 add-on Safe Callable Training Skill Spec.
- v7.38 Safe Codex Skill Internal Training Chain Connection.
- v7.38b Codex Panel Training Skill Packaging & Loading Fix.

Do not commit, tag, push, or release until the user explicitly approves release handling.

## Completed Local Sub-stages

- v7.32 consolidates experience lifecycle state, graph, audit timeline, source trace, integrity, and safety views for v7.31b-v7.31j.
- v7.33 renders case-analysis outputs strictly from backend `CaseAnalysisSkillOutputSchema.output_groups`, with feedback, risk event, audit, and source trace metadata.
- v7.34 maps v7.33 output feedback, risk event, audit, and source trace metadata into controlled experience improvement candidates, output-to-experience traces, diff summaries, readiness reports, audit, and source trace metadata.
- v7.35 builds Training Dataset Manifest, abstracted Training Examples, Training Task Plan, and reference-only Training Gate Report metadata from ready improvement candidates.
- v7.35a records controlled training-material parsing, OCR/document parse checks, legal retrieval checks, rule alignment, parse quality gate, audit, and source trace metadata.
- v7.35b generates redacted experience packages with legal summary, common fact extraction framework, case-cause-specific fact points, fact summary, diff readiness, audit, and source trace metadata.
- v7.36 runs Codex Skill Training Dry Run metadata simulation with safe logs, audit, source trace, and gate summary.
- v7.37 starts Codex Skill Internal Training Run metadata, metrics, logs, dry-run comparison, audit, source trace, and gate report generation.
- v7.37 add-on generates safe callable Training Skill Specs with provider type, credential alias, `credential_loaded`, gate requirements, output schema, prompt strategy, audit, and source trace metadata.
- v7.38 connects the safe Training Skill Spec into dry-run / internal simulation artifacts with differentiated experience package, facts diff, legal summary, readiness, audit, and source trace checks.
- v7.38b adds `.agents/skills/lawyer-ai-training-skill/` so Codex panel / agent sessions can load training workflow rules before future training development, dry-run validation, safety checks, and regression work.

## Current Direction

The implementation chain is complete through v7.38b in the current uncommitted worktree. The next task should be lightweight validation / release preparation only after explicit approval, or a new clearly scoped personal-version sub-stage.

Do not repeat v7.27-v7.38b provider / training / lifecycle implementations. Keep Team Workspace and External Client Delivery deferred.

## Validation Goal Before Any Release Handling

When the user confirms validation / release handling for v7.25-v7.34, run the appropriate lightweight-to-full validation set:

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
- v7.31d Skill Package versioning / system validation regression
- v7.31e Internal Training / Experience Package Builder regression
- v7.31f Practice Runtime Load Review Gate regression
- v7.31g Practice Runtime Controlled Loading & Monitoring regression
- v7.31h Practice Runtime Output Observation & Lawyer Feedback Loop regression
- v7.31i Practice Feedback Candidate Pack regression
- v7.31j Next Experience Package Rebuild regression
- v7.32 Experience Lifecycle regression
- v7.33 Case Analysis Skill Output Schema Workbench regression
- v7.34 Case Analysis Improvement Candidate regression
- v7.35 Training Dataset Builder & Gate regression
- v7.36 Codex Skill Training Dry Run regression
- v7.37 Codex Skill Internal Training Run regression
- v7.35a Raw Training Material Controlled Parsing regression
- v7.35b Redacted Experience Package Output regression
- v7.36 corrected Training Dataset Builder alias regression
- v7.37 Safe Callable Training Skill regression
- v7.38 Safe Codex Skill Internal Training Chain regression
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
- Do not read key values.
- Do not read or expose raw case materials.
- Do not generate final legal opinions.
- Do not generate final reports.
- Do not generate real final delivery files.
- Do not send email.
- Do not trigger external delivery.
- Do not automatically publish Skills.
