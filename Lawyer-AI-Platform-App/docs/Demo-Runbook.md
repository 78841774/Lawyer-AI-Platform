# Demo Runbook

This runbook starts the local MVP demo and walks through the browser flow.

## 1. Clear Local Demo Ports

From the repository root:

```bash
bash Lawyer-AI-Platform-App/scripts/kill-ports.sh
```

This clears LISTEN processes on ports `8001` and `3001`.

## 2. Start Backend

Open a terminal from the repository root:

```bash
bash Lawyer-AI-Platform-App/scripts/start-backend.sh
```

The local demo uses:

```bash
APP_ENV=local
DATABASE_URL=sqlite:///./local.db
LLM_PROVIDER=mock
```

The backend runs at:

```text
http://127.0.0.1:8001
```

Check backend health in another terminal:

```bash
curl http://127.0.0.1:8001/health
curl http://127.0.0.1:8001/llm/status
curl http://127.0.0.1:8001/dashboard/stats
```

For production-style PostgreSQL testing, use Docker Compose from `Lawyer-AI-Platform-App`. Do not put real DeepSeek or OpenAI API keys in committed files.

## 3. Start Frontend

Open a second terminal from the repository root:

```bash
bash Lawyer-AI-Platform-App/scripts/start-frontend.sh
```

The frontend runs at:

```text
http://localhost:3001
```

## 4. Run Browser Demo

Open:

```text
http://localhost:3001
```

Demo steps:

1. Open `Cases`.
2. Click `New Case`.
3. Enter a title and create the case.
4. On the case detail page, upload a `.txt` material.
5. Click `Extract Facts`.
6. Click `Run Legal Analysis`.
7. Click `Generate Report`.
8. Open `Reports`.
9. Open the generated report detail page.

The report detail page should show:

```text
Executive Summary
Facts Summary
Legal Issues
Legal Analysis
Preliminary Conclusion
```

## 5. Workspace Skill Loader Demo

The Skill Loader demo requires a published skill and a published package.

Open:

```text
http://localhost:3001/skills
```

Expected:

```text
Published Workspace skills are listed.
```

Then open a case:

```text
http://localhost:3001/cases/case_001
```

Expected:

```text
Available Skills
Applied Skills
```

Click `Apply Skill`.

The skill should appear in `Applied Skills`.

If no skills are listed, check the backend:

```bash
curl http://127.0.0.1:8001/workspace/skills
curl http://127.0.0.1:8001/skill-registry
```

Only skills with `skill.status = published` and package `status = published` are available to Workspace.

If the local `skill_001` is deprecated, do not manually edit the database. Build a fresh skill candidate, evaluate it, build a package, and publish it through the official APIs.

## Troubleshooting

If a port is already in use:

```bash
bash Lawyer-AI-Platform-App/scripts/kill-ports.sh
```

If backend dependencies are missing, rerun:

```bash
bash Lawyer-AI-Platform-App/scripts/start-backend.sh
```

If frontend dependencies are missing, rerun:

```bash
bash Lawyer-AI-Platform-App/scripts/start-frontend.sh
```
