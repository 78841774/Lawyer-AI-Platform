# Personal Production Runtime & Showcase Foundation v7.0

## Objective

v7.0 establishes the Personal Production Runtime & Showcase Foundation for AIHome.law. It moves the project from Personal Alpha Case OS release candidate metadata into a controlled personal production validation and product showcase phase.

v7.0 does not call real AI, OCR, or legal search providers. It does not generate final legal opinions, final report bodies, PDF or DOCX files, external deliveries, or automatic Skill publishing.

## Why Personal Production Before Team or Client Delivery

The roadmap now validates the personal production workflow before team workspace or external client delivery. This lets the system prove controlled runtime posture, showcase readiness, provider gating, and lawyer review flow in a narrower personal production setting first.

Route:

- Personal Alpha.
- Personal Production Runtime & Showcase.
- Real AI/OCR/Legal Search Controlled Runtime.
- Experience Package Skill Studio.
- Personal Production Pilot.
- Team Workspace when ready.
- External Client Delivery / Public Promotion Version when ready.

## Personal Production Mode

Personal production mode is defined as `controlled_ready` by default.

The mode keeps:

- Personal production execution disabled.
- Real providers disabled.
- External delivery disabled.
- Team workspace disabled.
- Lawyer review required.
- Manual final lock required.

## Showcase Mode

Showcase mode is enabled for product screenshots, demos, and presentation-ready UI.

It hides internal paths, provider secrets, raw source content, and heavy diagnostic payloads from the main screen. Developer diagnostics remain available in a collapsed section.

## Runtime Registry

v7.0 registers these runtime categories:

- AI Model Runtime.
- OCR Runtime.
- Legal Search Runtime.
- Skill Training Runtime.
- Delivery Runtime.
- Regression Runtime.
- Safety Runtime.

All live runtime modes remain disabled in v7.0. Mock and controlled metadata readiness are available.

## Provider Capabilities

v7.0 adds placeholder provider capability metadata for:

- OpenAI / GPT Provider.
- DeepSeek Provider.
- Local Model Provider.
- OCR Provider.
- Legal Search Provider.
- Case Law API Provider.
- Skill Training Provider.

The provider registry does not read `.env`, API keys, or local configuration paths.

## Readiness Checklist

The readiness API checks:

- Case OS release candidate readiness.
- Regression suite status.
- Hardening layer.
- Personal production mode.
- Showcase mode.
- AI/OCR/legal search/skill/delivery runtime registration.
- Lawyer review requirement.
- Manual final lock requirement.
- No automatic external delivery.
- No automatic final legal opinion.
- No public raw-content display.
- No provider secret exposure.

## Safety Boundary

v7.0 remains mock-first by default, controlled-first, provider-gated, lawyer-review-required, manual-final-lock-required, draft-first, and source-trace-required.

It does not enable real provider calls or external client delivery.

## UI/UX Showcase Requirements

The new `/personal-production` page provides:

- Showcase Hero.
- Production readiness cards.
- Runtime capability grid.
- Provider capability preview.
- Controlled workflow stepper.
- Safety and trust panel.
- Next v7 roadmap.
- Collapsed developer diagnostics.

The page is designed as a professional product console suitable for screenshots and demos.

## AI/OCR/Legal Search/Skill Roadmap

Next planned steps:

- v7.1 AI Provider Gateway & Prompt Runtime.
- v7.2 Controlled OCR Runtime.
- v7.3 Legal Search API Gateway.
- v7.4 Experience Package Skill Studio.

## Regression Updates

The regression suite now includes `check_personal_production_apis.sh`, which validates the v7.0 status, mode, showcase, runtime registry, provider capabilities, readiness, safety, and console summary APIs.

## v7.1 Readiness

v7.0 prepares the metadata foundation for v7.1 AI Provider Gateway & Prompt Runtime. Future provider work must remain controlled, gated, audited, and draft-first.
