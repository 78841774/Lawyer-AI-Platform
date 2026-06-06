# v7.29 Legal / Enterprise API Live Connection

v7.29 adds `/personal-legal-enterprise`, a controlled gateway for legal search and enterprise information API readiness.

Implementation location: `personal_legal_enterprise_gateway`.

API prefix: `/personal-legal-enterprise`.

The gateway registers legal search and enterprise information providers, secret boundary metadata, live gate metadata, usage / cost metadata, dry-run health, legal search dry-runs, enterprise lookup dry-runs, review queue metadata, source trace metadata, audit, and safety.

Legal search results are source-traced metadata candidates only and are not final citations. Enterprise information results are verification metadata only and are not final fact findings. Both require lawyer review.

This stage does not read API key values, call real providers, read real case materials, expose raw provider responses, train on open cases, write training sets, update or publish Skills, generate final legal opinions, generate final reports, create real PDF/DOCX files, send email, create public links, or trigger external delivery.
