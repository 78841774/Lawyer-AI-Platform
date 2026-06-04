# Real Case Local Sandbox v3.9

## Purpose

v3.9 prepares a local-only sandbox foundation for future personal real case dry-run workflows.

This stage only builds safety guards, dry-run workflow, status APIs, and audit log foundation. It is not production deployment and it does not process real case content.

## Why This Sandbox Exists

Future internal alpha work may need a controlled local workspace for personal real case testing. Before any real material can be considered, the platform needs a visible safety boundary:

* local-only case workspace rules
* provider mode guard
* material safety guard
* Git safety guard
* dry-run workflow
* manual review gate
* audit log foundation

## Local-Only Case Workspace Principles

Allowed roots are examples only:

* `~/Lawyer-AI-Local-Cases`
* `~/AIHome-Law-Local-Sandbox`

v3.9 does not automatically read these directories. It only checks path strings during dry-run.

Real case material must stay outside Git and must be ignored by Git. The repository must not contain `sandbox_cases`, `real_cases`, or `case_workspaces`.

## Provider Mode Guard

Allowed modes:

* `mock`
* `local`
* `local_only`
* `disabled`

Blocked modes:

* `live`
* `deepseek`
* `deepseek_live`
* `production`
* `remote`
* `external`

The guard blocks real LLM, DeepSeek live, real OCR, and real legal search provider modes during v3.9.

## Material Safety Guard

The material guard:

* Does not read file content.
* Does not traverse local case material folders.
* Does not upload material.
* Does not write real filenames.
* Redacts the local case root in audit logs.
* Blocks repository-internal paths such as `real_cases`, `sandbox_cases`, `case_workspaces`, and `storage/runtime`.

## Git Safety Guard

The Git guard checks for staged or tracked sensitive paths:

* `.env`
* `local.db`
* `sandbox_cases`
* `real_cases`
* `case_workspaces`
* `storage/runtime`
* `__pycache__`
* `__MACOSX`
* `.DS_Store`

The guard only reports. It does not delete, move, or untrack user files.

## Dry-Run Workflow

`POST /local-sandbox/dry-run`:

1. Runs Provider Mode Guard.
2. Runs Material Safety Guard.
3. Runs Git Safety Guard.
4. Returns `allowed_to_continue`.
5. Writes a local sandbox audit log.

Dry-run does not:

* Read real case material.
* Call real OCR.
* Call a real legal database.
* Call a real LLM.
* Call DeepSeek live provider.
* Create a report.
* Create a Skill.
* Publish Skill Registry records.
* Enable Workspace Runtime.
* Modify case data.

## Audit Log Foundation

Audit logs record only safe metadata:

* dry-run ID
* event type
* demo case/workspace IDs
* provider modes
* result
* warnings
* created time

Audit logs do not store:

* real material paths
* real filenames
* real OCR text
* real customer names
* API keys

## API

v3.9 adds:

* `GET /local-sandbox/status`
* `GET /local-sandbox/guards`
* `POST /local-sandbox/dry-run`
* `GET /local-sandbox/audit-logs`

## Relation To v3.6

v3.6 Skill Factory remains unchanged. v3.9 does not train, publish, overwrite `skill_001` / `skill_002`, or automatically enable Skill-aware case processing.

## Relation To v3.7

v3.7 OCR and Legal Search adapters remain mock-only. v3.9 guards prevent accidental use of real OCR or real legal search provider modes.

## Relation To v3.8

v3.8 Source Trace remains mock/local metadata only. v3.9 prepares local sandbox safety checks for future dry-run workflows, but does not attach real material citations.

## v4.0 Preparation

v3.9 prepares for a future v4.0 Internal Alpha Deployment Preparation stage:

* production environment skeleton
* secret management checklist
* backup and logging checklist
* permission checklist
* local-only real case manual procedure
* deployment readiness dashboard

## Safety Boundary

v3.9 does not read real case material content.
v3.9 does not call real OCR.
v3.9 does not call a real legal database.
v3.9 does not call a real LLM.
v3.9 does not call DeepSeek live provider.
v3.9 does not commit real case material.
v3.9 does not commit API keys.
v3.9 does not automatically process real cases.
v3.9 does not automatically enable Workspace Runtime.
v3.9 only prepares local sandbox guard, dry-run, and audit log foundation.

A1-A13 remain unchanged.
A10 remains `争议焦点法律深化分析`.
