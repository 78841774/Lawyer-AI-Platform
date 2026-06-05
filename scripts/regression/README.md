# Personal Alpha Case OS Regression Suite

## Purpose

v6.7 turns the v5.0-v6.6 manual verification flow into local regression scripts. The suite checks backend compilation, frontend build, Personal Alpha status APIs, Case OS core APIs, Case OS quality APIs, v6.8 hardening APIs, v6.9 release candidate APIs, v7.0 personal production APIs, metadata-only response safety, safe not_found behavior, injected/path-like input handling, git safety, runtime ignore rules, docs completeness, and tracked sensitive files.

The suite is local-only, mock-first, controlled-first, metadata-only, and redacted-only. It does not call real providers, generate legal opinions, generate final reports, create PDF/DOCX files, or commit runtime files.

## Start Backend

Run the backend in a separate terminal before API checks:

```bash
cd Lawyer-AI-Platform-App/backend
source .venv/bin/activate

APP_ENV=local \
DATABASE_URL=sqlite:///./local.db \
LLM_PROVIDER=mock \
LOCAL_DEV_TOKEN=dev-local-token \
JWT_SECRET_KEY=local-dev-secret-change-me \
JWT_ALGORITHM=HS256 \
JWT_EXPIRATION_MINUTES=120 \
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

## Run Full Regression

From repo root:

```bash
bash scripts/regression/run_personal_alpha_regression.sh
```

With an explicit case:

```bash
CASE_ID=case_v55_approve_all bash scripts/regression/run_personal_alpha_regression.sh
```

## Run One Check

```bash
bash scripts/regression/check_case_os_quality_apis.sh
```

## Environment Variables

- `API_BASE`: backend base URL, default `http://127.0.0.1:8001`
- `FRONTEND_BASE`: frontend base URL, default `http://127.0.0.1:3001`
- `CASE_ID`: Case OS case id, default `case_v55_approve_all`
- `LOCAL_DEV_TOKEN`: local dev token, default `dev-local-token`

## Script List

- `run_personal_alpha_regression.sh`: runs the full suite.
- `check_backend_compile.sh`: runs backend compileall.
- `check_frontend_build.sh`: runs frontend build.
- `check_case_os_status_apis.sh`: checks v5.0-v6.6 status endpoints.
- `check_case_os_core_apis.sh`: checks Case OS core endpoints.
- `check_case_os_quality_apis.sh`: checks v6.6 quality endpoints.
- `check_case_os_hardening_apis.sh`: checks v6.8 hardening endpoints.
- `check_case_os_release_candidate_apis.sh`: checks v6.9 release candidate endpoints and Personal Production next-step metadata.
- `check_personal_production_apis.sh`: checks v7.0 Personal Production Runtime & Showcase endpoints.
- `check_metadata_only_responses.sh`: checks selected responses for path, secret, and raw-content leakage.
- `check_safe_not_found.sh`: checks safe not_found responses.
- `check_injected_path_inputs.sh`: checks encoded path-like case id handling.
- `check_git_safety.sh`: checks git status and whitespace.
- `check_runtime_ignored.sh`: checks runtime storage ignore rules.
- `check_docs_not_empty.sh`: checks docs and changelog markdown files are non-empty.
- `check_no_sensitive_files.sh`: checks sensitive paths are not tracked.

## Safety

The scripts make read-only requests and local compile/build checks. They do not execute workflow actions, create export packages, create final locks, publish Skills, enable Workspace Runtime, read raw material text, or write runtime fixtures.
