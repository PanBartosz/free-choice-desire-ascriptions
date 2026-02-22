#!/usr/bin/env bash
set -euo pipefail

echo "[preflight] Checking for files that should not be committed..."

issues=0

check_pattern() {
  local label="$1"
  local pattern="$2"
  local found
  found="$(rg --files -g "$pattern" || true)"
  if [[ -n "$found" ]]; then
    echo "[preflight][FAIL] ${label}"
    echo "$found"
    issues=1
  else
    echo "[preflight][OK] ${label}"
  fi
}

check_pattern ".venv tracked candidates" ".venv/**"
check_pattern "tmp directory artifacts" "tmp/**"
check_pattern "Python caches" "**/__pycache__/**"
check_pattern "Compiled Python files" "*.pyc"
check_pattern "R history files" ".Rhistory"
check_pattern "nohup logs" "nohup.out"
check_pattern "Editor settings (.vscode)" ".vscode/**"
check_pattern "Backup files" "*.bak"
check_pattern "Quarto/Rmd support dirs (*_files)" "**/*_files/**"

if [[ "$issues" -ne 0 ]]; then
  echo "[preflight] Issues found."
  exit 1
fi

echo "[preflight] Clean."
