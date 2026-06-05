#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal UI Polish v7.8"
cd "${REPO_ROOT}"

frontend_pages=(
  "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-ai-gateway/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-material-runtime/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-intelligence/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-skill-studio/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx"
)

for page in "${frontend_pages[@]}"; do
  [ -f "${page}" ] || fail "missing page ${page}"
  grep -Eq "Developer Diagnostics|DiagnosticsPanel|<details" "${page}" || fail "${page} missing diagnostics"
  if grep -Eq "<details[^>]*[[:space:]]open([[:space:]]|>|=)" "${page}"; then
    fail "${page} diagnostics should be folded by default"
  fi
done

shared_ui="Lawyer-AI-Platform-App/frontend/components/personal-production/ProductionShowcaseUI.tsx"
[ -f "${shared_ui}" ] || fail "missing shared personal production UI component"

for term in \
  "未调用真实 provider" \
  "未读取 API key" \
  "未读取真实案件材料" \
  "未生成最终法律意见" \
  "未生成最终报告" \
  "未自动对外交付" \
  "律师复核必需" \
  "来源追踪必需"; do
  grep -Fq "${term}" "${shared_ui}" || fail "shared safety copy missing: ${term}"
done

for page in "${frontend_pages[@]}"; do
  grep -Eq "TrustSafetyPanel|安全清单|Safety Panel|Trust / Safety" "${page}" || fail "${page} missing trust/safety panel"
done

app_shell="Lawyer-AI-Platform-App/frontend/components/AppShell.tsx"
for nav in \
  "个人生产总控台" \
  "个人生产试点与展示包" \
  "个人生产交付包" \
  "受控案件生产工作流" \
  "经验包与技能工作室" \
  "法律与企业信息网关" \
  "材料解析与 OCR Runtime" \
  "AI 网关与草稿 Runtime"; do
  grep -Fq "${nav}" "${app_shell}" || fail "AppShell missing nav item: ${nav}"
done

scan_roots=(
  "Lawyer-AI-Platform-App/frontend/app"
  "Lawyer-AI-Platform-App/frontend/components"
  "00-Project-Context"
  "docs"
  "09-Change-Logs"
  "AGENTS.md"
)

scan_files=()
while IFS= read -r file; do
  scan_files+=("${file}")
done < <(rg --files "${scan_roots[@]}" | rg '(\.md$|\.tsx$|\.ts$|\.py$|\.sh$|README$|README\.md$)')
tmp_forbidden="$(mktemp)"
trap 'rm -f "${tmp_forbidden}"' EXIT

for phrase in \
  "自动胜诉" \
  "替代律师" \
  "保证准确" \
  "自动出具最终法律意见" \
  "自动完成客户交付" \
  "一键交付" \
  "全自动办案" \
  "自动发送客户" \
  "智能判案" \
  "包赢" \
  "无需律师"; do
  : > "${tmp_forbidden}"
  for file in "${scan_files[@]}"; do
    awk -v phrase="${phrase}" '
      /^## 禁用表达清单/ { in_forbidden=1 }
      /^## / && !/^## 禁用表达清单/ { in_forbidden=0 }
      index($0, phrase) && !in_forbidden { print FILENAME ":" FNR ":" $0 }
    ' "${file}" >> "${tmp_forbidden}"
  done
  if [ -s "${tmp_forbidden}" ]; then
    cat "${tmp_forbidden}" >&2
    fail "forbidden UI phrase found: ${phrase}"
  fi
done

for secret_pattern in "/Users/" "local.db" "storage/runtime" ".env" "OPENAI_API_KEY" "SECRET" "TOKEN" "PASSWORD"; do
  if rg -n --fixed-strings "${secret_pattern}" "${frontend_pages[@]}" "Lawyer-AI-Platform-App/frontend/components/personal-production" >/tmp/personal_ui_polish_sensitive.txt; then
    fail "frontend display contains sensitive/local marker: ${secret_pattern}"
  fi
done

pass "personal UI polish v7.8 checks"
