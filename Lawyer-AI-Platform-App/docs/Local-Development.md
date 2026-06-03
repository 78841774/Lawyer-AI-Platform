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
