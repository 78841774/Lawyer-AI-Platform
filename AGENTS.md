# Coding Agent Guide

## Current Direction

AIHome.law / Lawyer-AI-Platform is prioritizing personal production validation and showcase-ready presentation. Team workspace and external client delivery versions are deferred.

## Required Context

Read these files before substantial work:

- `00-Project-Context/CURRENT_STATE.md`
- `00-Project-Context/ROADMAP.md`
- `00-Project-Context/PROVIDER_ROADMAP.md`
- `00-Project-Context/SAFETY_BOUNDARY.md`
- `00-Project-Context/RELEASE_INDEX.md`
- `00-Project-Context/CODEX_HANDOFF.md`
- `00-Project-Context/NEXT_TASK.md`

## Safety Boundary

- mock-first by default
- controlled-first
- provider-gated
- manual-approval-required
- lawyer-review-required
- draft-only
- source-trace-required
- no automatic final legal opinion
- no automatic final report
- no automatic external delivery
- no automatic Skill publish
- no uncontrolled raw content exposure
- provider secrets never visible
- live provider calls disabled unless explicitly enabled in the target version

## Forbidden

- Do not reset the repository.
- Do not checkout over user changes.
- Do not call real providers.
- Do not read API keys.
- Do not return API keys.
- Do not expose raw case materials.
- Do not commit `.env`, `local.db`, `storage/runtime`, `node_modules`, `__pycache__`, `.DS_Store`, or real case materials.
- Do not mark AI output as final legal opinion.
- Do not generate final report text unless the target version explicitly permits it.

## Pre-Commit Checks

Before committing, run:

- backend compileall
- frontend build
- API smoke checks for the active version
- Personal Production regression checks
- full regression suite when feasible
- `git diff --check`
- sensitive-file status checks

## Current Next Task

Next Task: v7.9 Personal Production Demo Script & Screenshot Pack validation / release pending. Do not commit, tag, or push v7.9 until the user explicitly confirms commit/release handling.

## v7.9 Demo Pack Notes

- Keep the `个人生产` AppShell group as the primary route for v7.x showcase work.
- Keep Developer Diagnostics folded by default.
- Use shared Personal Production UI components for safety badges, Trust / Safety panels, steppers, status cards, and diagnostics where practical.
- Keep frontend display copy Chinese by default while allowing API field names and diagnostics JSON to remain English.
- Keep demo and promotional material mock-first, metadata-only, lawyer-review-required, source-trace-required, and provider-gated.
- Do not describe mock samples as real cases or imply automatic external delivery.
