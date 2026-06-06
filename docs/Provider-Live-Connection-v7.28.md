# v7.28 Unified Personal Live Connection Dashboard

v7.28 adds `/personal-live-connection`, a unified dashboard and API layer for AI, OCR, Document, Legal, and Enterprise provider readiness.

Chinese positioning: 个人生产统一受控接口接入总控台.

Implementation location: `personal_live_connection`.

v7.28 is not a standalone AI Provider Live Connection. AI Provider is one provider category inside the unified dashboard. The dashboard summarizes AI / OCR / Document / Legal / Enterprise provider readiness, secret boundary, live gate, usage / cost, health, audit, and safety metadata.

v7.29 may still add an independent Legal / Enterprise gateway because the v7.28 dashboard is an aggregation and control surface, not a replacement for category-specific gateway metadata.

The runtime remains dry-run by default and live-disabled. It returns provider cards, secret boundary metadata, live gate metadata, usage / cost metadata, dry-run health metadata, run metadata, audit, and safety. It does not execute provider network calls in this stage.

All outputs remain metadata-only, draft-only, owner-only, lawyer-review-required, source-trace-required, and audit-required. API key values are never read or returned. No final legal opinion, final report, real PDF/DOCX, email, public link, external delivery, Skill publishing, or training-set write is triggered.
