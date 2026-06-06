# Next Task

Next recommended task: v7.34 Case Analysis Output Feedback to Experience Improvement Loop.

## Current Gate

v7.24 Personal Practical Production Workbench is complete at commit `b4e4bca`, tag `v7.24-personal-practical-production-workbench`, and release `v7.24 Personal Practical Production Workbench`.

v7.25-v7.31a are complete through commit `86a0246` and tag `v7.31a`. v7.31b-v7.33 are complete in the current local worktree:

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

Do not commit, tag, push, or release until the user explicitly approves release handling.

## Completed Local Sub-stages

- v7.31i builds next-iteration candidate pack metadata only from triaged feedback/risk/observation metadata.
- v7.31j rebuilds next experience package draft metadata only from ready candidate packs and does not load drafts into practice runtime.
- v7.32 consolidates experience lifecycle state, graph, audit timeline, source trace, integrity, and safety views for v7.31b-v7.31j.
- v7.33 renders case-analysis outputs strictly from backend `CaseAnalysisSkillOutputSchema.output_groups`, with feedback, risk event, audit, and source trace metadata.

## v7.34 Direction

Case Analysis Output Feedback to Experience Improvement Loop.

- Use only v7.33 case-analysis output feedback, risk events, audit, and source trace metadata as input.
- Build controlled improvement-loop candidate metadata for later human review.
- Preserve lineage to output definition, workbench view, runtime load, experience package, feedback, risk event, audit, and source trace.
- Keep improvement candidates reference-only unless a later version explicitly adds a review/apply boundary.
- Do not auto-update Skills.
- Do not auto-mutate loaded packages, lawyer-approved packages, next package drafts, runtime policy, or training artifacts.
- Do not trigger real training, Skill publishing, final legal opinions, formal reports, real PDF/DOCX generation, public links, email, or external delivery.
- Do not call providers, read API keys, read raw case materials, read OCR text, expose local paths, or expose provider responses.

## Validation Goal Before Any Release Handling

When the user confirms validation / release handling for v7.25-v7.33, run the appropriate lightweight-to-full validation set:

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
