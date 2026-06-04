# Material Citation / Report Source Trace v3.8

## Purpose

v3.8 prepares a mock/local source trace foundation for linking Material, OCR Source Ref, Legal Search Source Ref, Report Citation, and Source Trace.

This stage is a safety-bounded metadata foundation. It does not process real case material and does not connect to real providers.

## Scope

v3.8 adds:

* Unified SourceRef fields for material, OCR, legal search, report, skill runtime, and mock sources.
* ReportCitation metadata.
* SourceTrace nodes and edges.
* Mock source trace builder.
* Mock citation resolver.
* API `GET /source-refs/status`.
* API `GET /source-refs/mock-trace/{report_id}`.
* API `GET /source-refs/resolve/{citation_id}`.
* Report runtime fields `source_refs`, `citations`, `trace`, and `citation_summary`.
* Frontend page `/source-refs`.
* Runtime status card for Source Trace.
* Report detail display for v3.8 citation trace fields.
* OCR and Legal Search source ref metadata display.

## Data Shape

Report runtime may include:

```json
{
  "source_refs": [],
  "citations": [],
  "trace": {},
  "citation_summary": {}
}
```

Old reports without these fields remain supported. The frontend displays `暂无引用溯源数据` when citation trace metadata is absent.

## Mock Source Refs

The mock chain uses:

* `source_ref_mock_material_001`
* `source_ref_mock_ocr_001`
* `source_ref_mock_legal_search_001`
* `citation_mock_001`
* `citation_mock_002`

The mock trace records only metadata and warnings. It does not read real file content.

## Safety Boundary

v3.8 does not:

* Read real case material.
* Commit real case material.
* Call real OCR.
* Call a real legal database.
* Call a real LLM.
* Call DeepSeek live provider.
* Store real OCR text.
* Store real legal search results.
* Publish Skill Registry records.
* Modify legacy Skill assets.
* Change A1-A13.

A10 remains `争议焦点法律深化分析`.

## Relation To Earlier Stages

v3.6 Skill Factory remains unchanged. v3.7 OCR and Legal Search adapters remain mock-only. v3.8 connects their mock source ref metadata into report trace structures and UI display.

## Current Boundary

This is a report source trace enhancement only. It prepares citation and trace metadata for later local-only sandbox work, but real case processing remains out of scope.
