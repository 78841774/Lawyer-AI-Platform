# Internal Alpha v3.0

v3.0 establishes the minimum identity and workspace foundation required for an internal alpha.

## Scope

This stage adds local identity and workspace ownership only. It does not add:

* Password login.
* JWT authentication.
* Payment.
* Complex RBAC.

The current identity mode is **Local Demo Identity**.

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

## Tables

v3.0 adds:

* `users`
* `workspaces`
* `workspace_members`

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
```

`POST /cases` keeps the old simple create flow and automatically writes:

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

## Next Step

v3.1 should replace Local Demo Identity with a real authentication system and formal authorization boundaries.
