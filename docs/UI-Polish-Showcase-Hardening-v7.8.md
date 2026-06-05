# UI Polish & Showcase Hardening v7.8

## Positioning

v7.8 unifies the Personal Production showcase experience across the v7.x page matrix. It does not add a new backend runtime. It focuses on page structure, Chinese UI copy, navigation clarity, Trust / Safety presentation, and repeatable UI polish regression.

## Page Matrix

- `/personal-production`: personal production control console and readiness overview.
- `/personal-showcase-pack`: showcase story flow and pilot sample presentation.
- `/personal-delivery-packet`: delivery packet draft, source bundle, export readiness, and final lock queue.
- `/personal-case-production`: controlled case production workflow.
- `/personal-skill-studio`: experience package and skill candidate draft studio.
- `/personal-intelligence`: legal and enterprise intelligence mock gateway.
- `/personal-material-runtime`: material parsing and OCR runtime preview.
- `/personal-ai-gateway`: AI gateway and draft runtime.

## Product Design Direction

v7.8 follows Product Design direction C: mixed workbench.

- `/personal-production` remains the operating overview.
- `/personal-showcase-pack` becomes the primary demo route.
- Runtime pages keep operational detail while sharing the same safety and diagnostics pattern.

## Shared UI Components

The frontend now has a shared Personal Production UI layer for:

- safety badges.
- status cards.
- runtime cards.
- story / showcase steppers.
- Trust / Safety panels.
- folded Developer Diagnostics.
- metadata row display.

## Safety Boundary

All Personal Production showcase pages must keep the following posture visible:

- mock-first.
- controlled-first.
- provider-gated.
- metadata-only.
- draft-only.
- lawyer-review-required.
- source-trace-required.
- final-lock-required.
- no final legal opinion.
- no final report.
- no automatic external delivery.
- no email sending.
- no real PDF/DOCX generation.

## Regression

`scripts/regression/check_personal_ui_polish.sh` checks:

- the eight Personal Production pages exist.
- Developer Diagnostics stay folded by default.
- shared Trust / Safety copy is present.
- AppShell includes the unified Personal Production navigation group.
- overclaiming UI phrases are absent from checked project surfaces.
- frontend display code does not contain local path or secret markers.

The check is included in `scripts/regression/run_personal_alpha_regression.sh`.
