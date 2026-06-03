# Local Development

## Backend

Start the backend from the backend directory:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
pip install -r requirements.txt
APP_ENV=local DATABASE_URL=sqlite:///./local.db LLM_PROVIDER=mock uvicorn app.main:app --reload --port 8001
```

The backend uses SQLite for local development. The database file is created at:

```text
Lawyer-AI-Platform-App/backend/local.db
```

Tables are created automatically on backend startup.

Local mode uses these defaults:

```bash
APP_ENV=local
DATABASE_URL=sqlite:///./local.db
LLM_PROVIDER=mock
```

When `APP_ENV=local`, SQLAlchemy creates missing local tables on startup. In production-style environments, set `APP_ENV=production` and use Alembic migrations instead of automatic table creation.

## Local Demo Identity

v3.0 uses Local Demo Identity for internal alpha development. v3.1 adds Dev Token / API Key identity on top of that local user. v3.2 adds local demo JWT login. There is no password registration, no OAuth, and no SSO.

When `APP_ENV=local`, backend startup ensures:

```text
user_local_001 / local@example.com / Local Demo User / admin / active
workspace_local_001 / Local Demo Workspace / owner user_local_001 / active
workspace_local_001 + user_local_001 / admin / active
token_local_001 / user_local_001 / Local Dev Token / active
```

Local SQLite startup also checks `cases` for missing `workspace_id` and `owner_user_id` columns. If they are missing, the backend adds them and backfills existing cases to the local demo workspace and user. Production environments should use Alembic migrations for these schema changes.

The local dev token plaintext is configured with:

```bash
LOCAL_DEV_TOKEN=dev-local-token
JWT_SECRET_KEY=local-dev-secret-change-me
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=120
```

If unset, local mode uses the values above. The database stores only the SHA-256 dev token hash.

`JWT_SECRET_KEY` is a local example value. Production must replace it.

Local mode allows no-token fallback to `user_local_001`. If a token is provided, it must be valid; wrong tokens return `401`.

## Health Check

```bash
curl http://127.0.0.1:8001/health
```

Expected response:

```json
{"status":"ok"}
```

Internal alpha identity checks:

```bash
curl http://127.0.0.1:8001/auth/status
curl http://127.0.0.1:8001/auth/dev-token
curl http://127.0.0.1:8001/users/me
curl http://127.0.0.1:8001/workspaces
curl http://127.0.0.1:8001/workspaces/workspace_local_001
curl http://127.0.0.1:8001/workspaces/workspace_local_001/cases
```

Token-authenticated checks:

```bash
curl http://127.0.0.1:8001/auth/status \
  -H "Authorization: Bearer dev-local-token"

curl http://127.0.0.1:8001/users/me \
  -H "Authorization: Bearer dev-local-token"

curl http://127.0.0.1:8001/workspaces \
  -H "X-Dev-Token: dev-local-token"
```

JWT login check:

```bash
curl -X POST http://127.0.0.1:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user_local_001","dev_token":"dev-local-token"}'
```

Use the returned `access_token`:

```bash
curl http://127.0.0.1:8001/auth/status \
  -H "Authorization: Bearer <JWT>"
```

## AIHome.law Frontend

Run the branded internal alpha console:

```bash
cd Lawyer-AI-Platform-App/frontend
npm install
npm run dev -- -p 3001
```

Open:

```text
http://localhost:3001
```

Expected local checks:

* Dashboard shows `AIHome.law`.
* Dashboard shows Auth Status.
* No-token local mode can show `local_fallback`.
* Local Login changes auth mode to `jwt`.
* Cases show `workspace_id` and `owner_user_id`.
* Workspaces and Runtime pages open from the sidebar.

## Database And Alembic

Install backend dependencies and check Python files:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
pip install -r requirements.txt
python -m compileall app
```

Check Alembic state:

```bash
APP_ENV=local DATABASE_URL=sqlite:///./local.db alembic current
```

v2.9 includes Alembic wiring but does not yet include an initial migration. Before v3.0, generate the initial migration and use Alembic for production schema changes.

## LLM Adapter

v2.8 keeps the unified LLM Adapter and adds DeepSeek Live Mode for real model calls.

