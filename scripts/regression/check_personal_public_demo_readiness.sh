#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Public Demo Readiness v7.10"
cd "${REPO_ROOT}"

required_files=(
  "README.md"
  "docs/Personal-Version-Polish-Public-Demo-Readiness-v7.10.md"
  "09-Change-Logs/v7.10.md"
  "Lawyer-AI-Platform-App/frontend/components/dashboard/BrandHero.tsx"
  "Lawyer-AI-Platform-App/frontend/components/AppShell.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-production/page.tsx"
)

for file in "${required_files[@]}"; do
  [ -s "${file}" ] || fail "missing or empty ${file}"
done

for term in \
  "Personal Production Pilot" \
  "mock-first" \
  "Team Workspace deferred" \
  "External Client Delivery deferred"; do
  grep -Fq "${term}" README.md || fail "README missing public demo term: ${term}"
done

grep -Eq "lawyer review required|律师复核必需" README.md || fail "README missing lawyer review boundary"
grep -Eq "no final legal opinion|不生成最终法律意见" README.md || fail "README missing final legal opinion boundary"
grep -Eq "no external delivery|不自动对外交付" README.md || fail "README missing external delivery boundary"

for term in \
  "AI Provider Live Gateway" \
  "OCR / Document Provider Live Gateway" \
  "Legal / Enterprise API Live Gateway" \
  "Skill Training" \
  "Controlled Case Analysis"; do
  grep -Fq "${term}" README.md || fail "README missing later route term: ${term}"
done

grep -Eq "provider-gated|受控接入" README.md || fail "README missing provider-gated route wording"
grep -Eq "lawyer-review-required|律师复核必需" README.md || fail "README missing lawyer-review-required route wording"

grep -Eq "个人生产验证|个人生产试点" "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx" || fail "personal-production missing personal validation copy"
grep -Eq "synthetic mock metadata|mock metadata 展示|仅为 mock metadata|模拟元数据" "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx" || fail "personal-showcase-pack missing synthetic mock metadata copy"
grep -Eq "Final Lock 不触发真实导出|最终锁定不触发真实导出|不触发真实导出" "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx" || fail "personal-delivery-packet missing Final Lock export boundary"
grep -Fq "受控案件生产工作流" "Lawyer-AI-Platform-App/frontend/app/personal-case-production/page.tsx" || fail "personal-case-production missing controlled workflow wording"

scan_files=(
  "README.md"
  "docs/Personal-Version-Polish-Public-Demo-Readiness-v7.10.md"
  "09-Change-Logs/v7.10.md"
  "Lawyer-AI-Platform-App/frontend/components/dashboard/BrandHero.tsx"
  "Lawyer-AI-Platform-App/frontend/components/AppShell.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-showcase-pack/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-delivery-packet/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-case-production/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-skill-studio/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-intelligence/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-material-runtime/page.tsx"
  "Lawyer-AI-Platform-App/frontend/app/personal-ai-gateway/page.tsx"
  "Lawyer-AI-Platform-App/frontend/components/personal-production/ProductionShowcaseUI.tsx"
)

tmp_forbidden="$(mktemp)"
trap 'rm -f "${tmp_forbidden}"' EXIT

for phrase in \
  "团队协作已上线" \
  "外部客户交付已上线" \
  "正式生产上线" \
  "自动胜诉" \
  "替代律师" \
  "保证准确" \
  "无需律师" \
  "包赢" \
  "已接入真实 AI 自动分析" \
  "自动案件分析" \
  "自动训练成专家"; do
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
    fail "forbidden public demo phrase found outside allowlist: ${phrase}"
  fi
done

for term in \
  "未调用真实 provider" \
  "不展示密钥值" \
  "未读取真实案件材料" \
  "不生成最终法律意见" \
  "不自动对外交付"; do
  found=false
  for file in "${scan_files[@]}"; do
    if grep -Fq "${term}" "${file}"; then
      found=true
      break
    fi
  done
  [ "${found}" = true ] || fail "public demo safety keyword missing: ${term}"
done

for sensitive in "/Users/" "local.db" "storage/runtime" ".env" "OPENAI_API_KEY" "SECRET" "TOKEN" "PASSWORD"; do
  if rg -n --fixed-strings "${sensitive}" "${scan_files[@]}" >/tmp/personal_public_demo_sensitive.txt; then
    fail "public demo files contain sensitive/local marker: ${sensitive}"
  fi
done

pass "personal public demo readiness v7.10 checks"
