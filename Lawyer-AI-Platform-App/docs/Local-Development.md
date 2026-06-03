# Local Development

## Backend

Start the backend from the backend directory:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

The backend uses SQLite for local development. The database file is created at:

```text
Lawyer-AI-Platform-App/backend/local.db
```

Tables are created automatically on backend startup.

## Health Check

```bash
curl http://127.0.0.1:8001/health
```

Expected response:

```json
{"status":"ok"}
```

## LLM Adapter

v2.7-A adds a unified LLM Adapter for future AI-backed Fact, Legal Analysis, Report, and Skill Training runtimes.

Local development uses the mock provider by default:

```bash
LLM_PROVIDER=mock
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=
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
  "configured": true
}
```

Test text generation:

```bash
curl -X POST http://127.0.0.1:8001/llm/test \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Summarize this legal fact: A borrower failed to repay a loan."}'
```

The mock adapter does not call any external API. If `LLM_PROVIDER=openai` is used without an API key, the adapter returns `OPENAI_API_KEY not configured` and the backend still starts normally.

## Case Service

Create a case:

```bash
curl -X POST http://127.0.0.1:8001/cases \
  -H "Content-Type: application/json" \
  -d '{"title":"材料测试案件"}'
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

Fact Runtime v0.9 reads uploaded material files, extracts rule-based facts, and stores them in SQLite.

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

To confirm Fact Runtime persistence, restart the backend and run:

```bash
curl http://127.0.0.1:8001/cases/case_001/facts
```

## Legal Analysis Runtime

Legal Analysis Runtime v1.0 reads saved facts, generates a rule-based legal analysis, and stores it in SQLite.

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
  "issues": [
    {
      "issue": "是否存在可分析的法律事实",
      "confidence": 0.8
    }
  ],
  "rules": [
    {
      "source": "MVP Rule Engine",
      "rule": "基于已抽取事实进行初步法律问题识别"
    }
  ],
  "reasoning": [
    "系统已发现 1 条案件事实",
    "其中 1 条事实可用于进一步法律分析"
  ],
  "conclusion": "案件具备初步法律分析条件",
  "risk_level": "medium",
  "confidence": 0.75,
  "status": "completed",
  "created_at": "2026-06-03T08:00:00"
}
```

If a case has no facts yet, run Fact Runtime first:

```bash
curl -X POST http://127.0.0.1:8001/cases/case_001/facts/extract
```

To confirm Legal Analysis Runtime persistence, restart the backend and run:

```bash
curl http://127.0.0.1:8001/cases/case_001/analysis
```

## Report Runtime

Report Runtime v1.1 reads saved facts and the latest legal analysis, generates a preliminary Markdown report, saves a report row in SQLite, and writes the Markdown file under `storage/reports/`.

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
  "source_refs": {
    "fact_ids": ["fact_001"],
    "analysis_id": "analysis_001"
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
