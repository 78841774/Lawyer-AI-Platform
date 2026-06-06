# Case Analysis Output Feedback Improvement Candidate v7.34

v7.34 adds a controlled conversion layer that maps v7.33 case-analysis output feedback, risk events, audit references, and source trace references into Experience Improvement Candidate metadata.

## Scope

- Builds `CaseAnalysisImprovementCandidate` metadata from schema-driven case-analysis outputs.
- Preserves lineage to output id, output group/type, workbench view, runtime load, package, experience cards, feedback ids, risk event ids, audit ids, and source trace ids.
- Builds output-to-experience trace metadata.
- Builds improvement diff summaries.
- Builds readiness reports for later v7.35 Training Dataset Builder & Training Gate use.

## Boundaries

- Does not modify loaded packages.
- Does not modify lawyer-approved packages.
- Does not modify `CaseAnalysisSkillOutputSchema`.
- Does not trigger training or build a training dataset.
- Does not replace runtime packages.
- Does not publish Skills.
- Does not call providers or read key values.
- Does not generate final legal opinions or formal reports.
- Does not create public links, send email, create real export files, or trigger external delivery.

## API

All endpoints remain under `/personal-skill-studio/training-artifacts`.

- `GET /case-analysis-improvement/status`
- `POST /case-analysis-improvement/candidates/build`
- `GET /case-analysis-improvement/candidates`
- `GET /case-analysis-improvement/candidates/{candidate_id}`
- `GET /case-analysis-improvement/candidates/{candidate_id}/readiness`
- `POST /case-analysis-improvement/candidates/{candidate_id}/mark-ready`
- `POST /case-analysis-improvement/candidates/{candidate_id}/archive`
- `GET /case-analysis-improvement/output-traces`
- `GET /case-analysis-improvement/output-traces/{trace_id}`
- `POST /case-analysis-improvement/diff/build`
- `GET /case-analysis-improvement/diffs`
- `GET /case-analysis-improvement/diffs/{diff_id}`
- `GET /case-analysis-improvement/candidates/{candidate_id}/audit`
- `GET /case-analysis-improvement/candidates/{candidate_id}/source-trace`
- `GET /v7-34/status`

## Frontend

The training artifacts workbench now includes a v7.34 panel showing candidate overview, filters, detail, readiness, trace, audit, source trace, and diff summary. The frontend does not generate candidates, map feedback types, decide candidate type, or decide readiness. It only renders backend metadata and invokes backend actions.

## Next

v7.35 may use `ready_for_training_dataset_build` candidates as inputs for Training Dataset Builder & Training Gate. v7.35 must still remain controlled, gated, metadata-only, and must not execute real training unless a later explicitly approved stage adds that behavior.
