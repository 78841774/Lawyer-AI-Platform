# Production Readiness

v2.9 adds the foundation needed to move from local MVP development toward a real deployment.

v3.0 adds an Internal Alpha identity and workspace foundation for local demos. v3.1 adds Dev Token / API Key current-user resolution. This is not production authentication.

## Local Mode

Local mode remains the default:

```bash
APP_ENV=local
DATABASE_URL=sqlite:///./local.db
LLM_PROVIDER=mock
```

Start the backend locally:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
APP_ENV=local DATABASE_URL=sqlite:///./local.db LLM_PROVIDER=mock python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

When `APP_ENV=local`, the backend runs SQLAlchemy `create_all` on startup so the SQLite database remains easy to use for demos and development.

Local mode also seeds `Local Demo User` and `Local Demo Workspace` for the internal alpha.

Local mode also seeds `Local Dev Token`. Plaintext token values are not stored in the database; only SHA-256 hashes are stored.

## Docker PostgreSQL Mode

Docker Compose provides a local PostgreSQL service for deployment-style testing:

```bash
cd Lawyer-AI-Platform-App
docker compose up --build
```

The backend container uses:

```bash
APP_ENV=production
DATABASE_URL=postgresql+psycopg2://lawyer_ai:lawyer_ai_local@postgres:5432/lawyer_ai
LLM_PROVIDER=mock
```

No real API key is stored in `docker-compose.yml`.

## DATABASE_URL

Supported database URLs:

```bash
sqlite:///./local.db
postgresql+psycopg2://lawyer_ai:lawyer_ai_local@postgres:5432/lawyer_ai
```

SQLite is intended for local development. PostgreSQL is intended for production-like environments.

## APP_ENV

`APP_ENV=local` enables local startup conveniences, including automatic table creation.

`APP_ENV=production` disables automatic `create_all`. Production environments should create and evolve schema with Alembic migrations.

The v3.0 SQLite compatibility path can add `cases.workspace_id` and `cases.owner_user_id` during local startup only. Production deployments should use Alembic migrations for the new `users`, `workspaces`, `workspace_members`, and case ownership fields.

v3.1 adds `auth_tokens`. Production deployments should create this table with Alembic migrations, not local startup seeding.

## Alembic Plan

v2.9 adds Alembic configuration and an empty versions directory. Alembic reads `DATABASE_URL` from the backend settings.

Check migration state:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
alembic current
```

No initial migration is generated in v2.9. Before v3.0, generate an initial migration from the SQLAlchemy models and use migrations for production schema changes.

## Secrets Handling

Do not commit `.env` or real API keys. Use environment variables or a deployment secret manager for:

```bash
DEEPSEEK_API_KEY
OPENAI_API_KEY
POSTGRES_PASSWORD
LOCAL_DEV_TOKEN
```

`.env.example` contains placeholders only.

`LOCAL_DEV_TOKEN` is for local development. In non-local environments, protected endpoints require a token; if the database does not contain a matching active token hash, requests return `401`.

## LLM Provider Configuration

Default local provider:

```bash
LLM_PROVIDER=mock
```

DeepSeek Live Mode:

```bash
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_TIMEOUT_SECONDS=30
```

If `LLM_PROVIDER=deepseek` is set without `DEEPSEEK_API_KEY`, the backend still starts and `/llm/test` returns a structured error.

## Ready Now

* Environment-driven backend configuration.
* Local SQLite defaults.
* PostgreSQL connection support through SQLAlchemy and `psycopg2`.
* Docker Compose PostgreSQL service.
* Alembic foundation.
* Mock and DeepSeek LLM provider configuration.
* Internal alpha Local Demo Identity.
* Minimum workspace ownership fields for cases.
* Dev Token / API Key auth foundation.
* Current-user dependency for users, workspaces, and core case APIs.

## Not Ready Yet

* Real user login and authorization.
* JWT/session authentication.
* OAuth.
* Complex RBAC and workspace isolation enforcement.
* Production secret manager integration.
* Generated initial Alembic migration.
* Managed cloud deployment.
* Production logging, monitoring, backup, and restore process.
* Formal end-to-end test suite.
