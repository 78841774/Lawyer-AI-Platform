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

- Stable baseline: `v7.5-personal-production-workflow-stack` at commit `75ca460`.
- Active local worktree scope: v7.6 Personal Delivery Packet.
- v7.6 must remain mock-first, metadata-only, draft-only, lawyer-review-required, final-lock-required, and source-trace-required.
- Do not start v7.7 until v7.6 validation and release preparation are complete and the user explicitly approves the next phase.
