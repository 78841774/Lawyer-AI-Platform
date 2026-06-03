# Lawyer AI Platform App

This directory contains the v0.5 MVP Coding scaffold for Lawyer AI Platform.

## Structure

* frontend: Next.js, TypeScript, Tailwind Workspace UI.
* backend: FastAPI service with MVP API foundation.
* ai-runtime: Runtime interfaces for fact extraction, legal analysis, and report generation.
* storage: Local development storage layout.
* infra: Database schema and infrastructure assets.
* docs: App-level implementation notes.

## MVP Focus

The first coding phase focuses on case management, material upload, fact extraction, legal analysis, and report generation.

## Local Demo

The local demo runs the FastAPI backend on port `8001` and the Next.js frontend on port `3001`.

From the repository root, run:

Clear demo ports:

```bash
bash Lawyer-AI-Platform-App/scripts/kill-ports.sh
```

Start the backend:

```bash
bash Lawyer-AI-Platform-App/scripts/start-backend.sh
```

Start the frontend in another terminal:

```bash
bash Lawyer-AI-Platform-App/scripts/start-frontend.sh
```

Open:

```text
http://localhost:3001
```

See `docs/Demo-Runbook.md` for the full browser demo flow.

## Troubleshooting

### port already in use

Run:

```bash
bash Lawyer-AI-Platform-App/scripts/kill-ports.sh
```

The script clears LISTEN processes on ports `8001` and `3001`.

### uvicorn not found

Use the backend startup script. It creates `.venv` if needed, installs dependencies, and starts uvicorn through the virtual environment:

```bash
bash Lawyer-AI-Platform-App/scripts/start-backend.sh
```

### npm dev port conflict

Clear port `3001`, then restart the frontend:

```bash
bash Lawyer-AI-Platform-App/scripts/kill-ports.sh
bash Lawyer-AI-Platform-App/scripts/start-frontend.sh
```
