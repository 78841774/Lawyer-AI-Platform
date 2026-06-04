# OCR / Legal Search Preparation v3.7

v3.7 prepares OCR, Legal Search, and citation/source trace foundations for future local-only real case processing.

This stage is adapter preparation only. It does not connect real OCR services, real legal databases, or real LLM providers.

## Goals

v3.7 adds:

* OCR Adapter abstraction.
* Mock OCR Provider.
* Legal Search Adapter abstraction.
* Mock Legal Search Provider.
* Source Refs / Citation schema foundation.
* Runtime UI status cards for OCR and Legal Search.
* Mock test pages for OCR and Legal Search.

## OCR Adapter Design

The OCR adapter defines a provider interface:

```text
get_status()
extract_text(request)
```

The request carries only metadata:

* `material_id`
* `filename`
* `relative_path`
* `provider`
* `mode`
* `mock_only`

The adapter does not read file content. `relative_path` is preserved as a source reference field only.

## Mock OCR Provider

The Mock OCR Provider returns:

* `provider=mock_ocr`
* `provider_mode=mock`
* `status=completed_mock`
* `text_available=true`
* mock page text
* mock source refs
* warnings that no real OCR provider is connected

It never calls an OCR SDK, network API, or local file reader.

## Legal Search Adapter Design

The Legal Search adapter defines a provider interface:

```text
get_status()
search(request)
```

The request carries:

* `query`
* `case_cause_code`
* `jurisdiction`
* `provider`
* `mode`
* `mock_only`

## Mock Legal Search Provider

The Mock Legal Search Provider returns:

* `provider=mock_legal_search`
* `provider_mode=mock`
* `status=completed_mock`
* one mock case-law hit
* mock citation data
* warnings that no external legal database was queried

It never calls a legal database, fetches case law, scrapes webpages, or invokes an LLM.

## Source Refs / Citation Foundation

v3.7 adds schema-only source reference structures:

* `SourceRef`
* `MaterialSourceRef`
* `OCRSourceRef`
* `LegalSearchSourceRef`
* `ReportCitation`

Supported source types are:

```text
material
ocr
legal_search
skill_runtime
```

Report runtime source refs are backward compatible and can now carry optional:

* `source_refs`
* `citations`
* `trace`

No database migration is introduced in v3.7.

## Relationship To Material Center

The Material Center remains the entry point for uploaded material metadata.

v3.7 does not read or process real files. Future local-only OCR processing can use `material_id`, `filename`, and `relative_path` as trace metadata after privacy and local-processing controls are ready.

## Relationship To Report Runtime

Report Runtime already stores `source_refs` as JSON.

v3.7 prepares a richer trace shape so future reports can cite:

* original materials
* OCR snippets
* legal search results
* skill runtime outputs

Formal citation persistence is out of scope until a later stage.

## Relationship To Skill Factory

v3.7 does not change the v3.6 Skill Factory loop.

The v3.6 flow remains:

```text
Versioned Training Package
-> Mock Training Run
-> Experience Package Candidate
-> Human Review
-> Controlled Skill Registry Publish
```

OCR and Legal Search adapters are future inputs for local-only case processing, not automatic Skill Factory training inputs.

## Safety Boundary

v3.7 does not:

* call real OCR
* call a real legal database
* call a real LLM
* call DeepSeek live provider
* use real case material
* read real case material
* commit real case material
* save API keys
* automatically process real cases
* publish Skills
* enable Workspace Runtime
* overwrite `skill_001` or `skill_002`
* modify legacy Skill source assets

A10 remains:

```text
争议焦点法律深化分析
```

## Future v3.8 / v4.0 Plan

Recommended v3.8 focus:

1. Material Citation / Report Source Trace Enhancement.
2. Local source-ref persistence design.
3. Report section citation mapping.
4. OCR text privacy and retention rules.
5. Legal Search citation normalization.

Recommended v4.0 focus:

1. Internal Alpha deployment preparation.
2. API key management review.
3. Local-only real case processing controls.
4. Manual runtime enablement gates.
