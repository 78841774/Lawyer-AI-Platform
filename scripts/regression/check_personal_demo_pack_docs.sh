#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/common.sh"

section "Personal Demo Pack Docs v7.9"
cd "${REPO_ROOT}"

required_files=(
  "docs/Personal-Production-Demo-Script-Screenshot-Pack-v7.9.md"
  "docs/AIHome-Law-Personal-Production-One-Pager-v7.9.md"
  "docs/AIHome-Law-Pitch-Deck-Outline-v7.9.md"
  "09-Change-Logs/v7.9.md"
)

for file in "${required_files[@]}"; do
  [ -s "${file}" ] || fail "missing or empty ${file}"
done

for term in \
  "mock-first" \
  "律师复核必需" \
  "来源可追踪" \
  "不生成最终法律意见" \
  "不自动对外交付"; do
  grep -Fq "${term}" "docs/Personal-Production-Demo-Script-Screenshot-Pack-v7.9.md" || fail "main v7.9 doc missing safety keyword: ${term}"
done

grep -Fq "AIHome.law Personal Production Pilot" README.md || fail "README missing Personal Production Pilot section"
grep -Fq "mock-first" README.md || fail "README missing mock-first display copy"
grep -Fq "controlled-runtime" README.md || fail "README missing controlled-runtime display copy"
grep -Fq "does not generate final legal opinions" README.md || fail "README missing English safety boundary"

scan_files=(
  "README.md"
  "docs/Personal-Production-Demo-Script-Screenshot-Pack-v7.9.md"
  "docs/AIHome-Law-Personal-Production-One-Pager-v7.9.md"
  "docs/AIHome-Law-Pitch-Deck-Outline-v7.9.md"
  "09-Change-Logs/v7.9.md"
  "00-Project-Context/CURRENT_STATE.md"
  "00-Project-Context/ROADMAP.md"
  "00-Project-Context/RELEASE_INDEX.md"
  "00-Project-Context/NEXT_TASK.md"
  "00-Project-Context/CODEX_HANDOFF.md"
  "AGENTS.md"
)

tmp_out="$(mktemp)"
trap 'rm -f "${tmp_out}"' EXIT

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
  : > "${tmp_out}"
  for file in "${scan_files[@]}"; do
    awk -v phrase="${phrase}" '
      /^## 禁用表达清单/ { in_forbidden=1 }
      /^## / && !/^## 禁用表达清单/ { in_forbidden=0 }
      index($0, phrase) && !in_forbidden { print FILENAME ":" FNR ":" $0 }
    ' "${file}" >> "${tmp_out}"
  done
  if [ -s "${tmp_out}" ]; then
    cat "${tmp_out}" >&2
    fail "forbidden demo phrase outside allowlist section: ${phrase}"
  fi
done

demo_material_files=(
  "README.md"
  "docs/Personal-Production-Demo-Script-Screenshot-Pack-v7.9.md"
  "docs/AIHome-Law-Personal-Production-One-Pager-v7.9.md"
  "docs/AIHome-Law-Pitch-Deck-Outline-v7.9.md"
  "09-Change-Logs/v7.9.md"
)

for sensitive in "/Users/" "local.db" "storage/runtime" ".env" "OPENAI_API_KEY" "SECRET" "TOKEN" "PASSWORD"; do
  if rg -n --fixed-strings "${sensitive}" "${demo_material_files[@]}" >/tmp/personal_demo_pack_sensitive.txt; then
    fail "demo pack contains sensitive/local marker: ${sensitive}"
  fi
done

pass "personal demo pack docs v7.9 checks"
