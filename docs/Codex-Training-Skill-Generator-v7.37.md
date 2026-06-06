# Codex Training Skill Generator v7.37

v7.37 adds a safe Training Skill Spec generator on top of the completed v7.35-v7.37 training chain.

## Baseline Skills

The generated Training Skill Spec combines existing baseline metadata from:

- `case_fact_extraction_skill`
- `case_legal_analysis_skill`
- `case-fact-extractor-v3@v1.0.0`
- `case-analysis-pro-v3@v1.0.0`

Lineage includes source package ids, source asset names, evaluation ids, gate ids, output groups, prompt strategy, and safety constraints.

## Differentiated Fact Experience Package

The generated Training Skill Spec now includes `differentiated_fact_extraction_experience_package`:

- `legal_summary`: legal point summary metadata
- `common_fact_extraction_framework`: shared fact structure only
- `case_cause_specific_fact_summaries`: per-case-cause fact points and fact summary
- `substantive_experience_profiles`: substantive references that may cross procedure only when boundary conditions pass
- `procedural_experience_profiles`: exact-match procedure/stage profiles that must not cross procedure or stage
- `case_cause_profiles`: per-case-cause profiles with nested substantive and procedural profile references
- `profile_loading_contract`: two-layer matching contract for substantive aggregation and procedural exact matching
- `diff_summary`: verifies that common structure is shared while case-cause points differ
- `readiness_status`: readiness metadata for internal dry-run training
- `audit_bundle_id` and `source_trace_bundle_id`: required for lawyer review

The common framework covers parties, basic legal relationship, timeline, right / duty source, performance / breach / damage, evidence mapping, disputed facts, court-accepted facts, and risk facts. It does not hardcode case-cause details.

Case-cause-specific points are learned from desensitized judgment structure, lawyer work-product structure, evidence index, court-reasoning summary, and legal retrieval metadata. The current dry-run profiles include private lending, sales contract, labor dispute, and marriage / family dispute examples.

Procedural profiles cover litigation first instance, litigation second instance, litigation retrial, commercial arbitration, and labor arbitration. They differentiate required materials, fact extraction points, evidence review points, legal summary points, substantive impact, procedure transition rules, and risk warnings.

Substantive profiles include fact extraction points, substantive legal summary points, claim basis patterns, issue-to-rule patterns, evidence-to-legal-effect patterns, court reasoning patterns, risk fact patterns, risk legal points, substantive impact points, source stage reference, runtime reference type, usage boundary, audit, and source trace.

Procedural profiles include required material patterns, procedural deadline rules, procedural burden rules, appeal-scope rules, retrial-threshold rules, arbitration-clause review rules, labor-arbitration precondition rules, transition rules, procedural risk warnings, exact-match usage boundary, audit, and source trace.

## Safe Callable Interface

The Skill Spec may include callable provider specs:

- `provider_type`: `OCR_API`, `Legal_API`, `Enterprise_API`
- `credential_alias`: environment variable name or backend credential alias
- `credential_loaded`: runtime-loaded boolean state
- `gate_requirements`: provider gate, credential-loaded check, audit, source trace, and manual approval rules
- `output_schema`: metadata-only result shape

The Skill Spec never stores credential values.

## Gate Checks

The v7.37 Training Skill gate verifies:

- provider specs are complete
- facts output schema is ready
- case-cause differentiation is present
- procedure and stage differentiation is present
- substantive/procedural experience split is present
- substantive cross-procedure reference boundary is present
- procedural exact-match boundary is present
- substantive impact points are present
- profile loading contract is present
- legal summary is present
- audit and source trace are complete
- the generated Skill remains not publishable and not runtime loadable

## APIs

Prefix: `/personal-skill-studio/training-artifacts`

- `GET /codex-training-skills/interface-doc`
- `GET /codex-training-skills/provider-adapters`
- `GET /codex-training-skills/provider-adapters/{provider_type}`
- `POST /codex-training-skills/generate`
- `GET /codex-training-skills`
- `GET /codex-training-skills/{training_skill_id}`
- `POST /codex-training-skills/{training_skill_id}/gate/run`
- `GET /codex-training-skills/{training_skill_id}/gate-report`
- `POST /codex-training-skills/{training_skill_id}/provider-call/mock`
- `GET /v7-37/status`

## Safety

The adapter placeholder checks credential alias presence and returns `credential_loaded=true/false` only. It does not return credential values and does not execute live provider calls in this stage.

## Regression

- `scripts/regression/check_personal_codex_training_skill_v737_apis.sh`
