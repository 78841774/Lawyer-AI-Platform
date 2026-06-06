# Skill Final Draft & Optimization Workbench v7.22

v7.22 adds an owner-only workbench for two Skill final draft metadata records:

- `case_fact_extraction_skill` / 案件事实提炼 Skill
- `case_legal_analysis_skill` / 案件法律分析 Skill

The workbench reads existing Skill Studio, Controlled Case Analysis, Fact Preview, Legal Draft, docs, and Project Context metadata. It does not invent a new evaluation system. If the baseline is incomplete, responses return `baseline_complete=false`, `missing_baseline_report`, and placeholder lineage metadata.

## Scope

- Baseline discovery metadata.
- Final draft metadata for two Skills.
- Lineage, quality, gate, optimization, source trace, audit, and safety metadata.
- Owner-only download metadata for Markdown / JSON / PDF draft metadata / DOCX draft metadata.

## Safety Boundary

- `owner_only=true`.
- `downloadable_by_owner_only=true`.
- `gate_reference_only=true`.
- `blocks_next_stage=false`.
- `quality_reference_only=true`.
- `final_skill_published=false`.
- `skill_auto_published=false`.
- `training_data_generated=false`.
- `writes_to_training_set=false`.
- `open_case_data_used=false`.
- No public link, email, external delivery, final legal opinion, final report, real PDF/DOCX, raw content, API key, or local path exposure.

## API

- `GET /personal-skill-studio/final-drafts`
- `GET /personal-skill-studio/final-drafts/{skill_id}`
- `GET /personal-skill-studio/final-drafts/{skill_id}/lineage`
- `GET /personal-skill-studio/final-drafts/{skill_id}/baseline`
- `GET /personal-skill-studio/final-drafts/{skill_id}/quality`
- `GET /personal-skill-studio/final-drafts/{skill_id}/gate`
- `GET /personal-skill-studio/final-drafts/{skill_id}/optimization`
- `GET /personal-skill-studio/final-drafts/{skill_id}/source-traces`
- `GET /personal-skill-studio/final-drafts/{skill_id}/audit`
- `POST /personal-skill-studio/final-drafts/{skill_id}/owner-downloads/mock`
- `GET /personal-skill-studio/final-draft-downloads`
- `GET /personal-skill-studio/final-draft-downloads/{download_id}`
- `GET /personal-skill-studio/final-drafts-safety`

## Frontend

The page `/personal-skill-studio/final-drafts` shows:

- Baseline Discovery Panel.
- Fact Skill Final Draft Card.
- Legal Analysis Skill Final Draft Card.
- Evaluation / Gate Panel.
- Optimization Suggestions Panel.
- Owner Download Boundary.
- Source Trace / Audit Panel.
- Trust / Safety Panel.
- Developer Diagnostics folded by default.

## Regression

`scripts/regression/check_personal_skill_final_drafts_apis.sh` covers the v7.22 endpoints and verifies metadata-only, owner-only, no publish, no training-set writes, no public link, no email, no external delivery, and no sensitive path or secret exposure.
