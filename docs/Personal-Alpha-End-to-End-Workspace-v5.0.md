# Personal Alpha End-to-End Workspace v5.0

## Objective

v5.0 adds a Personal Alpha End-to-End Local Case Workspace on top of the controlled workflows delivered from v4.3 through v4.9.

The workspace aggregates controlled stage status, source trace placeholders, and audit timeline metadata. It remains a local-only personal alpha workflow and is not production.

## Relationship To v4.3-v4.9

v5.0 does not replace the controlled stages. It creates a unified mock workspace view across:

- Controlled Material Preview
- Controlled OCR Preview
- Controlled Legal Search Preview
- Controlled Report Draft Assembly
- Controlled Lawyer Review
- Controlled Revision Request
- Controlled Final Review Lock

Each stage remains governed by its existing safety boundary.

## Production Boundary

v5.0 is not production because it does not enable real providers, final opinion generation, automatic Skill publishing, or automatic Workspace Runtime activation.

The default mode is mock-first / controlled-first.

## Personal Alpha Workspace

The Personal Alpha Workspace creates:

- unified workspace status
- unified audit timeline
- source trace aggregation placeholder
- mock or redacted-only workspace snapshot
- runtime-only storage record

The workspace snapshot is a local mock metadata artifact, not a legal deliverable.

## Gates

The workflow requires:

- explicit workspace confirmation
- manual review confirmation
- allowed workflow mode
- controlled local or mock provider mode
- runtime-only storage
- no raw content

`status_only` and `audit_timeline_only` may continue with confirmation warnings, but end-to-end modes require explicit confirmation and manual review.

## Safety Boundary

- v5.0 does not call a real LLM.
- v5.0 does not call DeepSeek live.
- v5.0 does not call real OCR.
- v5.0 does not call a real legal database.
- v5.0 does not submit raw material text.
- v5.0 does not submit raw OCR text.
- v5.0 does not submit raw legal search results.
- v5.0 workspace snapshot is stored only in ignored runtime storage.
- v5.0 does not generate a formal legal opinion.
- v5.0 does not automatically publish Skill.
- v5.0 does not automatically enable Workspace Runtime.

## Runtime Storage

Runtime records are written under:

`storage/runtime/personal_alpha_workspace`

Only mock or redacted metadata is stored:

- workspace run ID
- case ID
- workspace ID
- workflow mode
- stage statuses
- workspace snapshot
- unified audit timeline
- source refs
- timestamp

Raw material text, raw OCR text, real legal search results, and API keys are not stored.

## Audit Timeline

The unified audit timeline records mock stage events only. It does not contain raw material text, OCR text, legal search result text, API keys, real paths, client personal information, or case numbers.

## A1-A13

v5.0 does not alter the A1-A13 analysis chain.

A10 remains: 争议焦点法律深化分析。

## v5.1 Readiness

v5.1 can build on v5.0 with a Personal Alpha Case Dashboard that visualizes workspace runs, stage health, and audit timeline summaries while keeping the same local-only safety boundary unless separately approved.
