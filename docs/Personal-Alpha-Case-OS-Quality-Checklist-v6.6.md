# Personal Alpha Case OS Quality Checklist v6.6

## Objective

v6.6 adds a metadata-only quality checklist layer on top of the v6.5 Case OS export package workflow. It checks workflow completeness, safety boundaries, audit integrity, metadata closure, export package availability, review state readiness, quality findings, recommendations, and a quality score.

The quality layer is advisory only. It does not generate a legal opinion, final case report, PDF, DOCX, or any raw-content export.

## Relationship to v6.5

v6.5 introduced metadata-only JSON and Markdown export packages stored in ignored runtime storage. v6.6 reads only existing safe metadata surfaces, including metadata closure, unified audit summary, redaction check, review state, blockers, and export package summary. It does not read package files, local case material, OCR text, or legal search result text.

## Quality Checklist API

The checklist endpoint is:

```text
GET /case-os/{case_id}/quality/checklist
```

It returns workflow completeness checks, safety boundary checks, audit integrity checks, metadata closure checks, export package checks, review state checks, and recommendation readiness checks. Every item includes `mock_or_redacted_only=true` and `raw_content_included=false`.

## Quality Score Logic

The score endpoint is:

```text
GET /case-os/{case_id}/quality/score
```

Scoring starts from 100 and applies these penalties:

- critical: 25
- high: 15
- medium: 7
- low: 3

Grades are:

- A: 90-100
- B: 80-89
- C: 70-79
- D: 60-69
- F: 0-59

The score is advisory metadata only and is not a formal legal review result.

## Quality Findings Logic

The findings endpoint is:

```text
GET /case-os/{case_id}/quality/findings
```

Failed checklist items with finding codes are converted into metadata-only findings. Findings include category, severity, title, description, blocking status, target route, and recommended action. Findings do not include raw material text, OCR text, legal search text, quotes, local paths, real filenames, or final legal analysis.

## Quality Recommendations Logic

The recommendations endpoint is:

```text
GET /case-os/{case_id}/quality/recommendations
```

Recommendations are derived from findings and deduplicated by action. Every recommendation includes `would_execute_action=false`. v6.6 never executes workflow actions, never auto-fixes blockers, never creates final locks, and never creates export packages.

## Quality Report Preview

The report preview endpoint is:

```text
GET /case-os/{case_id}/quality/report-preview
```

It returns a metadata-only preview of sections that would be included in a quality report. It sets:

- `would_create_file=false`
- `would_generate_final_report=false`
- `would_generate_legal_opinion=false`
- `would_include_raw_content=false`

No file is written, no storage entry is created, and no final report body is generated.

## Readiness Logic

`ready_for_personal_alpha_review` is true only when:

- `required_failed_count == 0`
- `critical_failed_count == 0`
- `raw_content_included == false`
- `final_legal_opinion_generated == false`
- `final_report_generated == false`

## Metadata-Only Rule

v6.6 uses existing Case OS metadata. It does not read raw material text, raw OCR text, raw legal search result text, package file content, local paths, or real case files.

## No Raw Content Rule

Quality status, checklist, score, findings, recommendations, report preview, and summary all keep:

- `mock_or_redacted_only=true`
- `raw_content_included=false`
- no local absolute paths
- no API keys
- no raw quotes
- no real filenames

Path-like or unsafe case IDs are safely blocked or redacted without echoing unsafe values.

## No Final Legal Opinion

v6.6 does not generate or return a formal legal opinion. All quality results are advisory metadata for local personal alpha workflow review.

## No Final Report Generated

v6.6 does not generate a final case report body and does not create PDF or DOCX output.

## No Automatic Workflow Execution

v6.6 recommendations never execute actions. The quality layer does not create export packages, final locks, Skill publications, or Workspace Runtime enablement.

## Frontend Updates

The Case OS detail page now shows:

- Quality Status
- Quality Score
- Quality Checklist
- Quality Findings
- Quality Recommendations
- Quality Report Preview
- Quality Summary
- JSON panels for every quality response

## v6.7 Readiness

v6.7 can move into a Case OS regression suite that scripts v5.0-v6.6 curl checks, frontend smoke notes, runtime ignored checks, no-sensitive-files checks, and metadata-only response checks while continuing to avoid real providers and final report generation.
