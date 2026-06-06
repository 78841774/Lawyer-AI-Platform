# v7.31 Execute Codex Training on Closed Case Samples

## 中文定位

已结案件 Codex 训练执行。

## Scope

v7.31 adds a closed-case Codex training run layer on top of the v7.30 training artifact loader. Codex training means generation of metadata artifacts for AIHome.law Skills. It is not model fine-tuning and does not train model parameters.

When no real redacted closed-case sample set is available, v7.31 uses synthetic closed-case samples with `source_case_mode=synthetic_closed_case`. These samples are not represented as real cases.

## Generated Artifacts

- Training run manifest.
- Synthetic closed-case sample metadata across multi-level case causes.
- Experience package manifests for common civil, case-cause-specific, and evidence overlay packages.
- Generated Skill manifests for `case_fact_extraction_skill` and `case_legal_analysis_skill`.
- Evaluation manifests.
- Gate manifests.
- Test case manifests.
- Loading manifest.
- v7.30 loader dry-run validation metadata.
- Audit and safety metadata.

## API

Prefix: `/personal-skill-studio/training-artifacts`

- `GET /training-runs`
- `GET /training-runs/{run_id}`
- `POST /training-runs/mock`
- `GET /training-runs/{run_id}/summary`
- `GET /training-runs/{run_id}/case-cause-packages`
- `GET /training-runs/{run_id}/generated-skills`
- `GET /training-runs/{run_id}/evaluations`
- `GET /training-runs/{run_id}/gates`
- `GET /training-runs/{run_id}/test-cases`
- `GET /training-runs/{run_id}/loading-manifest`
- `POST /training-runs/{run_id}/load-dry-run/mock`
- `GET /training-runs/{run_id}/audit`
- `GET /training-runs/{run_id}/safety`

## Frontend

- `/personal-skill-studio/training-artifacts` shows v7.31 training run metadata, generated packages, generated Skills, evaluation / gate / test cases, loading manifest, and loader dry-run result.
- `/personal-skill-studio` links to the v7.31 closed-case training run surface.
- `/personal-production` shows v7.31 readiness.
- `/personal-production-pilot` aggregates v7.31 training run metadata.

## Safety Boundary

- `owner_only=true`
- `metadata_only=true`
- `training_artifact_only=true`
- `codex_training=true`
- `fine_tune_model_training=false`
- `closed_case_only=true`
- `open_case_data_used=false`
- `raw_content_included=false`
- `raw_ocr_content_included=false`
- `api_key_exposed=false`
- `secret_value_returned=false`
- `local_path_exposed=false`
- `writes_to_training_set=false`
- `skill_updated=false`
- `skill_published=false`
- `skill_auto_published=false`
- `load_dry_run=true`
- `load_executed=false`
- `final_legal_opinion_generated=false`
- `final_report_generated=false`
- `public_link_created=false`
- `email_sent=false`
- `external_delivery_triggered=false`
- `gate_reference_only=true`
- `blocks_next_stage=false`
- `audit_required=true`

## Regression

Added `scripts/regression/check_personal_codex_training_runs_apis.sh` and connected it to `scripts/regression/run_personal_alpha_regression.sh`.

## Next

Next planned sub-stage: v7.32 Training Artifact Load & Skill Context Runtime.
