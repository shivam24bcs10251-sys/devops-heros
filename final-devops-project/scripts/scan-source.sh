#!/usr/bin/env bash
set -euo pipefail
PROJECT_REPO_ROOT=$(git rev-parse --show-toplevel)
PROJECT_SCAN_DIR=$(mktemp -d)
trap 'rm -rf "$PROJECT_SCAN_DIR"' EXIT
git -C "$PROJECT_REPO_ROOT" archive HEAD final-devops-project | tar -x -C "$PROJECT_SCAN_DIR"
"${GITLEAKS_BIN:-gitleaks}" dir "$PROJECT_SCAN_DIR/final-devops-project" --redact --report-format json --report-path "$PROJECT_REPO_ROOT/final-devops-project/Output/reports/gitleaks.json"
