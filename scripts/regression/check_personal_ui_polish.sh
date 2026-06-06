#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Legal-Tech UI/UX Polish v7.24"
cd "${REPO_ROOT}"

frontend_pages=(
  "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-skill-studio/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-intelligence/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-material-runtime/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-ai-gateway/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-analysis/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-workspace/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-production-pilot/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-owner-output-center/page.tsx"
)

supporting_pages=(
  "Lawyer-AI-Platform-App/frontend/app/personal-case-analysis/legal-drafts/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-skill-studio/final-drafts/page.tsx"
)

for page in "${frontend_pages[@]}" "${supporting_pages[@]}"; do
  [ -f "${page}" ] || fail "missing page ${page}"
  grep -Eq "DiagnosticsPanel|<details|开发诊断" "${page}" || fail "${page} missing diagnostics"
  grep -Eq "TrustSafetyPanel|信任与安全|安全清单|安全边界" "${page}" || fail "${page} missing trust/safety panel"
  if grep -Eq "<details[^>]*[[:space:]]open([[:space:]]|>|=)" "${page}"; then
    fail "${page} diagnostics should be folded by default"
  fi
done

shared_ui="Lawyer-AI-Platform-App/frontend/components/personal-production/ProductionShowcaseUI.tsx"
[ -f "${shared_ui}" ] || fail "missing shared personal production UI component"

for component in \
  "SafetyBadge" \
  "DarkSafetyBadge" \
  "StatusPill" \
  "StatusCard" \
  "RuntimeCard" \
  "ShowcaseStepper" \
  "TrustSafetyPanel" \
  "DiagnosticsPanel" \
  "InfoRows"; do
  grep -Fq "export function ${component}" "${shared_ui}" || fail "shared component missing: ${component}"
done

for term in \
  "受控运行" \
  "仅模拟结果" \
  "律师复核必需" \
  "来源可追踪" \
  "不自动对外交付"; do
  grep -Fq "${term}" "${shared_ui}" || fail "shared safety badge missing: ${term}"
done

grep -Fq "不会触发真实导出/最终报告/最终法律意见" "${shared_ui}" || fail "stepper missing final-stage no-export wording"
grep -Fq "开发诊断（默认折叠）" "${shared_ui}" || fail "diagnostics missing folded Chinese title"
grep -Fq "信任与安全面板" "${shared_ui}" || fail "trust/safety panel missing Chinese default title"
grep -Fq "原始内容、本地路径或密钥值" "${shared_ui}" || fail "trust/safety panel missing sensitive-content boundary"

if grep -Eq "<details[^>]*[[:space:]]open([[:space:]]|>|=)" "${shared_ui}"; then
  fail "shared diagnostics should be folded by default"
fi

app_shell="Lawyer-AI-Platform-App/frontend/components/AppShell.tsx"
for nav in \
  "个人生产总控台" \
  "个人生产实战 Pilot" \
  "用户本人产出下载中心" \
  "个人案件与材料工作台" \
  "个人生产试点与展示包" \
  "个人生产交付包" \
  "受控案件分析 Runtime" \
  "经验包与技能工作室" \
  "法律与企业信息网关" \
  "材料解析与 OCR Runtime" \
  "AI 网关与草稿 Runtime"; do
  grep -Fq "${nav}" "${app_shell}" || fail "AppShell missing nav item: ${nav}"
done

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
  if rg -n --fixed-strings "${phrase}" "${frontend_pages[@]}" "${supporting_pages[@]}" "${shared_ui}" "${app_shell}" >/tmp/personal_ui_polish_forbidden.txt; then
    fail "forbidden UI phrase found: ${phrase}"
  fi
done

for sensitive_pattern in \
  "/Users" \
  "API key" \
  "raw content" \
  "local.db" \
  "storage/runtime" \
  "node_modules" \
  "__pycache__" \
  ".DS_Store" \
  "OPENAI_API_KEY" \
  "BEGIN PRIVATE KEY"; do
  if rg -n --fixed-strings "${sensitive_pattern}" "${frontend_pages[@]}" "${supporting_pages[@]}" "${shared_ui}" "${app_shell}" >/tmp/personal_ui_polish_sensitive.txt; then
    fail "frontend target pages contain sensitive/local marker: ${sensitive_pattern}"
  fi
done

for page in "${frontend_pages[@]}"; do
  grep -Eq "受控|草稿|模拟|律师复核|来源|安全|不自动对外交付" "${page}" || fail "${page} missing Chinese legal-tech safety copy"
done

pass "personal legal-tech UI/UX polish v7.24 checks"
