#!/usr/bin/env bash
set -euo pipefail

echo "== Provider env safety check =="

tracked_env_files="$(git ls-files | grep -E '(^|/)\.env($|\.)' || true)"

if [ -n "$tracked_env_files" ]; then
  disallowed="$(printf '%s\n' "$tracked_env_files" | grep -Ev '(^|/)\.env\.example$|(^|/)\.env\.provider\.example$' || true)"
  if [ -n "$disallowed" ]; then
    echo "FAIL tracked non-example .env-like file detected:"
    printf '%s\n' "$disallowed"
    exit 1
  fi
fi

if git check-ignore -q Lawyer-AI-Platform-App/backend/.env 2>/dev/null; then
  echo "PASS backend .env is ignored"
else
  echo "FAIL backend .env is not ignored"
  exit 1
fi

echo "PASS provider env safety check completed"
