# v7.27 OCR / Document Provider Live Connection

v7.27 adds a controlled OCR / Document provider live connection readiness layer under `/personal-material-runtime/live`.

Implementation location: `personal_material_runtime.live_gateway`.

API prefix: `/personal-material-runtime/live`.

The v7.27 implementation intentionally extends the existing Personal Material Runtime. It does not add a separate OCR-only route; this is the current design choice, not a missing route.

The stage is owner-only, metadata-only, draft-only, provider-gated, and dry-run by default. It exposes provider registry, secret boundary, live gate, dry-run health, source trace, audit, and safety metadata. It does not read API key values, upload materials, return raw OCR text, return raw document content, inject content into AI prompts, generate final legal opinions, generate final reports, create real PDF/DOCX files, send email, create public links, or trigger external delivery.

Key endpoints include provider metadata, secret boundary, live gate, dry-run health, live gate mock metadata, audit, and safety checks.
