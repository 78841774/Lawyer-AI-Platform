# Case Analysis Skill Output Schema Workbench v7.33

v7.33 integrates a schema-driven practical case-analysis workbench for Skill runtime outputs.

## Scope

- Defines `CaseAnalysisSkillOutputSchema` in the backend.
- Builds `CaseAnalysisRuntimeOutput` metadata from backend output definitions.
- Provides a workbench view builder, output registry, fact output engine, legal output engine, risk output engine, feedback engine, risk-event engine, audit engine, source trace engine, and safety engine.
- Renders frontend output groups strictly from backend `output_groups`.
- Supports output filtering by group, type, risk level, status, feedback count, and keyword.
- Supports output detail, mark-reviewed, lawyer feedback, risk event, audit summary, and source trace summary.

## API

- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/status`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/views`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/views/{view_id}`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/views/{view_id}/schema`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/views/{view_id}/outputs`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}`
- `POST /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/mark-reviewed`
- `POST /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/feedback`
- `POST /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/risk-event`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/feedback`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/risk-events`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/audit`
- `GET /personal-skill-studio/training-artifacts/case-analysis-workbench/outputs/{output_id}/source-trace`
- `GET /personal-skill-studio/training-artifacts/v7-33/status`

## Output Schema Boundary

The frontend must visualize backend schema only. It must not hardcode output names, output counts, legal-analysis report names, or output groups.

The default backend schema includes:

- `fact_extraction`: expected count `2`.
- `legal_analysis`: expected count `16` in the current metadata demo.

Both titles and output definitions are returned by backend schema and rendered as received.

## Safety Boundary

v7.33 is practical workbench integration, not training and not provider execution.

It does not read unredacted lawyer work product, raw case material, OCR text, local paths, key values, or provider raw responses. It does not modify loaded packages, auto-generate next packages, update Skills, trigger training, publish Skills, create final legal opinions, generate formal reports, create real PDF / DOCX files, create public links, send email, or trigger external delivery.

Feedback and risk events are metadata-only records for lawyer review and later controlled improvement loops.

## Validation

The lightweight API regression is:

`scripts/regression/check_personal_case_analysis_workbench_v733_apis.sh`

The script verifies status, view list/detail, schema, outputs, output detail, mark-reviewed, feedback, risk event, feedback/risk lists, audit, source trace, backend-returned fact / legal output groups, expected counts, and sensitive-response boundaries.
