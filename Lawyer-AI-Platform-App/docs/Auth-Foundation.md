# Auth Foundation v3.1

v3.1 adds the minimum authentication foundation for the internal alpha. It is a Dev Token / API Key foundation, not a formal login system.

## Scope

This stage does not add:

* Password login.
* OAuth.
* JWT sessions.
* Full RBAC.

The goal is to identify a request user before the platform moves to a real authentication provider.

## Dev Token Storage

v3.1 adds the `auth_tokens` table:

* `id`
* `token_id`
* `user_id`
* `token_hash`
* `token_name`
* `status`
* `created_at`
* `last_used_at`

Plaintext tokens are never stored in the database. The backend stores only a SHA-256 hash in `auth_tokens.token_hash`.

## Local Dev Token

When `APP_ENV=local`, startup ensures the local dev token exists:

```text
token_id: token_local_001
user_id: user_local_001
token_name: Local Dev Token
status: active
```

The plaintext token comes only from the environment:

```bash
LOCAL_DEV_TOKEN=dev-local-token
```

If `LOCAL_DEV_TOKEN` is not set, the backend uses `dev-local-token` for local development.

## Request Headers

The backend accepts either header:

```bash
Authorization: Bearer dev-local-token
X-Dev-Token: dev-local-token
```

If a token is provided, it must be valid. A wrong token returns `401`, even in local mode.

If no token is provided:

* `APP_ENV=local` falls back to `user_local_001`.
* Non-local environments return `401`.

## APIs

```bash
GET /auth/status
GET /auth/dev-token
```

`GET /auth/status` returns:

```json
{
  "authenticated": true,
  "user_id": "user_local_001",
  "auth_mode": "dev_token"
}
```

`auth_mode` can be:

* `dev_token`
* `local_fallback`

`GET /auth/dev-token` is available only when `APP_ENV=local`. It returns example headers for the configured local token. Production returns `403`.

## Protected APIs

v3.1 routes these endpoints through current-user resolution:

* `GET /users/me`
* `GET /workspaces`
* `GET /workspaces/{workspace_id}`
* `GET /workspaces/{workspace_id}/cases`
* `POST /cases`
* `GET /cases`
* `GET /cases/{case_id}`

Runtime endpoints can be moved to the same dependency in later hardening work.

## Workspace Rules

* Users can list only active workspaces where they are active members.
* Users can see cases only in workspaces they can access.
* `POST /cases` uses the current user's first active workspace.
* If the current user has no active workspace, `POST /cases` returns `400`.

## Next Step

v3.2 can replace or extend Dev Token identity with JWT or OAuth while keeping the same current-user dependency boundary.