Local development uses the mock provider by default. Mock mode does not require a DeepSeek API key and does not call an external API:

```bash
LLM_PROVIDER=mock
DEEPSEEK_API_KEY=
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_TIMEOUT_SECONDS=30
```

Start mock mode:

```bash
LLM_PROVIDER=mock uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Check the active adapter:

```bash
curl http://127.0.0.1:8001/llm/status
```

Expected mock response:

```json
{
  "provider": "mock",
  "model": "mock-legal-runtime",
  "configured": true,
  "base_url_configured": false
}
```

Test text generation:

```bash
curl -X POST http://127.0.0.1:8001/llm/test \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize this legal fact: A borrower failed to repay a loan."}'
```

The test endpoint also accepts optional context:

```bash
curl -X POST http://127.0.0.1:8001/llm/test \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize this legal fact: A borrower failed to repay a loan.","context":{"case_id":"case_001"}}'
```

To use DeepSeek Live Mode, set environment variables in your shell or local `.env` file:

```bash
LLM_PROVIDER=deepseek
DEEPSEEK_API_KEY=your_key
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_TIMEOUT_SECONDS=30
```

Do not commit `.env` or any real API key.

Start DeepSeek mode:

```bash
DEEPSEEK_API_KEY=your_key LLM_PROVIDER=deepseek uvicorn app.main:app --host 127.0.0.1 --port 8001
```

Check DeepSeek status:

```bash
curl http://127.0.0.1:8001/llm/status
```

If `LLM_PROVIDER=deepseek` is used without an API key, the backend still starts normally. `/llm/status` returns `configured: false`, and `/llm/test` returns a structured error with `DEEPSEEK_API_KEY not configured`.

## Case Service

Create a case:

```bash
curl -X POST http://127.0.0.1:8001/cases \
  -H "Content-Type: application/json" \
  -d '{"title":"材料测试案件"}'
```

In v3.1, `POST /cases` uses the current user's first active workspace. The response includes:

```json
{
  "workspace_id": "workspace_local_001",
  "owner_user_id": "user_local_001"
}
```

Create a database persistence test case:

```bash
curl -X POST http://127.0.0.1:8001/cases \
  -H "Content-Type: application/json" \
  -d '{"title":"数据库测试案件"}'
```

Get a case:

```bash
curl http://127.0.0.1:8001/cases/case_001
```

## Material Service

Create a test file:

```bash
echo "test material" > /tmp/test-material.txt
```

Upload material to a case:

```bash
curl -X POST "http://127.0.0.1:8001/cases/case_001/materials" \
  -F "file=@/tmp/test-material.txt" \
  -F "material_type=document"
```

List materials for a case:

```bash
curl http://127.0.0.1:8001/cases/case_001/materials
```

Uploaded original files are saved under:

```text
Lawyer-AI-Platform-App/storage/original-files/{case_id}/
```

## Database Persistence Check

After creating a case and uploading material, stop and restart the backend:

```bash
uvicorn app.main:app --reload --port 8001
```

Then confirm the SQLite-backed data is still available:

```bash
curl http://127.0.0.1:8001/cases/case_001
curl http://127.0.0.1:8001/cases/case_001/materials
```

## Fact Runtime

Fact Runtime v2.7-B reads uploaded material files, builds a fact extraction prompt, calls the configured LLM Adapter, parses the LLM output, and stores extracted facts in SQLite.

Local development uses `LLM_PROVIDER=mock`, so no external API is called.

Extract facts for a case:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/facts/extract
```

List facts for a case:

```bash
curl http://127.0.0.1:8001/cases/case_001/facts
```

Expected response shape:

```json
{
  "case_id": "case_001",
  "llm_provider": "mock",
  "llm_status": "success",
  "skill_used": "skill_002",
  "package_used": "ep_002",
  "facts": [
    {
      "fact_id": "fact_001",
      "case_id": "case_001",
      "material_id": "material_001",
      "content": "test material",
      "fact_type": "material_statement",
      "confidence": 0.8,
      "source_text": "test material",
      "status": "extracted",
      "created_at": "2026-06-03T08:00:00"
    }
  ]
}
```

If the case has an applied published skill, Fact Runtime uses the Experience Package `fact` prompt and writes a skill-domain fact type such as `contract_dispute_fact`.

