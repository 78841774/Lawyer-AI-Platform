# v7.31b Raw Work-Product Controlled Processing Experience Pipeline

## 中文定位

律师办案底稿受控解析、OCR/文档解析、法律检索、经验提炼、脱敏输出与人工复核确认管线。

## Scope

v7.31b accepts authorized lawyer work-product metadata for controlled internal processing. It creates demo-safe OCR/document parse job metadata, legal retrieval job metadata, redacted experience candidates, manual review status, source trace, audit, and safety metadata.

The stage does not place experience into the Skill pool and does not generate Codex Skill drafts. Those are v7.31c responsibilities.

## Pipeline

- Raw work-product boundary status confirms controlled internal processing only.
- OCR/document parse jobs return parse summaries and section metadata only.
- Legal retrieval jobs return statute and similar-case candidate metadata only.
- Experience candidates are built from parse/retrieval metadata.
- Candidates require redaction before manual review.
- Only `approved_for_skill_experience` candidates may be used by v7.31c.

## API

Prefix: `/personal-skill-studio/training-artifacts`

- `GET /raw-work-product-boundary/status`
- `POST /ocr-jobs`
- `GET /ocr-jobs`
- `GET /ocr-jobs/{job_id}`
- `POST /legal-retrieval-jobs`
- `GET /legal-retrieval-jobs`
- `GET /legal-retrieval-jobs/{job_id}`
- `POST /experience-candidates/build`
- `GET /experience-candidates`
- `GET /experience-candidates/{candidate_id}`
- `POST /experience-candidates/{candidate_id}/redact`
- `POST /experience-candidates/{candidate_id}/review`
- `GET /experience-candidates/{candidate_id}/audit`
- `GET /v7-31b/status`

## Safety Boundary

- `owner_only=true`
- `local_private_processing_only=true`
- `authorized_case_only=true`
- `raw_material_controlled=true`
- `redacted_output_only=true`
- `manual_review_required=true`
- `source_trace_required=true`
- `audit_required=true`
- `provider_call_executed=false`
- `credential_value_returned=false`
- `original_material_returned=false`
- `formal_training_set_generated=false`
- `skill_published=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `public_link_created=false`
- `email_sent=false`
- `external_delivery_triggered=false`

## Regression

- `scripts/regression/check_personal_training_experience_pipeline_v731b_apis.sh`
- Included in `scripts/regression/run_personal_alpha_regression.sh`

## Next

Next planned sub-stage: v7.31c Skill Experience Pool & Codex Skill Draft Builder.
