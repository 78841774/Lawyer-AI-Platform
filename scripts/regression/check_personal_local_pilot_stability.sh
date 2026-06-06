#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Local Pilot Stability v7.11"
cd "${REPO_ROOT}"

pages=(
  "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-skill-studio/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-intelligence/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-material-runtime/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-ai-gateway/page.tsx"
)

for page in "${pages[@]}"; do
  [ -s "${page}" ] || fail "missing or empty ${page}"
  grep -Fq "SafeErrorNotice" "${page}" || fail "${page} missing SafeErrorNotice fallback"
  grep -Eq "DiagnosticsPanel|<details" "${page}" || fail "${page} missing diagnostics"
done

shared_ui="Lawyer-AI-Platform-App/frontend/components/personal-production/ProductionShowcaseUI.tsx"
api_client="Lawyer-AI-Platform-App/frontend/services/api.ts"
app_shell="Lawyer-AI-Platform-App/frontend/components/AppShell.tsx"

for component in "SafeErrorNotice" "LocalPilotPath" "TrustSafetyPanel" "DiagnosticsPanel"; do
  grep -Fq "function ${component}" "${shared_ui}" || fail "shared UI missing ${component}"
done

for nav in \
  "个人生产总控台" \
  "个人生产试点与展示包" \
  "个人生产交付包" \
  "受控案件生产工作流" \
  "经验包与技能工作室" \
  "法律与企业信息网关" \
  "材料解析与 OCR Runtime" \
  "AI 网关与草稿 Runtime"; do
  grep -Fq "${nav}" "${app_shell}" || fail "AppShell missing personal production nav: ${nav}"
done

if grep -Eq "sk-[A-Za-z0-9_-]+|OPENAI_API_KEY|DEEPSEEK_API_KEY|BEGIN PRIVATE KEY" "${api_client}"; then
  fail "API client contains hardcoded provider secret marker"
fi

for file in "${pages[@]}" "${shared_ui}" "${api_client}"; do
  if grep -Fq "/Users/" "${file}"; then
    fail "${file} contains local absolute path"
  fi
  if grep -Eq "api[_ -]?key[[:space:]]*[:=][[:space:]]*['\"][^'\"]+['\"]" "${file}"; then
    fail "${file} appears to contain an API key literal"
  fi
done

if rg -n "<details[^>]*[[:space:]]open([[:space:]]|>|=)" "${pages[@]}" "${shared_ui}" >/tmp/personal_local_pilot_details.txt; then
  fail "Diagnostics details should be folded by default"
fi

copy_files=(
  "README.md"
  "docs/Personal-Version-Polish-Public-Demo-Readiness-v7.10.md"
  "docs/Personal-Production-Stability-Local-Pilot-Hardening-v7.11.md"
  "09-Change-Logs/v7.11.md"
  "${shared_ui}"
  "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx"
)

for term in \
  "live provider disabled" \
  "后续受控接入" \
  "不生成最终法律意见" \
  "不自动对外交付"; do
  found=false
  for file in "${copy_files[@]}"; do
    if [ -f "${file}" ] && grep -Fq "${term}" "${file}"; then
      found=true
      break
    fi
  done
  [ "${found}" = true ] || fail "local pilot stability copy missing: ${term}"
done

pass "personal local pilot stability v7.11 checks"
