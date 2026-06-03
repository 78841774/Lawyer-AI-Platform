# Internal Alpha

v3.0 established the minimum identity and workspace foundation required for an internal alpha.

v3.1 adds a Dev Token / API Key authentication foundation. It is still not a formal login system.

v3.2 adds JWT Auth Foundation. Local demo login exchanges `user_id + dev_token` for a JWT, but this is still not a production login system.

v3.2-B adds the AIHome.law branded frontend dashboard and product shell for internal alpha operations.

v3.2-C localizes the main frontend product copy for Chinese legal professionals while keeping the AIHome.law brand in English.

v3.3-A adds the frontend auth shell: the dashboard resolves the current user, current workspace, and current auth mode through authenticated API calls.

v3.3-C adds Runtime Trace UI surfaces for case detail, report detail, and runtime status pages. It only displays fields already returned by the backend APIs.

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

v3.0 also adds case ownership fields:

* `cases.workspace_id`
* `cases.owner_user_id`

For SQLite local development, backend startup checks for missing case ownership columns and adds them with `ALTER TABLE` when needed. Existing local cases are backfilled to `workspace_local_001` and `user_local_001`.

Production environments should use Alembic migrations instead of startup schema patching.

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

Navigation groups are reserved for:

* 主导航: 工作台, 案件, 报告.
* 智能能力: 技能, 经验包, 运行状态.
* 工作空间: 工作空间, 用户, 审计日志.
* 系统: 设置.
