# v7.25 Personal Practical Case Trial Readiness

中文定位：个人版实战案件试运行准备。

v7.25 在 v7.24 Personal Practical Production Workbench 稳定基线之后，新增 `/personal-trial-readiness` 试运行准备工作台。它用于进入真实办案前的个人版本地试运行准备，只记录 trial session、trial checklist、stage observation、issue log、quality review、safety confirmation、optimization backlog、audit 和 safety metadata。

## Scope

- Backend runtime: `personal_trial_readiness`.
- Frontend route: `/personal-trial-readiness`.
- Integration: Personal Production runtime registry、readiness、provider capabilities、总控台、Pilot Dashboard、AppShell navigation。
- Regression: `scripts/regression/check_personal_trial_readiness_apis.sh`.

## Trial Metadata

- Trial Session: case mode、owner user、case reference label、trial status.
- Trial Checklist: case workspace、material workspace、OCR status、fact preview、fact correction、legal draft、Skill final drafts、owner output center、source trace、review queue、Trust / Safety、Diagnostics.
- Stage Observation: usability score、quality score、issue count、notes、optimization suggestions.
- Issue Log: issue type、severity、suggested fix、status、`blocks_trial=false`.
- Quality Review: reference-only scoring and optimization suggestions.
- Safety Confirmation: owner-only、draft-only、no public link、no email、no external delivery、no final opinion、no final report、no open-case training、no Skill auto publish.
- Optimization Backlog: trial feedback candidates for v7.26.

## Safety Boundary

- `owner_only=true`
- `trial_metadata_only=true`
- `raw_case_content_included=false`
- `raw_ocr_content_included=false`
- `api_key_exposed=false`
- `provider_live_call_triggered=false`
- `public_link_created=false`
- `email_sent=false`
- `external_delivery_triggered=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `training_data_generated=false`
- `writes_to_training_set=false`
- `skill_updated=false`
- `skill_published=false`
- `gate_reference_only=true`
- `blocks_next_stage=false`

## Non-goals

v7.25 does not add new AI / OCR / legal / enterprise provider integration. It does not read real case materials, read API keys, train on open cases, publish Skills, generate final legal opinions, generate final reports, create real PDF/DOCX files, create public links, send email, or trigger external delivery.

## Next

v7.26 should use v7.25 issue log, quality review, and optimization backlog metadata to plan focused trial-feedback improvements.

