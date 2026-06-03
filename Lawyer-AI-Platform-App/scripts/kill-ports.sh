#!/usr/bin/env bash
set -euo pipefail

PORTS=(8001 3001)

for port in "${PORTS[@]}"; do
  pids="$(lsof -tiTCP:"${port}" -sTCP:LISTEN || true)"

  if [ -z "${pids}" ]; then
    echo "Port ${port}: no LISTEN process found"
    continue
  fi

  echo "Port ${port}: killing LISTEN PID(s): ${pids}"
  while IFS= read -r pid; do
    if [ -n "${pid}" ]; then
      kill "${pid}" 2>/dev/null || true
    fi
  done <<< "${pids}"
done
