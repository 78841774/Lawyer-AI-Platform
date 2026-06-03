# Internal Alpha

v3.0 established the minimum identity and workspace foundation required for an internal alpha.

v3.1 adds a Dev Token / API Key authentication foundation. It is still not a formal login system.

v3.2 adds JWT Auth Foundation. Local demo login exchanges `user_id + dev_token` for a JWT, but this is still not a production login system.

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
