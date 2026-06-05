# Codex Handoff

Before starting a new Codex session, read these files:

- `AGENTS.md`
- `00-Project-Context/CURRENT_STATE.md`
- `00-Project-Context/ROADMAP.md`
- `00-Project-Context/PROVIDER_ROADMAP.md`
- `00-Project-Context/SAFETY_BOUNDARY.md`
- `00-Project-Context/RELEASE_INDEX.md`
- `00-Project-Context/NEXT_TASK.md`

## Required Conduct

- Do not reset the repository.
- Do not checkout over user changes.
- Do not call real providers.
- Do not read API keys.
- Do not return API keys.
- Do not commit `.env`, `local.db`, `storage/runtime`, `node_modules`, `__pycache__`, `.DS_Store`, or real case materials.
- Keep provider-gated and mock-first behavior unless a target version explicitly changes it.
- Keep lawyer review required for AI-assisted legal workflows.
- Keep AI output draft-only unless a target version explicitly changes it.
- Run the regression suite before committing.

## Commit Boundary

Each version commit should include code, tests, docs, changelog, and project context updates that are part of that version.

## Current Handoff

- Stable baseline: `v7.8-ui-polish-showcase-hardening` at commit `b7ce642`.
- Active local worktree scope: v7.9 Personal Production Demo Script & Screenshot Pack.
- v7.9 must remain mock-first, metadata-only, draft-only, lawyer-review-required, final-lock-required, source-trace-required, and provider-gated.
- v7.9 does not introduce a new backend runtime, live provider mode, real final document generation, email sending, or external delivery.
- Do not commit, tag, or push v7.9 until validation is complete and the user explicitly approves commit and release work.