If the case has no applied skill, Fact Runtime uses the default fact extraction prompt and writes `material_statement`.

If the LLM adapter returns an error status, Fact Runtime returns `llm generation failed`.

To confirm Fact Runtime persistence, restart the backend and run:

```bash
curl http://127.0.0.1:8001/cases/case_001/facts
```

## Legal Analysis Runtime

Legal Analysis Runtime v2.7-C reads saved facts, builds a legal analysis prompt, calls the configured LLM Adapter, parses the LLM output, and stores the analysis in SQLite.

Local development uses `LLM_PROVIDER=mock`, so no external API is called.

Run legal analysis for a case:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/analysis/run
```

List legal analyses for a case:

```bash
curl http://127.0.0.1:8001/cases/case_001/analysis
```

The list endpoint returns all analysis records for the case in creation order.

Expected run response shape:

```json
{
  "analysis_id": "analysis_001",
  "case_id": "case_001",
  "llm_provider": "mock",
  "llm_status": "success",
  "skill_used": "skill_002",
  "package_used": "ep_002",
  "issues": [
    {
      "issue": "是否存在可分析的法律事实",
      "confidence": 0.8
    }
  ],
  "rules": [
    {
      "source": "LLM Adapter",
      "rule": "Legal analysis generated through configured LLM provider"
    },
    {
      "source": "Experience Package",
      "skill_id": "skill_002",
      "package_id": "ep_002",
      "rule": "Skill package analysis context loaded from Experience Package"
    }
  ],
  "reasoning": [
    "LLM Adapter processed 1 case facts.",
    "1 extracted facts were available for legal analysis."
  ],
  "conclusion": "案件具备初步法律分析条件",
  "risk_level": "medium",
  "confidence": 0.75,
  "status": "completed",
  "created_at": "2026-06-03T08:00:00"
}
```

When a case has an applied published skill, Legal Analysis uses the Experience Package `analysis` prompt and adds a non-empty `Experience Package` rule entry.

If the LLM adapter returns an error status, Legal Analysis returns `llm generation failed`.

If a case has no facts yet, run Fact Runtime first:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/facts/extract
```

To confirm Legal Analysis Runtime persistence, restart the backend and run:

```bash
curl http://127.0.0.1:8001/cases/case_001/analysis
```

## Report Runtime

Report Runtime v2.7-D reads saved facts and the latest legal analysis, builds a report prompt, calls the configured LLM Adapter, and stores the generated Markdown report in SQLite and under `storage/reports/`.

Local development uses `LLM_PROVIDER=mock`, so no external API is called.

Generate a report for a case:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/reports/generate
```

Expected response shape:

```json
{
  "report_id": "report_001",
  "case_id": "case_001",
  "report_type": "preliminary_legal_report",
  "title": "Preliminary Legal Report - 数据库测试案件",
  "status": "generated",
  "version": 1,
  "storage_path": "../storage/reports/case_001/report_001.md",
  "llm_provider": "mock",
  "llm_status": "success",
  "skill_used": "skill_002",
  "package_used": "ep_002",
  "source_refs": {
    "fact_ids": ["fact_001"],
    "analysis_id": "analysis_001",
    "skill_id": "skill_002",
    "package_id": "ep_002",
    "llm_provider": "mock",
    "llm_status": "success"
  },
  "created_at": "2026-06-03T08:00:00"
}
```

The generated Markdown includes:

```text
Executive Summary
Facts Summary
Legal Issues
Legal Analysis
Preliminary Conclusion
```

When a case has an applied published skill, the generated report content includes:

```text
Skill Used: Contract Dispute Skill Candidate
Skill ID: skill_002
Package ID: ep_002
```

LLM output must include Executive Summary, Facts Summary, Legal Issues, Legal Analysis, and Preliminary Conclusion sections. If the LLM output is incomplete, Report Runtime falls back to the existing template-generated report content.

If the LLM adapter returns an error status, Report Runtime returns `llm generation failed`.

If a case has no legal analysis yet, run Legal Analysis Runtime first:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/analysis/run
```

## Skill-Aware Frontend Check

Start the backend on port 8001 and the frontend on port 3001:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8001

