# Internal Alpha

v3.0 established the minimum identity and workspace foundation required for an internal alpha.

v3.1 adds a Dev Token / API Key authentication foundation. It is still not a formal login system.

v3.2 adds JWT Auth Foundation. Local demo login exchanges `user_id + dev_token` for a JWT, but this is still not a production login system.

v3.2-B adds the AIHome.law branded frontend dashboard and product shell for internal alpha operations.

v3.2-C localizes the main frontend product copy for Chinese legal professionals while keeping the AIHome.law brand in English.

v3.3-A adds the frontend auth shell: the dashboard resolves the current user, current workspace, and current auth mode through authenticated API calls.

v3.3-C adds Runtime Trace UI surfaces for case detail, report detail, and runtime status pages. It only displays fields already returned by the backend APIs.

v3.3-D improves Report / Skill visibility across reports, skills, experience packages, and the skill registry without changing the Skill Training main chain.

v3.4-A adds a Real Case Intake foundation for richer case creation fields while keeping the existing `POST /cases` API compatible with title-only creation.

v3.4-B adds folder-aware material intake so local users can upload a case material folder while preserving relative paths and directory context.

v3.4-C adds local end-to-end validation and hardening for the real case intake loop.

v3.5 adds Run History / Fact Dedup Foundation for repeated fact extraction, legal analysis, and report generation runs.

v3.6-B adds read-only Legacy Skill Analysis for existing casework Skills, SkillOpt datasets, and SkillOpt output artifacts. It confirms that legacy training data must be reshaped into reviewed data packages before any training or Skill Registry import.

## Scope

This stage adds local identity and workspace ownership only. It does not add:

* Password registration.
* Production JWT session management.
* OAuth or SSO.
* Payment.
* Complex RBAC.

The current identity modes are:

* `local_fallback`
* `dev_token`
* `jwt`

The frontend displays these as `local`, `dev_token`, or `JWT` for the internal alpha shell.

## Local Demo User

When `APP_ENV=local`, backend startup ensures this user exists:

```json
{
  "user_id": "user_local_001",
  "email": "local@example.com",
  "display_name": "Local Demo User",
  "role": "admin",
  "status": "active"
}
```

## Local Demo Workspace

When `APP_ENV=local`, backend startup ensures this workspace exists:

```json
{
  "workspace_id": "workspace_local_001",
  "name": "Local Demo Workspace",
  "owner_user_id": "user_local_001",
  "status": "active"
}
```

The local user is also inserted into `workspace_members` as an active admin member.

## Local Dev Token

When `APP_ENV=local`, backend startup ensures this dev token record exists:

```json
{
  "token_id": "token_local_001",
  "user_id": "user_local_001",
  "token_name": "Local Dev Token",
  "status": "active"
}
```

The plaintext token is read from `LOCAL_DEV_TOKEN`; if unset, local mode uses `dev-local-token`.

The database stores only the SHA-256 token hash. It does not store the plaintext token.

## Local JWT Login

v3.2 adds:

```bash
POST /auth/login
```

Request:

```json
{
  "user_id": "user_local_001",
  "dev_token": "dev-local-token"
}
```

Response includes a bearer JWT. The JWT contains `sub`, `exp`, and `jti`.

Production deployments must replace `JWT_SECRET_KEY`; `.env.example` contains local example values only.

The v3.3-A frontend auth shell stores the JWT in browser `localStorage` and attaches it to API requests as:

```bash
Authorization: Bearer <jwt>
```

When no JWT is present and the API base is local, the frontend can use the local dev token fallback with:

```bash
X-Dev-Token: dev-local-token
```

This fallback is only for local development and does not replace production authentication.

## Tables

v3.0 adds:

* `users`
* `workspaces`
* `workspace_members`

v3.1 adds:

* `auth_tokens`

v3.5 adds runtime history tables:

* `extraction_runs`
* `analysis_runs`
* `report_runs`

v3.6-B adds no database tables.

v3.0 also adds case ownership fields:

* `cases.workspace_id`
* `cases.owner_user_id`

v3.4-A adds nullable case intake fields:

* `cases.client_name`
* `cases.counterparty_name`
* `cases.contract_type`
* `cases.dispute_amount`
* `cases.jurisdiction`
* `cases.intake_notes`

Existing fields `cases.case_type` and `cases.objective` are reused for the intake form.

