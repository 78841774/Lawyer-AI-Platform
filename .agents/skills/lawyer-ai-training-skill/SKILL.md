---
name: lawyer-ai-training-skill
description: Use this skill for Lawyer-AI-Platform training pipeline work, including controlled raw material parsing, OCR/legal retrieval gates, redacted experience package generation, Codex training skill generation, dry-run/internal training, safety checks, and regression validation.
---

# Lawyer AI Training Skill

## Purpose

This Skill guides Codex when working on Lawyer-AI-Platform training workflows.

It is a Codex panel / agent Skill for training workflow orchestration.

It is not a production legal analysis Skill.
It is not a published runtime Skill.
It must not contain secrets, raw case materials, OCR text, provider raw responses, or local absolute paths.

## Mandatory Boundaries

- Raw training materials may be unredacted only inside controlled raw training material processing.
- Redacted / abstracted outputs only may enter:
  - Experience Package
  - Training Dataset Manifest
  - Codex Training Skill Spec
  - Frontend views
  - Runtime loading
- Secrets must never be written into Skill, code, docs, logs, tests, frontend, or training artifacts.
- Provider access must go through backend adapter or provider-gated loader.
- Skill may reference credential_alias and credential_loaded only.
- No provider raw response may be returned.
- No runtime package may be replaced automatically.
- No production Skill may be published automatically.

## Training Workflow

1. prepare-training-materials
2. run-ocr-and-document-parse
3. run-legal-retrieval
4. run-parse-quality-gate
5. build-redacted-experience-package
6. build-training-dataset
7. generate-training-skill
8. run-training-dryrun
9. run-internal-training
10. package-training-output
11. require-lawyer-review-before-runtime-load

## Callable Workflows

- `prepare-training-materials`: register controlled training material metadata and keep unredacted materials inside the controlled raw training material zone.
- `build-redacted-experience-package`: build abstracted experience metadata after OCR, document parse, legal retrieval, rule alignment, and parse quality gate pass.
- `build-training-dataset`: build metadata-only dataset manifests, examples, task plans, audit, and source trace.
- `generate-training-skill`: generate business-system Training Skill Spec metadata with provider alias boundaries only.
- `run-training-dryrun`: run internal dry-run simulation metadata and gate checks.
- `run-internal-training`: record internal training run metadata without external provider training.
- `check-training-safety`: run bundled safety scripts and relevant repository safety checks.
- `summarize-training-output`: summarize facts, legal points, differentiation, audit, source trace, readiness, and safety flags.

## Experience Package Rules

Experience package must be one unified CaseAnalysisExperiencePackage.

It must include:

- common_framework
- substantive_experience_profiles
- procedural_experience_profiles
- profile_loading_contract
- audit
- source_trace
- safety_flags

Substantive experience:
- may be referenced across procedures only when case_cause, substantive_issue, fact_pattern, evidence_pattern, and usage_boundary match.
- must include source_procedure_type and source_procedure_stage.

Procedural experience:
- must match procedure_type + procedure_stage exactly.
- must not be used across procedures or stages.

## Differentiation Rules

Codex must summarize differences during training. Do not hardcode one fixed template.

Codex must summarize:

- common_fact_extraction_framework
- case_cause_specific_fact_points
- common_legal_summary_framework
- case_cause_specific_legal_points
- required_material_patterns
- evidence_review_points
- substantive_impact_points
- procedural_transition_rules
- risk_warnings
- fact_extraction_adjustment_rules
- legal_summary_adjustment_rules

## Provider Contract

Training Skill may include:

- provider_type
- credential_alias
- credential_loaded
- gate_requirements

Training Skill must not include:

- API key value
- secret value
- token value
- provider raw response
- local path
- raw material text
- OCR full text

## Resources

Load only the resource needed for the task:

- `resources/training_pipeline_rules.md` for the end-to-end training chain.
- `resources/experience_package_schema.md` for CaseAnalysisExperiencePackage structure and loading boundaries.
- `resources/provider_adapter_contract.md` for provider alias and credential-loaded gate rules.
- `resources/safety_boundary.md` for forbidden output classes and safety flags.
- `resources/regression_checklist.md` for the current training regression set.

## Scripts

- `scripts/check_training_skill_safety.sh`
- `scripts/run_training_regression.sh`
- `scripts/check_no_secret_or_raw_material.sh`

## Completion Requirements

After any implementation task, Codex must run:

- backend compileall
- frontend npm run build when frontend changes
- relevant regression scripts
- run_personal_alpha_regression.sh
- git diff --check
- docs not empty check
- sensitive file check
- runtime ignored check

Codex must report:

- Changed Files
- Implemented
- Safety Preserved
- Intentionally Not Changed
- Checks
- Git Status