cd ../frontend
npm run dev -- -p 3001
```

Open the frontend:

```text
http://localhost:3001/skills
http://localhost:3001/cases/case_001
```

Use `case_001` to check the Skill-Aware path when a skill is already applied:

* `/skills` shows the published skill and package.
* The case detail page shows Applied Skills.
* Extract Facts displays the skill/package used by Fact Runtime.
* Run Legal Analysis displays the skill/package used by Legal Analysis.
* Generate Report displays the skill/package used by Report Runtime.
* The generated report detail page shows a Skill Used section and preserves the report body lines for Skill Used, Skill ID, and Package ID.

## Workspace API

Workspace API v1.2 provides read endpoints for the frontend workspace dashboard.

List all cases:

```bash
curl http://127.0.0.1:8001/cases
```

List all reports:

```bash
curl http://127.0.0.1:8001/reports
```

Get one report:

```bash
curl http://127.0.0.1:8001/reports/report_001
```

Get dashboard stats:

```bash
curl http://127.0.0.1:8001/dashboard/stats
```

Expected stats response:

```json
{
  "cases": 1,
  "materials": 1,
  "facts": 2,
  "analyses": 1,
  "reports": 2
}
```

## Frontend Workspace Dashboard

Frontend Workspace Dashboard v1.3 reads the v1.2 Workspace API and renders the main workspace pages.

Start the backend first:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

Start the frontend:

```bash
cd Lawyer-AI-Platform-App/frontend
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

Frontend routes:

```text
/
/cases
/reports
/reports/{report_id}
```

The frontend API base URL defaults to:

```text
http://127.0.0.1:8001
```

Override it with `NEXT_PUBLIC_API_BASE_URL` if needed.

## Demo Flow Polish

Demo Flow Polish v1.4 lets a user run the full MVP workflow in the browser.

Start the backend:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8001
```

Start the frontend:

```bash
cd Lawyer-AI-Platform-App/frontend
npm install
npm run dev -- -p 3001
```

Open:

```text
http://localhost:3001
```

Browser demo flow:

```text
1. Open /cases/new.
2. Create a case with a title.
3. Upload a .txt material on the case detail page.
4. Click Extract Facts.
5. Click Run Legal Analysis.
6. Click Generate Report.
7. Open /reports.
8. Open the generated report detail page.
```

The case detail page refreshes its materials, facts, legal analyses, and reports after each action.

## Skill Training Runtime

Skill Training Runtime v2.1 reads an existing case, facts, legal analyses, and reports, then generates a rule-based Skill Candidate draft.

Build a skill candidate from `case_001`:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/skills/build
```

Expected response shape:

```json
{
  "skill_id": "skill_001",
  "case_id": "case_001",
  "skill_name": "Contract Dispute Skill Candidate",
  "domain": "contract_dispute",
  "version": "0.1.0",
  "status": "candidate",
  "evaluation_score": 0.75,
  "package_path": "../skills/skill_001"
}
```

List all skill candidates:

```bash
curl http://127.0.0.1:8001/skills
```

Get one skill candidate:

```bash
curl http://127.0.0.1:8001/skills/skill_001
```

Generated local packages are written under:

```text
Lawyer-AI-Platform-App/skills/{skill_id}/
```

Package files:

```text
skill.json
fact_prompt.txt
analysis_prompt.txt
report_prompt.txt
templates/report_template.md
```

Generated packages are ignored by git, except `Lawyer-AI-Platform-App/skills/.gitkeep`.

If the build endpoint returns a missing input error, run the earlier case chain first:

```bash
curl http://127.0.0.1:8001/cases/case_001/facts
curl http://127.0.0.1:8001/cases/case_001/analysis
curl http://127.0.0.1:8001/cases/case_001/reports
```

## Skill Evaluation Runtime

Skill Evaluation Runtime v2.2 evaluates a Skill Candidate and decides whether it can enter `validated` status.

Evaluate `skill_001`:

```bash
curl -X POST http://127.0.0.1:8001/skills/skill_001/evaluate
```

Expected response shape:

