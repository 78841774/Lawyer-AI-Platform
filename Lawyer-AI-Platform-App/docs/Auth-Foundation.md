# Auth Foundation

v3.1 adds the minimum authentication foundation for the internal alpha. It is a Dev Token / API Key foundation, not a formal login system.

v3.2 adds JWT Auth Foundation for local demo login, JWT verification, and request identity parsing. It is still not a complete production login system.

v3.2-B surfaces auth state in the AIHome.law Dashboard and provides local login/logout controls.

## Scope

This stage does not add:

* Password login.
* OAuth.
* User registration.
* SSO.
* Full RBAC.

The goal is to identify a request user before the platform moves to a real authentication provider.

## JWT Configuration

v3.2 adds:

```bash
JWT_SECRET_KEY=local-dev-secret-change-me
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=120
```

`JWT_SECRET_KEY` must be replaced in production. Do not commit a real secret.

JWT access tokens include:

* `sub` as `user_id`
* `exp`
* `jti`

Expired or invalid JWTs return `401`.

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

The backend accepts these auth headers:

```bash
Authorization: Bearer <jwt>
Authorization: Bearer dev-local-token
X-Dev-Token: dev-local-token
```

Authentication priority:

* Bearer JWT
* Bearer dev token
* `X-Dev-Token`
* local fallback when `APP_ENV=local`

If a token is provided, it must be valid. A wrong token returns `401`, even in local mode.

If no token is provided:

* `APP_ENV=local` falls back to `user_local_001`.
* Non-local environments return `401`.

## APIs

```bash
GET /auth/status
POST /auth/login
GET /auth/dev-token
```

`POST /auth/login` is an Internal Alpha login endpoint:

```json
{
  "user_id": "user_local_001",
  "dev_token": "dev-local-token"
}
```

It returns:

```json
{
  "access_token": "...",
  "token_type": "bearer",
  "expires_in": 7200,
  "user_id": "user_local_001"
}
```

This endpoint uses `user_id + dev_token` only for internal alpha. v3.3 can replace it with password, OAuth, or SSO login.

`GET /auth/status` returns:

```json
{
  "authenticated": true,
  "user_id": "user_local_001",
  "auth_mode": "jwt",
  "expires_at": "2026-06-03T12:00:00+00:00"
}
```

`auth_mode` can be:

* `jwt`
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

v3.3 can replace the internal alpha login with formal password, OAuth, or SSO authentication.

## Frontend Auth Dashboard

The AIHome.law Dashboard displays:

* `auth_mode`
* current user
* current workspace
* local login and logout controls

Local Login calls `POST /auth/login`, stores the returned JWT in `localStorage`, and frontend API requests attach `Authorization: Bearer <token>`.

When the local JWT is cleared, local development can still show `local_fallback` through backend fallback behavior.
