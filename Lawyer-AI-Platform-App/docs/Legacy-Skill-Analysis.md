# Legacy Skill Analysis

v3.6-B audits existing legacy case-analysis Skill and SkillOpt assets only.

This document records what was found, how the assets should be classified, and what must happen before any training, import, or publication.

## Scope

This stage does not:

* Create new Skills.
* Import anything into Skill Registry.
* Publish Experience Packages.
* Run legacy Skill scripts.
* Call LLM providers.
* Start Skill Training.
* Copy raw case materials into the repository.

## Source Roots

The audit script checks the current repository and known local legacy locations, including:

* `/Users/wazhen/.codex/skills/case-fact-extractor-v3`
* `/Users/wazhen/.codex/skills/case-analysis-pro-v3`
* `/Users/wazhen/Documents/Codex/2026-05-28/law-search-users-wazhen-codex-skills/SkillOpt`
* `/Users/wazhen/Documents/Codex/2026-05-28/law-search-users-wazhen-codex-skills/legal-skillopt`
* `/Users/wazhen/Lawyer-AI-Platform/training_samples`
* `/Users/wazhen/Lawyer-AI-Platform/08-Skill-Training`

## Current Inventory

The current read-only scan found:

* Legacy Skill assets: 17
* Legacy Codex Skills: 2
* SkillOpt initial Skills: 3
* SkillOpt best_skill outputs: 12
* SkillOpt dataset files: 19
* SkillOpt dataset items: 96
* SkillOpt output runs: 14

The 17 Skill assets are analysis targets, not production Skill Registry records.

## Legacy Skill Assets

| asset_group | count | meaning | migration posture |
| --- | ---: | --- | --- |
| Legacy Codex Skills | 2 | Existing local Codex Skills for fact extraction and case analysis | Keep read-only; extract rules, rubrics, prompts, templates |
| SkillOpt initial Skills | 3 | Initial SkillOpt seeds for fact extraction, case analysis, and routing | Convert to package templates after review |
| SkillOpt best_skill outputs | 12 | Historical optimized Skill outputs from prior SkillOpt runs | Compare and extract stable deltas only |

The named Skill families are:

* `case-fact-extractor-v3`
* `case-analysis-pro-v3`
* `legal-casework-router`

## Ability Modules

Reusable capability modules detected across the old assets include:

* Fact extraction.
* Evidence matrix construction.
* Amount audit.
* Contradiction detection.
* Legal element mapping.
* Case analysis.
* Claim basis analysis.
* Defense analysis.
* Litigation strategy.
* Report generation.
* Judgment review.
* Execution assessment.
* Scoring and admission gates.

## Dataset Inventory

The SkillOpt training data is present under `legal-skillopt/data`.

Current dataset summary:

| dimension | count |
| --- | ---: |
| dataset files | 19 |
| dataset items | 96 |
| `case-fact-extractor-v3` samples | 46 |
| `case-analysis-pro-v3` samples | 50 |
| fact extraction tasks | 46 |
| case analysis tasks | 19 |
| post-judgment evaluation tasks | 31 |
| desensitized items | 93 |
| unknown privacy-level items | 3 |

The 63 items in `legal_casework_split/inbox/items.json` should be treated as uncurated until reviewed.

## Migration Levels

The audit uses conservative migration levels:

| level | meaning |
| --- | --- |
| Level 1 | Read-only reference |
| Level 2 | Runtime rule candidate |
| Level 3 | Prompt template candidate |
| Level 4 | Evaluation rubric candidate |
| Level 5 | Training dataset candidate |
| Level 6 | Experience Package template candidate |

Current recommendations:

* Legacy Codex Skills are mainly Level 4 candidates because they contain scoring gates, review rules, scripts, and operational policy.
* SkillOpt initial Skills and best_skill outputs are mainly Level 6 candidates because they can inform future Experience Package templates.
* Dataset files are candidates for a separate curated Dataset Package, not direct Skill Registry import.

## Risk Flags

The audit found recurring risks:

* OCR dependency.
* External legal search dependency.
* Manual lawyer review dependency.
* Sensitive data and desensitization risk.
* Not safe for automatic execution.
* Requires legal professional review before user-facing reliance.

## Required Next Step

Before v3.6-D training or registry import, the legacy data should be reshaped into a controlled data package:

1. Normalize each sample into a stable schema.
2. Separate `inbox`, `curated`, `rejected`, and `raw-private`.
3. Preserve source references without copying raw case files.
4. Add privacy status and reviewer status.
5. Split reusable content into runtime rules, prompt templates, report templates, evaluation rubrics, and dataset examples.
6. Validate that no private or unreviewed sample enters training.

## Generated Reports

The local script writes runtime reports to:

* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/reports/legacy_skill_analysis.md`
* `/Users/wazhen/Lawyer-AI-Platform/Lawyer-AI-Platform-App/backend/reports/legacy_skill_analysis.json`

The reports are runtime artifacts and are not committed by default.
