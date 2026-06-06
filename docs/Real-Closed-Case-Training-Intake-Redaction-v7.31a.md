# v7.31a Real Closed-Case Training Intake & Redaction Pipeline

## 中文定位

真实已结案件训练材料导入与脱敏管线。

## Scope

v7.31a prepares authorized closed-case training material metadata before real closed-case Codex training. This stage does not execute Codex training. It only creates intake, redaction, case-cause classification, training sample segment, review queue, source trace, audit, and safety metadata.

## Inputs

Allowed inputs are authorized closed-case training materials, closed-case judgment metadata, closed-case fact summaries, legal analysis metadata, evidence metadata, redacted training samples, and synthetic closed-case samples.

Forbidden inputs are open or unresolved cases, current practical cases, unauthorized materials, API keys, secrets, local absolute paths, private identity data, raw OCR content that should not enter training, and unconfirmed private raw content.

## Pipeline

- Intake metadata confirms `source_case_mode=real_closed_case`, owner authorization, and closed-case status.
- Redaction metadata confirms identity, phone, ID number, address, and raw OCR removal.
- Redaction preserves legally relevant metadata such as jurisdiction context, age/capacity context, subject type, contract type, object type, timeline markers, and evidence type.
- Case-cause classification maps intake metadata to multi-level case-cause paths.
- Training sample segmentation creates fact and legal segments for `case_fact_extraction_skill` and `case_legal_analysis_skill`.
- Review queue requires manual review before future real closed-case Codex training.
- Source trace and audit metadata are retained without raw content.

## API

Prefix: `/personal-skill-studio/training-artifacts`

- `GET /real-closed-case-intake/status`
- `POST /real-closed-case-intake/mock`
- `GET /real-closed-case-intakes`
- `GET /real-closed-case-intakes/{intake_id}`
- `GET /real-closed-case-intakes/{intake_id}/redaction-report`
- `POST /real-closed-case-intakes/{intake_id}/redaction/mock`
- `GET /real-closed-case-intakes/{intake_id}/case-cause-classification`
- `POST /real-closed-case-intakes/{intake_id}/case-cause-classification/mock`
- `GET /real-closed-case-intakes/{intake_id}/segments`
- `POST /real-closed-case-intakes/{intake_id}/segments/mock`
- `GET /real-closed-case-intakes/{intake_id}/review-queue`
- `POST /real-closed-case-intakes/{intake_id}/review-queue/{review_item_id}/actions/mock`
- `GET /real-closed-case-intakes/{intake_id}/source-traces`
- `GET /real-closed-case-intakes/{intake_id}/audit`
- `GET /real-closed-case-intakes/{intake_id}/safety`

## Safety Boundary

- `owner_only=true`
- `metadata_only=true`
- `closed_case_only=true`
- `real_closed_case_intake=true`
- `open_case_data_used=false`
- `raw_content_included=false`
- `raw_ocr_content_included=false`
- `redaction_required=true`
- `api_key_exposed=false`
- `secret_value_returned=false`
- `local_path_exposed=false`
- `writes_to_training_set=false`
- `skill_updated=false`
- `skill_published=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `public_link_created=false`
- `email_sent=false`
- `external_delivery_triggered=false`
- `audit_required=true`
- `source_trace_required=true`
- `manual_review_required=true`

## Next

Next planned sub-stage: v7.31b Raw Work-Product Controlled Processing Experience Pipeline.
