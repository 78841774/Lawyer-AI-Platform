# Next Task

Next Task: v7.3-v7.5 validation and release preparation

## Goal

Validate and close the current local worktree implementation for:

- v7.3 Legal & Enterprise Intelligence Gateway.
- v7.4 Experience Package Skill Studio.
- v7.5 Real Case Production Workflow.

## Expected Direction

- Confirm v7.3 legal search and enterprise intelligence gateway APIs.
- Confirm v7.4 experience package, skill candidate, test case, evaluation, and promotion gate APIs.
- Confirm v7.5 case production, workflow orchestration, readiness, and lawyer review gate APIs.
- Keep all three versions mock-first, controlled-first, provider-gated, source-trace-required, and lawyer-review-required.
- Keep v7.3, v7.4, and v7.5 marked as validation/release pending until commit and tag are created.
- Do not start v7.6 Personal Delivery Packet unless validation passes and the user explicitly starts it.

## Safety Boundary

- No real provider calls.
- No API key reads.
- No raw case material reads.
- No final legal opinion.
- No final report.
- No external delivery.
- No automatic Skill publish.