```json
{
  "skill_id": "skill_001",
  "evaluation_score": 0.82,
  "validation_status": "validated",
  "metrics": {
    "fact_pattern_quality": 0.8,
    "reasoning_quality": 0.85,
    "prompt_quality": 0.8,
    "template_quality": 0.75,
    "legal_relevance": 0.85,
    "report_reusability": 0.9
  }
}
```

Read evaluation details:

```bash
curl http://127.0.0.1:8001/skills/skill_001/evaluation
```

Read the evaluated skill:

```bash
curl http://127.0.0.1:8001/skills/skill_001
```

Confirm the local Skill Package was updated:

```bash
cat Lawyer-AI-Platform-App/skills/skill_001/skill.json
```

The updated `skill.json` includes:

```text
evaluation_score
validation_status
evaluation_details
```

SQLite compatibility note:

v2.2 adds `evaluation_details`, `validation_status`, and `validated_at` to the `skills` table. Local SQLite development uses a startup compatibility check to add missing columns. Production should use Alembic migrations for this schema change.

## Experience Package Builder

Experience Package Builder v2.3 exports a validated Skill Candidate as a standard local Experience Package.

Build a package from `skill_001`:

```bash
curl -X POST http://127.0.0.1:8001/skills/skill_001/packages/build
```

Expected response shape:

```json
{
  "package_id": "ep_001",
  "skill_id": "skill_001",
  "name": "Contract Dispute Experience Package",
  "domain": "contract_dispute",
  "version": "0.1.0",
  "status": "built",
  "package_path": "../experience-packages/ep_001"
}
```

List packages:

```bash
curl http://127.0.0.1:8001/experience-packages
```

Get package metadata:

```bash
curl http://127.0.0.1:8001/experience-packages/ep_001
```

Get package manifest:

```bash
curl http://127.0.0.1:8001/experience-packages/ep_001/manifest
```

Generated packages are written under:

```text
Lawyer-AI-Platform-App/experience-packages/{package_id}/
```

Package files:

```text
package.json
skill.json
prompts/fact_prompt.txt
prompts/analysis_prompt.txt
prompts/report_prompt.txt
templates/report_template.md
tests/test_case.json
```

Generated packages are ignored by git, except `Lawyer-AI-Platform-App/experience-packages/.gitkeep`.

## Skill Registry

Skill Registry v2.4 provides a unified view of Skills and Experience Packages.

It does not create a separate registry table. It reads from `skills` and `experience_packages` as the source of truth.

List registry entries:

```bash
curl http://127.0.0.1:8001/skill-registry
```

Get one registry detail:

```bash
curl http://127.0.0.1:8001/skill-registry/skill_001
```

List domain summaries:

```bash
curl http://127.0.0.1:8001/skill-registry/domains
```

Publish a validated skill with a built package:

```bash
curl -X POST http://127.0.0.1:8001/skill-registry/skill_001/publish
```

Deprecate a published skill and its package:

```bash
curl -X POST http://127.0.0.1:8001/skill-registry/skill_001/deprecate
```

Publish rules:

```text
skill.validation_status must be validated
package.status must be built
deprecated skills cannot be published again
```

After publish:

```text
skill.status = published
package.status = published
```

After deprecate:

```text
skill.status = deprecated
package.status = deprecated
```

## Workspace Skill Loader

Workspace Skill Loader v2.5 exposes published skills to the case workspace.

It adds the `case_skill_bindings` table:

```text
binding_id
case_id
skill_id
package_id
status
created_at
```

List Workspace-available skills:

```bash
curl http://127.0.0.1:8001/workspace/skills
```

Get one Workspace skill:

```bash
curl http://127.0.0.1:8001/workspace/skills/skill_001
```

Apply a skill to a case:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/skills/skill_001/apply
```

List applied skills for a case:

```bash
curl http://127.0.0.1:8001/cases/case_001/skills
```

Workspace loading rules:

```text
skill.status must be published
package.status must be published
```

If `skill_001` was deprecated during v2.4 lifecycle testing, `POST /skill-registry/skill_001/publish` returns an error by design. Create a fresh Skill Candidate through the normal build, evaluate, package, and publish APIs before running the Workspace Skill Loader demo.

Frontend routes:

```text
/skills
/cases/{case_id}
```

The Skills page lists published Workspace skills.

The case detail page shows Available Skills, an Apply Skill button, and Applied Skills.