For SQLite local development, backend startup checks for missing case ownership and intake columns and adds them with `ALTER TABLE` when needed. Existing local cases are backfilled to `workspace_local_001` and `user_local_001`.

Production environments should use Alembic migrations instead of startup schema patching.

## Legacy Skill Analysis

v3.6-B found these local legacy assets:

* 17 legacy Skill assets.
* 19 SkillOpt dataset files.
* 96 SkillOpt dataset items.
* 14 SkillOpt output runs.
* 12 SkillOpt `best_skill.md` outputs.

The known Skill families are:

* `case-fact-extractor-v3`
* `case-analysis-pro-v3`
* `legal-casework-router`

This stage is analysis only. It does not create Skills, publish Experience Packages, import Skill Registry records, run LLM calls, or change the Skill Training main chain.

The required next step is to reshape reviewed legacy data into Dataset Packages, Runtime Rules, Prompt Templates, Report Templates, and Evaluation Rubrics before any training stage.

## APIs

```bash
GET /users/me
GET /workspaces
GET /workspaces/{workspace_id}
GET /workspaces/{workspace_id}/cases
POST /workspaces/{workspace_id}/cases
GET /cases
GET /cases/{case_id}
POST /cases
GET /auth/status
POST /auth/login
GET /auth/dev-token
```

In v3.1, `POST /cases` keeps the simple create flow and uses the current user's first active workspace.

```json
{
  "workspace_id": "workspace_local_001",
  "owner_user_id": "user_local_001"
}
```

`POST /workspaces/{workspace_id}/cases` writes the requested active workspace and the current local user.

## Minimum Checks

The internal alpha only checks:

* Current user must be active.
* Workspace must exist and be active.
* Case creation must target an active workspace.
* Users can access only workspaces where they are active members.
* Non-local environments require a token for protected endpoints.
* Bearer JWT requests are resolved before dev token requests.

## Next Step

v3.3 can replace local demo login with formal password, OAuth, or SSO authentication.

## AIHome.law Frontend

The internal alpha frontend now uses the AIHome.law brand:

* Brand name: `AIHome.law`
* Chinese tagline: `法律 AI 工作空间`
* Hero copy: `把案件材料转化为事实、法律分析、报告与可复用经验。`
* Product style: legal-tech console with dark navy, graphite, white, professional blue, and gold accents.
* Main UI copy is Chinese-first for internal alpha users.
* API fields and technical identifiers such as `case_id`, `workspace_id`, `owner_user_id`, `skill_id`, `package_id`, `llm_provider`, and `source_refs` remain in English for compatibility.

The frontend shell is designed for long-term expansion:

* Left sidebar with grouped navigation.
* Topbar with current workspace, auth mode, runtime provider, and user status.
* Main content area for workflow pages.
* Future space for inspector or activity panels.

The Dashboard auth card resolves:

* 当前用户 through `GET /users/me`.
* 当前工作空间 through `GET /workspaces` followed by `GET /workspaces/{workspace_id}`.
* 当前认证模式 through `GET /auth/status`.

## Runtime Trace UI

v3.3-C displays runtime trace information without changing backend storage or Skill Training:

* Case Detail shows LLM runtime status, fact extraction records, legal analysis records, report runtime records, and an audit-trail empty state.
* Report Detail shows report runtime metadata, including `llm_provider`, `llm_status`, `skill_used`, `package_used`, and `source_refs` when present.
* Runtime page shows Provider, Model, Configured, and Base URL Configured status.
* Missing backend fields are rendered as `暂无`, `暂无运行记录`, or `暂无引用来源`.

Current persisted runtime data is limited:

* Report `source_refs` persists `fact_ids`, `analysis_id`, `llm_provider`, `llm_status`, and optionally `skill_id` / `package_id`.
* Fact list records persist `fact_id`, `material_id`, `confidence`, `status`, and `created_at`, but not independent `source_refs` or LLM metadata.
* Legal analysis list records persist `analysis_id`, `case_id`, `status`, `risk_level`, `confidence`, and `created_at`, but not independent LLM metadata.

No `/skill-candidates/*` API, Skill Candidate table, Real Business Intake flow, or production deployment is added in this phase.

## Run History / Fact Dedup Foundation

v3.5 persists runtime runs for:

