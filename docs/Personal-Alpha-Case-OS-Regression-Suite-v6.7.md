# Personal Alpha Case OS Regression Suite v6.7

## Objective

v6.7 adds a local regression suite for the Personal Alpha Case OS workflow. It converts the v5.0-v6.6 manual verification steps into repeatable shell scripts that can be run from the repository root.

v6.7 is a test and quality assurance version. It does not add new business workflow behavior.

## Relationship to v6.6

v6.6 added metadata-only Case OS quality APIs. v6.7 verifies those APIs alongside earlier Personal Alpha modules, Case OS orchestration, audit timeline, review state machine, metadata closure, export package, and safety responses.

## Regression Scripts

The suite lives under `scripts/regression/`:

- `run_personal_alpha_regression.sh`
- `check_backend_compile.sh`
- `check_frontend_build.sh`
- `check_case_os_status_apis.sh`
- `check_case_os_core_apis.sh`
- `check_case_os_quality_apis.sh`
- `check_metadata_only_responses.sh`
- `check_safe_not_found.sh`
- `check_injected_path_inputs.sh`
- `check_git_safety.sh`
- `check_runtime_ignored.sh`
- `check_docs_not_empty.sh`
- `check_no_sensitive_files.sh`
- `frontend_smoke_notes.md`
- `README.md`

## How to Run

Start the backend first:

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

Run the full suite from repo root:

```bash
CASE_ID=case_v55_approve_all bash scripts/regression/run_personal_alpha_regression.sh
```

Run a single check:

```bash
bash scripts/regression/check_case_os_quality_apis.sh
```

## Backend Compile Check

`check_backend_compile.sh` runs `python -m compileall` over the backend app and Personal Alpha modules. If `.venv` exists, it activates it first. If `.venv` is missing, it warns and tries `python` or `python3`.

## Frontend Build Check

`check_frontend_build.sh` runs `npm run build` in `Lawyer-AI-Platform-App/frontend`.

## Status API Checks

`check_case_os_status_apis.sh` verifies `/health`, Personal Alpha module status endpoints, `/case-os/status`, and `/case-os`. It checks safety fields such as `production_enabled=false`, `raw_content_included=false`, and final report/legal opinion disabled fields when present.

## Case OS API Checks

`check_case_os_core_apis.sh` verifies Case OS detail, audit, next action, safety checklist, stage orchestration, transitions, action eligibility, blockers, review state, metadata closure, and export package status/summary endpoints.

## Quality API Checks

`check_case_os_quality_apis.sh` verifies v6.6 quality status, checklist, score, findings, recommendations, report preview, and summary endpoints. It checks that quality responses remain metadata-only and that report preview/recommendation flags stay false.

## Metadata-Only Checks

`check_metadata_only_responses.sh` checks selected responses for absence of local paths, secret-like values, raw content phrases, and unsafe filenames.

## Safe Not Found Checks

`check_safe_not_found.sh` verifies safe not_found responses for missing Case OS case ids. It also checks that responses do not expose local paths, runtime storage, `.env`, or stack traces.

## Injected Input Checks

`check_injected_path_inputs.sh` sends an encoded path-like case id and verifies that responses do not echo `/Users`, `real_cases`, `client.pdf`, runtime paths, or secrets.

## Git Safety Checks

`check_git_safety.sh` runs `git status --short` and `git diff --check`, then ensures sensitive paths are not present in the working tree status.

## Runtime Ignored Checks

`check_runtime_ignored.sh` uses `git check-ignore` to verify that runtime storage paths remain ignored, including Case OS export package runtime paths.

## Frontend Smoke Notes

`frontend_smoke_notes.md` documents manual browser checks for `/case-os` and `/case-os/<case_id>`, including the quality checklist panel and no raw content/final report body display.

## No Raw Content Rule

Regression scripts check that selected API responses do not expose local paths, real case directories, secrets, raw material text, raw OCR text, raw legal search text, or final report/legal opinion generated flags.

## No Final Legal Opinion

The suite verifies metadata-only status and generated flags. It does not request or generate legal opinions.

## No Final Report Generated

The suite verifies final report generated flags and report preview file-generation flags. It does not create PDF, DOCX, or final report bodies.

## v6.8 Readiness

v6.8 can focus on Case OS hardening: unified safe not_found responses, blocked/redacted response structures, shared no-raw-content guards, shared runtime storage guards, and API response consistency while staying metadata-only.
