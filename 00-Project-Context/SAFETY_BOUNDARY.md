# Safety Boundary

The project safety posture is:

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

## Forbidden By Default

- Do not call real providers.
- Do not read API keys.
- Do not return API keys.
- Do not expose raw case materials.
- Do not label AI output as final legal opinion.
- Do not generate final report content without the target version explicitly allowing it.
- Do not publish Skills automatically.