* `POST /cases/{case_id}/facts/extract`
* `POST /cases/{case_id}/analysis/run`
* `POST /cases/{case_id}/reports/generate`

Each run records `run_id`, status, LLM metadata, skill/package metadata, source references, created/completed timestamps, and an `is_latest` marker. Only one run of each type is marked latest per case.

Fact extraction now applies deterministic deduplication within the same case. If normalized fact content, `material_id`, and `fact_type` match an existing fact, the existing fact is reused instead of creating a duplicate. This phase does not add semantic deduplication, vectors, OCR, DeepSeek Live validation, production deployment, or Skill Training main-chain changes.

Case Detail displays `运行历史` with fact extraction, legal analysis, and report generation run groups. Intake Status also returns latest run ids when available.

## Report / Skill Visibility

v3.3-D makes existing report and skill metadata visible in the frontend:

* Reports page displays `report_id`, `case_id`, `report_type`, LLM metadata, Skill metadata, Package metadata, and `created_at`.
* Report Detail keeps the report runtime information area and structures `source_refs` fields such as `fact_ids`, `analysis_id`, `llm_provider`, `llm_status`, `skill_id`, and `package_id`.
* Skills page displays Skill records from `GET /skills`, including `case_id`, `evaluation_score`, `validation_status`, and `package_path`.
* Experience Packages page displays `GET /experience-packages` results and provides a manifest detail page.
* Skill Registry page displays `GET /skill-registry` results and provides publish/deprecate actions backed by existing endpoints.

This phase does not modify Skill Training, add `/skill-candidates/*`, or change backend persistence.

## Real Case Intake Foundation

v3.4-A makes case creation closer to a real legal intake workflow while staying intentionally small:

* Create Case page collects `title`, `client_name`, `counterparty_name`, `case_type`, `contract_type`, `dispute_amount`, `jurisdiction`, `objective`, and `intake_notes`.
* `title` remains the only required frontend field.
* `POST /cases` remains the creation endpoint and still supports title-only requests.
* `GET /cases` and `GET /cases/{case_id}` return the new nullable intake fields.
* Cases list displays client, counterparty, case type, contract type, and dispute amount.
* Case Detail displays a dedicated `Intake 信息` card.

This phase does not add OCR, PDF parsing enhancements, formal legal review, team approval, Skill Training changes, production deployment, or `/skill-candidates/*` APIs.

## Folder-Aware Material Intake

v3.4-B extends material intake without changing the Skill Training main chain:

* Case Detail supports single-file upload and browser folder upload.
* Folder upload reads `webkitRelativePath` and sends it as `relative_path`.
* Material records preserve `original_filename`, `relative_path`, `folder_path`, `file_ext`, `upload_batch_id`, and `display_order`.
* Old material rows are compatible through fallbacks to `filename`, empty `folder_path`, and `display_order = 0`.
* Materials are stored under `storage_root/original-files/{case_id}/{upload_batch_id}/`.
* Relative paths are cleaned to prevent path traversal.
* Material Center groups uploaded files by folder path.
* Fact extraction prompt/context includes filename and folder path metadata.
* Fact extraction responses include material `source_refs` where available.

This phase does not add complex OCR, zip automatic extraction, PDF parsing enhancement, formal legal review, or team approval. Local testing should use sanitized materials only.

## Real Case Intake E2E Validation

v3.4-C validates the internal alpha loop:

```text
Real Case Intake -> Folder-aware Material Upload -> Intake Status -> Fact Extraction -> Legal Analysis -> Report Generation -> Runtime Trace -> Report Detail Review
```

Added hardening:

* `GET /cases/{case_id}/intake/status` returns material/fact/analysis/report counts and next recommended action.
* Case Detail displays Intake status, next-step hints, material folder grouping, and recent runtime result summaries.
* Fact extraction responses expose `source_refs` with material `filename` and `relative_path`.
* Report generation `source_refs` includes `material_refs` where available.
* `scripts/validate_real_case_intake_v3_4.py` runs the local E2E check with temporary sanitized text samples.

This phase does not add complex OCR, zip automatic extraction, DeepSeek Live testing, Skill Training changes, production deployment, or formal legal opinion generation.

Navigation groups are reserved for:

* 主导航: 工作台, 案件, 报告.
* 智能能力: 技能, 经验包, 运行状态.
* 工作空间: 工作空间, 用户, 审计日志.
* 系统: 设置.
