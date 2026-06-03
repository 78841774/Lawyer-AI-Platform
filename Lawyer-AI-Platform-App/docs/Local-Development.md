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
