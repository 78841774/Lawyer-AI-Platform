# Internal Alpha Deployment v4.0

## Goal

v4.0 prepares a personal local Internal Alpha readiness foundation. It is designed for dashboard visibility, local sandbox guard summaries, dry-run workflow checks, audit logs, deployment readiness, secret/database/runtime readiness, and a manual review gate.

v4.0 is not production deployment. It is not team-wide collaboration. It does not automatically process real cases.

## Safety Boundary

- v4.0 does not read real case material content.
- v4.0 does not call real OCR.
- v4.0 does not call real legal databases.
- v4.0 does not call real LLMs.
- v4.0 does not call DeepSeek live provider.
- v4.0 does not commit real case materials.
- v4.0 does not commit API keys.
- v4.0 does not automatically enable Workspace Runtime.
- v4.0 does not automatically publish Skill Registry entries.
- v4.0 only provides Internal Alpha readiness, dry-run, dashboard, checklist, and audit foundation.

## Local-Only Real Case Preparation

Real case preparation must remain local-only and dry-run-only. Any real materials must stay outside Git, outside the application storage tree, and outside tracked repositories. The supported local-only roots are intended for later personal dry-run preparation only.

The Internal Alpha dry-run calls v3.9 Local Sandbox guards and blocks live provider modes. It records only redacted path markers in audit logs.

## Dashboard

The `/internal-alpha` dashboard shows:

- Internal Alpha status
- Deployment readiness checklist
- Secret management checklist
- Database readiness status
- Subsystem status aggregation
- Internal Alpha dry-run form
- Dry-run result
- Audit logs

## Deployment Readiness Checklist

The checklist includes Git cleanliness, sensitive ignore rules, local DB ignore rules, real case directory ignore rules, local sandbox readiness, provider live disablement, real OCR disablement, real legal search disablement, Workspace Runtime auto-disablement, and manual review requirements.

Build and compile checks are marked for manual verification because the readiness API does not run build commands or external services.

## Secret Management

The secret checklist reports whether secret handling boundaries are in place. It never returns secret values. Local dev JWT settings are acceptable only for Internal Alpha. Production requires external secret management and rotated secrets.

## Database Readiness

v4.0 supports SQLite local alpha mode and keeps `local.db` ignored. The backend remains `DATABASE_URL` based and PostgreSQL-ready in architecture. Production migration remains out of scope.

## Dry-Run Workflow

The Internal Alpha dry-run:

1. Requires `dry_run_only=true`.
2. Requires manual review confirmation.
3. Calls v3.9 Local Sandbox dry-run.
4. Checks readiness.
5. Blocks live, DeepSeek live, production, remote, and external modes.
6. Writes a local mock audit log.
7. Does not read material content, create reports, create skills, publish registries, or enable runtime.

## Audit Logs

Audit logs record only local alpha identifiers, case/workspace identifiers, provider modes, result, warnings, timestamps, and `<local_case_root_redacted>`. They do not record real material paths, file content, OCR text, API keys, customer names, or sensitive details.

## Relationship To v3.6-v3.9

v4.0 aggregates and preserves earlier foundations:

- v3.6 Skill Factory remains controlled, human-reviewed, and not auto-published.
- v3.7 OCR and Legal Search remain mock adapter foundations.
- v3.8 Source Trace remains mock source reference/citation foundation.
- v3.9 Local Sandbox guards are reused as the active dry-run safety gate.

## A1-A13

A1-A13 remain unchanged:

- A1: 案由分析
- A2: 法规清单
- A3: 类案检索
- A4: 请求权 / 抗辩权基础
- A5: 举证策略
- A6: 诉状 / 答辩状
- A7: 诉求量化 / 反请求
- A8: 证据清单
- A9: 质证意见
- A10: 争议焦点法律深化分析
- A11: 庭审提纲
- A12: 代理词
- A13: 结案报告 / 结案框架

A10 remains: 争议焦点法律深化分析.

## Next Step

v4.1 should prepare a Personal Real Case Alpha dry-run flow for local external folders, metadata-only material inventory, mock previews, source trace preview, report draft preview, and manual review. It remains non-production and local-only.
